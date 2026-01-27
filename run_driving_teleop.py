#!/usr/bin/env python3
"""Wrapper to run the teleop as a package module from the project root.

Use this instead of executing Commands/driving_teleop.py directly.
Example: `.venv/bin/python run_driving_teleop.py`
"""
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(root))

from importlib import import_module

if __name__ == "__main__":
    import_module("Commands.driving_teleop")
