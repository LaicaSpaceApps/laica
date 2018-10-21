#!/usr/bin/python3.5
import matplotlib as p
from scipy.io import wavfile
import numpy as np
import sys as s
import cv2 as cv

def get_message():
    if(len(s.argv)!=1):
        messageType = s.argv[1]
        if(len(s.argv) != 2):
            fileName = s.argv[2]
        else:
            fileName = "cam"
    else:
        print("Error! Give the file name")
        s.exit()
    return messageType,fileName

def print_image(img):
    cv.namedWindow('image')
    cv.imshow('image',img)
    cv.waitKey(300)
    cv.destroyWindow('image')

def get_frame(f):
    imgList = []
    count = 0
    ret = True
    cap = cv.VideoCapture(str(f))
    cv.namedWindow('image')

    while(cap.isOpened() and ret):
        ret, frame = cap.read()
        if(count!=60 and ret):
            count = 0
            imgList.append(frame)
            cv.imshow('image',frame)
        count+=1
        cv.waitKey(30)

    cap.release()
    cv.destroyAllWindows()

    if(len(imgList)!=0):
        return imgList
    else:
        print("Error!")
        s.exit()

def cam2dna():
    cap = cv.VideoCapture(0)
    cv.namedWindow('image')
    while(True):
        ret, frame = cap.read()
        cv.imshow('image',frame)
        height, width, channels = frame.shape
        #(thresh, frame) = cv.threshold(frame, 128, 255, cv.THRESH_BINARY)# | cv.THRESH_OTSU
        frame = np.array2string(frame, precision=2, separator='',suppress_small=True)
        message = ''.join(format(ord(x),'b') for x in frame)
        code_to_DNA(message,width)
        if cv.waitKey(100) & 0xFF == ord('q'):
            s.exit()
    cap.release()
    cv.destroyAllWindows()

def get_bit(t,f):
    if(t == "string"):
        message = ''.join(format(ord(x),'b') for x in f)
        size = len(message)

    elif(t == "image"):
        img = cv.imread(str(f))
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        height, width= img.shape
        size = width
        (thresh, img) = cv.threshold(img, 128, 255, cv.THRESH_BINARY)
        #print img.shape
        img = np.array2string(img, precision=2, separator='',suppress_small=False)
        message = ''.join(format(ord(x),'b') for x in img)
        #print len(message)
        #print_image(img)

    elif(t == "video"):
        imgList = []
        counter = 0
        imgList = get_frame(f)
        f = ''
        while(len(imgList) != counter):
            height, width, channels = imgList[counter].shape
            (thresh, imgList[counter]) = cv.threshold(imgList[counter], 128, 255, cv.THRESH_BINARY)# | cv.THRESH_OTSU
            img = np.array2string(imgList[counter], precision=2, separator='',suppress_small=True)
            f +=img
            counter+=1
            size = width
        message = ''.join(format(ord(x),'b') for x in f)
        del imgList

    else:
        cam2dna()

    return message,size

def code_to_DNA(message,size):
    counter = 0
    new_message = []
    print message
    while(counter != (len(message))):
        if(message[counter] == '1'):
            new_message.append('A')
        if(message[counter] == '0'):
            new_message.append('C')
        if((counter % (size-1)) == 0 and counter>1):
            new_message.append('T')
        counter+=1
    new_message.append('G')
    print(''.join(str(p) for p in new_message))

def main():
    messageType,fileName = get_message()
    message,size = get_bit(messageType,fileName)
    code_to_DNA(message,size)

if __name__ == '__main__':
    main()
