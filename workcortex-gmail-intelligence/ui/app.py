"""
ui/app.py - Streamlit Web Interface

Live execution UI with real-time event polling and results display.
Authenticate first, then enter sender email and run the pipeline.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Try importing backend package; if that fails adjust path and retry
try:
    from backend.events import listen, clear
    from backend.main import run_pipeline
    from backend.gmail import authenticate
except Exception:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from backend.events import listen, clear
    from backend.main import run_pipeline
    from backend.gmail import authenticate


# Page config
st.set_page_config(
    page_title="WorkCortex Gmail Intelligence",
    page_icon="📧",
    layout="wide"
)

# Title and description
st.title("📧 WorkCortex Gmail Intelligence")
st.markdown("Extract recipient emails from Gmail and apply ML-based identity resolution.")

# Initialize session state
if 'authenticated_email' not in st.session_state:
    st.session_state.authenticated_email = None
if 'service' not in st.session_state:
    st.session_state.service = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'events' not in st.session_state:
    st.session_state.events = []
if 'context' not in st.session_state:
    st.session_state.context = {}

# Sidebar: Authentication
st.sidebar.header("🔐 Authentication")
if not st.session_state.authenticated_email:
    if st.sidebar.button("🔐 Authenticate with Google", key="auth_btn"):
        try:
            with st.spinner("Opening OAuth consent..."):
                service = authenticate()
                profile = service.users().getProfile(userId="me").execute()
                auth_email = profile.get("emailAddress")
                st.session_state.authenticated_email = auth_email
                st.session_state.service = service
                st.success(f"✅ Authenticated as: {auth_email}")
                st.rerun()
        except Exception as e:
            st.error(f"Authentication failed: {e}")
else:
    st.sidebar.markdown(f"**✅ Authenticated:** {st.session_state.authenticated_email}")
    if st.sidebar.button("🔄 Re-authenticate", key="reauth_btn"):
        st.session_state.authenticated_email = None
        st.session_state.service = None
        st.rerun()

# Main configuration (only show if authenticated)
if st.session_state.authenticated_email:
    st.sidebar.header("⚙️ Configuration")
    
    sender_email = st.sidebar.text_input(
        "Sender Email",
        placeholder="example@gmail.com",
        help="Email address to fetch messages from"
    )
    
    output_path = st.sidebar.text_input(
        "Output Excel Path",
        placeholder="C:/Users/YOU/recipients.xlsx",
        help="Where to save the Excel file"
    )
    
    enable_ml = st.sidebar.checkbox(
        "Enable ML Identity Resolution",
        value=True,
        help="Group similar email addresses"
    )
    
    verify_mx = st.sidebar.checkbox(
        "Verify recipient domains (MX lookup)",
        value=False,
        help="Perform MX DNS lookup to ensure recipient domains accept email"
    )
    
    # Main controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Start Execution", disabled=st.session_state.running or not sender_email or not output_path):
            if not sender_email:
                st.error("Please enter a sender email")
            elif not output_path:
                st.error("Please enter an output path")
            else:
                st.session_state.running = True
                st.session_state.events = []
                st.session_state.context = {}
                
                context = {
                    "sender": sender_email,
                    "output_path": output_path,
                    "enable_ml": enable_ml,
                    "verify_mx": verify_mx,
                    "service": st.session_state.service  # Pass authenticated service
                }
                
                # Run pipeline synchronously (no threading - Streamlit compatible)
                try:
                    st.info("⏳ Running execution pipeline...")
                    success, result_ctx, events = run_pipeline(
                        context["sender"],
                        context["output_path"],
                        enable_ml=context["enable_ml"],
                        verify_mx=context["verify_mx"],
                        service=context.get("service")
                    )
                    st.session_state.context = result_ctx
                    st.session_state.events = events
                except Exception as e:
                    st.session_state.context = {"_error": str(e)}
                    st.session_state.events = list(listen())
                finally:
                    st.session_state.running = False
                    st.rerun()
    
    with col2:
        if st.button("🔄 Reset", disabled=st.session_state.running):
            st.session_state.events = []
            st.session_state.context = {}
            clear()
            st.rerun()
    
    # Display execution log
    if st.session_state.events:
        st.header("📋 Execution Log")
        
        # Convert to DataFrame
        events_data = []
        for event in st.session_state.events:
            events_data.append({
                "Timestamp": event.get("timestamp", "?"),
                "Order": event.get("order", "?"),
                "Step": event.get("step", "?"),
                "Tool": event.get("tool", "?"),
                "Status": event.get("status", "?")
            })
        
        if events_data:
            df_events = pd.DataFrame(events_data)
            st.dataframe(df_events, use_container_width=True)
    
    # Display results
    if st.session_state.context:
        context = st.session_state.context
        
        st.header("✨ Results")
        
        if context.get("excel_path"):
            st.success("✓ Execution completed successfully")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Recipients", context.get("recipient_count", 0))
            
            with col2:
                st.metric("Output File", Path(context.get("excel_path", "")).name)
            
            with col3:
                if enable_ml:
                    st.metric("Identities", context.get("identity_count", 0))
        elif context.get("_error"):
            st.error(f"❌ Execution failed: {context.get('_error')}")
else:
    st.info("👆 Click **Authenticate with Google** in the sidebar to get started.")

