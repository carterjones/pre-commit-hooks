#!/usr/bin/env python

import argparse
from os import path
from pathlib import Path
import sys

import markdown
from lxml import etree


def check_links(filename):
    # Set a return code flag.
    retcode = 0

    if not filename.endswith(".md"):
        return retcode

    filepath = Path(filename)
    print(f"Checking {filename}...")

    if not filepath.is_file():
        raise Exception(f"{filepath} is not a file")

    with open(filepath) as f:
        data = f.read()

    # etree.fromstring requires a single outer element, so that is the purpose
    # of div here.
    md_data = "<div>" + markdown.markdown(data) + "</div>"
    doc = etree.fromstring(md_data)
    for link in doc.xpath("//a"):
        href = link.get("href")

        # Filter out all external links. For now, this just assumes that all
        # external links start with 'http' or 'mailto'. This is a fautly
        # assumption, but it works for my needs.
        skip = False
        for prefix in ("http", "mailto"):
            if href.startswith(prefix):
                skip = True
                break
        if skip:
            continue

        # Check to see if this href is a valid filepath. If not, print a
        # message.
        target = Path(href)
        if href.startswith("/"):
            # Global references can be either files or directories.
            path_exists = target.exists()
        else:
            # Local references must reference a file.
            path_exists = target.is_file()
        if not path_exists:
            print(f"{filepath} points to {target}, which does not exist.")
            retcode = 1

    return retcode


def main():
    filenames = sys.argv[1:]

    retcode = 0
    for filename in filenames:
        retcode |= check_links(filename)

    return retcode


if __name__ == "__main__":
    exit(main())
