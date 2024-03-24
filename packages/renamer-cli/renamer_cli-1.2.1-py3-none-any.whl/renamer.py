import os
import sys
import argparse
import json
import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Rename files and directories based on a user-defined pattern')

    parser.add_argument('-d', '--directory',
                        default=os.getcwd(),
                        help="Path to the directory containing files and directories to be renamed.")

    parser.add_argument('-p', '--pattern',
                        help="Naming pattern for renaming files and directories. Use placeholders like {name}, {parent}, {date}, etc.")

    parser.add_argument('-f', '--files-only',
                        action='store_true',
                        help="Rename only files, not directories.")

    parser.add_argument('-D', '--directories-only',
                        action='store_true',
                        help="Rename only directories, not files.")

    parser.add_argument('-e', '--extensions',
                        nargs='+',
                        help="Rename only files with specified extensions.")

    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help="Perform renaming recursively, including files and directories in subdirectories.")

    parser.add_argument('-i', '--interactive',
                        action='store_true',
                        help="Enable interactive mode for manual confirmation of each renaming operation.")
    
    parser.add_argument('-u', '--undo',
                        action='store_true',
                        help="Undo the last file and directory renaming operation.")
    
    args = parser.parse_args()
    
    if not args.undo and not args.pattern:
        parser.error("When not using --undo, the --pattern option is required.")


    return args



def perform_file_renaming(directory, pattern, files_only=False, directories_only=False, extensions=None, recursive=False, interactive=False):
    
    if recursive:
        
        # get all directories in the specified directory
        directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        
        if directories:
            for subdir in directories:
                # recursivly call the function for each subdirectory
                perform_file_renaming(os.path.join(directory, subdir), pattern, files_only, directories_only, extensions, recursive, interactive)
        perform_file_renaming(directory, pattern, files_only, directories_only, extensions, False, interactive)

    else:
        # get list of files and directories in the specified directory
        files, directories = filter_files_and_directories(directory, files_only, directories_only, extensions)
        
        # rename files and directories
        if files or directories:
            rename_and_log(directory, pattern, files, directories, interactive)
        
        
def filter_files_and_directories(directory, files_only, directories_only, extensions):
    # get a list of files and directories in the specified directory
    files_and_dirs = os.listdir(directory)
    
    # filter files and directories based on options
    files = []
    directories = []
    for item in files_and_dirs:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            item_extension = os.path.splitext(item)[1]
            if extensions is None:
                files.append(item)
            elif item_extension[1:] in [ext if not ext.startswith('.') else ext[1:] for ext in extensions]:
                files.append(item)
        elif os.path.isdir(item_path):
            directories.append(item)
    
    # if only renaming files, clear the directories list
    if files_only:
        directories = []
    
    # if only renaming directories, clear the files list
    if directories_only:
        files = []
    
    return files, directories


def rename_and_log(directory, pattern, files, directories, interactive):
    
    rename_log = {} 
    # rename files
    for filename in files:
        if filename == 'renaming_log.json':
            continue
        old_path = os.path.join(directory, filename)
        base_name, file_extension = os.path.splitext(filename)
        date = datetime.datetime.now().strftime("%Y%m%d")
        parent_dir = os.path.basename(os.path.dirname(old_path))
        new_name = pattern.format(name=base_name, ext=file_extension, date=date, parent=parent_dir)
        new_path = os.path.join(directory, new_name)
        if interactive:
            confirm = input(f"Rename '{filename}' to '{new_name}'? (y/n): ")
            if confirm.lower() != 'y' and confirm.lower() != 'yes':
                continue
        os.rename(old_path, new_path)
        rename_log[filename] = new_name
    
    # rename directories
    for dirname in directories:
        old_path = os.path.join(directory, dirname)
        date = datetime.datetime.now().strftime("%Y%m%d")
        parent_dir = os.path.basename(os.path.dirname(old_path))
        new_name = pattern.format(name=dirname, ext='', date=date, parent=parent_dir)
        new_path = os.path.join(directory, new_name)
        if interactive:
            confirm = input(f"Rename '{dirname}' to '{new_name}'? (y/n): ")
            if confirm.lower() != 'y' and confirm.lower() != 'yes':
                continue
        os.rename(old_path, new_path)
        rename_log[dirname] = new_name
    
    print("File and directory renaming complete.")
    
    # log renaming operations
    log_renaming_operations(directory, rename_log)


def log_renaming_operations(directory, rename_log):
    log_file = os.path.join(directory, 'renaming_log.json')
    with open(log_file, 'w') as f:
        json.dump(rename_log, f, indent=4)

    print(f"Renaming log has been saved to {log_file}")
    
    
def undo_rename(directory, files_only=False, directories_only=False, extensions=None, recursive=False):
    if recursive:
        # Get all directories in the specified directory
        directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        
        # Recursively call the function for each subdirectory
        for subdir in directories:
            undo_rename(os.path.join(directory, subdir), files_only, directories_only, extensions, recursive)
    
    # Perform undo renaming operation for the current directory
    undo_rename_single(directory, files_only, directories_only, extensions)


def undo_rename_single(directory, files_only=False, directories_only=False, extensions=None):
    
    
    log_file = os.path.join(directory, 'renaming_log.json')
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            rename_log = json.load(f)
    
        if not rename_log:
            print(f"Renaming log in {directory} is empty.")
            return
    
        
        print("Previewing changes:")
        # preview changes
        for old_name, new_name in rename_log.items():
            old_path = os.path.join(directory, new_name)
            new_path = os.path.join(directory, old_name)
    
            # Check if the item matches the filter criteria
            if files_only and os.path.isdir(old_path):
                continue  # Skip if only files are allowed and the item is a directory
            if directories_only and os.path.isfile(old_path):
                continue  # Skip if only directories are allowed and the item is a file
            if extensions and not any(old_name.endswith(ext) for ext in extensions):
                continue  # Skip if specific extensions are provided and the item's extension is not in the list
            
            print(f"Rename '{new_name}' back to '{old_name}'")


        confirm = input("Do you agree to undo these changes? (y/n): ")
        if confirm.lower() != 'y' and confirm.lower() != 'yes':
            print("Undo operation aborted.")
            return
        
        
        entries_to_remove = []
        
        for old_name, new_name in rename_log.items():
            old_path = os.path.join(directory, new_name)
            new_path = os.path.join(directory, old_name)
    
            # Check if the item matches the filter criteria
            if files_only and os.path.isdir(old_path):
                continue  # Skip if only files are allowed and the item is a directory
            if directories_only and os.path.isfile(old_path):
                continue  # Skip if only directories are allowed and the item is a file
            if extensions and not any(old_name.endswith(ext) for ext in extensions):
                continue  # Skip if specific extensions are provided and the item's extension is not in the list

            # Perform undo renaming
            os.rename(old_path, new_path)
            entries_to_remove.append(old_name)
        
        for entry in entries_to_remove:
            del rename_log[entry]
        
        # Update the renaming log
        with open(log_file, 'w') as f:
            json.dump(rename_log, f, indent=4)
    
        print(f"Undo renaming operation completed for {directory}.")
    else:
        print(f"Renaming log does not exist in {directory}.")




def main():

    args = parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)

    if args.undo:
        undo_rename(args.directory, args.files_only, args.directories_only, args.extensions, args.recursive)
    else:
        perform_file_renaming(args.directory, args.pattern, args.files_only, args.directories_only, args.extensions, args.recursive, args.interactive)


if __name__ == "__main__":
    main()
