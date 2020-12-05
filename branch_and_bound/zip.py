from zipfile import ZipFile
import os
import glob

def write_dir(zipObj, path):
    '''Write everything in the directory path to the zip object.'''
    for file in [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0],'*'))]:
        zipObj.write(file)


# Lab
with ZipFile('branch_and_bound_lab.zip', 'w') as zipObj:
    zipObj.write('branch_and_bound_lab.ipynb')
    write_dir(zipObj, 'images-lab')
    write_dir(zipObj, 'data')
    zipObj.close()
    
# Demo - Branch and Bound
with ZipFile('branch_and_bound_demo.zip', 'w') as zipObj:
    zipObj.write('branch_and_bound_demo.ipynb')
    write_dir(zipObj, 'images-demo')
    zipObj.close()
    
# Demo - Bin Packing
with ZipFile('bin_packing_demo.zip', 'w') as zipObj:
    zipObj.write('bin_packing_demo.ipynb')
    write_dir(zipObj, 'data-bin_packing')
    zipObj.close()