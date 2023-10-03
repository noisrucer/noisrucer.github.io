import re
import os

list_files = os.listdir()

for fname in list_files:
    if not fname.endswith('.md') or not fname.startswith('2022-02-20'):
        continue
    contents = ""
    print(fname)

    with open(fname, 'r') as f:

        while True:
            line = f.readline()

            if not line:
                break
            # x = re.search("$.*$", line)
            # if x:
            #     o = re.sub("$ ","$$", x.string, 1)
            #     o = re.sub(" $","$$", o, 1)
            #     line = o

            y1 = re.search('../../assets/img/', line)
            if y1:
                o = re.sub('../../assets/img/', '/assets/img/', y1.string, 1)
                line = o
            y2 = re.search('../../assets/img/', line)
            if y2:
                o = re.sub('../../assets/img/', '/assets/img/', y2.string, 1)
                line = o

            contents += line

    with open(fname, 'w') as f:
        f.write(contents)
