"""
Backend package for WorkCortex Gmail Intelligence.
"""

from .events import emit, listen, clear, get_all
from .engine import Engine
from .gmail import fetch_emails, authenticate
from .ml import resolve_identities, normalize_email
from .excel import save_excel
from .api import run_pipeline

__all__ = [
    'emit', 'listen', 'clear', 'get_all',
    'Engine',
    'fetch_emails', 'authenticate',
    'resolve_identities', 'normalize_email',
    'save_excel'
    'run_pipeline'
]
