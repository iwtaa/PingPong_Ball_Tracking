from motionblur import motion_blur
import cv2
import os
import random
import shutil

intensity_range = [(20, 36), (46, 80)]
orientation_range = (0, 180)

images_folder = r"C:\Users\invite\Downloads\imagenet-1k_tennis-table-ball.v6i.yolov8 - Copie (2)\test\images"
labels_folder = r"C:\Users\invite\Downloads\imagenet-1k_tennis-table-ball.v6i.yolov8 - Copie (2)\test\labels"

images = os.listdir(images_folder)
counter = 0
for image in images:
    counter += 1

    print(str(counter / len(images)) + "%")
    img = cv2.imread(images_folder + '\\' + image)

    for n in range(2):
        intensity = random.randint(intensity_range[n][0], intensity_range[n][1])
        if intensity % 2:
            intensity += 1
        orientation = random.randint(orientation_range[0], orientation_range[1])

        augmented_img = motion_blur(img, intensity, orientation)
        cv2.imwrite(images_folder + '\\blurred_' + str(n) + "_" + image, augmented_img)
        source_file = labels_folder + "\\" + image[:-4] + ".txt"
        destination_file = labels_folder + "\\blurred_" + str(n) + "_" + image[:-4] + ".txt"
        shutil.copy(source_file, destination_file)
