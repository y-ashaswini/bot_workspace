#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from std_msgs.msg import String
import matplotlib.pyplot as plt
from tensorflow import keras

model = keras.models.load_model("src/vision/Model")
cap = cv2.VideoCapture(0)

def array2dir(array):
    if array[0][0] > array[0][1] and array[0][0] > array[0][2]:
        print("Right")
    elif array[0][1] > array[0][0] and array[0][1] > array[0][2]:
        print("Left")
    elif array[0][2] > array[0][1] and array[0][2] > array[0][0]:
        print("Up")
    else:
        print("HATA!")


def talker():
    rospy.init_node('arrow', anonymous=True)

    while not rospy.is_shutdown():
        ret, img = cap.read()
        if not ret:
            break
    
        cv2.imshow('Camera', img)

        img = cv2.resize(img, (224, 224))

        img = np.asarray(img)
        plt.imshow(img)
        img = np.expand_dims(img, axis=0)
        output = model.predict(img)
        # print(output)
        array2dir(output)


        # press esc to exit
        key = cv2.waitKey(1)
        if (key == 27):
            break


        if rospy.is_shutdown():
            cap.release()
            cv2.destroyAllWindows()



if __name__ == "__main__":
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
