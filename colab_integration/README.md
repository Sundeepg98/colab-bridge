# Colab Integration Tool

This tool enables Claude Coder to execute code in Google Colab notebooks.

## Components

- **bridge.py** - Client that sends commands from Claude to Colab
- **processor.py** - Runs in Colab to process commands

## Setup

See the [Colab Integration Guide](../docs/guides/COLAB_INTEGRATION.md) for detailed setup instructions.

## Quick Usage

```python
from colab_integration.bridge import ClaudeColabBridge

bridge = ClaudeColabBridge()
result = bridge.execute_code("print('Hello from Colab!')")
print(result['output'])
```

## Features

- Execute Python code remotely
- Install packages in Colab
- Run shell commands
- Access GPU/TPU resources
- Multi-instance support