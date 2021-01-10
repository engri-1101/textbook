from os import walk
import re
import numpy as np
import sys

def make_student_version(key):
    """Make a student version of the given lab key in the same directory."""
    file = open(key, "r")
    file_text = file.read()

    # find all code answers
    code_starts = [m.start() for m in re.finditer('### BEGIN SOLUTION', file_text)]
    code_ends = [m.end() for m in re.finditer('### END SOLUTION', file_text)]
    assert len(code_starts) == len(code_ends)
    code_answers = list(zip(code_starts, code_ends))

    # find all text answers (blue) and comments (red)
    comment_starts = [m.start() for m in re.finditer("<font color='red'>", file_text)]
    answer_starts = [m.start() for m in re.finditer("<font color='blue'>", file_text)]
    text_starts = comment_starts + answer_starts
    text_starts.sort()
    text_ends = [m.end() for m in re.finditer("</font>", file_text)]
    assert len(text_starts) == len(text_ends)
    text = list(zip(text_starts, text_ends))

    # remove answers and comment text
    to_remove = code_answers + text
    to_remove.sort()
    to_remove = np.array(to_remove)
    for r in range(len(to_remove)):
        i,j = to_remove[r]
        file_text = file_text[:i] + file_text[j:]
        to_remove = to_remove - (j-i) # adjust other indices

    file.close()
    
    student_file = key.replace('_key', '')
    file = open(student_file, "w")
    file.write(file_text)
    file.close()
    
args = sys.argv
assert len(args) == 2
key = args[1]
make_student_version(key)
    
# find all key files
# keys = []
# dirs = list(walk('.'))[0][1]
# for directory in dirs:
#     files = list(walk('./%s' % (directory)))[0][2]
#     for file in files:
#         file_split = file.split('.')
#         assert len(file_split) <= 2
#         if len(file_split) == 2 and file_split[1] == 'ipynb':
#             file_name = file_split[0]
#             if file_name.split('_')[-1] == 'key':
#                 keys.append('./%s/%s' % (directory, file))