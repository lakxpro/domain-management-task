# File Client CLI

## Overview

This is a Python CLI tool for retrieving file metadata and content from a REST API. It provides the following commands:
- `stat`: Print file metadata
- `read`: Retrieve and save file content

## Requirements

- Python 3.9.19 (I used [pyenv])

## Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:lakxpro/domain-management-task.git
   cd domain-management-task
   ```

2. **Create a virtual environment and install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   pip install -e .
   ```

## Comands 
- After completing the setup, you should be able to run commands using:
    ```bash
    file-client
    ```
- To display all available options and commands, use: 
    ```bash
    file-client --help
    ```

## Tests 
- To run the tests, use the following command:
    ```bash
    python -m unittest -v test/test_stat_command.py 
    ```
    or 
    ```bash
    python -m unittest discover -s test
    ```

## Run local flask server (for testing)
    ```bash
    python flask_server.py
    ```
- The server will be running at http://127.0.0.1:5000.
- There are two test files with UUIDs: "123e4567-e89b-12d3-a456-426614174000" and "123e4567-e89b-12d3-a456-426614174001".