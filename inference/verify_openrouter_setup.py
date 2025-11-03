"""
Verify OpenRouter setup and test API connections
Run this before starting your first research to ensure everything is configured correctly
"""

import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

def check_env_var(var_name: str, description: str) -> tuple:
    """Check if an environment variable is set"""
    value = os.getenv(var_name)
    if value:
        # Mask the key for security
        masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
        return True, masked
    return False, "Not set"

def test_openrouter():
    """Test OpenRouter API connection"""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return False, "API key not set"
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=10.0,
        )
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="alibaba/tongyi-deepresearch-30b-a3b",
            messages=[{"role": "user", "content": "Say 'test' in one word"}],
            max_tokens=10
        )
        
        return True, "Connected successfully"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"

def test_serper():
    """Test Serper API connection"""
    try:
        import http.client
        import json
        
        api_key = os.getenv("SERPER_KEY_ID")
        if not api_key:
            return False, "API key not set"
        
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": "test"})
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        
        if res.status == 200:
            return True, "Connected successfully"
        else:
            return False, f"HTTP {res.status}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"

def test_jina():
    """Test Jina API connection"""
    try:
        import requests
        
        api_key = os.getenv("JINA_API_KEYS")
        if not api_key:
            return False, "API key not set"
        
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(
            "https://r.jina.ai/https://example.com",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Connected successfully"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"

def test_openai():
    """Test OpenAI API connection"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("API_KEY")
        api_base = os.getenv("API_BASE")
        
        if not api_key:
            return False, "API key not set"
        if not api_base:
            return False, "API base not set"
        
        client = OpenAI(api_key=api_key, base_url=api_base, timeout=10.0)
        
        response = client.chat.completions.create(
            model=os.getenv("SUMMARY_MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "Say 'test' in one word"}],
            max_tokens=10
        )
        
        return True, "Connected successfully"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"

def main():
    console.print(Panel.fit(
        "[bold cyan]🔧 DeepResearch OpenRouter Setup Verification[/bold cyan]\n"
        "This script will check your configuration and test API connections",
        border_style="cyan"
    ))
    
    # Check environment variables
    console.print("\n[bold]📋 Step 1: Checking Environment Variables[/bold]\n")
    
    env_table = Table(title="Environment Variables")
    env_table.add_column("Variable", style="cyan")
    env_table.add_column("Description", style="white")
    env_table.add_column("Status", style="green")
    env_table.add_column("Value", style="yellow")
    
    env_checks = [
        ("OPENROUTER_API_KEY", "OpenRouter API key", check_env_var("OPENROUTER_API_KEY", "OpenRouter")),
        ("SERPER_KEY_ID", "Serper search API key", check_env_var("SERPER_KEY_ID", "Serper")),
        ("JINA_API_KEYS", "Jina web reading API key", check_env_var("JINA_API_KEYS", "Jina")),
        ("API_KEY", "OpenAI API key", check_env_var("API_KEY", "OpenAI")),
        ("API_BASE", "OpenAI API base URL", check_env_var("API_BASE", "OpenAI")),
    ]
    
    all_env_ok = True
    for var_name, description, (status, value) in env_checks:
        status_icon = "✓" if status else "✗"
        status_color = "green" if status else "red"
        env_table.add_row(
            var_name,
            description,
            f"[{status_color}]{status_icon}[/{status_color}]",
            value
        )
        if not status:
            all_env_ok = False
    
    console.print(env_table)
    
    if not all_env_ok:
        console.print("\n[bold red]❌ Some environment variables are missing![/bold red]")
        console.print("\n[yellow]To fix this:[/yellow]")
        console.print("1. Copy the example file: [cyan]cp .env.openrouter.example .env[/cyan]")
        console.print("2. Edit .env and add your API keys")
        console.print("3. Run this script again")
        return False
    
    console.print("\n[bold green]✓ All environment variables are set![/bold green]")
    
    # Test API connections
    console.print("\n[bold]🌐 Step 2: Testing API Connections[/bold]\n")
    console.print("[dim]This may take a few seconds...[/dim]\n")
    
    api_table = Table(title="API Connection Tests")
    api_table.add_column("Service", style="cyan")
    api_table.add_column("Purpose", style="white")
    api_table.add_column("Status", style="green")
    api_table.add_column("Details", style="yellow")
    
    api_tests = [
        ("OpenRouter", "Main LLM", test_openrouter),
        ("Serper", "Web Search", test_serper),
        ("Jina AI", "Web Reading", test_jina),
        ("OpenAI/Compatible", "Summarization", test_openai),
    ]
    
    all_api_ok = True
    for service_name, purpose, test_func in api_tests:
        with console.status(f"[yellow]Testing {service_name}...[/yellow]"):
            status, message = test_func()
        
        status_icon = "✓" if status else "✗"
        status_color = "green" if status else "red"
        api_table.add_row(
            service_name,
            purpose,
            f"[{status_color}]{status_icon}[/{status_color}]",
            message
        )
        if not status:
            all_api_ok = False
    
    console.print(api_table)
    
    # Final summary
    console.print("\n" + "="*80 + "\n")
    
    if all_env_ok and all_api_ok:
        console.print(Panel.fit(
            "[bold green]✅ Setup Complete![/bold green]\n\n"
            "All checks passed! You're ready to run DeepResearch.\n\n"
            "[bold]Next steps:[/bold]\n"
            "1. Run a test: [cyan]python run_openrouter.py --topic \"test\"[/cyan]\n"
            "2. Research Yang Zhenning: [cyan]bash run_openrouter_yang.sh[/cyan]\n"
            "3. Custom topic: [cyan]python run_openrouter.py --topic \"your topic\"[/cyan]",
            border_style="green"
        ))
        return True
    else:
        console.print(Panel.fit(
            "[bold red]❌ Setup Incomplete[/bold red]\n\n"
            "Some checks failed. Please review the errors above.\n\n"
            "[bold]Common issues:[/bold]\n"
            "• Invalid API keys - Check your credentials\n"
            "• Network issues - Check your internet connection\n"
            "• API quotas - Ensure you have remaining credits\n"
            "• Wrong API base URL - Verify your .env settings",
            border_style="red"
        ))
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Verification cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)

