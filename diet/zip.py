from zipfile import ZipFile
import os
import glob

def write_dir(zipObj, path):
    '''Write everything in the directory path to the zip object.'''
    for file in [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0],'*'))]:
        zipObj.write(file)

# Lab
with ZipFile('diet_lab.zip', 'w') as zipObj:
    zipObj.write('diet_lab.ipynb')
    write_dir(zipObj, 'data')
    zipObj.close()