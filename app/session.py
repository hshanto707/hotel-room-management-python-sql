# app/session.py

session_data = {}

def save_session(data):
    """Save data to the session."""
    global session_data
    session_data = data

def get_session():
    """Retrieve the current session data."""
    return session_data

def clear_session():
    """Clear all session data."""
    global session_data
    session_data = {}
