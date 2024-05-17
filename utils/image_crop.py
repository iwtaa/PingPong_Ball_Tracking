import cv2

image = r"pingpongball_image_62279"
image_folder_path = r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\utils\ImageNet"
label_folder_path = r"asdfg"
size_end = (640, 640)

img = cv2.imread(image_folder_path + "\\" + image + '.jpg')
size_orig = img.shape

print(size_end, size_orig)
if size_orig[0] < size_end[0] or size_orig[1] < size_end[1]:
    print("cannot crop an image smaller than the crop region")
    exit(0)

labels = label_folder_path + '\\' + image + '.txt'
label = labels.readlines()[0]
x, y, w, h, _ = label
x = x * size_orig[0]
y = y * size_orig[1]

if x - int(size_end/2) < 0:
    x += abs(x - int(size_end)/2)
if size_orig[0] - x > size_end[0]:
    x -= size_end[0] - abs(size_orig[0] - x)
if y - int(size_end[1] / 2) < 0:
    y += abs(y - int(size_end[1]) / 2)
if size_orig[1] - y > size_end[1]:
    y -= size_end[1] - abs(size_orig[1] - y)

cv2.imshow(img)