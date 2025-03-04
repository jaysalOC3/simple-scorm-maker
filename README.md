# SCORM-Maker: Automated SCORM Package Generator

## Introduction

SCORM-Maker is a Python-based command-line tool that simplifies the creation of SCORM-compliant e-learning packages from various media formats. It automates the generation of SCORM manifest files and content packaging, making it easier for corporate training and educational content creators to deploy e-learning content on SCORM-compliant LMS platforms.

## Installation

To install SCORM-Maker, you need to have Python 3.8 or later installed. You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

SCORM-Maker is a command-line tool that can be used to generate SCORM packages from a directory of content. The basic usage is as follows:

```bash
python scorm_maker/cli.py --input /path/to/content/directory --output /path/to/output/directory --config /path/to/custom_config.yaml
```

### Options

*   `--input` (required): The path to the directory containing the content to be packaged.
*   `--output` (required): The path to the directory where the SCORM package should be created.
*   `--config` (optional): The path to a custom configuration file. If not specified, the default `scorm_config.yaml` file will be used.

## Configuration

SCORM-Maker uses a YAML file (`scorm_config.yaml`) to configure the SCORM package. The configuration file allows you to specify package metadata, organization information, SCORM standard version, content completion criteria, UI customization, and content items.

Here is an example `scorm_config.yaml` file:

```yaml
# SCORM-Maker Configuration File

# Package metadata
package:
  title: "Introduction to Data Science"
  identifier: "DS101_2023"
  version: "1.0"
  language: "en-US"
  description: "A comprehensive introduction to data science concepts and tools."

# Organization information
organization:
  name: "Data Science Academy"
  identifier: "DSA_2023"

# SCORM standard version (options: "1.2", "2004_3rd", "2004_4th")
scorm_version: "2004_4th"

# Content completion criteria (options: "all_items", "percentage", "last_item")
completion_criteria: "percentage"
# Required if completion_criteria is "percentage"
completion_percentage: 80

# UI customization
ui:
  theme:
    primary_color: "#3498db"
    secondary_color: "#2c3e50"
    text_color: "#333333"
    background_color: "#ffffff"
  logo_url: "assets/logo.png"
  show_progress_bar: true
  show_table_of_contents: true

# Content items
content_items:
  - file: "01_introduction.html"
    title: "Introduction to Data Science"
    description: "Overview of data science concepts and applications."
    required: true

  - file: "02_data_collection.pdf"
    title: "Data Collection Methods"
    description: "Methods and best practices for collecting data."
    required: true

  - file: "03_data_cleaning.html"
    title: "Data Cleaning and Preparation"
    description: "Techniques for cleaning and preparing data for analysis."
    required: true

  - file: "04_visualization.html"
    title: "Data Visualization"
    description: "Creating effective visualizations to communicate insights."
    required: false

  - file: "05_machine_learning.mp4"
    title: "Introduction to Machine Learning"
    description: "Basic concepts of machine learning algorithms."
    required: true

  - file: "06_case_study.html"
    title: "Case Study: Predictive Analytics"
    description: "Real-world application of data science techniques."
    required: false
```

### Package Metadata

*   `package.title`: The title of the SCORM package.
*   `package.identifier`: A unique identifier for the SCORM package.
*   `package.version`: The version of the SCORM package.
*   `package.language`: The language of the SCORM package.
*   `package.description`: A description of the SCORM package.

### Organization Information

*   `organization.name`: The name of the organization.
*   `organization.identifier`: A unique identifier for the organization.

### SCORM Standard Version

*   `scorm_version`: The SCORM standard version to use. Options are "1.2", "2004\_3rd", and "2004\_4th".

### Content Completion Criteria

*   `completion_criteria`: The criteria for completing the content. Options are "all\_items", "percentage", and "last\_item".
*   `completion_percentage`: The percentage of content items that must be completed to complete the content. Required if `completion_criteria` is "percentage".

### UI Customization

*   `ui.theme.primary_color`: The primary color of the UI.
*   `ui.theme.secondary_color`: The secondary color of the UI.
*   `ui.theme.text_color`: The text color of the UI.
*   `ui.theme.background_color`: The background color of the UI.
*   `ui.logo_url`: The URL of the logo to display in the UI.
*   `ui.show_progress_bar`: Whether to show the progress bar in the UI.
*   `ui.show_table_of_contents`: Whether to show the table of contents in the UI.

### Content Items

*   `content_items`: A list of content items to include in the SCORM package. Each content item has the following properties:
    *   `file`: The path to the content file.
    *   `title`: The title of the content item.
    *   `description`: A description of the content item.
    *   `required`: Whether the content item is required to be completed.

## File Structure

```
scorm_maker/
    __init__.py
    cli.py (Handles command-line arguments)
    config.py (Handles configuration loading and validation)
    content_processor.py (Handles content processing and sequencing)
    scorm_generator.py (Handles SCORM manifest and package creation)
    template_handler.py (Handles template loading and rendering)
    utils.py (Helper functions)
    templates/ (HTML templates included with the package)
scorm_config.yaml (Example configuration file)
requirements.txt (List of Python dependencies)
README.md (Documentation)
