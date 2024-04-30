import shutil
import os
import cv2

data_folder = "D:\\Dataset\\Blender_output3"
training_folder = ""
validation_folder = ""
tests_folder = ""


sequences = os.listdir(data_folder)
for sequence in sequences:
    print(sequence)
    files = os.listdir(data_folder + '\\' + sequence)
    positions_file = open(data_folder + '\\' + sequence + "\\pos32.txt")
    size_file = open(data_folder + '\\' + sequence + "\\size.txt")
    positions = positions_file.readlines()
    sizes = size_file.readlines()

    for file in files:
        if file[-4:] != ".png":
            continue
        img = cv2.imread(data_folder + '\\' + sequence + '\\' + file)
        index = int(file[:-4]) - 1
        position = positions[index].rstrip().split(" ")
        size = float(sizes[index].rstrip())
        w = size*2 / img.shape[1]
        h = size*2 / img.shape[0]
        x = float(position[0])
        y = (1.0 - float(position[1]))

        end_file = open(data_folder + '\\yolov8\\labels\\' + sequence + '_' + str(file[:-4]) + '.txt', 'w')
        end_file.write("0 " + str(x) + " " + str(y) + " " + str(w) + " " + str(h))

        shutil.copyfile(data_folder + "\\" + sequence + "\\" + file, data_folder + '\\yolov8\\images\\' + sequence + '_' + str(file[:-4]) + '.png')