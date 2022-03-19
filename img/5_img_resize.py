import cv2
import numpy as np

img = cv2.imread("arim/img/img.jpeg")
height, width = img.shape[:2]

m_small = np.float32([[0.5, 0, 0], [0,0.5,0]])

m_big = np.float32([[2,0,0],[0,2,0]])

dst1= cv2.warpAffine(img, m_small, (int(width*0.5), int(height*0.5)))
dst2= cv2.warpAffine(img, m_big, (int(width*2), int(height*2)))

dst3 = cv2.warpAffine(img, m_small, (int(width*0.5), int(height*0.5)), None, cv2.INTER_AREA)
dst4 = cv2.warpAffine(img, m_big, (int(width*2), int(height*2)), None, cv2.INTER_CUBIC)

cv2.imshow("original", img)
cv2.imshow("small", dst1)
cv2.imshow("big", dst2)
cv2.imshow("small INTER_AREA", dst3)
cv2.imshow("big INTER_CUBIC", dst4)

cv2.waitKey()
cv2.destroyAllWindows()
# 결과 이미지 = cv2.resize(이미지, 출력 이미지 크기(width, height), dst, 가로 배율, 세로 배율, 보간방법)
DST1= cv2.resize(img, (int(width*0.5), int(height*0.5)), interpolation= cv2.INTER_AREA)
DST2= cv2.resize(img, None, None, 2,2, cv2.INTER_CUBIC)

cv2.imshow("original", img)
cv2.imshow("small", DST1)
cv2.imshow("big", DST2)
cv2.waitKey()
cv2.destroyAllWindows()