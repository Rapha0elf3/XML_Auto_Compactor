from datetime import date
from pathlib import Path
from shutil import make_archive
import os
import platform
import subprocess

def get_last_month():

    actual_date = date.today()
    last_month = None

    if actual_date.month == 1:
        last_month = f"{actual_date.year - 1}-{12:02d}"
    else:
        last_month = f"{actual_date.year}-{(actual_date.month - 1):02d}"

    return last_month

def process_file(config, log):
    storage_path = config["storage_path"]
    working_path = config["working_path"]
    target_file = get_last_month()
    source_folder = None
    stored = False

    try:
        for file in Path(storage_path).iterdir():
            if file.name == f"{target_file}.zip":
                stored = True
                log("File is already compressed!")
                break

    except FileNotFoundError:
        log("Storage folder not found")
        return
    except OSError as e:
        log(f"File system error: {e}")
        return

    try:
        if not stored:
            for file in Path(working_path).iterdir():
                if file.name == target_file:
                    if file.is_dir():
                        source_folder = file
                        log("Folder to compress was found!")
                        log("Starting compression...")
                        make_archive(
                            Path(storage_path) / target_file,
                            "zip",
                            source_folder
                        )
                        break

            if source_folder is None:
                log("Folder to compress not found.")
                log("Check if the working directory is correct")
                return


    except FileNotFoundError:
        log("File or folder not found")
        return
    except OSError as e:
        log(f"File system error: {e}")
        return

    match platform.system():

        case "Windows":
            os.startfile(Path(storage_path))
        case "Linux":
            subprocess.Popen(["xdg-open", str(Path(storage_path))])
        case "Darwin":
            subprocess.Popen(["open", str(Path(storage_path))])
