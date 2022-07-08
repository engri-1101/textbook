import sys
import json

lab_name = sys.argv[0]

# get auto-generated id from .guides_tmp
with open(".guides_tmp/metadata.json") as f:
  sections = json.load(f)["sections"]
  id = sections[0]["id"]

# update guides to have the id
with open(".guides/metadata.json", "r") as f:
  metadata = json.load(f)
  metadata["sections"][0]["id"] = id
  metadata["sections"][0]["files"]["path"] = f"{lab_name}_key.ipynb"

with open(".guides/metadata.json", "w") as f:
  json.dump(metadata, f, indent=2)

with open(".guides/book.json", "r") as f:
  book = json.load(f)
  book["children"][0]["id"] = id
  book["children"][0]["pageId"] = id
  book["name"] = lab_name

with open(".guides/book.json", "w") as f:
  json.dump(book, f, indent=2)

