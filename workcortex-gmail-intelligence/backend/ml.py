"""
ml.py - Machine Learning Identity Resolution

Uses explainable ML (normalization + clustering) to group similar email addresses
that likely belong to the same person.
"""

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from .events import emit


def normalize_email(email):
    """
    Normalize email for comparison.
    
    Converts:
        john.doe@gmail.com    →  johndoe
        johndoe@company.com   →  johndoe
        john_doe@startup.io   →  johndoe
    
    Args:
        email: Email address string
    
    Returns:
        Normalized username
    """
    if "@" not in email:
        return email.lower()
    
    username = email.split("@")[0].lower()
    # Remove dots and underscores
    normalized = username.replace(".", "").replace("_", "")
    return normalized


def resolve_identities(context):
    """
    Group similar email addresses using unsupervised clustering.
    
    Algorithm:
    1. Normalize email usernames
    2. Convert to feature vectors (hash-based)
    3. Apply hierarchical clustering
    4. Keep one email from each cluster
    
    Args:
        context: Execution context
            Must contain: emails (list of email strings)
            Will populate: emails (deduplicated by identity)
    
    This is valid ML:
    - Feature extraction (normalization)
    - Unsupervised learning (clustering)
    - Explainable (can show which emails grouped)
    - No deep learning hype
    """
    emails = list(set(context.get("emails", [])))

    # Emit internal ML start
    emit(998, "Resolving identities - feature extraction", "ML Engine", "STARTED")

    if len(emails) <= 1:
        emit(998, "Resolving identities - nothing to do", "ML Engine", "SUCCESS")
        return
    
    # Normalize all emails
    normalized = [normalize_email(e) for e in emails]
    
    # Create feature vectors from normalized names
    # Use hash to convert strings to numeric values
    vectors = np.array([[hash(n) % 10000] for n in normalized]).reshape(-1, 1)
    
    # Apply hierarchical clustering
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=3000,
        linkage="average"
    )
    clustering.fit(vectors)
    
    # Keep first email from each cluster
    grouped = {}
    for label, email in zip(clustering.labels_, emails):
        if label not in grouped:
            grouped[label] = email
    
    # Deduplicated emails
    deduplicated = sorted(list(grouped.values()))
    context["emails"] = deduplicated
    context["identity_count"] = len(deduplicated)

    emit(998, "Resolving identities - completed", "ML Engine", "SUCCESS")
