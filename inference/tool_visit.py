"""
Enhanced Visit Tool with modular design and comprehensive logging
Features:
- Configuration management
- Rich logging with file output
- Modular function design
- Better error handling and debugging
"""

import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

import requests
import tiktoken
from openai import OpenAI
from qwen_agent.tools.base import BaseTool, register_tool
from rich.console import Console
from rich.logging import RichHandler
import logging

from prompt import EXTRACTOR_PROMPT


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class VisitConfig:
    """Configuration for the Visit tool"""
    
    # API Configuration
    jina_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    summary_model_name: str = "alibaba/tongyi-deepresearch-30b-a3b"
    
    # Timeouts and Limits
    visit_timeout: int = 50
    max_content_length: int = 150000
    max_tokens: int = 95000
    batch_timeout: int = 900  # 15 minutes for batch processing
    
    # Retry Configuration
    jina_max_retries: int = 3
    jina_retry_delay: float = 0.5
    html_read_max_attempts: int = 8
    summary_max_retries: int = 3
    parse_max_retries: int = 3
    
    # LLM Configuration
    llm_temperature: float = 0.7
    llm_base_url: str = "https://openrouter.ai/api/v1"
    
    # Logging
    enable_debug_logging: bool = True
    log_dir: str = "log"
    
    @classmethod
    def from_env(cls) -> "VisitConfig":
        """Create configuration from environment variables"""
        return cls(
            jina_api_key=os.getenv("JINA_API_KEYS", "").strip(),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", "").strip(),
            summary_model_name=os.getenv("SUMMARY_MODEL_NAME", "alibaba/qwen-max"),
            visit_timeout=int(os.getenv("VISIT_SERVER_TIMEOUT", 50)),
            max_content_length=int(os.getenv("WEBCONTENT_MAXLENGTH", 150000)),
            summary_max_retries=int(os.getenv("VISIT_SERVER_MAX_RETRIES", 1)),
            enable_debug_logging=os.getenv("DEBUG_VISIT", "true").lower() == "true",
        )
    
    def validate(self) -> None:
        """Validate required configuration"""
        if not self.jina_api_key:
            raise ValueError("JINA_API_KEYS not set in environment")
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logger(config: VisitConfig) -> logging.Logger:
    """Setup rich logger with file output"""
    os.makedirs(config.log_dir, exist_ok=True)
    
    # Create timestamp for log file
    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    log_file = os.path.join(config.log_dir, f"log_{timestamp}.log")
    
    # Create logger
    logger = logging.getLogger("visit_tool")
    logger.setLevel(logging.DEBUG if config.enable_debug_logging else logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Rich console handler (only for warnings and errors to not clutter output)
    console_handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=False)
    console_handler.setLevel(logging.WARNING)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# Helper Functions
# ============================================================================

def truncate_to_tokens(text: str, max_tokens: int = 95000) -> str:
    """
    Truncate text to a maximum number of tokens.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens
        
    Returns:
        Truncated text
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON object from text that might contain markdown code blocks.
    
    Args:
        text: Text containing JSON
        
    Returns:
        Cleaned JSON string
    """
    # Remove markdown code blocks
    text = text.replace("```json", "").replace("```", "").strip()
    
    # Extract JSON from string if needed
    left = text.find('{')
    right = text.rfind('}')
    
    if left != -1 and right != -1 and left <= right:
        return text[left:right+1]
    
    return text


def format_error_response(url: str, goal: str, error_msg: str = None) -> str:
    """
    Format a standardized error response.
    
    Args:
        url: The URL that was attempted
        goal: The user's goal
        error_msg: Optional specific error message
        
    Returns:
        Formatted error response
    """
    response = f"The useful information in {url} for user goal {goal} as follows: \n\n"
    
    if error_msg:
        response += f"Error: {error_msg}\n\n"
    
    response += "Evidence in page: \n"
    response += "The provided webpage content could not be accessed. Please check the URL or file format.\n\n"
    response += "Summary: \n"
    response += "The webpage content could not be processed, and therefore, no information is available.\n\n"
    
    return response


def format_success_response(url: str, goal: str, evidence: str, summary: str) -> str:
    """
    Format a standardized success response.
    
    Args:
        url: The URL that was visited
        goal: The user's goal
        evidence: Extracted evidence
        summary: Generated summary
        
    Returns:
        Formatted success response
    """
    response = f"The useful information in {url} for user goal {goal} as follows: \n\n"
    response += f"Evidence in page: \n{evidence}\n\n"
    response += f"Summary: \n{summary}\n\n"
    return response


