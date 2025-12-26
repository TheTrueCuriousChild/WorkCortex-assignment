"""
excel.py - Excel Export

Saves deduplicated recipient emails to Excel file using Pandas.
"""

import pandas as pd
from .events import emit


def save_excel(context):
    """
    Save recipient emails to Excel file.
    
    Args:
        context: Execution context
            Must contain: emails (list), output_path (str)
    
    Raises:
        Exception: If file write fails
    """
    emails = context.get("emails", [])
    output_path = context.get("output_path")
    
    if not output_path:
        raise ValueError("output_path not provided in context")
    
    # Deduplicate and sort
    unique_emails = sorted(set(emails))

    # Emit start for internal excel write
    try:
        emit(999, "Saving to Excel - Preparing file", "Pandas/Excel", "STARTED")

        # Create DataFrame
        df = pd.DataFrame(unique_emails, columns=["recipient_email"])

        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write to Excel
        df.to_excel(output_path, index=False, sheet_name="Recipients")

        context["excel_path"] = output_path
        context["recipient_count"] = len(unique_emails)

        emit(999, "Saving to Excel - Completed write", "Pandas/Excel", "SUCCESS")
    except Exception as e:
        emit(999, "Saving to Excel - Failed write", "Pandas/Excel", f"FAILED: {e}")
        raise

