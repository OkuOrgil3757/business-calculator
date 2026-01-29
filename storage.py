"""
Storage module for JSON data persistence.
"""

import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def ensure_data_dir():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_json(filename):
    """Load data from a JSON file."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_json(filename, data):
    """Save data to a JSON file."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_calculations():
    """Load saved calculations."""
    return load_json("calculations.json")


def save_calculations(calculations):
    """Save calculations."""
    save_json("calculations.json", calculations)


def generate_id():
    """Generate a unique ID based on timestamp."""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")
