import json

# get auto-generated id from .guides_tmp
with open(".guides_tmp/metadata.json") as f:
  sections = json.load(f)["sections"]
  # assert len(sections) == 1
  id = sections[0]["id"]

# update guides to have the id
with open(".guides/metadata.json", "r") as f:
  metadata = json.load(f)
  metadata["sections"][0]["id"] = id

with open(".guides/metadata.json", "w") as f:
  json.dump(metadata, f, indent=2)

with open(".guides/book.json", "r") as f:
  book = json.load(f)
  book["children"][0]["id"] = id
  book["children"][0]["pageId"] = id

with open(".guides/book.json", "w") as f:
  json.dump(book, f, indent=2)

