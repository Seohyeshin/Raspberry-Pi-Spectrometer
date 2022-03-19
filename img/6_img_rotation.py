import cv2
import numpy as np

img = cv2.imread("arim/img/img.jpeg")
rows, cols = img.shape[:2]

d45= 45.0*np.pi/180
d90= 90.0*np.pi/180

m45=np.float32([[np.cos(d45), -1*np.sin(d45), rows//2],[np.sin(d45), np.cos(d45), -1*cols//4]])
m90=np.float32([[np.cos(d90), -1*np.sin(d90), rows],[np.sin(d90), np.cos(d90), 0]])

r45 = cv2.warpAffine(img, m45, (cols, rows))
r90 = cv2.warpAffine(img, m90, (rows, cols))

cv2.imshow("origin", img)
cv2.imshow("45", r45)
cv2.imshow("90", r90)
cv2.waitKey()
cv2.destroyAllWindows()

# 변환행렬 = cv2.getRotationMatrix2D(회전 중심(x,y), 회전각도, 확대/축소비율)
M45 = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 0.5)
M90 = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1.5)

img45 = cv2.warpAffine(img, M45, (cols, rows))
img90 = cv2.warpAffine(img, M90, (int(rows*1.5), int(cols*1.5)))

cv2.imshow("origin", img)
cv2.imshow("45", img45)
cv2.imshow("90", img90)
cv2.waitKey()
cv2.destroyAllWindows()