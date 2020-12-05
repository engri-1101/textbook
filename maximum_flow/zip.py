from zipfile import ZipFile
import os
import glob

def write_dir(zipObj, path):
    '''Write everything in the directory path to the zip object.'''
    for file in [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0],'*'))]:
        zipObj.write(file)


# Lab
with ZipFile('max_flow_lab.zip', 'w') as zipObj:
    zipObj.write('max_flow_lab.ipynb')
    write_dir(zipObj, 'images-lab')
    zipObj.close()
    
# Lab - Colab
with ZipFile('max_flow_lab_colab.zip', 'w') as zipObj:
    zipObj.write('max_flow_lab.ipynb')
    write_dir(zipObj, 'images-lab')
    zipObj.close()
    
# Lab (3-4)
with ZipFile('max_flow_lab_part3-4.zip', 'w') as zipObj:
    zipObj.write('max_flow_lab_part3-4.ipynb')
    write_dir(zipObj, 'images-lab')
    write_dir(zipObj, 'images-key')
    zipObj.close()
    
# Lab (3-4) - Colab
with ZipFile('max_flow_lab_part3-4_colab.zip', 'w') as zipObj:
    zipObj.write('max_flow_lab_part3-4_colab.ipynb')
    write_dir(zipObj, 'images-lab')
    write_dir(zipObj, 'images-key')
    zipObj.close()