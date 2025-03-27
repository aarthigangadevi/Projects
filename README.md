# GitHub Multiple Projects Upload Script

## Overview
This script automates the process of creating GitHub repositories and pushing multiple local projects using the PyGithub library. It ensures that each project is initialized as a Git repository, commits files, sets up a remote repository, and pushes the code to GitHub.

## Features
- Authenticates with GitHub using a personal access token.
- Checks if the specified local projects exist.
- Initializes Git repositories if not already initialized.
- Creates a new GitHub repository if it does not exist.
- Commits all files and sets up the remote repository.
- Pushes the projects to GitHub.

## Prerequisites
- Python 3 installed on your system.
- A GitHub account.
- A GitHub personal access token with repository permissions.
- Git installed on your system.

## Installation
1. Clone the repository or download the script.
   ```bash
   git clone https://github.com/YOUR_USERNAME/Repository_Uploader.git
   cd Repository_Uploader
   ```
2. Install the required dependencies:
   ```bash
   pip install PyGithub
   ```

## Usage
1. Run the script:
   ```bash
   python Repository_Uploader.py
   ```
2. Enter your GitHub credentials when prompted.
3. The script will process each project directory listed and upload it to GitHub.

## Configuration
To customize the script:
- Modify the `projects` list in `main()` to specify the directories of the projects you want to upload.
- Change the repository visibility by modifying the `private=True` setting in the `create_repo()` function.

## Troubleshooting
- Ensure Git is installed and configured with your GitHub account.
- If the script fails due to authentication issues, regenerate your GitHub personal access token.
- Verify that the project directories exist and contain valid files.

## Author
[Aarthi Gangadevi](https://github.com/YOUR_USERNAME)

