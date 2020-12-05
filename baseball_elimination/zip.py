from zipfile import ZipFile
import os
import glob

def write_dir(zipObj, path):
    '''Write everything in the directory path to the zip object.'''
    for file in [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0],'*'))]:
        zipObj.write(file)


# Lab
with ZipFile('baseball_elimination_lab.zip', 'w') as zipObj:
    zipObj.write('baseball_elimination_lab.ipynb')
    write_dir(zipObj, 'data')
    zipObj.write('max_flow.py')
    zipObj.close()
    
# Lab - Colab
with ZipFile('baseball_elimination_lab_colab.zip', 'w') as zipObj:
    zipObj.write('baseball_elimination_lab_colab.ipynb')
    write_dir(zipObj, 'data')
    zipObj.write('max_flow.py')
    zipObj.close()