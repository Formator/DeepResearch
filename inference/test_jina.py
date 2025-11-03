"""
Enhanced standalone script to test Jina API and Visit tool
Features:
- Tests Jina API connection
- Validates configuration
- Tests full Visit tool functionality
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment first
load_dotenv()

# Import after loading env
from tool_visit import Visit, VisitConfig

console = Console()


def test_configuration():
    """Test configuration loading and validation"""
    console.print("\n[bold cyan]📋 Testing Configuration[/bold cyan]\n")
    
    config = VisitConfig.from_env()
    
    # Display configuration
    table = Table(title="Visit Tool Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Jina API Key", f"{config.jina_api_key[:15]}...{config.jina_api_key[-10:]}" if config.jina_api_key else "❌ NOT SET")
    table.add_row("OpenRouter API Key", f"{config.openrouter_api_key[:15]}..." if config.openrouter_api_key else "❌ NOT SET")
    table.add_row("Summary Model", config.summary_model_name)
    table.add_row("Jina Timeout", f"{config.visit_timeout}s")
    table.add_row("Max Retries", str(config.jina_max_retries))
    table.add_row("Debug Logging", "✓" if config.enable_debug_logging else "✗")
    table.add_row("Log Directory", config.log_dir)
    
    console.print(table)
    console.print()
    
    # Validate
    config.validate()
    console.print("[green]✓[/green] Configuration validated successfully!\n")
    
    return config


def test_jina_direct():
    """Test Jina API directly"""
    console.print("[bold cyan]🔍 Testing Direct Jina API Connection[/bold cyan]\n")
    
    config = VisitConfig.from_env()
    
    if not config.jina_api_key:
        console.print("[red]✗[/red] Jina API key not found!")
        return False
    
    import requests
    
    test_url = "https://www.google.com"
    jina_endpoint = f"https://r.jina.ai/{test_url}"
    
    console.print(f"Testing: {test_url}")
    console.print(f"Endpoint: {jina_endpoint}\n")
    
    headers = {
        "Authorization": f"Bearer {config.jina_api_key}",
    }
    
    response = requests.get(jina_endpoint, headers=headers, timeout=30)
    
    if response.status_code == 200:
        content = response.text
        console.print(Panel.fit(
            f"[bold green]✅ Success![/bold green]\n\n"
            f"Status: {response.status_code}\n"
            f"Response length: {len(content)} characters\n"
            f"Preview: {content[:200]}...",
            border_style="green",
            title="Jina API Test"
        ))
        return True
    else:
        console.print(Panel.fit(
            f"[bold red]❌ Failed[/bold red]\n\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text[:500]}",
            border_style="red",
            title="Jina API Error"
        ))
        return False


def test_visit_tool():
    """Test the full Visit tool functionality"""
    console.print("\n[bold cyan]🔧 Testing Visit Tool[/bold cyan]\n")
    
    # Initialize Visit tool
    console.print("Initializing Visit tool...")
    visit_tool = Visit()
    console.print("[green]✓[/green] Visit tool initialized\n")
    
    # Test single URL
    console.print("[bold]Test 1: Single URL Visit[/bold]")
    test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    test_goal = "Get a brief overview of Python programming language"
    
    console.print(f"URL: {test_url}")
    console.print(f"Goal: {test_goal}\n")
    
    params = {
        "url": test_url,
        "goal": test_goal
    }
    
    console.print("Fetching and summarizing... (this may take a moment)\n")
    
    result = visit_tool.call(params)
    
    if result and not result.startswith("[Visit] Failed"):
        console.print(Panel(
            result[:500] + "..." if len(result) > 500 else result,
            title="[green]Visit Tool Result[/green]",
            border_style="green"
        ))
        console.print(f"\n[green]✓[/green] Full response length: {len(result)} characters")
        return True
    else:
        console.print(Panel(
            result[:500] if result else "No response",
            title="[red]Visit Tool Error[/red]",
            border_style="red"
        ))
        return False


def main():
    """Run all tests"""
    console.print("\n" + "="*70)
    console.print("[bold magenta]🧪 Visit Tool Test Suite[/bold magenta]")
    console.print("="*70)
    
    results = {}
    
    # Test 1: Configuration
    results["configuration"] = test_configuration()
    
    # Test 2: Direct Jina API
    results["jina_api"] = test_jina_direct()
    
    # Test 3: Full Visit Tool (only if previous tests passed)
    if results["configuration"] and results["jina_api"]:
        results["visit_tool"] = test_visit_tool()
    else:
        console.print("\n[yellow]⚠[/yellow] Skipping Visit Tool test due to previous failures")
        results["visit_tool"] = False
    
    # Summary
    console.print("\n" + "="*70)
    console.print("[bold cyan]📊 Test Summary[/bold cyan]")
    console.print("="*70 + "\n")
    
    table = Table()
    table.add_column("Test", style="cyan")
    table.add_column("Result", style="bold")
    
    for test_name, passed in results.items():
        status = "[green]✓ PASSED[/green]" if passed else "[red]✗ FAILED[/red]"
        table.add_row(test_name.replace("_", " ").title(), status)
    
    console.print(table)
    
    # Final verdict
    all_passed = all(results.values())
    console.print()
    
    if all_passed:
        console.print(Panel.fit(
            "[bold green]🎉 All tests passed![/bold green]\n\n"
            "Your Visit tool is configured correctly and working as expected.\n"
            "Check the log/ directory for detailed execution logs.",
            border_style="green",
            title="Success"
        ))
    else:
        failed_tests = [name for name, passed in results.items() if not passed]
        console.print(Panel.fit(
            f"[bold red]❌ Some tests failed[/bold red]\n\n"
            f"Failed tests: {', '.join(failed_tests)}\n\n"
            "Please check the error messages above and:\n"
            "1. Verify your API keys in .env file\n"
            "2. Check network connectivity\n"
            "3. Review logs in log/ directory",
            border_style="red",
            title="Failure"
        ))
    
    console.print()


if __name__ == "__main__":
    main()
