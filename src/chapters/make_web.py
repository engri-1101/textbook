import argparse
import nbformat

def main(notebooks):
    """Remove non-web components from the given notebooks."""
    nb_list = notebooks.split(",")
    nb_list = [t + "_master.ipynb" for t in nb_list]
    n = len(nb_list)
    if n == 0:
        raise Exception("No notebooks selected")
    read = []

    # Read the notebooks
    for i in range(n):
        read.append(nbformat.read(nb_list[i], 4))

    # Find and remove cells with tag 'non-web'
    for i in range(n):
        nb = read[i]
        indices_to_pop = []
        for j, c in enumerate(nb.cells):
            cell_tags = c.metadata.get('tags')
            if cell_tags:
                if 'non-web' in cell_tags:
                    indices_to_pop.append(j)
        indices_to_pop.reverse()
        for j in indices_to_pop:
            nb.cells.pop(j)
        
        # Save the new notebook
        name = nb_list[i].replace("_master", "_web")
        nbformat.write(nb, name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help="comma-delimited string of Jupyter Notebooks (without _master.ipynb)")
    args = parser.parse_args()
    main(args.list)