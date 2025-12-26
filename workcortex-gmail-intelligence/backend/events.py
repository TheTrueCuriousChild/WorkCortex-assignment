"""
events.py - Live Event System

Thread-safe queue for streaming execution logs during runtime.
"""

import queue
import time
from datetime import datetime

_event_queue = queue.Queue()


def emit(order, step, tool, status):
    """
    Emit a structured event.
    
    Args:
        order: Step order (integer)
        step: Human-readable step description
        tool: Tool/service name (Gmail API, ML, Excel, etc)
        status: STARTED, SUCCESS, or FAILED
    """
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order": order,
        "step": step,
        "tool": tool,
        "status": status
    }
    _event_queue.put(event)


def listen():
    """
    Yield all events from queue (non-blocking).
    
    Yields:
        Event dictionaries
    """
    while not _event_queue.empty():
        yield _event_queue.get()


def get_all():
    """
    Get all events without removing them (for replay).
    
    Returns:
        List of all events
    """
    events = []
    temp_events = []
    
    while not _event_queue.empty():
        event = _event_queue.get()
        events.append(event)
        temp_events.append(event)
    
    # Put events back
    for event in temp_events:
        _event_queue.put(event)
    
    return events


def clear():
    """Clear the event queue."""
    while not _event_queue.empty():
        try:
            _event_queue.get_nowait()
        except queue.Empty:
            break
