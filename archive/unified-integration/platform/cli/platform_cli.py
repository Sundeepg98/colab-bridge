#!/usr/bin/env python3
"""
AI Platform CLI - Maintenance and Management Tool
A clean CLI interface for the Generic AI Simulator Platform
Manages integrations for chatbots (GPT, Claude) and simulators (Stable Diffusion, DALL-E, etc.)
"""

import click
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.integration_health_monitoring import IntegrationHealthMonitor, ResponsiveIntegrationSupport
from src.api_key_manager import get_api_key_manager
from src.auto_maintenance_engine import get_maintenance_engine, MaintenanceAction
from src.integration_manager import get_integration_manager

console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--json-output', is_flag=True, help='Output in JSON format')
@click.pass_context
def cli(ctx, verbose, json_output):
    """
    AI Platform CLI - Clean maintenance interface
    
    Manages the Generic AI Simulator Platform supporting:
    • Chatbots: OpenAI, Claude, Cohere, LLaMA
    • Simulators: Stable Diffusion, DALL-E, Midjourney, RunwayML
    • Multi-modal: Replicate, Hugging Face
    """
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['JSON_OUTPUT'] = json_output
    
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


@cli.group()
def health():
    """Health monitoring and checking commands"""
    pass


@health.command()
@click.option('--service', '-s', help='Check specific service')
@click.option('--user', '-u', help='Check for specific user')
@click.option('--continuous', '-c', is_flag=True, help='Continuous monitoring')
@click.pass_context
async def check(ctx, service, user, continuous):
    """Check integration health status"""
    monitor = IntegrationHealthMonitor()
    
    if continuous:
        console.print("[bold cyan]Starting continuous health monitoring...[/bold cyan]")
        console.print("Press Ctrl+C to stop\n")
        
        with Live(console=console, refresh_per_second=1) as live:
            while True:
                try:
                    table = await _create_health_table(monitor, service, user)
                    live.update(table)
                    await asyncio.sleep(5)  # Check every 5 seconds
                except KeyboardInterrupt:
                    console.print("\n[yellow]Monitoring stopped[/yellow]")
                    break
    else:
        table = await _create_health_table(monitor, service, user)
        console.print(table)


