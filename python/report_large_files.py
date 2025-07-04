import os
from gitignore_parser import parse_gitignore_str


def get_ignored_files(gitignore_path):
    """Parse the .gitignore file and return a function to check ignored files."""
    if not os.path.exists(gitignore_path):
        return lambda x: False  # If no .gitignore, no files are ignored
    with open(gitignore_path, 'r') as f:
        return parse_gitignore_str(f.read(), base_dir=os.path.dirname(gitignore_path))
    

def find_large_files(base_path, ignore_func, size_limit_mb=10):
    """Find files larger than the specified size limit that are not ignored."""
    large_files = []
    size_limit_bytes = size_limit_mb * 1024 * 1024

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not ignore_func(file_path) and '.git' not in file_path:  # Check if the file is not ignored
                file_size = os.path.getsize(file_path)
                if file_size > size_limit_bytes:
                    large_files.append((file_path, file_size))
    return large_files


base_path = os.getcwd()  # Current directory
gitignore_path = os.path.join(base_path, '.gitignore')
ignore_func = get_ignored_files(gitignore_path)

large_files = find_large_files(base_path, ignore_func)

if large_files:
    print("Files over 10MB that are not ignored by .gitignore:")
    for file_path, file_size in large_files:
        print(f"{file_path} - {file_size / (1024 * 1024):.2f} MB")
else:
    print("No files over 10MB found that are not ignored by .gitignore.")
