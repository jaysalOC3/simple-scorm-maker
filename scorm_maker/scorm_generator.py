"""
SCORM package generation for SCORM-Maker.

This module handles the creation of SCORM manifests and packages.
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional
import uuid

from .content_processor import copy_assets
from .template_handler import render_template


class ScormGenerationError(Exception):
    """Exception raised for SCORM generation errors."""
    pass


def generate_scorm_package(
    content_items: List[Dict],
    output_dir: Path,
    config: Dict
) -> Path:
    """
    Generate a SCORM package.
    
    Args:
        content_items (List[Dict]): List of processed content items.
        output_dir (Path): Path to the output directory.
        config (Dict): Configuration dictionary.
        
    Returns:
        Path: Path to the generated SCORM package.
        
    Raises:
        ScormGenerationError: If there are issues generating the SCORM package.
    """
    try:
        # Create a temporary directory for the SCORM package
        package_dir = output_dir / 'scorm_package_temp'
        os.makedirs(package_dir, exist_ok=True)
        
        # Copy content files and assets to the package directory
        input_dir = content_items[0]['file_path'].parent
        copy_assets(input_dir, package_dir, content_items)
        
        # Generate the SCORM manifest
        generate_manifest(package_dir, content_items, config)
        
        # Generate the index.html file
        generate_index_html(package_dir, content_items, config)
        
        # Generate the SCORM API wrapper
        generate_scorm_api_wrapper(package_dir, config)
        
        # Generate content wrappers
        generate_content_wrappers(package_dir, content_items, config)
        
        # Create the ZIP file
        package_name = config['package']['title'].replace(' ', '_')
        zip_path = output_dir / f"{package_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, package_dir)
                    zipf.write(file_path, arcname)
        
        # Clean up the temporary directory
        shutil.rmtree(package_dir)
        
        return zip_path
    
    except Exception as e:
        raise ScormGenerationError(f"Error generating SCORM package: {str(e)}")


def generate_manifest(package_dir: Path, content_items: List[Dict], config: Dict) -> None:
    """
    Generate the SCORM manifest file (imsmanifest.xml).
    
    Args:
        package_dir (Path): Path to the package directory.
        content_items (List[Dict]): List of processed content items.
        config (Dict): Configuration dictionary.
    """
    scorm_version = config['scorm_version']
    
    # Determine the manifest template based on the SCORM version
    if scorm_version == '1.2':
        template_name = 'imsmanifest_1.2.xml'
    elif scorm_version == '2004_3rd':
        template_name = 'imsmanifest_2004_3rd.xml'
    elif scorm_version == '2004_4th':
        template_name = 'imsmanifest_2004_4th.xml'
    else:
        raise ScormGenerationError(f"Unsupported SCORM version: {scorm_version}")
    
    # Generate a unique identifier for the package
    package_id = config['package'].get('identifier', str(uuid.uuid4()))
    
    # Prepare the context for the template
    context = {
        'package': config['package'],
        'organization': config['organization'],
        'content_items': content_items,
        'package_id': package_id,
    }
    
    # Render the manifest template
    manifest_content = render_template(template_name, context)
    
    # Write the manifest file
    manifest_path = package_dir / 'imsmanifest.xml'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)


def generate_index_html(package_dir: Path, content_items: List[Dict], config: Dict) -> None:
    """
    Generate the index.html file.
    
    Args:
        package_dir (Path): Path to the package directory.
        content_items (List[Dict]): List of processed content items.
        config (Dict): Configuration dictionary.
    """
    # Prepare the context for the template
    context = {
        'package': config['package'],
        'organization': config['organization'],
        'content_items': content_items,
        'ui': config['ui'],
        'completion_criteria': config['completion_criteria'],
        'completion_percentage': config.get('completion_percentage', 100),
    }
    
    # Render the index template
    index_content = render_template('index.html', context)
    
    # Write the index file
    index_path = package_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)


def generate_scorm_api_wrapper(package_dir: Path, config: Dict) -> None:
    """
    Generate the SCORM API wrapper JavaScript file.
    
    Args:
        package_dir (Path): Path to the package directory.
        config (Dict): Configuration dictionary.
    """
    scorm_version = config['scorm_version']
    
    # Determine the API wrapper template based on the SCORM version
    if scorm_version == '1.2':
        template_name = 'SCORM_API_wrapper_1.2.js'
    elif scorm_version in ['2004_3rd', '2004_4th']:
        template_name = 'SCORM_API_wrapper_2004.js'
    else:
        raise ScormGenerationError(f"Unsupported SCORM version: {scorm_version}")
    
    # Prepare the context for the template
    context = {
        'package': config['package'],
        'completion_criteria': config['completion_criteria'],
        'completion_percentage': config.get('completion_percentage', 100),
    }
    
    # Render the API wrapper template
    api_wrapper_content = render_template(template_name, context)
    
    # Create the scorm_package directory if it doesn't exist
    scorm_package_dir = package_dir / 'scorm_package'
    os.makedirs(scorm_package_dir, exist_ok=True)
    
    # Write the API wrapper file
    api_wrapper_path = scorm_package_dir / 'SCORM_API_wrapper.js'
    with open(api_wrapper_path, 'w', encoding='utf-8') as f:
        f.write(api_wrapper_content)


def generate_content_wrappers(package_dir: Path, content_items: List[Dict], config: Dict) -> None:
    """
    Generate content wrapper files for different content types.
    
    Args:
        package_dir (Path): Path to the package directory.
        content_items (List[Dict]): List of processed content items.
        config (Dict): Configuration dictionary.
    """
    # Create the scorm_package directory if it doesn't exist
    scorm_package_dir = package_dir / 'scorm_package'
    os.makedirs(scorm_package_dir, exist_ok=True)
    
    # Generate PDF viewer wrapper
    pdf_items = [item for item in content_items if item['type'] == 'pdf']
    if pdf_items:
        pdf_wrapper_content = render_template('pdf_viewer_wrapper.js', {'config': config})
        pdf_wrapper_path = scorm_package_dir / 'pdf_viewer_wrapper.js'
        with open(pdf_wrapper_path, 'w', encoding='utf-8') as f:
            f.write(pdf_wrapper_content)
    
    # Generate video player wrapper
    video_items = [item for item in content_items if item['type'] == 'video']
    if video_items:
        video_wrapper_content = render_template('video_player_wrapper.js', {'config': config})
        video_wrapper_path = scorm_package_dir / 'video_player_wrapper.js'
        with open(video_wrapper_path, 'w', encoding='utf-8') as f:
            f.write(video_wrapper_content)
    
    # Generate audio player wrapper
    audio_items = [item for item in content_items if item['type'] == 'audio']
    if audio_items:
        audio_wrapper_content = render_template('audio_player_wrapper.js', {'config': config})
        audio_wrapper_path = scorm_package_dir / 'audio_player_wrapper.js'
        with open(audio_wrapper_path, 'w', encoding='utf-8') as f:
            f.write(audio_wrapper_content)
