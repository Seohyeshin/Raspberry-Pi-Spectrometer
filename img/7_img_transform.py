import cv2
import numpy as np
from matplotlib import pyplot as plt

file_name = "arim/img/img.jpeg"
img = cv2.imread(file_name)
rows, cols = img.shape[:2]

pts1 = np.float32([[100,50], [200,50],[100,200]])
pts2 = np.float32([[80,70],[210,60],[250,120]])

mtrx=cv2.getAffineTransform(pts1, pts2)
dst=cv2.warpAffine(img, mtrx, (int(cols*1.5), rows))

cv2.imshow("origin", img)
cv2.imshow("affin", dst)
cv2.waitKey()
cv2.destroyAllWindows()