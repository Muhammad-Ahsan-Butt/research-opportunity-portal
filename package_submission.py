"""
Submission packaging script for Computer Networks Assignment #1.
Packages project files into the required ZIP naming format: P24_0000_NAME_CLASS.zip
"""

import os
import zipfile

ZIP_NAME = "P24_0026_MUHAMMAD_AHSAN_BSAI5A.zip"

INCLUDED_DIRECTORIES = ["backend", "frontend", "database", "postman", "tests"]
INCLUDED_FILES = [
    "README.md",
    "requirements.txt",
    "docker-compose.yml",
    ".env.example",
    ".gitignore",
    "ASSIGNMENT.md"
]

EXCLUDED_EXTENSIONS = [".pyc", ".pyo", ".DS_Store"]
EXCLUDED_DIRS = ["__pycache__", ".git", "venv", ".venv", "env"]


def create_submission_zip():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, ZIP_NAME)

    print(f"Creating submission package: {ZIP_NAME}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root files
        for filename in INCLUDED_FILES:
            file_path = os.path.join(base_dir, filename)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=filename)
                print(f"  Added file: {filename}")

        # Add directories
        for directory in INCLUDED_DIRECTORIES:
            dir_path = os.path.join(base_dir, directory)
            if not os.path.exists(dir_path):
                continue

            for root, dirs, files in os.walk(dir_path):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

                for file in files:
                    if any(file.endswith(ext) for ext in EXCLUDED_EXTENSIONS):
                        continue

                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, base_dir)
                    zf.write(full_path, arcname=rel_path)
                    print(f"  Added file: {rel_path}")

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\nSubmission ZIP created successfully: {ZIP_NAME} ({size_mb:.2f} MB)")
    print(f"File path: {zip_path}")


if __name__ == "__main__":
    create_submission_zip()
