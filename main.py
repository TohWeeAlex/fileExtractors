import os
import shutil
import sys
from pathlib import Path                ## Package for filepath handling

from tkinter import filedialog          ## Package for file explorer dialogue

from alive_progress import alive_bar    ## Package for progress bar

def user_input(prompt):
    raw_input = input(prompt)
    if raw_input in "YyNn":
        if raw_input in "Yy":
            return True
        else:
            return False
    else:
        user_input(prompt)

def ask_dir():
    print("ask_dir function start")
    selected_dir = filedialog.askdirectory()
    print(f'"{selected_dir}" has been selected')
    returned_path = Path(selected_dir)
    return returned_path

def dir_check_N_make(path: Path):
    if not (path.is_dir()):
        path.mkdir(parents=True, exist_ok=True)
    #LOGGING
    # else:
    #     print(f'"{path}" already exsist! Using existing path.')

def adding_folder_func():
    adding_folders = True
    src_paths = []
    while adding_folders:
        src_paths.append(ask_dir())
        adding_folders = user_input("Do you have more folders to include? (Y/n):")
    return src_paths

def copy_all_files_to_flat(sort_flag: bool = False, overwrite_flag: bool = False, move_flag: bool = False, dirList_flag: bool = False) -> None:
    """
    Copy every file in src_dir (including subdirectories) into dst_dir.
    If two files in different locations share the same name, a numeric suffix is appended.

    Parameters:
        src_dir (str): Path to the source directory tree.
        dst_dir (str): Path to the destination directory (will be created if missing).
        overwrite (bool): If True, overwrite files of the same name; otherwise, add suffix.
    """

    #print(f'sort set to {sort}, overwrite set to {overwrite}')

    #print("Script start")
    
    if dirList_flag:
        # Browse for Folder list
        print("Looking for folder list")
        src_paths = [dirPath.rstrip('\n') for dirPath in open(Path(filedialog.askopenfilename(filetypes=(('text files', 'txt'),))))]
        print(src_paths)
    else:
        src_paths = adding_folder_func()

    dst_path = ask_dir()
    
    #print("Input and Output path selected")

    if sort_flag:
        dst_path = Path(f"{dst_path}/Sorted_Output")
        dir_check_N_make(dst_path)
    else:
        dir_check_N_make(dst_path)

    # Track which filenames we've already used
    existing = {}
    for src_path in src_paths:
        for root, _, files in os.walk(src_path):
            with alive_bar(len(files)) as bar:
                for fname in files:
                    src_file = Path(root) / fname
                    base, ext = os.path.splitext(fname)

                    # Determine destination filename
                    if overwrite_flag or fname not in existing:
                        target_name = fname
                        existing[fname] = 1
                    else:
                        # Conflict: append a counter suffix before the extension
                        count = existing[fname]
                        existing[fname] += 1
                        target_name = f"{base}_Copy{count}{ext}"

                    if sort_flag:
                        dst_file = dst_path / ext / target_name
                        dir_check_N_make(Path(dst_path / ext ))
                    else:
                        dst_file = dst_path / target_name

                    # Perform the copy (preserve metadata)
                    bar.text(f'Now transfering: "{target_name}"')
                    shutil.copy2(src_file, dst_file)
                    if move_flag and os.path.exists(src_file):
                        os.remove(src_file)
                    bar()

if __name__ == "__main__":
    print(sys.argv)

    copy_all_files_to_flat(sort_flag=("--sorted" in sys.argv), overwrite_flag=("--overwrite" in sys.argv), move_flag=("--move" in sys.argv), dirList_flag=("--list" in sys.argv))

    # path = Path(str(ask_dir()) + "/Sorted_Output")
    # print(path)
    # path.mkdir(parents=True, exist_ok=True)
    print("Done.")