# ============================================================================
# Main Visit Tool
# ============================================================================

@register_tool('visit', allow_overwrite=True)
class Visit(BaseTool):
    """
    Visit tool for fetching and summarizing web content.
    
    This tool fetches webpage content using Jina API and generates
    structured summaries using LLM.
    """
    
    name = 'visit'
    description = 'Visit webpage(s) and return the summary of the content.'
    
    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": ["string", "array"],
                "items": {"type": "string"},
                "minItems": 1,
                "description": "The URL(s) of the webpage(s) to visit. Can be a single URL or an array of URLs."
            },
            "goal": {
                "type": "string",
                "description": "The goal of the visit for webpage(s)."
            }
        },
        "required": ["url", "goal"]
    }
    
    def __init__(self):
        """Initialize the Visit tool with configuration and logging"""
        super().__init__()
        # Lazy loading: config and logger are initialized on first use
        self._config = None
        self._logger = None
        self.console = Console()
    
    @property
    def config(self) -> VisitConfig:
        """Lazy-load configuration (only when first accessed)"""
        if self._config is None:
            self._config = VisitConfig.from_env()
        return self._config
    
    @property
    def logger(self) -> logging.Logger:
        """Lazy-load logger (only when first accessed)"""
        if self._logger is None:
            self._logger = setup_logger(self.config)
            self._logger.info("Visit tool initialized")
            self._logger.debug(f"Configuration: jina_timeout={self.config.visit_timeout}s, "
                             f"max_retries={self.config.jina_max_retries}")
        return self._logger
    
    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Main entry point for the visit tool.
        
        Args:
            params: Dictionary containing 'url' (str or list) and 'goal' (str)
            
        Returns:
            Formatted summary of webpage content
        """
        start_time = time.time()
        
        # Parse parameters
        try:
            url = params["url"]
            goal = params["goal"]
        except (KeyError, TypeError) as e:
            error_msg = "[Visit] Invalid request format: Input must be a JSON object containing 'url' and 'goal' fields"
            self.logger.error(f"Parameter parsing failed: {e}")
            return error_msg
        
        self.logger.info(f"Processing visit request - URL type: {type(url).__name__}, Goal: {goal[:50]}...")
        
        # Handle single URL
        if isinstance(url, str):
            response = self._process_single_url(url, goal)
        # Handle multiple URLs
        elif isinstance(url, list):
            response = self._process_multiple_urls(url, goal)
        else:
            error_msg = f"[Visit] Invalid URL type: {type(url).__name__}"
            self.logger.error(error_msg)
            return error_msg
        
        elapsed = time.time() - start_time
        self.logger.info(f"Visit request completed in {elapsed:.2f}s, response length: {len(response)}")
        
        return response.strip()
    
    def _process_single_url(self, url: str, goal: str) -> str:
        """
        Process a single URL.
        
        Args:
            url: URL to visit
            goal: User's goal
            
        Returns:
            Formatted response
        """
        self.logger.debug(f"Processing single URL: {url}")
        print(f"  → Fetching: {url}")
        result = self._fetch_and_summarize(url, goal)
        print(f"  ✓ Completed: {url}")
        return result
    
    def _process_multiple_urls(self, urls: List[str], goal: str) -> str:
        """
        Process multiple URLs with timeout protection.
        
        Args:
            urls: List of URLs to visit
            goal: User's goal
            
        Returns:
            Combined formatted responses
        """
        self.logger.info(f"Processing {len(urls)} URLs")
        responses = []
        start_time = time.time()
        
        for idx, url in enumerate(urls, 1):
            elapsed = time.time() - start_time
            
            # Check batch timeout
            if elapsed > self.config.batch_timeout:
                self.logger.warning(f"Batch timeout reached ({self.config.batch_timeout}s), "
                                   f"processed {idx-1}/{len(urls)} URLs")
                timeout_response = format_error_response(url, goal, "Batch timeout exceeded")
                responses.append(timeout_response)
                continue
            
            self.logger.debug(f"Processing URL {idx}/{len(urls)}: {url}")
            print(f"  → [{idx}/{len(urls)}] Fetching: {url}")
            
            cur_response = self._fetch_and_summarize(url, goal)
            responses.append(cur_response)
            print(f"  ✓ [{idx}/{len(urls)}] Completed: {url}")
        
        total_elapsed = time.time() - start_time
        self.logger.info(f"Batch processing completed: {len(urls)} URLs in {total_elapsed:.2f}s")
        
        return "\n=======\n".join(responses)
    
    def _fetch_and_summarize(self, url: str, goal: str) -> str:
        """
        Fetch webpage content and generate summary.
        
        Args:
            url: URL to fetch
            goal: User's goal
            
        Returns:
            Formatted summary response
        """
        self.logger.debug(f"Fetching and summarizing: {url}")
        
        # Fetch content
        content = self._fetch_html_content(url)
        
        # Check if fetch was successful
        if not content or content.startswith("[visit] Failed"):
            self.logger.warning(f"Failed to fetch content from: {url}")
            return format_error_response(url, goal, "Failed to fetch webpage")
        
        self.logger.debug(f"Fetched {len(content)} characters from {url}")
        
        # Generate summary
        return self._generate_summary(url, goal, content)
    
    def _fetch_html_content(self, url: str) -> str:
        """
        Fetch HTML content from URL with retries.
        
        Args:
            url: URL to fetch
            
        Returns:
            Webpage content or error message
        """
        self.logger.debug(f"Attempting to fetch HTML from: {url}")
        
        for attempt in range(1, self.config.html_read_max_attempts + 1):
            if attempt > 1:
                print(f"    ⟳ Retry attempt {attempt}/{self.config.html_read_max_attempts}...")
            self.logger.debug(f"Fetch attempt {attempt}/{self.config.html_read_max_attempts}")
            
            content = self._fetch_via_jina(url)
            
            # Check if content is valid
            if (content and 
                not content.startswith("[visit] Failed") and 
                content != "[visit] Empty content." and 
                not content.startswith("[document_parser]")):
                self.logger.debug(f"Successfully fetched content on attempt {attempt}")
                return content
            
            self.logger.debug(f"Attempt {attempt} failed: {content[:100] if content else 'None'}")
        
        self.logger.error(f"All {self.config.html_read_max_attempts} fetch attempts failed for: {url}")
        return "[visit] Failed to read page."
    
    def _fetch_via_jina(self, url: str) -> str:
        """
        Fetch webpage content via Jina API with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            Webpage content or error message
        """
        jina_endpoint = f"https://r.jina.ai/{url}"
        headers = {
            "Authorization": f"Bearer {self.config.jina_api_key}",
        }
        
        for attempt in range(1, self.config.jina_max_retries + 1):
            self.logger.debug(f"Jina API request attempt {attempt}/{self.config.jina_max_retries}: {url}")
            
            response = requests.get(
                jina_endpoint,
                headers=headers,
                timeout=self.config.visit_timeout
            )
            
            if response.status_code == 200:
                content = response.text
                self.logger.info(f"Jina API success: {len(content)} chars from {url}")
                return content
            
            # Log error details
            self.logger.warning(f"Jina API error (attempt {attempt}): "
                              f"status={response.status_code}, "
                              f"response={response.text[:200]}")
            
            # Retry delay (except on last attempt)
            if attempt < self.config.jina_max_retries:
                time.sleep(self.config.jina_retry_delay)
        
        self.logger.error(f"Jina API failed after {self.config.jina_max_retries} attempts: {url}")
        return "[visit] Failed to read page."
    
    def _generate_summary(self, url: str, goal: str, content: str) -> str:
        """
        Generate structured summary from webpage content using LLM.
        
        Args:
            url: Source URL
            goal: User's goal
            content: Webpage content
            
        Returns:
            Formatted summary response
        """
        self.logger.debug(f"Generating summary for {url}, content length: {len(content)}")
        
        # Truncate content to max tokens
        content = truncate_to_tokens(content, max_tokens=self.config.max_tokens)
        self.logger.debug(f"Content truncated to {len(content)} characters")
        
        print(f"    🤖 Generating summary with LLM...")
        # Try to get summary with progressive truncation
        summary_data = self._extract_with_llm(content, goal, url)
        print(f"    ✓ Summary generated")
        
        # Parse and format response
        if not summary_data:
            self.logger.warning(f"Failed to generate summary for {url}")
            return format_error_response(url, goal, "Summary generation failed")
        
        # Parse JSON response
        parsed_data = self._parse_summary_json(summary_data, url)
        
        if not parsed_data:
            self.logger.warning(f"Failed to parse summary JSON for {url}")
            return format_error_response(url, goal, "Summary parsing failed")
        
        # Format successful response
        return format_success_response(
            url=url,
            goal=goal,
            evidence=parsed_data.get("evidence", "No evidence extracted"),
            summary=parsed_data.get("summary", "No summary generated")
        )
    
    def _extract_with_llm(self, content: str, goal: str, url: str) -> Optional[str]:
        """
        Extract information using LLM with progressive truncation on failure.
        
        Args:
            content: Webpage content
            goal: User's goal
            url: Source URL (for logging)
            
        Returns:
            Raw LLM response or None
        """
        current_content = content
        summary_retries = 3
        
        while summary_retries >= 0:
            # Create extraction prompt
            messages = [{
                "role": "user",
                "content": EXTRACTOR_PROMPT.format(
                    webpage_content=current_content,
                    goal=goal
                )
            }]
            
            # Call LLM
            self.logger.debug(f"Calling LLM for extraction (retries left: {summary_retries})")
            raw_response = self._call_llm(messages)
            
            # Check if response is valid
            if raw_response and len(raw_response) >= 10:
                self.logger.debug("LLM extraction successful")
                return raw_response
            
            # Log failure and prepare retry
            attempt_num = 3 - summary_retries + 1
            self.logger.warning(f"LLM extraction attempt {attempt_num}/3 failed, "
                              f"response length: {len(raw_response) if raw_response else 0}")
            
            # Progressive truncation
            if summary_retries > 0:
                truncate_length = int(0.7 * len(current_content))
            else:
                truncate_length = 25000
            
            self.logger.debug(f"Truncating content from {len(current_content)} to {truncate_length} chars")
            current_content = current_content[:truncate_length]
            summary_retries -= 1
        
        self.logger.error(f"LLM extraction failed after all retries for {url}")
        return None
    
    def _parse_summary_json(self, raw_response: str, url: str) -> Optional[Dict]:
        """
        Parse JSON response from LLM with retry logic.
        
        Args:
            raw_response: Raw response from LLM
            url: Source URL (for logging)
            
        Returns:
            Parsed dictionary or None
        """
        # Clean response
        if isinstance(raw_response, str):
            raw_response = extract_json_from_text(raw_response)
        
        # Try to parse
        for attempt in range(1, self.config.parse_max_retries + 1):
            self.logger.debug(f"JSON parse attempt {attempt}/{self.config.parse_max_retries}")
            parsed = json.loads(raw_response)
            self.logger.debug("JSON parsing successful")
            return parsed
        
        self.logger.error(f"JSON parsing failed after {self.config.parse_max_retries} attempts for {url}")
        return None
    
    def _call_llm(self, messages: List[Dict], max_retries: int = None) -> str:
        """
        Call OpenRouter LLM API with retry logic.
        
        Args:
            messages: List of message dictionaries
            max_retries: Maximum retry attempts (uses config default if None)
            
        Returns:
            LLM response content or empty string
        """
        if max_retries is None:
            max_retries = self.config.summary_max_retries
        
        if not self.config.openrouter_api_key:
            self.logger.error("OpenRouter API key not set")
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
        client = OpenAI(
            api_key=self.config.openrouter_api_key,
            base_url=self.config.llm_base_url,
            timeout=600.0,
        )
        
        for attempt in range(1, max_retries + 1):
            self.logger.debug(f"LLM API call attempt {attempt}/{max_retries}")
            
            chat_response = client.chat.completions.create(
                model=self.config.summary_model_name,
                messages=messages,
                temperature=self.config.llm_temperature,
                extra_headers={
                    "HTTP-Referer": "https://github.com/QwenLM/DeepResearch",
                    "X-Title": "DeepResearch",
                }
            )
            
            # Validate response structure
            if not chat_response or not chat_response.choices:
                self.logger.warning(f"LLM returned invalid response on attempt {attempt}: no choices")
                continue
            
            if not chat_response.choices[0].message:
                self.logger.warning(f"LLM returned invalid response on attempt {attempt}: no message")
                continue
            
            content = chat_response.choices[0].message.content
            
            if content:
                self.logger.debug(f"LLM response received: {len(content)} characters")
                return extract_json_from_text(content)
            
            self.logger.warning(f"LLM returned empty content on attempt {attempt}")
        
        self.logger.error(f"LLM call failed after {max_retries} attempts")
        return ""
