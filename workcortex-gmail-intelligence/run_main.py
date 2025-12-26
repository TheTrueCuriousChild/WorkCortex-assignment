#!/usr/bin/env python
"""
run_main.py - Production CLI Entry Point

Runs the complete Gmail Intelligence system with real Gmail API integration.
Handles OAuth2 authentication, email fetching, ML deduplication, and Excel export.

Usage:
    python run_main.py

Requirements:
    - credentials.json must be in the backend/ directory
    - Valid Google Cloud Console OAuth2 credentials
"""

import sys
import os
import logging

# Setup logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('execution.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from backend.engine import Engine
from backend.gmail import fetch_emails
from backend.ml import resolve_identities
from backend.excel import save_excel
from backend.events import listen, clear


def main():
    """Run the complete Gmail intelligence pipeline."""
    
    logger.info("=" * 70)
    logger.info("WorkCortex Gmail Intelligence System - Production Mode")
    logger.info("=" * 70)
    
    try:
        # User input
        print("\n📧 Gmail Intelligence System - Production")
        print("-" * 70)
        
        sender = input("📧 Enter sender email (gmail): ").strip()
        if not sender:
            logger.error("Sender email is required")
            return 1
        
        output_path = input("💾 Enter output Excel path (e.g., C:/Users/YOU/recipients.xlsx): ").strip()
        if not output_path:
            logger.error("Output path is required")
            return 1
        
        enable_ml_input = input("🤖 Enable ML identity resolution? (yes/no) [default: yes]: ").strip().lower()
        enable_ml = enable_ml_input != "no"
        
        verify_mx_input = input("🔍 Verify MX records? (yes/no) [default: no]: ").strip().lower()
        verify_mx = verify_mx_input == "yes"
        
        print("\n" + "=" * 70)
        print(f"Configuration:")
        print(f"  Sender Email: {sender}")
        print(f"  Output Path: {output_path}")
        print(f"  ML Enabled: {enable_ml}")
        print(f"  MX Verification: {verify_mx}")
        print("=" * 70)
        
        logger.info(f"Starting pipeline with sender: {sender}")
        
        # Clear previous events
        clear()
        
        # Setup execution context
        context = {
            "sender": sender,
            "output_path": output_path,
            "enable_ml": enable_ml,
            "verify_mx": verify_mx
        }
        
        # Create and configure engine
        engine = Engine()
        engine.add_step(1, "Fetching Gmail Emails", "Gmail API", fetch_emails)
        
        if enable_ml:
            engine.add_step(2, "Resolving Duplicate Identities", "ML Engine", resolve_identities)
            engine.add_step(3, "Saving to Excel", "Pandas/Excel", save_excel)
        else:
            engine.add_step(2, "Saving to Excel", "Pandas/Excel", save_excel)
        
        # Run engine
        logger.info("Running execution pipeline...")
        success = engine.run(context)
        
        # Print log table
        print("\n" + "-" * 100)
        print(f"{'Timestamp':<20} | {'Order':<5} | {'Step':<35} | {'Tool':<20} | {'Status':<15}")
        print("-" * 100)
        
        for event in listen():
            timestamp = event.get("timestamp", "?")
            order = event.get("order", "?")
            step = event.get("step", "?")[:35]
            tool = event.get("tool", "?")[:20]
            status = event.get("status", "?")
            
            print(f"{timestamp:<20} | {order:<5} | {step:<35} | {tool:<20} | {status:<15}")
            logger.info(f"Step {order}: {step} ({tool}) - {status}")
        
        print("-" * 100)
        
        # Print results
        if success:
            print(f"\n✓ SUCCESS ✓")
            print(f"  ✅ Recipients extracted: {context.get('recipient_count', 0)}")
            print(f"  ✅ File saved: {context.get('excel_path', '?')}")
            if context.get('verification_failures'):
                print(f"  ⚠️  Domains failed MX check: {len(context.get('verification_failures', []))}")
            print()
            
            logger.info(f"Pipeline completed successfully")
            logger.info(f"Recipients: {context.get('recipient_count', 0)}")
            logger.info(f"Excel file: {context.get('excel_path', '?')}")
            return 0
        else:
            print(f"\n✗ FAILED ✗")
            print(f"Check logs above for errors")
            print()
            logger.error("Pipeline failed")
            return 1
    
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
        print("\n\n⚠️  Pipeline cancelled by user")
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