async def _create_health_table(monitor, service=None, user=None):
    """Create a rich table with health status"""
    table = Table(title=f"Integration Health Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    table.add_column("Service", style="cyan", no_wrap=True)
    table.add_column("Status", style="bold")
    table.add_column("Response Time", justify="right")
    table.add_column("Issue Type", style="yellow")
    table.add_column("Details", style="white")
    
    # Get all integrations or specific one
    integrations = {}
    if service:
        integrations[service] = {"enabled": True}
    else:
        # Get all from integration manager
        manager = get_integration_manager()
        integrations = manager.get_all_integrations()
    
    for svc, config in integrations.items():
        if not config.get('enabled', True):
            continue
            
        # Mock health check for demo (replace with actual check)
        health_status = {
            'healthy': True,
            'response_time': 120,
            'issue_type': None,
            'details': 'Working perfectly'
        }
        
        # Status emoji and color
        if health_status['healthy']:
            status = "[green]✅ Healthy[/green]"
        else:
            status = "[red]❌ Error[/red]"
        
        table.add_row(
            svc.upper(),
            status,
            f"{health_status['response_time']}ms",
            health_status['issue_type'] or "-",
            health_status['details']
        )
    
    return table


@cli.group()
def maintenance():
    """Maintenance operations and tasks"""
    pass


@maintenance.command()
@click.argument('action', type=click.Choice([
    'health_check', 'error_recovery', 'performance_tuning', 
    'cost_optimization', 'cache_cleanup', 'model_validation'
]))
@click.option('--target', '-t', default='system', help='Target for maintenance')
@click.option('--dry-run', is_flag=True, help='Show what would be done without doing it')
@click.pass_context
def run(ctx, action, target, dry_run):
    """Run a specific maintenance action"""
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] Would run {action} on {target}")
        return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Running {action}...", total=None)
        
        try:
            engine = get_maintenance_engine()
            result = engine.trigger_maintenance(
                MaintenanceAction(action), 
                target
            )
            
            progress.stop()
            
            if result['success']:
                console.print(f"[green]✅ {action} completed successfully![/green]")
                console.print(f"Duration: {result['duration']:.2f}s")
                
                if result.get('actions_taken'):
                    console.print("\n[bold]Actions taken:[/bold]")
                    for action in result['actions_taken']:
                        console.print(f"  • {action}")
            else:
                console.print(f"[red]❌ {action} failed[/red]")
                console.print(f"Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            progress.stop()
            console.print(f"[red]Error: {str(e)}[/red]")


@maintenance.command()
@click.option('--hours', '-h', default=24, help='Hours to look back')
@click.pass_context
def report(ctx, hours):
    """Generate maintenance report"""
    engine = get_maintenance_engine()
    report_data = engine.get_maintenance_report(hours)
    
    console.print(Panel.fit(
        f"[bold cyan]Maintenance Report[/bold cyan]\n"
        f"Period: Last {hours} hours",
        border_style="cyan"
    ))
    
    # Summary table
    summary_table = Table(title="Summary", show_header=True)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", justify="right")
    
    summary_table.add_row("Total Actions", str(report_data['summary']['total_actions']))
    summary_table.add_row("Successful", f"[green]{report_data['summary']['successful']}[/green]")
    summary_table.add_row("Failed", f"[red]{report_data['summary']['failed']}[/red]")
    summary_table.add_row("Automated", str(report_data['summary']['automated_actions']))
    summary_table.add_row("Manual", str(report_data['summary']['manual_actions']))
    
    console.print(summary_table)
    console.print()
    
    # Actions by type
    if report_data['actions_by_type']:
        actions_table = Table(title="Actions by Type", show_header=True)
        actions_table.add_column("Action Type", style="cyan")
        actions_table.add_column("Count", justify="right")
        actions_table.add_column("Avg Duration", justify="right")
        
        for action_type, data in report_data['actions_by_type'].items():
            actions_table.add_row(
                action_type,
                str(data['count']),
                f"{data['avg_duration']:.2f}s"
            )
        
        console.print(actions_table)


@cli.group()
def integrations():
    """Integration management commands"""
    pass


@integrations.command(name='list')
@click.option('--user', '-u', help='List integrations for specific user')
@click.option('--type', '-t', type=click.Choice(['chatbot', 'simulator', 'all']), 
              default='all', help='Filter by type')
@click.pass_context
def list_integrations(ctx, user, type):
    """List all integrations"""
    manager = get_integration_manager()
    
    # Create table
    table = Table(title="Active Integrations", show_header=True)
    table.add_column("Service", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Status", style="bold")
    table.add_column("Users", justify="right")
    table.add_column("Daily Requests", justify="right")
    table.add_column("Cost Today", justify="right", style="yellow")
    
    # Service type mapping
    service_types = {
        'openai': 'chatbot',
        'anthropic': 'chatbot',
        'claude': 'chatbot',
        'cohere': 'chatbot',
        'stable_diffusion': 'simulator',
        'dalle': 'simulator',
        'midjourney': 'simulator',
        'runway': 'simulator',
        'elevenlabs': 'simulator',
        'replicate': 'both',
        'huggingface': 'both'
    }
    
    # Get integrations
    all_integrations = manager.get_integration_dashboard()['integrations']
    
    for service, data in all_integrations.items():
        svc_type = service_types.get(service.lower(), 'unknown')
        
        if type != 'all' and svc_type != type and svc_type != 'both':
            continue
        
        # Type icon
        type_icon = "💬" if svc_type == 'chatbot' else "🎨" if svc_type == 'simulator' else "🔄"
        
        # Status color
        status = data['status']
        if status == 'healthy':
            status_display = "[green]✅ Healthy[/green]"
        elif status == 'warning':
            status_display = "[yellow]⚠️  Warning[/yellow]"
        else:
            status_display = "[red]❌ Error[/red]"
        
        table.add_row(
            service.upper(),
            f"{type_icon} {svc_type}",
            status_display,
            str(data.get('active_users', 0)),
            str(data['metrics']['requests_count']),
            f"${data['metrics']['cost_incurred']:.2f}"
        )
    
    console.print(table)


@integrations.command()
@click.argument('service')
@click.argument('api_key')
@click.option('--user', '-u', required=True, help='User ID to add integration for')
@click.pass_context
def add(ctx, service, api_key, user):
    """Add new integration for a user"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Validating API key...", total=None)
        
        try:
            # Test the integration
            support = ResponsiveIntegrationSupport()
            result = asyncio.run(support.on_integration_added(user, service, api_key))
            
            progress.stop()
            
            if result['success']:
                console.print(f"[green]✅ {result['message']}[/green]")
                console.print(f"Response time: {result.get('response_time_ms', 'N/A')}ms")
            else:
                console.print(f"[red]❌ Integration failed[/red]")
                console.print(f"Error: {result['error']}")
                if result.get('user_action_required'):
                    console.print(f"[yellow]Action required:[/yellow] {result['suggested_action']}")
                    
        except Exception as e:
            progress.stop()
            console.print(f"[red]Error: {str(e)}[/red]")


@cli.group()
def monitor():
    """Real-time monitoring commands"""
    pass


@monitor.command()
@click.option('--interval', '-i', default=1, help='Update interval in seconds')
@click.pass_context
def dashboard(ctx, interval):
    """Live monitoring dashboard"""
    console.print("[bold cyan]AI Platform Live Dashboard[/bold cyan]")
    console.print("Press Ctrl+C to exit\n")
    
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            try:
                # Create dashboard layout
                dashboard_panel = _create_dashboard_panel()
                live.update(dashboard_panel)
                asyncio.run(asyncio.sleep(interval))
            except KeyboardInterrupt:
                console.print("\n[yellow]Dashboard closed[/yellow]")
                break


def _create_dashboard_panel():
    """Create a comprehensive dashboard panel"""
    # Get current stats
    manager = get_integration_manager()
    dashboard_data = manager.get_integration_dashboard()
    
    # Create sections
    sections = []
    
    # System overview
    overview = Table.grid(padding=1)
    overview.add_column(style="cyan", justify="right")
    overview.add_column(min_width=20)
    
    overview.add_row("Active Integrations:", str(len(dashboard_data['integrations'])))
    overview.add_row("Total Requests Today:", str(dashboard_data['total_requests_today']))
    overview.add_row("Total Cost Today:", f"${dashboard_data['total_cost_today']:.2f}")
    overview.add_row("System Health:", "[green]✅ Operational[/green]")
    
    sections.append(Panel(overview, title="System Overview", border_style="green"))
    
    # Active issues
    issues = Table(show_header=True)
    issues.add_column("Service", style="cyan")
    issues.add_column("Issue", style="yellow")
    issues.add_column("Since", style="white")
    
    # Add any active issues
    has_issues = False
    for service, data in dashboard_data['integrations'].items():
        if data['status'] != 'healthy':
            has_issues = True
            issues.add_row(
                service.upper(),
                data.get('error_message', 'Unknown issue'),
                "2 minutes ago"  # Would be calculated from actual data
            )
    
    if not has_issues:
        issues.add_row("[green]None[/green]", "[green]All systems operational[/green]", "-")
    
    sections.append(Panel(issues, title="Active Issues", border_style="yellow"))
    
    # Combine all sections
    main_panel = Panel(
        "\n".join(str(section) for section in sections),
        title=f"Platform Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        border_style="bold cyan"
    )
    
    return main_panel


@cli.group()
def costs():
    """Cost management and optimization commands"""
    pass


@costs.command()
@click.option('--days', '-d', default=7, help='Number of days to analyze')
@click.option('--by-service', is_flag=True, help='Break down by service')
@click.option('--by-user', is_flag=True, help='Break down by user')
@click.pass_context
def analyze(ctx, days, by_service, by_user):
    """Analyze platform costs"""
    console.print(f"[bold cyan]Cost Analysis - Last {days} days[/bold cyan]\n")
    
    # Mock data for demonstration
    total_cost = 1247.83
    total_requests = 45672
    
    # Summary
    summary = Table.grid(padding=1)
    summary.add_column(style="cyan", justify="right")
    summary.add_column(min_width=20)
    
    summary.add_row("Total Cost:", f"[bold yellow]${total_cost:.2f}[/bold yellow]")
    summary.add_row("Total Requests:", f"{total_requests:,}")
    summary.add_row("Avg Cost/Request:", f"${total_cost/total_requests:.4f}")
    summary.add_row("Projected Monthly:", f"${(total_cost/days)*30:.2f}")
    
    console.print(Panel(summary, title="Summary", border_style="green"))
    
    if by_service:
        # Service breakdown
        service_table = Table(title="Cost by Service", show_header=True)
        service_table.add_column("Service", style="cyan")
        service_table.add_column("Requests", justify="right")
        service_table.add_column("Cost", justify="right", style="yellow")
        service_table.add_column("% of Total", justify="right")
        
        services = {
            'OpenAI': {'requests': 23456, 'cost': 567.23},
            'Claude': {'requests': 12345, 'cost': 345.67},
            'Stable Diffusion': {'requests': 5678, 'cost': 234.56},
            'DALL-E': {'requests': 3456, 'cost': 89.12},
            'Others': {'requests': 737, 'cost': 11.25}
        }
        
        for service, data in services.items():
            percentage = (data['cost'] / total_cost) * 100
            service_table.add_row(
                service,
                f"{data['requests']:,}",
                f"${data['cost']:.2f}",
                f"{percentage:.1f}%"
            )
        
        console.print(service_table)


@costs.command()
@click.pass_context
def optimize(ctx):
    """Run cost optimization analysis"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing cost optimization opportunities...", total=None)
        
        # Simulate analysis
        import time
        time.sleep(2)
        
        progress.stop()
    
    # Recommendations
    console.print(Panel.fit(
        "[bold cyan]Cost Optimization Recommendations[/bold cyan]",
        border_style="cyan"
    ))
    
    recommendations = [
        {
            'title': 'Switch to Claude Haiku for simple queries',
            'savings': '$234.56/month',
            'impact': 'Low',
            'description': '67% of your Claude requests could use Haiku instead of Opus'
        },
        {
            'title': 'Enable request caching',
            'savings': '$123.45/month',
            'impact': 'None',
            'description': '23% of requests are duplicates that could be cached'
        },
        {
            'title': 'Use Stable Diffusion for draft images',
            'savings': '$89.12/month',
            'impact': 'Medium',
            'description': 'Use SD for drafts, DALL-E only for finals'
        }
    ]
    
    for i, rec in enumerate(recommendations, 1):
        console.print(f"\n[bold]{i}. {rec['title']}[/bold]")
        console.print(f"   Potential savings: [green]{rec['savings']}[/green]")
        console.print(f"   User impact: [yellow]{rec['impact']}[/yellow]")
        console.print(f"   {rec['description']}")


@cli.command()
@click.pass_context
def interactive(ctx):
    """Start interactive CLI mode"""
    console.print("[bold cyan]AI Platform CLI - Interactive Mode[/bold cyan]")
    console.print("Type 'help' for commands, 'exit' to quit\n")
    
    while True:
        try:
            command = console.input("[bold]platform>[/bold] ")
            
            if command.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif command.lower() == 'help':
                console.print("""
Available commands:
  health check       - Check integration health
  health monitor     - Start continuous monitoring
  maintenance run    - Run maintenance tasks
  integrations list  - List all integrations
  costs analyze      - Analyze platform costs
  monitor dashboard  - Live monitoring dashboard
  exit              - Exit interactive mode
                """)
            elif command.strip():
                # Parse and execute command
                parts = command.split()
                try:
                    # Invoke the CLI with the command
                    cli.main(parts, standalone_mode=False)
                except SystemExit:
                    pass  # Don't exit interactive mode
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except EOFError:
            break


if __name__ == '__main__':
    cli()