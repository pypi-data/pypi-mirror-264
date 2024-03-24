import shutil
import pandas as pd
import os
from ..util import folder


def extract_formula_and_tag(compound_formula_tag):
    parts = compound_formula_tag.split()

    # First part is the compound formula
    compound_formula = parts[0]

    # The rest are tags
    tags = "_".join(parts[1:])

    return compound_formula, tags


def move_files_based_on_tags(cif_dir, is_interactive_mode=True):
    print(
        "This script sorts CIF files based on specific tags present in their third line."
    )

    # With graphic user interface
    if is_interactive_mode:
        print(folder_info)
        folder_info = folder.choose_CIF_directory(cif_dir)
        folder_name = os.path.basename(folder_info)

    # No graphic user interface - enter the folder path
    if not is_interactive_mode:
        print(folder_info)
        folder_info = cif_dir
        folder_name = os.path.basename(folder_info)

    # Create an empty dataframe to track the moved files
    df = pd.DataFrame(columns=["Filename", "Formula", "Tag(s)"])

    # Get a list of all .cif files in the chosen directory
    files_lst = [
        os.path.join(folder_info, file)
        for file in os.listdir(folder_info)
        if file.endswith(".cif")
    ]
    total_files = len(files_lst)

    # Iterate through each .cif file, extract its tag and sort it accordingly
    for idx, file_path in enumerate(files_lst, start=1):
        folder_name = os.path.basename(folder_info)
        filename = os.path.basename(file_path)
        print(f"Processing {filename}, ({idx}/{total_files})")

        # Initialize variables outside of the with statement
        compound_formula = None
        tags = None
        subfolder_path = None

        # Open and read the file
        with open(file_path, "r") as f:
            f.readline()  # First line
            f.readline()  # Second line
            third_line = f.readline().strip()  # Third line
            third_line = third_line.replace(",", "")
            third_line_parts = [
                part.strip() for part in third_line.split("#") if part.strip()
            ]

        # File is now closed after the with block
        if third_line_parts:
            compound_formula, tags = extract_formula_and_tag(
                third_line_parts[1]
            )
            print("Formula:", compound_formula, "Tags:", tags)

        if tags:
            subfolder_path = os.path.join(folder_info, f"{folder_name}_{tags}")
            new_file_path = os.path.join(subfolder_path, filename)
            new_row_df = pd.DataFrame(
                {
                    "Filename": [filename],
                    "Formula": [compound_formula],
                    "Tag(s)": [tags],
                }
            )
            df = pd.concat([df, new_row_df], ignore_index=True)

            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

            # Check if the file exists and delete it to avoid the PermissionError
            if os.path.exists(new_file_path):
                os.remove(new_file_path)

            # Now move the file after it's been closed
            shutil.move(file_path, subfolder_path)
            print(
                f"{os.path.basename(file_path)} has been moved to {subfolder_path}"
            )

    folder.save_to_csv_directory(folder_info, df, "tags_log")
