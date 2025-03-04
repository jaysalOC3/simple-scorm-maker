"""
Configuration handling for SCORM-Maker.

This module handles loading and validating the configuration from a YAML file.
"""

import os
from pathlib import Path
import yaml


class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


def load_config(config_file):
    """
    Load and validate configuration from a YAML file.
    
    Args:
        config_file (str or Path): Path to the configuration file.
        
    Returns:
        dict: Validated configuration dictionary.
        
    Raises:
        ConfigError: If the configuration is invalid or missing required fields.
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate the configuration
        validate_config(config)
        
        return config
    
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing YAML configuration: {str(e)}")
    
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: {config_file}")


def validate_config(config):
    """
    Validate the configuration dictionary.
    
    Args:
        config (dict): Configuration dictionary to validate.
        
    Raises:
        ConfigError: If the configuration is invalid or missing required fields.
    """
    # Check if config is a dictionary
    if not isinstance(config, dict):
        raise ConfigError("Configuration must be a dictionary")
    
    # Validate package metadata
    if 'package' not in config:
        raise ConfigError("Missing 'package' section in configuration")
    
    package = config['package']
    if not isinstance(package, dict):
        raise ConfigError("'package' section must be a dictionary")
    
    required_package_fields = ['title', 'identifier', 'version', 'language']
    for field in required_package_fields:
        if field not in package:
            raise ConfigError(f"Missing required field '{field}' in 'package' section")
    
    # Validate organization information
    if 'organization' not in config:
        raise ConfigError("Missing 'organization' section in configuration")
    
    organization = config['organization']
    if not isinstance(organization, dict):
        raise ConfigError("'organization' section must be a dictionary")
    
    required_org_fields = ['name', 'identifier']
    for field in required_org_fields:
        if field not in organization:
            raise ConfigError(f"Missing required field '{field}' in 'organization' section")
    
    # Validate SCORM version
    if 'scorm_version' not in config:
        raise ConfigError("Missing 'scorm_version' in configuration")
    
    valid_scorm_versions = ['1.2', '2004_3rd', '2004_4th']
    if config['scorm_version'] not in valid_scorm_versions:
        raise ConfigError(f"Invalid 'scorm_version'. Must be one of: {', '.join(valid_scorm_versions)}")
    
    # Validate completion criteria
    if 'completion_criteria' not in config:
        raise ConfigError("Missing 'completion_criteria' in configuration")
    
    valid_completion_criteria = ['all_items', 'percentage', 'last_item']
    if config['completion_criteria'] not in valid_completion_criteria:
        raise ConfigError(f"Invalid 'completion_criteria'. Must be one of: {', '.join(valid_completion_criteria)}")
    
    # If completion criteria is 'percentage', validate completion_percentage
    if config['completion_criteria'] == 'percentage':
        if 'completion_percentage' not in config:
            raise ConfigError("Missing 'completion_percentage' when 'completion_criteria' is 'percentage'")
        
        if not isinstance(config['completion_percentage'], (int, float)):
            raise ConfigError("'completion_percentage' must be a number")
        
        if config['completion_percentage'] < 0 or config['completion_percentage'] > 100:
            raise ConfigError("'completion_percentage' must be between 0 and 100")
    
    # Validate UI customization
    if 'ui' not in config:
        raise ConfigError("Missing 'ui' section in configuration")
    
    ui = config['ui']
    if not isinstance(ui, dict):
        raise ConfigError("'ui' section must be a dictionary")
    
    # Validate content items
    if 'content_items' not in config:
        raise ConfigError("Missing 'content_items' section in configuration")
    
    content_items = config['content_items']
    if not isinstance(content_items, list):
        raise ConfigError("'content_items' section must be a list")
    
    if not content_items:
        raise ConfigError("'content_items' list cannot be empty")
    
    for i, item in enumerate(content_items):
        if not isinstance(item, dict):
            raise ConfigError(f"Content item at index {i} must be a dictionary")
        
        if 'file' not in item:
            raise ConfigError(f"Content item at index {i} is missing required field 'file'")
        
        if 'title' not in item:
            raise ConfigError(f"Content item at index {i} is missing required field 'title'")
