#!/usr/bin/env python3
"""
Post-generation tasks

File: hooks/post_gen_project.py

Copyright 2025 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""

import os
import sys
import subprocess


def use_git():
    """Commit initial project to a git repository """
    print("Initialising a new Git repository")
    subprocess.run(["git", "init"], check=True)

    print("Adding files")
    subprocess.run(["git", "add", "."], check=True)

    print("Making initial commit")
    subprocess.run(["git", "commit", "-m", "Init"], check=True)

    print("Git repository initialized")
    return 0



if __name__ == "__main__":
    {% if cookiecutter.use_git is true %}

    sys.exit(use_git())

    {% else %}

    sys.exit(0)

    {% endif %}
