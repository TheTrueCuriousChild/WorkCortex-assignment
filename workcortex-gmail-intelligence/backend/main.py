"""
main.py - Backend CLI Entry Point

Runs the complete execution pipeline with live event logging.
This is the internal module; use run_main.py from project root.
"""

from .engine import Engine
from .gmail import fetch_emails
from .ml import resolve_identities
from .excel import save_excel
from .events import listen, clear


def run_pipeline(sender, output_path, enable_ml=True, verify_mx=False, service=None):
    """
    Run the complete Gmail intelligence pipeline.
    
    Args:
        sender: Email to fetch from
        output_path: Where to save Excel file
        enable_ml: Whether to apply ML deduplication
        verify_mx: Whether to verify MX records
        service: Optional pre-authenticated Gmail service (from UI)
    
    Returns:
        Tuple of (success: bool, context: dict, events: list)
    """
    # Clear any previous events
    clear()
    
    # Setup execution context
    context = {
        "sender": sender,
        "output_path": output_path,
        "enable_ml": enable_ml,
        "verify_mx": verify_mx
    }
    
    # If service provided (from UI), use it; otherwise fetch_emails will authenticate
    if service:
        context["service"] = service
    
    # Create and configure engine
    engine = Engine()
    engine.add_step(1, "Fetching Gmail Emails", "Gmail API", fetch_emails)
    
    if enable_ml:
        engine.add_step(2, "Resolving Duplicate Identities", "ML Engine", resolve_identities)
        engine.add_step(3, "Saving to Excel", "Pandas/Excel", save_excel)
    else:
        engine.add_step(2, "Saving to Excel", "Pandas/Excel", save_excel)
    
    # Run engine
    success = engine.run(context)
    
    return success, context, list(listen())


def main():
    """Interactive entrypoint to run the production pipeline.

    Prompts for sender, output path and options, then runs the pipeline
    and prints live logs to the console. This preserves the module API
    while restoring script behavior for `python -m backend.main`.
    """
    try:
        print("\n📧 Gmail Intelligence System")
        print("-" * 60)

        sender = input("📧 Enter sender email (gmail): ").strip()
        if not sender:
            print("❌ Sender email is required")
            return 1

        output_path = input("💾 Enter output Excel path (e.g., C:/Users/YOU/recipients.xlsx): ").strip()
        if not output_path:
            print("❌ Output path is required")
            return 1

        enable_ml_input = input("🤖 Enable ML identity resolution? (yes/no) [default: yes]: ").strip().lower()
        enable_ml = enable_ml_input != "no"

        verify_mx_input = input("🔍 Verify MX records? (yes/no) [default: no]: ").strip().lower()
        verify_mx = verify_mx_input == "yes"

        print("\n" + "=" * 60)
        print(f"Sender: {sender}")
        print(f"Output: {output_path}")
        print(f"ML Enabled: {enable_ml}")
        print(f"Verify MX: {verify_mx}")
        print("=" * 60 + "\n")

        success, context, events = run_pipeline(sender, output_path, enable_ml=enable_ml, verify_mx=verify_mx)

        # Print log table
        print("\n" + "-" * 100)
        print(f"{'Timestamp':<20} | {'Order':<5} | {'Step':<35} | {'Tool':<20} | {'Status':<15}")
        print("-" * 100)
        for event in events:
            timestamp = event.get("timestamp", "?")
            order = event.get("order", "?")
            step = event.get("step", "?")[:35]
            tool = event.get("tool", "?")[:20]
            status = event.get("status", "?")
            print(f"{timestamp:<20} | {order:<5} | {step:<35} | {tool:<20} | {status:<15}")
        print("-" * 100)

        if success:
            print(f"\n✓ SUCCESS")
            print(f"  Recipients extracted: {context.get('recipient_count', 0)}")
            print(f"  File saved: {context.get('excel_path', '?')}")
            return 0
        else:
            print(f"\n✗ FAILED - Check logs above for errors")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline cancelled by user")
        return 130


if __name__ == "__main__":
    import sys
    sys.exit(main())

