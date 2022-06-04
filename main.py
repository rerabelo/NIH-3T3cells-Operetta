import os
from cells import parseFile

if __name__ == "__main__":

  files = []
  groups = os.listdir('images/')
  for group in groups:
    try:
      for file in os.listdir('images/' + group):
        if file.endswith(".tif"):
          files.append('images/' + group + '/' + file)
    except NotADirectoryError:
      continue

  for idx, file in enumerate(files):
    # os.system("python cells.py " + file + " test")
    print("{}/{}: {}".format(idx + 1, len(files), file))
    parseFile(file, "prefix")
