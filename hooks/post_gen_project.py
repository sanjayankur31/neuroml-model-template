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
    print(">> Initialising a new Git repository")
    subprocess.run(["git", "init"], check=True)

    print(">> Adding files")
    subprocess.run(["git", "add", "."], check=True)

    print(">> Making initial commit")
    subprocess.run(["git", "commit", "-m", "Init"], check=True)

    print(">> Git repository initialized")
    return 0


def use_git_annex():
    """Use git-annex for simdata folder"""
    print(">> Initialising git-annex")
    subprocess.run(["git", "annex", "init"], check=True)

    print(">> Marking data/ to be managed by git-annex")
    # note: no quotes around `include=data/*` here as it'll be split into a
    # separate argument already
    command = "git annex config --set annex.largefiles include=data/*"
    subprocess.run(command.split(), check=True)


    print(">> Adding data/ to git-annex")
    with open("data/Readme.md", 'a') as f:
        print("\n\nThis folder is managed by [git-annex](https://git-annex.branchable.com/).", file=f)

    command = "git annex add data/"
    subprocess.run(command.split(), check=True)

    subprocess.run(["git", "commit", "-m", "'Initialised git-annex'"], check=True)

    print()
    print()
    print(">> The data/ folder will not be managed by git-annex")
    print(">> For remotes you can use with git-annex, please see: https://git-annex.branchable.com/special_remotes/")
    print(">> https://gin.g-node.org/ provides a public git-annex enabled Git forge that")

    return 0


if __name__ == "__main__":
    {% if cookiecutter.use_git is true %}

    ret1 = use_git()
    if ret1 != 0:
        sys.exit(1)

    {% if cookiecutter.use_git_annex is true %}

    ret2 = use_git_annex()
    if ret2 != 0:
        sys.exit(1)

    {% endif %}

    {% endif %}


    sys.exit(0)
