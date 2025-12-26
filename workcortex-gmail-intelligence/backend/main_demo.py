"""
main_demo.py - Demo version without Gmail API

Run this to see the system working without needing Gmail credentials.
"""

import sys
from .engine import Engine
from .ml import resolve_identities
from .excel import save_excel
from .events import listen, clear


def mock_fetch_emails(context):
    """Mock Gmail fetch for demo purposes."""
    context["emails"] = [
        "alice@company.com",
        "bob@company.com",
        "alice.smith@company.com",
        "bob.jones@example.org",
        "carol@startup.io",
        "charlie.brown@startup.io",
        "david@tech.io",
        "eve@research.org",
        "frank@consulting.com",
    ]


def main():
    """Run demo with mock data."""
    
    print("\n📧 Gmail Intelligence System (DEMO MODE)")
    print("Using mock email data (no Gmail API required)\n")
    
    # Clear any previous events
    clear()
    
    # Setup execution context
    context = {
        "sender": "john.doe@company.com (DEMO)",
        "output_path": "recipients_demo.xlsx",
        "enable_ml": True
    }
    
    # Create and configure engine
    engine = Engine()
    engine.add_step(1, "Fetching Gmail Emails", "Gmail API (MOCK)", mock_fetch_emails)
    engine.add_step(2, "Resolving Duplicate Identities", "ML Engine", resolve_identities)
    engine.add_step(3, "Saving to Excel", "Pandas/Excel", save_excel)
    
    # Run engine
    success = engine.run(context)
    
    # Print log table
    print("-" * 100)
    print(f"{'Timestamp':<20} | {'Order':<5} | {'Step':<35} | {'Tool':<20} | {'Status':<15}")
    print("-" * 100)
    
    for event in listen():
        timestamp = event.get("timestamp", "?")
        order = event.get("order", "?")
        step = event.get("step", "?")[:35]
        tool = event.get("tool", "?")[:20]
        status = event.get("status", "?")
        
        print(f"{timestamp:<20} | {order:<5} | {step:<35} | {tool:<20} | {status:<15}")
    
    print("-" * 100)
    
    # Print results
    if success:
        print(f"\n✓ SUCCESS")
        print(f"  Recipients extracted: {context.get('recipient_count', 0)}")
        print(f"  File saved: {context.get('excel_path', '?')}")
        print(f"\n  📊 Excel file: recipients_demo.xlsx")
        return 0
    else:
        print(f"\n✗ FAILED - Check logs above for errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
