import kornia
import argparse
import cv2
import torch
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default=r"C:\Users\invite\PycharmProjects\PingPong_Ball_Tracking\footage_video\CoreView_178_Core2 05004035 3-4.mp4", required=False)
    parser.add_argument("--buffer", default=10, required=False)
    return parser.parse_args()


def main():
    args = parse_args()
    cap = cv2.VideoCapture(args.video)
    if cap is None:
        print("Video is unreachable. Make sure to enter a valid path.")
        exit(0)

    ret, img = cap.read()
    imgcopy = img
    for i in range(10):
        cap.read()
    ret, background = cap.read()
    img = img.transpose(2, 0, 1)
    background = background.transpose(2, 0, 1)
    end_image = np.array(img.tolist() + background.tolist())
    end_tensor = torch.tensor(np.array([end_image])) / 255
    DeFMO = kornia.feature.DeFMO()
    tsr = DeFMO(end_tensor)
    DeFMO.forward()
    for sub_image in tsr:
        for image in sub_image:
            image_rgb = image.detach().numpy()[:3]
            image_rgb = image_rgb.transpose(1, 2, 0) * 255
            image_rgb = image_rgb.astype(np.uint8)
            mask = image.detach().numpy()[3:]
            mask = mask.transpose(1, 2, 0) * 255
            mask = mask.astype(np.uint8)
            while True:

                cv2.imshow("test result2", mask)
                cv2.imshow("test result3", image_rgb)
                cv2.imshow("test result4", imgcopy)
                if cv2.waitKey(10) == 27:
                    break
    print("main")


if __name__ == "__main__":
    main()
