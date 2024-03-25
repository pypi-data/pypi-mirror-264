"""
Renamer-CLI - A command-line tool for renaming files and directories.

This script provides functionality to rename files and directories
in a specified directory based on user-defined patterns. It offers various
options for customizing the renaming process, including specifying patterns,
filtering files/directories by type or extension, and performing operations
recursively.

For usage instructions and available options, run `renamer --help`.

Author: READMEmaybe
Date: March 2024

License: MIT License
"""
import os
import sys
import argparse
import json
import datetime


def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=("Rename files and directories based on a user-defined "
                     "pattern")
    )

    parser.add_argument(
        '-d', '--directory',
        default=os.getcwd(),
        help=("Path to the directory containing files and directories to be "
              "renamed.")
    )

    parser.add_argument(
        '-p', '--pattern',
        help=("Naming pattern for renaming files and directories. Use "
              "placeholders like {name}, {parent}, {date}, etc.")
    )

    parser.add_argument(
        '-f', '--files-only',
        action='store_true',
        help="Rename only files, not directories."
    )

    parser.add_argument(
        '-D', '--directories-only',
        action='store_true',
        help="Rename only directories, not files."
    )

    parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        help="Rename only files with specified extensions."
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help=("Perform renaming recursively, including files and directories "
              "in subdirectories.")
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help=("Enable interactive mode for manual confirmation of each "
              "renaming operation.")
    )

    parser.add_argument(
        '-u', '--undo',
        action='store_true',
        help="Undo the last file and directory renaming operation.")

    args = parser.parse_args()

    error_message = "When not using --undo, the --pattern option is required."
    if not args.undo and not args.pattern:
        parser.error(error_message)

    return args


def perform_file_renaming(
    directory, pattern, files_only=False, directories_only=False,
    extensions=None, recursive=False, interactive=False
):
    """
    Perform renaming of files and directories based on the specified pattern.

    Args:
        directory (str): The path to the directory.
        pattern (str): The naming pattern for renaming files and directories.
        files_only (bool): If True, rename only files. Default is False.
        directories_only (bool): If True, rename only dirs. Default is False.
        extensions (list of str): filter by file extension. Default is None.
        recursive (bool): If True, renaming recursively. Default is False.
        interactive (bool): Enables manual confirmation. Default is False.
    """
    if recursive:
        _ = os.listdir(directory)
        dirs = [d for d in _ if os.path.isdir(os.path.join(directory, d))]

        if dirs:
            for subdir in dirs:
                perform_file_renaming(
                    os.path.join(directory, subdir), pattern, files_only,
                    directories_only, extensions, recursive, interactive)
        perform_file_renaming(
            directory, pattern, files_only, directories_only,
            extensions, False, interactive)

    else:
        files, directories = filter_files_and_directories(
            directory, files_only, directories_only, extensions)

        if files or directories:
            rename_and_log(directory, pattern, files, directories, interactive)


def filter_files_and_directories(
    directory, files_only, directories_only, extensions
):
    """
    Filter files and directories based on the provided options.

    Args:
        directory (str): The path to the directory to be filtered.
        files_only (bool): If True, only files will be considered.
        directories_only (bool): If True, only directories will be considered.
        extensions (list of str): List of file extensions to filter by.

    Returns:
        list: A list containing filenames.
        list: A list containing directory names.
    """
    files = []
    directories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            item_extension = os.path.splitext(item)[1]
            if extensions is None:
                files.append(item)
            elif item_extension[1:] in [ext if not ext.startswith('.') else ext[1:] for ext in extensions]:
                files.append(item)
        elif os.path.isdir(item_path):
            directories.append(item)

    if files_only:
        directories = []
    if directories_only:
        files = []

    return files, directories


def rename_and_log(directory, pattern, files, directories, interactive):
    """
    Rename files and directories based on the provided pattern
        and log the renaming operations.

    Args:
        directory (str):
            The path to the directory used.
        pattern (str):
            The naming pattern for renaming files and directories.
            Use placeholders like {name}, {ext}, {date}, {parent}, etc.
        files (list of str):
            A list containing filenames to be renamed.
        directories (list of str):
            A list containing directory names to be renamed.
        interactive (bool):
            If True, enables manual confirmation of each renaming operation.
    """
    rename_log = {}
    for filename in files:
        if filename == 'renaming_log.json':
            continue
        old_path = os.path.join(directory, filename)
        base_name, file_extension = os.path.splitext(filename)
        date = datetime.datetime.now().strftime("%Y%m%d")
        parent_dir = os.path.basename(os.path.dirname(old_path))
        new_name = pattern.format(
            name=base_name, ext=file_extension, date=date, parent=parent_dir)
        new_path = os.path.join(directory, new_name)
        if interactive:
            confirm = input(f"Rename '{filename}' to '{new_name}'? (y/n): ")
            if confirm.lower() != 'y' and confirm.lower() != 'yes':
                continue
        os.rename(old_path, new_path)
        rename_log[filename] = new_name

    for dirname in directories:
        old_path = os.path.join(directory, dirname)
        date = datetime.datetime.now().strftime("%Y%m%d")
        parent_dir = os.path.basename(os.path.dirname(old_path))
        new_name = pattern.format(
            name=dirname, ext='', date=date, parent=parent_dir)
        new_path = os.path.join(directory, new_name)
        if interactive:
            confirm = input(f"Rename '{dirname}' to '{new_name}'? (y/n): ")
            if confirm.lower() != 'y' and confirm.lower() != 'yes':
                continue
        os.rename(old_path, new_path)
        rename_log[dirname] = new_name

    print("File and directory renaming complete.")

    log_renaming_operations(directory, rename_log)


