import cv2 
import time
import os

class TakeImage:
    def __init__(self, directory, classname, side, num_img, duration=3):
        self.directory = directory              # folder name 
        self.classname = classname              # class name
        self.side = side                        # side of the image sidexside
        if not os.path.isdir(str(directory)+classname):        # check if the directory exits or not
            os.mkdir(str(directory)+classname)                 # if not, create one    
        self.count = len(os.listdir(directory+classname)) # number of images currently in the directory
        self.number = num_img                   # number of images need to take
        self.duration = duration                # time between images

    def take(self):
        # create Video Capture
        key = cv2.waitKey(1)
        camera = cv2.VideoCapture(0)
        start = time.time()
        pause = False
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
                    cv2.putText(frame, str(timer),(105, 105),cv2.FONT_HERSHEY_SIMPLEX,2,(225,0,0),3)
                else:
                    cv2.putText(frame, 'P',(105, 105),cv2.FONT_HERSHEY_SIMPLEX,2,(225,0,0),3)

                # show frame
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)

                # exit if the folder have all image or user hit the s key
                if self.count == self.number or key == ord('s'): 
                    camera.release()  
                    print("You have taken "+str(self.count)+" images "+" in "+self.classname)
                    break

                if key == ord('p'):
                    pause = True


                if key == ord('c'):
                    start = time.time()
                    pause = False

                # save image
                if time.time()-start > self.duration and not pause:
                    #crop the frame
                    crop = frame[start_y:start_y+self.side,start_x:start_x+self.side]

                    # save image
                    image_name = self.getNextName()
                    if cv2.imwrite(filename=self.directory+self.classname+'/'+image_name, img=crop):
                        print(image_name+" is saved in "+self.directory+self.classname)
                    else:
                        print("Fail to save "+image_name)

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
        images = os.listdir(self.directory+self.classname)
        if len(images) == 0:
            name = self.classname+"-"+str(0)+".jpg"
        else:
            num = len(images)
            name = self.classname+"-"+str(num)+".jpg"
        return name

