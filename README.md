# Line Counter

This Python script counts the number of lines in all files in a specified directory, excluding specified files and extensions.

## Usage

Run the script in your terminal and follow the prompts:

1. Enter the directory to search.
2. Enter the files or directories to exclude (comma separated).
3. Enter the file extensions to exclude (comma separated).

The script will then print the line counts for each file extension, sorted by the number of lines, and the total line count.

## Example Use Case

Let's say you want to count the lines of code in a Python project, but you want to exclude test files and any files in the `venv` directory. Here's how you might use this script:

1. Run the script in your terminal:

    ```bash
    python line_counter.py
    ```

2. When prompted, enter the directory of your Python project:

    ```bash
    Enter the directory to search: /path/to/your/project
    ```

3. When prompted, enter the files or directories to exclude. In this case, we're excluding the `venv` directory and any files that end with `_test.py`:

    ```bash
    Enter the files or directories to exclude (comma separated): venv, *_test.py
    ```

4. When prompted, enter the file extensions to exclude. In this case, we're not excluding any extensions, so just press Enter:

    ```bash
    Enter the file extensions to exclude (comma separated): 
    ```

The script will then print the line counts for each file extension, sorted by the number of lines, and the total line count. In this example, it will count the lines in all `.py` files in your project, excluding test files and files in the `venv` directory.
