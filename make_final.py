import os
from all_contours import make_contours

path = "path-to-folder/PEB/"

for dir in ['0001-1000', '1001-2000', '2001-2740']:
    now_dir = path + dir + "/"
    content = os.listdir(now_dir)
    for i in content:
        if i[-4:] == ".jpg":
            make_contours(now_dir, i)