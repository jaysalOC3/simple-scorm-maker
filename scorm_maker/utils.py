"""
Utility functions for SCORM-Maker.

This module provides helper functions for the SCORM-Maker tool.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename (str): The filename to sanitize.
        
    Returns:
        str: The sanitized filename.
    """
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    
    # Remove leading/trailing whitespace
    sanitized = sanitized.strip()
    
    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "unnamed"
    
    return sanitized


def ensure_directory(directory: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (Path): The directory to ensure exists.
    """
    os.makedirs(directory, exist_ok=True)


def copy_file(src: Path, dest: Path) -> None:
    """
    Copy a file from source to destination.
    
    Args:
        src (Path): The source file path.
        dest (Path): The destination file path.
    """
    # Create parent directories if they don't exist
    ensure_directory(dest.parent)
    
    # Copy the file
    shutil.copy2(src, dest)


def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.
    
    Args:
        filename (str): The filename to get the extension from.
        
    Returns:
        str: The file extension (lowercase, including the dot).
    """
    return os.path.splitext(filename)[1].lower()


def get_mime_type(filename: str) -> str:
    """
    Get the MIME type for a file based on its extension.
    
    Args:
        filename (str): The filename to get the MIME type for.
        
    Returns:
        str: The MIME type.
    """
    extension = get_file_extension(filename)
    
    # Common MIME types
    mime_types = {
        '.pdf': 'application/pdf',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.txt': 'text/plain',
    }
    
    return mime_types.get(extension, 'application/octet-stream')


def generate_unique_id(prefix: str = 'id_') -> str:
    """
    Generate a unique identifier.
    
    Args:
        prefix (str, optional): Prefix for the identifier. Defaults to 'id_'.
        
    Returns:
        str: A unique identifier.
    """
    import uuid
    return f"{prefix}{uuid.uuid4().hex[:8]}"
