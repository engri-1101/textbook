from zipfile import ZipFile
import os
import glob

def write_dir(zipObj, path):
    '''Write everything in the directory path to the zip object.'''
    for file in [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0],'*'))]:
        zipObj.write(file)


# Lab
with ZipFile('minimum_cut_lab.zip', 'w') as zipObj:
    zipObj.write('minimum_cut_lab.ipynb')
    zipObj.write('max_flow.py')
    zipObj.write('social_network.py')
    write_dir(zipObj, 'images-lab')
    write_dir(zipObj, 'images-key')
    write_dir(zipObj, 'data-lab')
    zipObj.close()
    
