#!/bin/bash

if [[ $# -le 1 ]]; then
    echo "Usage: $0 file1.sf file2.sf ...";
    exit 1;
fi

while [[ $# > 0 ]]; do
    FILE_NAME="$1"
    if ! [[ ${FILE_NAME} =~ ".sf" ]]; then
        echo "${FILE_NAME} is not ends with \".sf\"";
        exit 1;
    fi

    COMBINED_FILE="${FILE_NAME/%.sf/}.sfc"

    python include.py --output "$COMBINED_FILE" "$FILE_NAME"

    if [[ $? != "0" ]]; then
        exit $?;
    fi

    f2j -r "$COMBINED_FILE"

    if [[ $? != "0" ]]; then
        exit $?;
    fi

    rm "$COMBINED_FILE"

    shift
done
