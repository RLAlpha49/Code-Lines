#!/usr/bin/env python3
"""
This module provides a script to count the number of lines in all files within a specified directory,
excluding specified files and extensions.

The script uses a `LineCounter` class to perform the line counting. The `LineCounter` class has methods
to normalize paths, filter files based on inclusions and exclusions, count lines in a file, and count lines
in each file in the directory.

The script also includes a `parse_arguments` function to parse command line arguments, and a `main` function
to execute the main program flow.

This script is intended to be run from the command line. It takes a directory to search, and optional arguments
for files or directories to include or exclude, and file extensions to include or exclude.

Example:
    python main.py /path/to/directory --exclude venv --exclude-extensions .txt

This will count the lines in all files in `/path/to/directory`, excluding any files in the `venv` directory
and any files with a `.txt` extension.
"""

import argparse
import fnmatch
import os
from typing import Dict, List, Optional, Tuple, Union


class LineCounter:
    """
    A class used to count the lines in files within a specified directory, excluding specified files and extensions.

    Attributes
    ----------
    directory : str
        The directory to search.
    inclusions : list of str
        The files or directories to include.
    include_extensions : list of str
        The file extensions to include.
    exclusions : list of str
        The files or directories to exclude.
    exclude_extensions : list of str
        The file extensions to exclude.

    Methods
    -------
    _normalize_paths():
        Normalize the paths of the directory, inclusions, and exclusions.
    _filter_files(root: str, files: Union[List[str], str]) -> List[str]:
        Filter the files in a directory based on inclusions and exclusions.
    _count_lines_in_file(file: str) -> int:
        Count the number of lines in a file.
    _count_lines() -> Tuple[Dict[str, int], int]:
        Count the lines in each file in the directory, excluding specified files and extensions.
    count() -> Tuple[Dict[str, int], int]:
        Count the lines in each file in the directory, excluding specified files and extensions.
    """

    def __init__(
        self,
        directory: str,
        inclusions: Optional[List[str]] = None,
        include_extensions: Optional[List[str]] = None,
        exclusions: Optional[List[str]] = None,
        exclude_extensions: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize a LineCounter instance.

        This method initializes a LineCounter instance with the specified directory, inclusions, include_extensions,
        exclusions, and exclude_extensions. If inclusions or include_extensions are not provided, they are set to an
        empty list. If exclusions or exclude_extensions are not provided, they are also set to an empty list.

        Args:
            directory (str): The directory to search.
            inclusions (Optional[List[str]]): Files or directories to include. Defaults to None.
            include_extensions (Optional[List[str]]): File extensions to include. Defaults to None.
            exclusions (Optional[List[str]]): Files or directories to exclude. Defaults to None.
            exclude_extensions (Optional[List[str]]): File extensions to exclude. Defaults to None.
        """
        self.directory = directory
        self.inclusions = inclusions or []
        self.include_extensions = include_extensions or []
        self.exclusions = exclusions or []
        self.exclude_extensions = exclude_extensions or []

    def _normalize_paths(self) -> None:
        """
        Normalize the paths of the directory, inclusions, and exclusions.

        This method normalizes the paths of the directory, inclusions, and exclusions by converting them to a common
        standard format. This is done using the `os.path.normpath` function, which converts a pathname to the normal
        form for the current operating system.

        This method does not return anything as it modifies the instance variables in-place.
        """
        self.directory = os.path.normpath(self.directory)
        self.inclusions = [os.path.normpath(i) for i in self.inclusions]
        self.exclusions = [os.path.normpath(e) for e in self.exclusions]

    def _filter_files(self, root: str, files: Union[List[str], str]) -> List[str]:
        """
        Filter the files in a directory based on inclusions and exclusions.

        This method takes a root directory and a list of files, and returns a list of files that meet the inclusion
        and exclusion criteria. If inclusions are specified, it returns the files that start with any of the
        inclusions and have an extension that is in the list of included extensions. If exclusions are specified,
        it returns the files that do not start with any of the exclusions and do not have an extension that is in the
        list of excluded extensions.

        Args:
            root (str): The root directory to filter files in.
            files (Union[List[str], str]): The files to filter.

        Returns:
            List[str]: The filtered files.
        """
        if self.inclusions:
            return [
                f
                for f in files
                if any(
                    os.path.join(str(root), str(f)).startswith(
                        os.path.join(str(self.directory), str(i))
                    )
                    for i in self.inclusions
                )
                and (
                    not self.include_extensions
                    or os.path.splitext(f)[1] in self.include_extensions
                )
            ]

        return [
            f
            for f in files
            if all(
                not os.path.join(str(root), str(f)).startswith(
                    os.path.join(str(self.directory), str(e))
                )
                for e in self.exclusions
            )
            and (
                not self.exclude_extensions
                or os.path.splitext(f)[1] not in self.exclude_extensions
            )
        ]

    def _count_lines_in_file(self, file: str) -> int:
        """
        Count the number of lines in a file.

        This method opens a file in read mode, ignoring any encoding errors, and counts the number of lines in the file.
        If an exception occurs while opening or reading the file, it prints an error message and returns 0.

        Args:
            file (str): The path to the file to count lines in.

        Returns:
            int: The number of lines in the file, or 0 if an error occurred.
        """
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)
        except (IOError, OSError) as e:
            print(f"Error reading {file}: {str(e)}")
            return 0

    def _count_lines(self) -> Tuple[Dict[str, int], int]:
        """
        Count the lines in each file in the directory, excluding specified files and extensions.

        This method walks through the directory, and for each file, it checks if the file's extension is in the list
        of excluded extensions. If the file's extension is not in the list of excluded extensions, it counts the
        lines in the file. It treats files without extensions as having a '.noext' extension. The line counts for
        each extension and the total line count are stored in a dictionary and returned.

        Returns:
            Tuple[Dict[str, int], int]: A tuple where the first element is a dictionary with the file extensions
            as keys and the line counts as values, and the second element is the total line count.
        """
        line_counts: Dict[str, int] = {}
        total_lines = 0
        for root, _, files in os.walk(self.directory):
            for items in fnmatch.filter(self._filter_files(root, files), "*"):
                ext = os.path.splitext(items)[1]
                if ext == "":
                    ext = ".noext"
                if self.exclude_extensions and ext in self.exclude_extensions:
                    continue
                file = os.path.join(root, items)
                lines_in_file = self._count_lines_in_file(file)
                line_counts[ext] = line_counts.get(ext, 0) + lines_in_file
                total_lines += lines_in_file
        return line_counts, total_lines

    def count(self) -> Tuple[Dict[str, int], int]:
        """
        Count the lines in each file in the directory, excluding specified files and extensions.

        This method first normalizes the paths of the directory, inclusions, and exclusions, and then counts the
        lines in each file in the directory. The line counts for each extension and the total line count are stored
        in a dictionary and returned.

        Returns:
            Tuple[Dict[str, int], int]: A tuple where the first element is a dictionary with the file extensions
            as keys and the line counts as values, and the second element is the total line count.
        """
        self._normalize_paths()
        return self._count_lines()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    This function uses argparse to parse command line arguments. It sets up arguments for the directory to search,
    files or directories to include, file extensions to include, files or directories to exclude, and file extensions
    to exclude. It then parses the arguments and checks if both include and exclude, or both include_extensions and
    exclude_extensions are provided. If they are, it raises an error. It returns the parsed arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Count lines in a directory excluding or including specified files and extensions."
    )
    parser.add_argument("directory", type=str, help="The directory to search.")
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        nargs="*",
        default=None,
        help="Files or directories to include.",
    )
    parser.add_argument(
        "-ix",
        "--include-extensions",
        type=str,
        nargs="*",
        default=None,
        help="File extensions to include.",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        nargs="*",
        default=None,
        help="Files or directories to exclude.",
    )
    parser.add_argument(
        "-ex",
        "--exclude-extensions",
        type=str,
        nargs="*",
        default=None,
        help="File extensions to exclude.",
    )

    args = parser.parse_args()

    if (args.include and args.exclude) or (
        args.include_extensions and args.exclude_extensions
    ):
        parser.error(
            "Only one of include or exclude, and only one of include_extensions or exclude_extensions can be provided."
        )

    return args


def main() -> None:
    """
    Execute the main program flow.

    This function parses the command line arguments, initializes a LineCounter instance with the parsed arguments,
    counts the lines in each file in the directory excluding specified files and extensions, sorts the line counts
    by the number of lines, and prints the line counts for each file extension and the total line count.

    The function does not return anything as it is intended to be the main entry point of the program.
    """
    args = parse_arguments()

    line_counter = LineCounter(
        args.directory,
        args.include,
        args.include_extensions,
        args.exclude,
        args.exclude_extensions,
    )
    line_counts, total_lines = line_counter.count()
    sorted_line_counts = dict(
        sorted(line_counts.items(), key=lambda item: item[1], reverse=True)
    )
    print()
    for ext, count in sorted_line_counts.items():
        print(f"Total lines for files with extension {ext}: {count}")
    print(f"\nTotal lines in directory {args.directory}: {total_lines}")


if __name__ == "__main__":
    main()
