from os import walk
import re
import numpy as np

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
         
# temporarily done manually
keys = ['./baseball_elimination/baseball_elimination_lab_key.ipynb',
        './lp_formulation/lp_formulation_lab_key.ipynb',
        './transportation/transportation_lab_key.ipynb',
        './first_year_writing_seminar/fws_lab_key.ipynb',
        './simplex/simplex_lab_key.ipynb',
        './tsp_integer_programming/tsp_integer_programming_lab_key.ipynb',
        './seat_packing/seat_packing_lab_key.ipynb',
        './branch_and_bound/branch_and_bound_lab_key.ipynb',
        './diet/diet_lab_key.ipynb',
        './game_theory/game_theory_lab_key.ipynb']


# starting with just lp formulation key
for key in keys:
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
#         print(k,file_text[i:j])
        file_text = file_text[:i] + file_text[j:]
        to_remove = to_remove - (j-i) # adjust other indices

    file.close()
    
    student_file = key.replace('_key', '')
    file = open(student_file, "w")
    file.write(file_text)
    file.close()