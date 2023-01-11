import cv2
import numpy as np

def mdim(img,loc): ## y(loc)위치에 있는 grayscale값 얻어서 리스트로 반환 
    imgg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    a = imgg[loc,:]
    return a