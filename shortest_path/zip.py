from zipfile import ZipFile
import os
import glob

def write_dir(zipObj, path):
    '''Write everything in the directory path to the zip object.'''
    for file in [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0],'*'))]:
        zipObj.write(file)


# Demo 
with ZipFile('shortest_path_demo.zip', 'w') as zipObj:
    zipObj.write('shortest_path_demo.ipynb')
    write_dir(zipObj, 'data')
    write_dir(zipObj, 'graph_tools.py')
    zipObj.close()
    
# Demo - Colab
with ZipFile('shortest_path_demo_colab.zip', 'w') as zipObj:
    zipObj.write('shortest_path_demo_colab.ipynb')
    write_dir(zipObj, 'data')
    write_dir(zipObj, 'graph_tools.py')
    zipObj.close()