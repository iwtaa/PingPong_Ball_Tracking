# Ping Pong ball Detection
This contains code for training, tuning and using a YOLOv8 detection model for tennis table balls. Aswell as a prototype GUI for the whole process.

### Content list
- Compressed dataset, extracted, cropped, augmented (motionblur) from the ImageNet1k dataset
- The scripts for the whole creation of the dataset
- yolov_tune, for tuning the hyperparameters provided to the training afterward
- yolov_train, for training a model on the dataset
- yolov_image, for using the model on an image
- yolov_video, for using the model on a video

## Dependencies
- Numpy
- scikit_image
- opencv-python
- ultralytics
- MatPlotLib