def log_renaming_operations(directory, rename_log):
    """
    Log renaming operations to a JSON file.

    Args:
        directory (str):
            The directory where the renaming log will be saved.
        rename_log (dict):
            A dictionary containing the old and new filenames.
    """
    log_file = os.path.join(directory, 'renaming_log.json')
    with open(log_file, 'w') as f:
        json.dump(rename_log, f, indent=4)

    print(f"Renaming log has been saved to {log_file}")


def undo_rename(
    directory, files_only=False,
    directories_only=False, extensions=None, recursive=False
):
    """Undo the last file and directory renaming operation.

    Args:
        directory (str):
            The directory containing the files and directories to be restored.
        files_only (bool, optional):
            If True, only files will be restored. Defaults to False.
        directories_only (bool, optional):
            If True, only directories will be restored. Defaults to False.
        extensions (list, optional):
            A list of file extensions to be restored. Defaults to None.
        recursive (bool, optional):
            If True, the restoration will be performed recursively.
    """
    if recursive:
        _ = os.listdir(directory)
        dirs = [d for d in _ if os.path.isdir(os.path.join(directory, d))]

        for subdir in dirs:
            undo_rename(
                os.path.join(directory, subdir), files_only,
                directories_only, extensions, recursive)

    undo_rename_single(directory, files_only, directories_only, extensions)


def undo_rename_single(
    directory, files_only=False, directories_only=False, extensions=None
):
    """
    Undo the last file and directory renaming operation in a single directory.

    Args:
        directory (str):
            The directory containing the files and directories to be restored.
        files_only (bool, optional):
            If True, only files will be restored. Defaults to False.
        directories_only (bool, optional):
            If True, only directories will be restored. Defaults to False.
        extensions (list, optional):
            A list of file extensions to be restored. Defaults to None.
    """
    log_file = os.path.join(directory, 'renaming_log.json')
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            rename_log = json.load(f)

        if not rename_log:
            print(f"Renaming log in {directory} is empty.")
            return

        print("Previewing changes:")
        for old_name, new_name in rename_log.items():
            old_path = os.path.join(directory, new_name)
            new_path = os.path.join(directory, old_name)
            if files_only and os.path.isdir(old_path):
                continue
            if directories_only and os.path.isfile(old_path):
                continue
            if extensions and not any(old_name.endswith(ext) for ext in extensions):
                continue
            print(f"Rename '{new_name}' back to '{old_name}'")

        confirm = input("Do you agree to undo these changes? (y/n): ")
        if confirm.lower() != 'y' and confirm.lower() != 'yes':
            print("Undo operation aborted.")
            return

        entries_to_remove = []
        for old_name, new_name in rename_log.items():
            old_path = os.path.join(directory, new_name)
            new_path = os.path.join(directory, old_name)
            if files_only and os.path.isdir(old_path):
                continue
            if directories_only and os.path.isfile(old_path):
                continue
            if extensions and not any(old_name.endswith(ext) for ext in extensions):
                continue
            os.rename(old_path, new_path)
            entries_to_remove.append(old_name)

        for entry in entries_to_remove:
            del rename_log[entry]

        with open(log_file, 'w') as f:
            json.dump(rename_log, f, indent=4)

        print(f"Undo renaming operation completed for {directory}.")
    else:
        print(f"Renaming log does not exist in {directory}.")


def main():
    """Entry point for the renamer CLI."""
    args = parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)

    if args.undo:
        undo_rename(
            args.directory, args.files_only,
            args.directories_only, args.extensions, args.recursive)
    else:
        perform_file_renaming(args.directory, args.pattern,
                              args.files_only, args.directories_only,
                              args.extensions, args.recursive,
                              args.interactive)


if __name__ == "__main__":
    main()
