import argparse
import nbformat

def concatenate(notebooks):
    """Concatenate the given notebooks in order."""
    nb_list = notebooks.split(",")
    nb_list = [t + "_master.ipynb" for t in nb_list]
    n = len(nb_list)
    if n == 0:
        raise Exception("No notebooks selected")
    read = []

    # Read the notebooks
    for i in range(n):
        read.append(nbformat.read(nb_list[i], 4))

    # Create a new notebook
    final_notebook = nbformat.v4.new_notebook(metadata=read[0].metadata)

    # Concatenate the notebooks
    final_notebook.cells = read[0].cells
    for i in range(1, n):
        final_notebook.cells += read[i].cells

    # Return the new notebook
    return final_notebook


def main(nb_string, name):
    """Remove web components from concatenated notebook."""
    nb = concatenate(nb_string)

    # Find and remove cells with tag 'web-only'
    for i, c in enumerate(nb.cells):
        cell_tags = c.metadata.get('tags')
        if cell_tags:
            if 'web-only' in cell_tags:
                nb.cells.pop(i)

    # Save the new notebook
    nbformat.write(nb, name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help="comma-delimited string of Jupyter Notebooks (without _master.ipynb)")
    parser.add_argument('-n', '--name', help="name of new Jupyter Notebook")
    args = parser.parse_args()
    main(args.list, args.name)