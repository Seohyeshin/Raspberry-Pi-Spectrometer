import cv2
import numpy as np

img = cv2.imread("arim/img/img.jpeg")
rows, cols = img.shape[0:2] # 이미지의 높이를 rows에 이미지의 넓이를 cols에 저장

dx, dy = 100, 50 # dx에 x축으로 이동할 거리, dy에 y축으로 이동할 거리 저장

mtrx = np.float32([[1,0,dx], [0,1,dy]]) # 변환 행렬 생성

# 결과이미지 = cv2.warpAffine(이미지, 변환행렬, 크기(width, height) [, None, 보간법, 외곽영역 보정방법])
# 보간법: cv2.INTER_LINEAR(인접한 4개 픽셀값에 거리 가중치 사용, 기본값),  cv2.INTER_NEAREST(가장 가까운 픽셀 값 사용),
# cv2.INTER_AREA(픽셀 영역 관계를 이용한 재샘플링), cv2.INTER_CUBIC(인접한 16개 픽셀 값에 거리 가중치 사용), cv2.INTER_LANCZOS4(인접한 8개 픽셀을 이용한 란초의 알고리즘)

# 외곽영역 보정방법: cv2.BORDER_CONSTANT(고정색상값), cv2.BORDER_REPLICATE(가장 자리 복제), 
# cv2.BORDER_WRAP(반복), cv2.BORDER_REFLECT(반사)

dst = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy)) 
dst2  = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy), None, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, (255,0,0))
dst3 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy), None, cv2.INTER_LINEAR, cv2.BORDER_REFLECT)

cv2.imshow("original", img)
cv2.imshow("trans", dst)
cv2.imshow("BORDER_CONSTANT", dst2)
cv2.imshow("BODDER_REFLECT", dst3)
cv2.waitKey()
cv2.destroyAllWindows()