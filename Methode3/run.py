import cv2
import numpy as np
import sys
import argparse
import queue
from scipy import signal
from skimage.measure import label, regionprops
from ultralytics import YOLO
import math

sys.path.insert(0, '../External Repositories/deblatting_python')
from deblatting import estimateFMH


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default=r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video\CoreView_178_Core2 05004035 3-4.mp4", required=False)
    parser.add_argument("--buffer", default=9, required=False)
    return parser.parse_args()


def main():
    args = parse_args()
    cap = cv2.VideoCapture(args.video)
    if cap is None:
        print("Video is unreachable. Make sure to enter a valid path.")
        exit(0)

    model = YOLO('yolov8n.pt')

    ret, img = cap.read()
    img_buffer = queue.Queue()
    background = np.zeros(np.shape(img))
    masks = np.empty((args.buffer, img.shape[0], img.shape[1]))
    counter = 0
    positions = []
    while ret:

        background += (img / args.buffer)
        img_buffer.put(img)

        masks[:-1] = masks[1:]
        masks[-1] = maskPersons(img, model)
        if counter >= args.buffer:
            mask = concatenateMasks(masks)
            background -= img_buffer.get() / args.buffer
            new_pos = estimateBlurredObjectPosition(img, background, mask=mask)
            if new_pos is not None:
                positions.append([counter, new_pos])

            for index, item in enumerate(positions):
                if index == len(positions) - 1:
                     break
                if positions[index + 1][0] - item[0] < 5:
                    cv2.line(img, item[1], positions[index + 1][1], [0, 255, 0], 1)

            img = cv2.bitwise_and(img, img, mask=mask.astype(np.uint8) * 255)
            cv2.imshow("test", img)
            if cv2.waitKey(10) == 27:
                break

        ret, img = cap.read()
        counter += 1


def fmo_detect_range(I, B, minarea=0.1, maxarea=50):
    ## simulate FMO detector -> find approximate location of FMO
    dI = (np.sum(np.abs(I - B), 2) > 0.1).astype(float)
    labeled = label(dI)
    regions = regionprops(labeled)
    ind = -1
    maxsol = 0.85
    for ki in range(len(regions)):
        x1, y1, x2, y2 = regions[ki].bbox
        '''and regions[ki].bbox[2] -  and regions[ki].bbox'''
        if minarea < regions[ki].area < 0.01 * np.prod(dI.shape) and regions[ki].area < maxarea and x2 - x1 > 1 and y2 - y1 > 1:
            if regions[ki].solidity > maxsol:
                ind = ki
                maxsol = regions[ki].solidity
    if ind == -1:
        raise UnvalidTargetError("The target is not valid.")
    print(regions[ind].bbox, regions[ind].area, regions[ind].solidity)
    return regions[ind].bbox, regions[ind].minor_axis_length


def concatenateMasks(masks):
    mask = np.ones(masks[0].shape)
    for i in range(masks.shape[0]):
        mask = (mask == True) & (masks[i] == True)
    return mask


# Temporary detection method
def maskPersons(I, model):
    names = model.names
    objects = model.predict(I, imgsz=640, conf=0.3)
    mask = np.ones(I.shape[:2]).astype(bool)
    for obj in objects:
        for i, box in enumerate(obj.boxes.xywh):
            x, y, w, h = np.array(box.tolist()).astype(int)
            w = min(w, I.shape[1] - x)
            h = min(h, I.shape[0] - y)
            label = names[int(obj.boxes.cls[i])]
            print(label, x, y, w, h)
            mask[int(y - (h / 2)):int(y + (h / 2)), int(x - (w / 2)):int(x + (w / 2))] = np.zeros((h, w))
    return mask


class UnvalidTargetError(Exception):
    pass


# Get the largest ROI.
# TODO For deblurring everything, output all ROIs
def detectROI(I, B, mask=None):
    if mask is not None:
        I = cv2.bitwise_and(I, I, mask=mask.astype(np.uint8) * 255)
        B = cv2.bitwise_and(B, B, mask=mask.astype(np.uint8) * 255)
    I = I / 255
    B = B / 255
    try:
        bbox, diameter = fmo_detect_range(I, B, 100, 300)
    except UnvalidTargetError:
        raise UnvalidTargetError("The target is not valid.")

    if bbox == None:
        raise UnvalidTargetError("The target is not valid.")
    ext = int(np.round(0.5 * diameter))

    # [x1, y1, x2, y2]
    ROI = [bbox[0] - ext, bbox[1] - ext, bbox[2] + ext, bbox[3] + ext]
    return ROI, diameter


def estimateMaskTrajectory(I, B, ROI, diameter):
    I = I[ROI[0]:ROI[2], ROI[1]:ROI[3], :] / 255
    B = B[ROI[0]:ROI[2], ROI[1]:ROI[3], :] / 255

    if 0 in I.shape:
        raise UnvalidTargetError("The target is not valid.")
    M0 = np.ones([int(np.round(diameter))] * 2)
    H, F, M = estimateFMH(I, B, M0)
    H = np.where(H == 0., H, 1.0)
    return H.astype(np.uint8)


def getMaskCenter(H):
    framePositions = np.argwhere(H == 1)
    return (int(np.sum(framePositions[:, 1]) / framePositions.shape[0]),
            int(np.sum(framePositions[:, 0]) / framePositions.shape[0]))


def estimateBlurredObjectPosition(I, B, mask=None):
    try:
        ROI, diameter = detectROI(I, B, mask=mask)
        mask = estimateMaskTrajectory(I, B, ROI, diameter)
    except UnvalidTargetError:
        return None
    return [sum(x) for x in zip(getMaskCenter(mask), (ROI[1], ROI[0]))]


if __name__ == "__main__":
    main()
