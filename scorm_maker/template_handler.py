"""
Template handling for SCORM-Maker.

This module handles loading and rendering of templates.
"""

import os
from pathlib import Path
from typing import Dict, Optional
import jinja2


class TemplateError(Exception):
    """Exception raised for template errors."""
    pass


def get_template_path() -> Path:
    """
    Get the path to the templates directory.
    
    Returns:
        Path: Path to the templates directory.
    """
    # Get the path to the templates directory within the package
    template_path = Path(__file__).parent / 'templates'
    
    # Ensure the templates directory exists
    if not template_path.exists() or not template_path.is_dir():
        raise TemplateError(f"Templates directory not found: {template_path}")
    
    return template_path


def render_template(template_name: str, context: Dict) -> str:
    """
    Render a template with the given context.
    
    Args:
        template_name (str): Name of the template file.
        context (Dict): Context dictionary for template rendering.
        
    Returns:
        str: Rendered template content.
        
    Raises:
        TemplateError: If there are issues loading or rendering the template.
    """
    try:
        # Get the templates directory
        template_dir = get_template_path()
        
        # Set up the Jinja2 environment
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Load the template
        template = env.get_template(template_name)
        
        # Render the template
        return template.render(**context)
    
    except jinja2.exceptions.TemplateError as e:
        raise TemplateError(f"Error rendering template '{template_name}': {str(e)}")
    
    except Exception as e:
        raise TemplateError(f"Error loading template '{template_name}': {str(e)}")
