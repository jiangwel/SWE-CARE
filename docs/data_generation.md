# Data Generation

This document describes how to generate input files for the SWE-CARE project.

## `get_input.py`

The `get_input.py` script is responsible for fetching the dataset and generating prompt files.

### Usage

Run the script using Python:

```bash
python3 get_input.py
```

### Description

1.  **Dataset**: Loads the `inclusionAI/SWE-CARE` dataset (test split).
2.  **Processing**: Iterates through each item in the dataset.
    *   Parses the `commit_to_review` field to extract `patch_to_review`.
    *   Reads the template from `template_inp.txt`.
    *   Fills the template with `instance_id`, `base_commit`, `problem_statement`, and `patch_to_review`.
3.  **Output**: Generates a text file for each instance in the `inputs/` directory.
    *   **File Name**: `{{instance_id}}` (e.g., `All-Hands-AI__OpenHands-8343@9d4e2af`).
    *   **Content**: The filled template containing the task description, issue, and patch to be reviewed.

### Output Directory

The generated files are stored in:

```
/Users/jiangwei/Develop/SWE-CARE/inputs/
```
