# Line Counter

This Python script counts the number of lines in all files within a specified directory, excluding or including
specified files and extensions.

## Installation

To install the script, you can clone the repository and run the script directly:

```bash
git clone https://github.com/yourusername/line-counter.git
cd line-counter
python main.py
```

## Making the Script Executable

The script can always be run by calling `python /path/to/main.py`, but you can make it executable so that you can run it
by typing `line-counter` or `line-counter.bat` into your terminal. Here's how you can do it:

### Unix-like Systems (Linux, macOS)

1. Make the script executable. You can do this by changing the permissions of the script file. Open a terminal, navigate
   to the directory containing the script, and run the following command:

    ```bash
    chmod +x main.py
    ```

2. Rename your script to line-counter (without the .py extension). You can do this with the following command:

    ```bash
    mv main.py line-counter
    ```

3. Move your script to a directory that's on your system's PATH. The PATH is a list of directories that your system
   searches through when looking for executables. You can move your script to /usr/local/bin, which is a common place to
   put custom scripts:

    ```bash
    sudo mv line-counter /usr/local/bin
    ```

Now, you should be able to run your script from anywhere by typing line-counter into your terminal.

### Windows

1. Add the directory containing the line-counter batch file to your system's PATH. Here's how you can do it:
    - Right-click on 'Computer' and click on 'Properties'.
    - Click on 'Advanced system settings'.
    - Click on 'Environment Variables'.
    - Under 'System Variables', find the 'Path' variable, select it, and click on 'Edit'.
    - In the 'Variable value' field, append the full path to the directory containing the batch file.

Now, you should be able to run your script from anywhere by typing line-counter.bat into your command prompt, followed
by any arguments the script accepts.

To make the script executable as line-counter instead of line-counter.bat, you can create an alias in Windows:

1. Open a command prompt.
2. Run the following command:

    ```bash
    doskey line-counter=line-counter.bat $*
    ```

Note: This alias will only be available in the current session. To make it permanent, you can add it to your user's
profile script. For example, you can add the doskey command to your user's profile script, which is located at C:
\Users\YourUsername\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 for PowerShell or C:
\Users\YourUsername\Documents\profile.ps1 for Command Prompt.

## Usage

The script is intended to be run from the command line. It takes a directory to search, and optional arguments for files
or directories to include or exclude, and file extensions to include or exclude.

Here are the available command line arguments:

- `directory`: The directory to search. This is a required argument.
- `-i` or `--include`: Files or directories to include. This is an optional argument.
- `-ix` or `--include-extensions`: File extensions to include. This is an optional argument.
- `-e` or `--exclude`: Files or directories to exclude. This is an optional argument.
- `-ex` or `--exclude-extensions`: File extensions to exclude. This is an optional argument.

Note: Only one of `include` or `exclude`, and only one of `include-extensions` or `exclude-extensions` can be provided.

Files with no extensions are given the `.noext` extension by the script. This allows you to include or exclude such
files using the `--include-extensions` or `--exclude-extensions` arguments respectively.

## Examples

Here are some examples of how to use the script:

1. Count the lines in all files in a directory, excluding any files in the venv directory and any files with a .txt
   extension: <pre>bash python main.py /path/to/directory --exclude venv --exclude-extensions .txt </pre>
2. Count the lines in all Python files in a directory, including only files in the src directory:  <pre>python main.py
   /path/to/directory --include src --include-extensions .py </pre>

The script will then print the line counts for each file extension, sorted by the number of lines, and the total line
count.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for more information.