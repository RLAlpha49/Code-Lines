"""
This module contains functions to count the number of lines in all files in a directory,
excluding specified files and extensions. It prompts the user for input and prints the line counts.
"""

import os
import fnmatch


def count_lines(directory, exclusions, exclude_extensions):
    """
    Count the number of lines in all files in a directory, excluding specified files and extensions.

    Parameters:
    directory (str): The directory to search.
    exclusions (list): A list of file or directory names to exclude.
    exclude_extensions (list): A list of file extensions to exclude.

    Returns:
    tuple: A tuple containing a dictionary of line counts by extension and the total line count.
    """
    line_counts = {}
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclusions]
        files = [f for f in files if f not in exclusions]
        for items in fnmatch.filter(files, "*"):
            ext = os.path.splitext(items)[1]
            if ext and ext not in exclude_extensions:
                file = os.path.join(root, items)
                try:
                    with open(file, "r", encoding="utf-8", errors="ignore") as f:
                        for _ in f:
                            line_counts[ext] = line_counts.get(ext, 0) + 1
                            total_lines += 1
                except Exception as e:  # pylint: disable=W0718
                    print(f"Error reading {file}: {str(e)}")
    return line_counts, total_lines


def main():
    """
    Main function to execute the script. Prompts the user for input and prints the line counts.
    """
    directory = input("Enter the directory to search: ")
    exclusions = input(
        "Enter the files or directories to exclude (comma separated): "
    ).split(",")
    exclusions = [exclusion.strip() for exclusion in exclusions]
    exclude_extensions = input(
        "Enter the file extensions to exclude (comma separated): "
    ).split(",")
    exclude_extensions = [extension.strip() for extension in exclude_extensions]
    line_counts, total_lines = count_lines(directory, exclusions, exclude_extensions)
    sorted_line_counts = dict(
        sorted(line_counts.items(), key=lambda item: item[1], reverse=True)
    )
    print()
    for ext, count in sorted_line_counts.items():
        print(f"Total lines for files with extension {ext}: {count}")
    print(f"\nTotal lines in directory {directory}: {total_lines}")


if __name__ == "__main__":
    main()
