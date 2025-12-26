"""
api.py - Backend integration API

Provides a simple `run_pipeline(context)` function that the UI
can call to execute the engine without duplicating wiring logic.
"""

from .events import clear
from .engine import Engine
from .gmail import fetch_emails
from .ml import resolve_identities
from .excel import save_excel


def run_pipeline(context):
    """
    Run the full pipeline using the Engine.

    Args:
        context: dict with at least `sender` and `output_path` keys.

    Returns:
        success (bool)
    """
    # Ensure events are cleared before running
    clear()

    engine = Engine()
    engine.add_step(1, "Fetching Gmail Emails", "Gmail API", fetch_emails)

    if context.get("enable_ml", True):
        engine.add_step(2, "Resolving Duplicate Identities", "ML Engine", resolve_identities)
        engine.add_step(3, "Saving to Excel", "Pandas/Excel", save_excel)
    else:
        engine.add_step(2, "Saving to Excel", "Pandas/Excel", save_excel)

    success = engine.run(context)

    # Populate helpful metrics if available
    if "emails" in context:
        context.setdefault("identity_count", len(context.get("emails", [])))

    return success
