"""
engine.py - Simple Execution Engine

Runs steps sequentially, emits live logs, handles errors.
"""

from .events import emit


class Engine:
    """
    Simple execution engine that runs steps in order.
    
    Each step:
    - Emits STARTED
    - Executes function
    - Emits SUCCESS or FAILED
    """
    
    def __init__(self):
        """Initialize engine."""
        self.steps = []
    
    def add_step(self, order, name, tool, func, retries=0):
        """
        Add a step to execute.
        
        Args:
            order: Step order (1, 2, 3, ...)
            name: Human-readable step name
            tool: Tool/service name
            func: Function to execute (takes context dict)
        """
        # store retry count per step
        self.steps.append((order, name, tool, func, int(retries)))
    
    def run(self, context):
        """
        Run all steps in order.
        
        Args:
            context: Dictionary for sharing data between steps
        
        Returns:
            True if all succeeded, False if any failed
        """
        for order, name, tool, func, retries in self.steps:
            attempt = 0
            while True:
                attempt += 1
                emit(order, name, tool, "STARTED")
                try:
                    func(context)
                    emit(order, name, tool, "SUCCESS")
                    break
                except Exception as e:
                    # If retries remain, emit RETRIED and try again
                    if attempt <= retries:
                        emit(order, name, tool, "RETRIED")
                        # small backoff could be added here
                        continue
                    else:
                        emit(order, name, tool, f"FAILED: {str(e)}")
                        return False

        return True
