import os

def get_chapters(path):
    """Yield files containing "chapter" in their name"""
    for entry in os.scandir(path):
        if "chapter" in entry.name:
            yield entry
