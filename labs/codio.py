import sys
import json
import glob

lab_name = sys.argv[1]

# get auto-generated id from .guides_tmp
filename = glob.glob(".guides_tmp/content/Page-1*.json")[0]

#need to first get the filename since now has randomness on it.
with open(filename) as f:
  id = json.load(f)["id"]

# update guides content to have the id
with open(".guides/content/Using-Jupyter-Notebooks.json", "r") as f:
  metadata = json.load(f)
  metadata["id"] = id
  metadata["files"][0]["path"] = "{lab_name}_lab.ipynb".format(lab_name = lab_name)

with open(".guides/content/Using-Jupyter-Notebooks.json", "w") as f:
  json.dump(metadata, f, indent=2)

with open(".guides/content/index.json", "r") as f:
  index = json.load(f)
  index["title"] = lab_name

with open(".guides/content/index.json", "w") as f:
  json.dump(index, f, indent=2)

