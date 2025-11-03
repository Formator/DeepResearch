"""
Run DeepResearch using OpenRouter API
No local model deployment needed - fully cloud-based solution

Usage:
    python run_openrouter.py --topic "Yang Zhenning" --output "./outputs"
"""

import argparse
import json
import os
from datetime import datetime
from react_agent_openrouter import MultiTurnReactAgent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint
import time

from dotenv import load_dotenv
load_dotenv()

console = Console()

def ensure_env_vars():
    """Check if required environment variables are set"""
    required_vars = {
        "OPENROUTER_API_KEY": "Get from https://openrouter.ai/",
        "SERPER_KEY_ID": "Get from https://serper.dev/",
        "JINA_API_KEYS": "Get from https://jina.ai/",
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  - {var}: {description}")
    
    if missing_vars:
        console.print("\n[bold red]❌ Missing required environment variables:[/bold red]")
        for var in missing_vars:
            console.print(f"[yellow]{var}[/yellow]")
        console.print("\n[bold cyan]Please set these in your .env file or export them:[/bold cyan]")
        console.print("  export OPENROUTER_API_KEY='your-key-here'")
        console.print("  export SERPER_KEY_ID='your-key-here'")
        console.print("  export JINA_API_KEYS='your-key-here'")
        return False
    return True

def save_result(result: dict, output_dir: str, topic: str):
    """Save the research result to a file"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
    safe_topic = safe_topic.replace(' ', '_')[:50]
    
    # Save full result as JSON
    json_path = os.path.join(output_dir, f"{safe_topic}_{timestamp}_full.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # Save readable markdown version
    md_path = os.path.join(output_dir, f"{safe_topic}_{timestamp}_readable.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Deep Research: {topic}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Question\n{result['question']}\n\n")
        f.write(f"## Answer\n{result['prediction']}\n\n")
        f.write(f"## Status\n- Termination: {result['termination']}\n")
        f.write(f"- Total rounds: {len([m for m in result['messages'] if m['role'] == 'assistant'])}\n\n")
        f.write(f"## Research Process\n\n")
        
        for i, msg in enumerate(result['messages']):
            if msg['role'] == 'system':
                continue
            elif msg['role'] == 'user':
                if '<tool_response>' in msg['content']:
                    f.write(f"### Tool Response {i}\n```\n{msg['content']}\n```\n\n")
                else:
                    f.write(f"### User Query\n{msg['content']}\n\n")
            elif msg['role'] == 'assistant':
                f.write(f"### Agent Action {i}\n{msg['content']}\n\n")
    
    return json_path, md_path

def run_research(topic: str, output_dir: str, model_name: str, temperature: float, top_p: float):
    """Run deep research on the given topic"""
    
    console.print(Panel.fit(
        f"[bold cyan]🔍 Starting Deep Research[/bold cyan]\n"
        f"Topic: [yellow]{topic}[/yellow]\n"
        f"Model: [green]{model_name}[/green]\n"
        f"Output: [blue]{output_dir}[/blue]",
        border_style="cyan"
    ))
    
    # Configure the LLM
    llm_cfg = {
        'model': model_name,
        'generate_cfg': {
            'temperature': temperature,
            'top_p': top_p,
        },
    }
    
    # Initialize the agent
    console.print("\n[bold green]✓[/bold green] Initializing agent...")
    agent = MultiTurnReactAgent(
        llm=llm_cfg,
        function_list=["search", "visit", "google_scholar", "PythonInterpreter"]
    )
    
    # Run the research
    console.print("[bold green]✓[/bold green] Starting research process...\n")
    start_time = time.time()
    
    try:
        result = agent._run(question=topic, answer="")
        
        elapsed_time = time.time() - start_time
        
        # Save results
        console.print("\n[bold green]✓[/bold green] Research completed! Saving results...")
        json_path, md_path = save_result(result, output_dir, topic)
        
        # Display summary
        console.print("\n" + "="*80)
        console.print(Panel.fit(
            f"[bold green]✅ Research Complete![/bold green]\n\n"
            f"Time elapsed: [cyan]{elapsed_time/60:.1f} minutes[/cyan]\n"
            f"Status: [yellow]{result['termination']}[/yellow]\n"
            f"Rounds: [blue]{len([m for m in result['messages'] if m['role'] == 'assistant'])}[/blue]\n\n"
            f"[bold]Output files:[/bold]\n"
            f"  📄 Full JSON: [blue]{json_path}[/blue]\n"
            f"  📝 Readable MD: [blue]{md_path}[/blue]",
            border_style="green"
        ))
        
        # Display the answer
        console.print("\n[bold cyan]📋 Final Answer:[/bold cyan]")
        console.print(Panel(
            Markdown(result['prediction']),
            border_style="cyan",
            title="Research Result"
        ))
        
        return result
        
    except KeyboardInterrupt:
        console.print("\n[bold red]❌ Research interrupted by user[/bold red]")
        return None
    except Exception as e:
        console.print(f"\n[bold red]❌ Error during research: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Run DeepResearch using OpenRouter API - No local deployment needed!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python run_openrouter.py --topic "Yang Zhenning"
  
  # With custom output directory
  python run_openrouter.py --topic "Yang Zhenning" --output "./my_research"
  
  # With custom model and parameters
  python run_openrouter.py --topic "Quantum Computing" --model "alibaba/tongyi-deepresearch-30b-a3b" --temperature 0.7

Environment Variables Required:
  OPENROUTER_API_KEY  - Your OpenRouter API key (https://openrouter.ai/)
  SERPER_KEY_ID       - Your Serper API key for search (https://serper.dev/)
  JINA_API_KEYS       - Your Jina API key for web scraping (https://jina.ai/)
  SUMMARY_MODEL_NAME  - (Optional) Model name for summarization via OpenRouter (default: alibaba/qwen-max)
        """
    )
    
    parser.add_argument(
        "--topic",
        type=str,
        default="Yang Zhenning",
        help="The research topic/question (default: Yang Zhenning)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./outputs/openrouter",
        help="Output directory for results (default: ./outputs/openrouter)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="alibaba/tongyi-deepresearch-30b-a3b",
        help="Model name on OpenRouter (default: alibaba/tongyi-deepresearch-30b-a3b)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.6,
        help="Temperature for generation (default: 0.6)"
    )
    
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.95,
        help="Top-p for generation (default: 0.95)"
    )
    
    args = parser.parse_args()
    
    # Check environment variables
    if not ensure_env_vars():
        return
    
    # Set default summary model if not set (using OpenRouter Qwen model)
    if not os.getenv("SUMMARY_MODEL_NAME"):
        os.environ["SUMMARY_MODEL_NAME"] = "alibaba/tongyi-deepresearch-30b-a3b"
    
    # Run the research
    run_research(
        topic=args.topic,
        output_dir=args.output,
        model_name=args.model,
        temperature=args.temperature,
        top_p=args.top_p
    )

if __name__ == "__main__":
    main()

