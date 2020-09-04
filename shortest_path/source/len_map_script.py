string = """

v910 , v34 , v45 , v56 , v67 , v78 , v144 , v913 , v1314 , v79 , v89 , v146 , v145 , v137 , v143 , v214 , v1213 , v114 , v111 , v1112 , v112 , v12 , v212 , v23 , v123 , v1012 , v1011

"""

objects = string.split(",")
str_new = ""
for obj in objects:
    i = obj.strip()
    i_new = i
    new_obj = i+"txt,"
    str_new = str_new + new_obj
print("["+ str_new)


