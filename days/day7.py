from utils import Clock, read_data
from pprint import pprint
import xml.etree.ElementTree as ET


clock = Clock()
clock.tic()

data = read_data()

root = ET.Element("root")
curr_dir = root
ET.SubElement(root, "dir", {"name": "/"})
parent_map = {} # unbelievable

for datum in data:
    match datum.split():
        case "$", "cd", "..":
            curr_dir = parent_map[curr_dir]
        case "$", "cd", dir_name:
            subdirs = curr_dir.findall("dir")
            for subdir in subdirs:
                if subdir.get("name") == dir_name: dest_dir = subdir
            curr_dir = dest_dir
        case "$", "ls":
            pass
        case "dir", dir_name:
            dir = ET.SubElement(curr_dir, "dir", {"name": dir_name})
            parent_map[dir] = curr_dir # unbelievable
        case size, filename:
            file = ET.SubElement(curr_dir, "file", {"size": size, "name": filename})

def set_dir_size(dir):
    size = 0
    for file in dir.iter("file"):
        size += int(file.get("size"))
    dir.set("size", str(size))

for dir in root.iter("dir"):
    set_dir_size(dir)

silver = 0
for dir in root.iter("dir"):
    dir_size = int(dir.get("size"))
    if dir_size <= 100000:
        silver += dir_size
    
clock.toc(f"Silver {silver}")
clock.tic()

memory_need = 30000000 - (70000000 - int(root[0].get("size")))
deletables = [dir for dir in root.iter("dir") if int(dir.get("size")) >= memory_need]
sizes = sorted([int(deletable.get("size")) for deletable in deletables])
gold = str(sizes[0])

clock.toc(f"Gold {gold}")
