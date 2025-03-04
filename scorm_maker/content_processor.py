"""
Content processing for SCORM-Maker.

This module handles processing and sequencing of content files.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Supported file extensions and their corresponding MIME types
SUPPORTED_EXTENSIONS = {
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
}


class ContentProcessingError(Exception):
    """Exception raised for content processing errors."""
    pass


def process_content(input_dir: Path, config: Dict) -> List[Dict]:
    """
    Process content files from the input directory.
    
    Args:
        input_dir (Path): Path to the directory containing content files.
        config (Dict): Configuration dictionary.
        
    Returns:
        List[Dict]: List of processed content items.
        
    Raises:
        ContentProcessingError: If there are issues processing the content.
    """
    # Get content items from config
    config_items = config.get('content_items', [])
    
    # Create a mapping of filenames to config items
    config_item_map = {item['file']: item for item in config_items}
    
    # Find all content files in the input directory
    content_files = []
    for ext in SUPPORTED_EXTENSIONS.keys():
        content_files.extend(list(input_dir.glob(f'**/*{ext}')))
    
    if not content_files:
        raise ContentProcessingError(f"No supported content files found in {input_dir}")
    
    # Process each content file
    processed_items = []
    for file_path in content_files:
        # Get the relative path from the input directory
        rel_path = file_path.relative_to(input_dir)
        file_name = str(rel_path)
        
        # Check if this file is in the config
        if file_name in config_item_map:
            # Use the config item
            item_config = config_item_map[file_name]
            title = item_config.get('title', file_name)
            description = item_config.get('description', '')
            required = item_config.get('required', True)
        else:
            # Create a default item
            title = get_title_from_filename(file_name)
            description = ''
            required = True
        
        # Get the file extension and MIME type
        ext = file_path.suffix.lower()
        mime_type = SUPPORTED_EXTENSIONS.get(ext, 'application/octet-stream')
        
        # Create the processed item
        processed_item = {
            'file_path': file_path,
            'rel_path': rel_path,
            'title': title,
            'description': description,
            'required': required,
            'mime_type': mime_type,
            'type': get_content_type(ext),
        }
        
        processed_items.append(processed_item)
    
    # Sort the processed items
    processed_items = sort_content_items(processed_items)
    
    return processed_items


def get_title_from_filename(filename: str) -> str:
    """
    Generate a title from a filename.
    
    Args:
        filename (str): The filename to process.
        
    Returns:
        str: A human-readable title.
    """
    # Remove the file extension
    base_name = os.path.splitext(os.path.basename(filename))[0]
    
    # Remove any leading numbers and underscores (e.g., "01_Introduction" -> "Introduction")
    base_name = re.sub(r'^\d+[_\s-]*', '', base_name)
    
    # Replace underscores, hyphens, and dots with spaces
    base_name = re.sub(r'[_\-.]', ' ', base_name)
    
    # Capitalize the first letter of each word
    title = ' '.join(word.capitalize() for word in base_name.split())
    
    return title


def get_content_type(extension: str) -> str:
    """
    Determine the content type based on the file extension.
    
    Args:
        extension (str): The file extension.
        
    Returns:
        str: The content type.
    """
    extension = extension.lower()
    
    if extension == '.pdf':
        return 'pdf'
    elif extension in ['.mp4', '.webm']:
        return 'video'
    elif extension in ['.mp3', '.wav']:
        return 'audio'
    elif extension in ['.jpg', '.jpeg', '.png', '.gif']:
        return 'image'
    elif extension in ['.html', '.htm']:
        return 'html'
    else:
        return 'unknown'


def sort_content_items(items: List[Dict]) -> List[Dict]:
    """
    Sort content items based on filename prefixes.
    
    Args:
        items (List[Dict]): List of content items.
        
    Returns:
        List[Dict]: Sorted list of content items.
    """
    def get_sort_key(item):
        # Extract the filename
        filename = str(item['rel_path'])
        
        # Check if the filename starts with a number
        match = re.match(r'^(\d+)', os.path.basename(filename))
        if match:
            # Return the number as an integer for sorting
            return (0, int(match.group(1)), filename)
        else:
            # If no number prefix, sort after numbered items
            return (1, 0, filename)
    
    return sorted(items, key=get_sort_key)


def copy_assets(input_dir: Path, output_dir: Path, content_items: List[Dict]) -> None:
    """
    Copy content files and their assets to the output directory.
    
    Args:
        input_dir (Path): Path to the input directory.
        output_dir (Path): Path to the output directory.
        content_items (List[Dict]): List of processed content items.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy each content file
    for item in content_items:
        src_path = item['file_path']
        dest_path = output_dir / item['rel_path']
        
        # Create parent directories if they don't exist
        os.makedirs(dest_path.parent, exist_ok=True)
        
        # Copy the file
        shutil.copy2(src_path, dest_path)
    
    # Copy assets (e.g., images, CSS, JS) referenced in HTML files
    # This would require parsing HTML files and finding references to assets
    # For simplicity, we'll just copy all files in the input directory
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            src_path = Path(root) / file
            rel_path = src_path.relative_to(input_dir)
            dest_path = output_dir / rel_path
            
            # Skip if the file is already copied
            if dest_path.exists():
                continue
            
            # Create parent directories if they don't exist
            os.makedirs(dest_path.parent, exist_ok=True)
            
            # Copy the file
            shutil.copy2(src_path, dest_path)
