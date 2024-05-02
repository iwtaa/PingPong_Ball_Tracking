import os

folder_path = "C:\\Users\\invite\\Downloads\\1.v2i.yolov8\\train"

files = os.listdir(folder_path + "\\labels")
for file in files:
    if file[-4:] != ".txt":
        continue

    lines = open(folder_path + "\\labels\\" + file).readlines()
    new_lines = []
    for line in lines:
        data = line.split(" ")
        if data[0] == '0':
            new_lines.append(line)
    new_file = open(folder_path + "\\new_labels\\" + file, 'w')
    new_file.writelines(new_lines)
