from filter.supercell_size import move_files_based_on_supercell_size
from os.path import join
from util.folder import (
    remove_directories,
    get_cif_file_count_from_directory,
    move_files,
    get_cif_file_path_list_from_directory,
)


def test_move_files_based_on_supercell_size():
    base_dir = "test/supercell_size_cif_files"
    filtered_dir = join(
        base_dir, "supercell_size_cif_files_filter_supercell_size"
    )

    # Setup: Ensure the environment is clean before testing
    remove_directories([filtered_dir])

    # Test: move files based on the maximum number of atoms in the supercell
    move_files_based_on_supercell_size(base_dir, False, 100)

    assert (
        get_cif_file_count_from_directory(filtered_dir) == 4
    ), "Not all expected files were copied."
    assert (
        get_cif_file_count_from_directory(base_dir) == 1
    ), "Not all expected files were copied."

    # Finish: bring the filtered backs and remove generated folders
    move_files(base_dir, get_cif_file_path_list_from_directory(filtered_dir))
    assert (
        get_cif_file_count_from_directory(base_dir) == 5
    ), "Not all expected files were copied."
    remove_directories([filtered_dir])
