# Sora Platform CLI

A clean, dedicated CLI tool for platform maintenance and monitoring without adding crons and background scripts to the main application.

## Installation

```bash
# Install dependencies
pip install click rich asyncio aiohttp

# Make executable
chmod +x sora_cli.py
```

## Quick Start

```bash
# Check integration health
aip health check

# Run maintenance task
aip maintenance run health_check

# Live monitoring dashboard
aip monitor dashboard

# Interactive mode
aip interactive
```

## Commands Overview

### 🏥 Health Monitoring

```bash
# Check all integrations
aip health check

# Check specific service
aip health check -s openai

# Continuous monitoring (updates every 5s)
aip health check --continuous
```

### 🔧 Maintenance Operations

```bash
# Run specific maintenance action
aip maintenance run health_check
aip maintenance run error_recovery
aip maintenance run performance_tuning
aip maintenance run cost_optimization
aip maintenance run cache_cleanup
aip maintenance run model_validation

# Dry run (see what would happen)
aip maintenance run health_check --dry-run

# Generate maintenance report
aip maintenance report --hours 24
```

### 🔌 Integration Management

```bash
# List all integrations
aip integrations list

# Filter by type
aip integrations list --type chatbot
aip integrations list --type simulator

# Add integration for user
aip integrations add openai sk-abc123... --user user123
```

### 📊 Real-time Monitoring

```bash
# Live dashboard
aip monitor dashboard

# Custom refresh interval
aip monitor dashboard --interval 5
```

### 💰 Cost Management

```bash
# Analyze costs
aip costs analyze --days 7

# Breakdown by service
aip costs analyze --by-service

# Get optimization recommendations
aip costs optimize
```

## Interactive Mode

Start an interactive session for easier command execution:

```bash
aip interactive

platform> health check
platform> maintenance run cache_cleanup
platform> costs analyze --days 30
platform> exit
```

## Output Examples

### Health Check Output
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     Integration Health Status - 2024-01-15 14:32:10     ┃
┡━━━━━━━━━━┯━━━━━━━━━━━━━┯━━━━━━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━┩
│ Service  │ Status      │ Response Time │ Issue    │ Details          │
├──────────┼─────────────┼──────────────┼──────────┼──────────────────┤
│ OPENAI   │ ✅ Healthy  │ 120ms        │ -        │ Working perfectly│
│ CLAUDE   │ ✅ Healthy  │ 89ms         │ -        │ Working perfectly│
│ STABLE   │ ❌ Error    │ -            │ API_KEY  │ Invalid API key  │
└──────────┴─────────────┴──────────────┴──────────┴──────────────────┘
```

### Cost Analysis Output
```
╭─────────────────────────────────────╮
│          Cost Analysis              │
│         Last 7 days                 │
├─────────────────────────────────────┤
│     Total Cost: $1,247.83          │
│ Total Requests: 45,672             │
│ Avg Cost/Request: $0.0273          │
│ Projected Monthly: $5,347.85       │
╰─────────────────────────────────────╯

Cost by Service
┏━━━━━━━━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━━━┓
┃ Service        │ Requests │ Cost     │ % of Total┃
┡━━━━━━━━━━━━━━━━┿━━━━━━━━━━┿━━━━━━━━━━┿━━━━━━━━━━━┩
│ OpenAI         │ 23,456   │ $567.23  │ 45.5%     │
│ Claude         │ 12,345   │ $345.67  │ 27.7%     │
│ Stable Diff    │ 5,678    │ $234.56  │ 18.8%     │
│ DALL-E         │ 3,456    │ $89.12   │ 7.1%      │
│ Others         │ 737      │ $11.25   │ 0.9%      │
└────────────────┴──────────┴──────────┴───────────┘
```

### Live Dashboard
```
╭─── Platform Status - 2024-01-15 14:35:22 ─────────╮
│                                                    │
│ ╭─── System Overview ───────────────────────────╮ │
│ │  Active Integrations: 12                      │ │
│ │  Total Requests Today: 4,567                  │ │
│ │  Total Cost Today: $124.56                    │ │
│ │  System Health: ✅ Operational                │ │
│ ╰───────────────────────────────────────────────╯ │
│                                                    │
│ ╭─── Active Issues ─────────────────────────────╮ │
│ │ Service  │ Issue           │ Since           │ │
│ ├──────────┼─────────────────┼─────────────────┤ │
│ │ STABLE   │ Invalid API key │ 2 minutes ago   │ │
│ ╰───────────────────────────────────────────────╯ │
╰────────────────────────────────────────────────────╯
```

## Automation Examples

### Cron Jobs (Run from CLI instead of in-app)

```bash
# Health check every 5 minutes
*/5 * * * * /path/to/sora_cli.py health check --json-output >> /var/log/sora/health.log

# Maintenance every hour
0 * * * * /path/to/sora_cli.py maintenance run health_check

# Cost report daily at 9 AM
0 9 * * * /path/to/sora_cli.py costs analyze --days 1 --json-output

# Cache cleanup nightly
0 2 * * * /path/to/sora_cli.py maintenance run cache_cleanup
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh - Simple monitoring wrapper

while true; do
    aip health check
    
    # Check exit code
    if [ $? -ne 0 ]; then
        # Send alert
        echo "Health check failed" | mail -s "Sora Platform Alert" admin@example.com
    fi
    
    sleep 300  # 5 minutes
done
```

### Integration with Other Tools

```bash
# Export to JSON for processing
aip health check --json-output | jq '.integrations[] | select(.status != "healthy")'

# Pipe to monitoring system
aip costs analyze --json-output | curl -X POST https://metrics.example.com/api/costs -d @-

# Generate daily report
aip maintenance report --hours 24 > /var/reports/daily-$(date +%Y%m%d).txt
```

## Benefits

1. **Clean Separation**: Maintenance logic separate from main app
2. **No App Bloat**: No crons or background workers in the application
3. **Easy Testing**: CLI commands can be tested independently
4. **Flexible Scheduling**: Use system cron, systemd timers, or orchestrators
5. **Rich Output**: Beautiful terminal UI with rich formatting
6. **Scriptable**: JSON output mode for automation
7. **Interactive Mode**: Quick commands without remembering syntax

## Development

### Adding New Commands

```python
@cli.command()
@click.option('--example', '-e', help='Example option')
@click.pass_context
def newcommand(ctx, example):
    """Description of new command"""
    console.print(f"[bold cyan]Running new command with {example}[/bold cyan]")
```

### Running Tests

```bash
# Run CLI tests
python -m pytest tests/test_cli.py

# Test specific command
aip health check --dry-run
```

This CLI provides all maintenance functionality in a clean, dedicated tool without adding complexity to the main application!