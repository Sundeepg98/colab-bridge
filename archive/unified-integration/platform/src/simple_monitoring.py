"""
Simple monitoring decorators without the hanging issue
"""

import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def simple_monitor(operation_type="unknown"):
    """Simple monitoring decorator that doesn't hang"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(f"{f.__name__} completed in {elapsed:.3f}s - type: {operation_type}")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"{f.__name__} failed after {elapsed:.3f}s - error: {e}")
                raise
        return decorated_function
    return decorator