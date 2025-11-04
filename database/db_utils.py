"""
Database utilities for user authentication
Handles SQLite database operations, user registration, and login
"""

import sqlite3
import hashlib
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """Initialize the database and create users table if not exists"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table with id, username, and hashed password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def hash_password(password):
    """
    Hash a password using SHA-256 for secure storage
    Args:
        password (str): Plain text password
    Returns:
        str: Hashed password in hexadecimal format
    """
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """
    Register a new user in the database
    Args:
        username (str): Username for registration
        password (str): Plain text password
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password before storing
        password_hash = hash_password(password)
        
        # Insert new user
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    
    except sqlite3.IntegrityError:
        # Username already exists
        return False, "Username already exists. Please choose another."
    
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def verify_user(username, password):
    """
    Verify user credentials during login
    Args:
        username (str): Username to verify
        password (str): Plain text password to verify
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hash the provided password
    password_hash = hash_password(password)
    
    # Check if user exists with matching password hash
    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password_hash = ?',
        (username, password_hash)
    )
    
    user = cursor.fetchone()
    conn.close()
    
    return user is not None


# Initialize database on module import
init_db()
