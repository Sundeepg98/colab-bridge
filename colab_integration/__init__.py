"""
Colab Bridge - Universal Google Colab Integration

A universal tool that allows any IDE, coding assistant, or Python application
to execute code in Google Colab with GPU access and ML libraries.

Example usage:
    from colab_integration import UniversalColabBridge
    
    bridge = UniversalColabBridge(tool_name="my_tool")
    result = bridge.execute_code("print('Hello from Colab!')")
    print(result['output'])
"""

from .universal_bridge import UniversalColabBridge
from .auto_colab import AutoColabManager

__version__ = "1.0.0"
__author__ = "sundeepg98"
__email__ = "sundeepg8@gmail.com"

__all__ = [
    "UniversalColabBridge",
    "AutoColabManager",
]