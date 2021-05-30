#!/usr/bin/env bash

# Each parameter is a filename passed in by pre-commit.
for file in "${@}"; do
    # Only evaluate md files.
    if [[ "${file}" != *.md ]]; then
        continue
    fi

    # Convert tabs to two spaces.
    gsed -i 's/\t/  /g' "${file}"

    # Remove non-printable characters.
    gsed -i 's/[^[:print:]]//g' "${file}"
done
