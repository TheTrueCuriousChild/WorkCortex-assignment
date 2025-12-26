#!/usr/bin/env python
"""
test_production.py - Direct production test with real Gmail API

This script directly tests the production pipeline with your actual Gmail account.
"""

import sys
import os

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.engine import Engine
from backend.gmail import fetch_emails
from backend.ml import resolve_identities
from backend.excel import save_excel
from backend.events import listen, clear

def test_production():
    """Test production with real Gmail API"""
    
    print("\n" + "="*80)
    print("WorkCortex Gmail Intelligence - PRODUCTION TEST")
    print("="*80)
    
    # Configuration
    sender = "upendra162005@gmail.com"  # Your actual sender email
    output_path = "C:/Users/Bimal Chakravarty/Divide/Documents/ML_submission/workcortex-gmail-intelligence/recipients_production.xlsx"
    enable_ml = True
    verify_mx = False
    
    print(f"\n📧 Sender: {sender}")
    print(f"💾 Output: {output_path}")
    print(f"🤖 ML Enabled: {enable_ml}")
    print(f"🔍 MX Verify: {verify_mx}")
    print("\n" + "-"*80)
    print("Starting production pipeline...\n")
    
    # Clear events
    clear()
    
    # Setup context
    context = {
        "sender": sender,
        "output_path": output_path,
        "enable_ml": enable_ml,
        "verify_mx": verify_mx
    }
    
    # Create engine
    engine = Engine()
    engine.add_step(1, "Fetching Gmail Emails", "Gmail API", fetch_emails)
    engine.add_step(2, "Resolving Duplicate Identities", "ML Engine", resolve_identities)
    engine.add_step(3, "Saving to Excel", "Pandas/Excel", save_excel)
    
    # Run
    success = engine.run(context)
    
    # Print results
    print("\n" + "-"*100)
    print(f"{'Timestamp':<20} | {'Order':<5} | {'Step':<35} | {'Tool':<20} | {'Status':<15}")
    print("-"*100)
    
    for event in listen():
        timestamp = event.get("timestamp", "?")
        order = event.get("order", "?")
        step = event.get("step", "?")[:35]
        tool = event.get("tool", "?")[:20]
        status = event.get("status", "?")
        print(f"{timestamp:<20} | {order:<5} | {step:<35} | {tool:<20} | {status:<15}")
    
    print("-"*100)
    
    if success:
        print(f"\n✅ PRODUCTION TEST SUCCESSFUL")
        print(f"   Recipients extracted: {context.get('recipient_count', 0)}")
        print(f"   File saved: {context.get('excel_path', '?')}")
        return 0
    else:
        print(f"\n❌ PRODUCTION TEST FAILED")
        print(f"   Check logs above for errors")
        return 1

if __name__ == "__main__":
    sys.exit(test_production())
