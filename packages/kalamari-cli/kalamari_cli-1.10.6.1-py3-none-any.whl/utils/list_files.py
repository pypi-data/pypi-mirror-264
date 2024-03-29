import subprocess
import os


def list_git_files(directory, show_tree):
    """
    List all files in a directory that are not ignored by git using `git ls-files` command.

    This function uses the `git ls-files` command to list all files that are not ignored
    by .gitignore files. It can also display the directory tree structure if requested.

    Args:
        directory (str): The root directory to list files from.
        show_tree (bool, optional): If True, prints the directory tree structure. Defaults to False.
    """
    try:
        file_list = []
        # Change the current working directory to the specified directory
        original_directory = (
            subprocess.check_output("pwd", shell=True).decode("utf-8").strip()
        )
        os.chdir(directory)

        # Execute `git ls-files` command to list all tracked files
        result = subprocess.check_output("git ls-files", shell=True).decode("utf-8")

        # Change back to the original directory
        os.chdir(original_directory)

        files = result.split("\n")

        for file in files:
            file_list.append(file)
            if show_tree:
                depth = file.count("/")
                print("    " * depth + "|-- " + file.split("/")[-1])

        return file_list
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"Error listing git files: {e}") from e

def test_list_git_files():
    """
    Test the list_git_files function with a known directory structure.
    """
    # Assuming the current directory has a .git and it's not empty
    directory = "."
    print("Testing list_git_files with show_tree=False")
    file_list = list_git_files(directory, show_tree=False)
    print(file_list)

    print("\nTesting list_git_files with show_tree=True")
    file_list = list_git_files(directory, show_tree=True)
    print(file_list)

if __name__ == "__main__":
    test_list_git_files()
