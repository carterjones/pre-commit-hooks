#!/usr/bin/env python

from os import listdir
from os.path import isfile, join

import frontmatter


class KnowledgeLabEntry(object):
    def __init__(self, filename):
        self.filename = filename
        fm = frontmatter.load(filename)
        self.content = fm.content
        self.index_headers = {}
        self.metadata = {}
        for m_key, m_item in fm.metadata.items():
            if m_key.startswith("_"):
                self.index_headers[m_key[1:]] = m_item
            else:
                self.metadata[m_key] = m_item


def generate_filenames():
    return [f for f in listdir(".") if isfile(join(".", f))]


def to_kl_entries(filenames):
    for filename in filenames:
        if filename.startswith("_") or filename.startswith("."):
            continue
        yield KnowledgeLabEntry(filename)


def to_link(filename):
    return f"[{filename}]({filename})"


def to_index_table_structure(kl_entries):
    index_headers = {}
    entries = list(kl_entries)
    entries.sort(key=lambda x: x.filename)
    for kl_entry in entries:
        for index_header in kl_entry.index_headers:
            index_headers[index_header] = True

    column_names = ["filename"]
    column_names.extend(list(index_headers.keys()))
    rows = [column_names]
    for kle in entries:
        row = [to_link(kle.filename)]
        for column_name in column_names:
            if column_name == "filename":
                continue
            row.append(str(kle.index_headers.get(column_name, "")))
        rows.append(row)

    return rows


def to_md_table(table):
    md_table = ""
    for i in range(len(table)):
        row = table[i]
        md_row = "|" + "|".join(row) + "|\n"
        if i == 1:
            num_columns = len(row)
            md_table += "|-" * num_columns + "|\n"
        md_table += md_row

    return md_table


def to_current_filenames_md_list(kl_entries):
    current_entries = []
    for entry in kl_entries:
        if entry.index_headers.get("current", False):
            current_entries.append(entry)
    current_entries.sort(key=lambda x: x.filename)

    md_list = "# Current entries\n"
    for entry in current_entries:
        md_list += "- " + to_link(entry.filename) + "\n"

    return md_list


def main():
    filenames = generate_filenames()
    kles = list(to_kl_entries(filenames))
    table = to_index_table_structure(kles)
    md_table = to_md_table(table)
    md_current_list = to_current_filenames_md_list(kles)

    with open("_index.md", "w") as fw:
        fw.write(md_current_list)
        fw.write("# All entries\n")
        fw.write(md_table)


if __name__ == "__main__":
    main()
