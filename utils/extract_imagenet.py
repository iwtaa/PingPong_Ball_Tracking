from datasets import load_dataset
from PIL import Image
import threading
import numpy as np
import queue
import math

num_thread = 5
size_thread = 1000
dataset = load_dataset('imagenet-1k', split='train')

def process(data, thread):
    size = len(data['image'])
    for i in range(size):
        if data['label'][i] == 722:
            print("found")
            data['image'][i].save("./ImageNet/pingpongball_image_" + str(thread * size_thread + i) + ".jpg")


data = dataset.iter(size_thread)
threads = queue.Queue()

for i in range(math.ceil(dataset.num_rows / size_thread)):
    print(str(i*size_thread) + "/" + str(dataset.num_rows))
    batch = data.__next__()
    thread = threading.Thread(target=process, args=(batch, i,))
    thread.start()
    threads.put(thread)

    if i < num_thread:
        continue
    threads.get().join()

while not threads.empty():
    threads.get().join()
