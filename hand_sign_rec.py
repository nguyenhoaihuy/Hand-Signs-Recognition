import os
import zipfile
import random
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile
from os import getcwd

import cv2
import time
import os
from tensorflow.keras.preprocessing import image
class TakeImage:
    def __init__(self, directory, side, num_img, duration=2):
        self.directory = directory              # folder name
        self.side = side                        # side of the image sidexside
        if not os.path.isdir(directory):        # check if the directory exits or not
            os.mkdir(directory)                 # if not, create one    
        self.count = len(os.listdir(directory)) # number of images currently in the directory
        self.number = num_img                   # number of images need to take
        self.duration = duration                # time between images
        self.checkpoint_path = "training_1/cp.ckpt"
        self.model = tf.keras.models.Sequential([
        # YOUR CODE HERE
            tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(300, 300, 3)),
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2,2), 
            tf.keras.layers.Conv2D(32, (3,3), activation='relu'), 
            tf.keras.layers.MaxPooling2D(2,2),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'), 
            tf.keras.layers.MaxPooling2D(2,2),
            # Flatten the results to feed into a DNN
            tf.keras.layers.Flatten(), 
            # 512 neuron hidden layer
            tf.keras.layers.Dense(512, activation='relu'), 
            # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class ('cats') and 1 for the other ('dogs')
            tf.keras.layers.Dense(5, activation='softmax')
        ])
        self.model.compile(optimizer="rmsprop", loss='categorical_crossentropy', metrics=['acc'])
        self.model.load_weights(self.checkpoint_path)

    def take(self):
        # create Video Capture
        key = cv2.waitKey(1)
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        start = time.time()
        pause = False
        result = 0
        while True:
            try:
                # get a frame from camera
                check, frame = camera.read()
                # draw a cropped rectangle
                start_x, start_y, end_x, end_y = self.getRectanglePoints(
                    camera.get(cv2.CAP_PROP_FRAME_WIDTH),
                    camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
                # -2 because we don't want to get the border of the rectangle in images
                cv2.rectangle(frame, (start_x-2, start_y-2), (end_x, end_y),(0,255,0), 1)

                if not pause:
                # add timer
                    timer = self.timer(start)

                cv2.putText(frame, str(result),(10, 105),cv2.FONT_HERSHEY_SIMPLEX,2,(225,255,255),3)

                # show frame
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)

                # exit if the folder have all image or user hit the s key
                if self.count == self.number or key == ord('s'): 
                    camera.release()  
                    print("You have taken "+str(self.count)+" images "+" in "+self.directory)
                    break

                if key == ord('p'):
                    pause = True


                if key == ord('c'):
                    start = time.time()
                    pause = False

                # save image
                if timer == 0 and not pause:
                    #crop the frame
                    crop = frame[start_y:start_y+self.side,start_x:start_x+self.side]

                    # save image
                    image_name = self.getNextName()
                    path='test/all/test.jpg'
                    if cv2.imwrite(filename=path, img=crop):
                        print(path+" is saved in "+self.directory)
                    else:
                        print("Fail to save "+image_name)

                    test_datagen = ImageDataGenerator(rescale=1./255)
                    pred_dir='test'
                    test_generator = test_datagen.flow_from_directory(
                        directory=pred_dir,
                        target_size=(300, 300),
                        color_mode="rgb",
                        batch_size=20,
                        class_mode='categorical',
                        shuffle=False
                    )
                    test_generator.reset()

                    pred=self.model.predict_generator(test_generator, steps=len(test_generator), verbose=1)
                    print(pred[0])
                    result = findMax(pred[0])
#                     if findMax(pred[0]) == 'zero':
#                         result = 0
#                     if findMax(pred[0]) == 'one':
#                         result = 1
#                     if findMax(pred[0]) == 'two':
#                         result = 2
                    
                    #os.remove(path)
                    self.count += 1
                    start = time.time()

            except(KeyboardInterrupt):
                print("Turning off camera.")
                camera.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

    def getRectanglePoints(self, width, height):
        # initialize start point and end point
        start_x = start_y = 0
        end_x = end_y = 0
        # 
        start_x = int(width/2 - self.side/2)
        start_y = int(height/2 - self.side/2)
        end_x = int(width/2 + self.side/2)
        end_y = int(height/2 + self.side/2)
        return start_x, start_y, end_x, end_y

    def timer(self, start):
        end = time.time()
        return int(self.duration - end + start)+1

    def getNextName(self):
        name = ""
        images = os.listdir(self.directory)
        if len(images) == 0:
            name = self.directory+"-"+str(0)+".jpg"
        else:
            num = len(images)
            name = self.directory+"-"+str(num)+".jpg"
        return name

def findMax(list):
    result = 0
    id_result = 0
    for i in range(len(list)):
        if list[i] > result:
            result = list[i]
            id_result = i
    
    return os.listdir(TRAINING_DIR)[id_result]




TRAINING_DIR = "data/training"
VALIDATION_DIR = "data/validation"
# train_datagen = ImageDataGenerator( 
#     rescale = 1.0/255,
#     rotation_range=40,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest'
# )
# test_datagen = ImageDataGenerator(rescale=1./255)

# train_generator = train_datagen.flow_from_directory(TRAINING_DIR,
#                                                     batch_size=20,
#                                                     class_mode='categorical',
#                                                     target_size=(300, 300))
# validation_generator = test_datagen.flow_from_directory(
#         VALIDATION_DIR,
#         target_size=(300, 300),
#         batch_size=20,
#         class_mode='categorical')

test = TakeImage("test", 300, 100,1)
test.take()