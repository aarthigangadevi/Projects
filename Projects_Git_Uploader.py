#!/usr/bin/env python3
"""
GitHub Multiple Projects Upload Script using PyGithub
This script automates the process of creating GitHub repositories and pushing multiple local projects.
"""

import os
import sys
import subprocess
import time
from github import Github
from getpass import getpass
from pathlib import Path

def run_command(command, cwd=None):
    """Execute a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def is_git_repo(path):
    """Check if a directory is already a git repository."""
    return os.path.isdir(os.path.join(path, ".git"))

def initialize_git_repo(path):
    """Initialize a git repository if it doesn't exist yet."""
    if not is_git_repo(path):
        success, output = run_command("git init", cwd=path)
        if success:
            print(f"Initialized git repository in {path}")
        else:
            print(f"Failed to initialize git repository: {output}")
            return False
    return True

def commit_all_files(path, message="Initial commit"):
    """Add all files and create a commit."""
    success, _ = run_command("git add .", cwd=path)
    if not success:
        print(f"Failed to add files in {path}")
        return False
    
    # Check if there are changes to commit
    status_success, status_output = run_command("git status --porcelain", cwd=path)
    if status_success and not status_output.strip():
        print(f"No changes to commit in {path}")
        return True
    
    success, output = run_command(f'git commit -m "{message}"', cwd=path)
    if success:
        print(f"Created commit in {path}")
        return True
    else:
        print(f"Failed to create commit: {output}")
        return False

def setup_remote(path, repo_url):
    """Set up or update the remote repository URL."""
    # Check if origin remote exists
    check_success, check_output = run_command("git remote -v", cwd=path)
    
    if "origin" in check_output:
        # Remove existing origin remote
        success, _ = run_command("git remote remove origin", cwd=path)
        if not success:
            print(f"Failed to remove existing remote in {path}")
            return False
    
    # Add new origin remote
    success, output = run_command(f"git remote add origin {repo_url}", cwd=path)
    if success:
        print(f"Set up remote for {path}")
        return True
    else:
        print(f"Failed to set up remote: {output}")
        return False

def push_to_github(path):
    """Push the repository to GitHub."""
    # Try pushing to 'main' branch first, then 'master' if that fails
    success, output = run_command("git push -u origin main", cwd=path)
    if not success:
        # Check if we need to create a main branch
        branch_success, branch_output = run_command("git branch", cwd=path)
        if branch_success and "main" not in branch_output:
            # Create a main branch if it doesn't exist
            run_command("git checkout -b main", cwd=path)
            success, output = run_command("git push -u origin main", cwd=path)
        
        # If main still fails, try master
        if not success:
            success, output = run_command("git push -u origin master", cwd=path)
    
    if success:
        print(f"Successfully pushed {path} to GitHub")
        return True
    else:
        print(f"Failed to push to GitHub: {output}")
        return False

def main():
    # List of projects to push (replace with your actual paths)
    projects = [
       # "Enter your path here"
    ]
    
    # Get GitHub credentials
    print("GitHub Authentication")
    print("---------------------")
    username = input("GitHub Username: ")
    token = getpass("GitHub Personal Access Token: ")
    
    try:
        # Initialize GitHub API
        g = Github(token)
        user = g.get_user()
        print(f"Successfully authenticated as {user.login}")
        
        # Process each project
        for project_path in projects:
            path = Path(project_path).expanduser().resolve()
            project_name = path.name
            
            print(f"\nProcessing project: {project_name}")
            print("-" * 50)
            
            if not path.exists() or not path.is_dir():
                print(f"Error: {path} is not a valid directory. Skipping.")
                continue
                
            # Step 1: Initialize git repository if needed
            if not initialize_git_repo(path):
                continue
                
            # Step 2: Create GitHub repository if it doesn't exist
            print(f"Checking if repository '{project_name}' exists...")
            repo = None
            try:
                repo = user.get_repo(project_name)
                print(f"Repository {project_name} already exists on GitHub")
            except Exception:
                print(f"Creating new repository: {project_name}")
                repo = user.create_repo(
                    project_name,
                    description=f"Repository for {project_name}",
                    private=True  # Set to False for public repositories
                )
                # Sleep briefly to avoid rate limiting and ensure repo is created
                time.sleep(1)
            
            # Step 3: Commit all files
            if not commit_all_files(path):
                continue
                
            # Step 4: Set up remote
            if not setup_remote(path, repo.clone_url):
                continue
                
            # Step 5: Push to GitHub
            if not push_to_github(path):
                continue
                
            print(f"Successfully uploaded {project_name} to GitHub")
            
        print("\nAll projects processed!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
