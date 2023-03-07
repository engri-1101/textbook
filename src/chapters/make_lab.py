import re
import argparse
import nbformat
import numpy as np
import json

# TODO: Add helpful warnings (e.g. questions with no number)

TEXT_START = "<font color=('|\")(red|blue)('|\")>"
# TODO: Change this implementation
# This implementation prevents using other colors.
# The font tag is also not supported by GitHub.
TEXT_END = "</font>"
CODE_ANSWER_START = "### BEGIN SOLUTION"
CODE_ANSWER_END = "### END SOLUTION"


def delete_pairs(string, start_match, end_match):
    """Return index pairs of sections to delete from the string."""
    starts = [(m.start()) for m in re.finditer(start_match, string)]
    ends = [(m.end()) for m in re.finditer(end_match, string)]
    if len(starts) != len(ends):
        raise ValueError("Mismatch between openings and closings")
    return list(zip(starts, ends))


def delete(string, index_pairs):
    """Return string with substrings specified from index_pairs removed."""
    index_pairs = np.array(index_pairs)
    for r in range(len(index_pairs)):
        i,j = index_pairs[r]
        string = string[:i] + string[j:]
        index_pairs = index_pairs - (j-i)
    return string

def remove_cell(nb_string):
    """Return notebook with cells tagged 'key-only' removed."""
    nb = nbformat.read(nb_string, 4)

    # Find and remove cells with tag 'key-only'
    indices_to_pop = []
    for i, c in enumerate(nb.cells):
        cell_tags = c.metadata.get('tags')
        if cell_tags:
            if 'key-only' in cell_tags:
                indices_to_pop.append(i)
    indices_to_pop.reverse()
    for i in indices_to_pop:
        nb.cells.pop(i)

    # Save the new notebook
    nbformat.write(nb, nb_string)


def main(key):
    """Make a student version of the given lab key in the same directory."""
    with open(key, "r", encoding="utf-8") as f:
        nb = json.load(f)
        for cell in nb["cells"]:
            source = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                index_pairs = delete_pairs(source, TEXT_START, TEXT_END)
            if cell["cell_type"] == "code":
                index_pairs = delete_pairs(source, CODE_ANSWER_START, CODE_ANSWER_END)
            source = delete(source, index_pairs)
            cell["source"] = [line + "\n" for line in source.split("\n")]
            # delete last line break after last line
            cell["source"][-1] = cell["source"][-1][:-1]

    student = key.replace("_key", "")
    with open(student, "w") as f:
        json.dump(nb, f)

    remove_cell(student)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help="Jupyter Notebook key file")
    args = parser.parse_args()
    main(args.key)
