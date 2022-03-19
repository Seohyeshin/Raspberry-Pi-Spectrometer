import cv2
import numpy as np

img=cv2.imread("arim/img/img.jpeg")
img2= img.astype(np.uint16) #img의 dtype을 uint16으로 바꾸어 img2에 저장한다. (각 컬러의 값을 더하는 과정에서 8bit를 넘을 수 있으므로 dtype을 변환한다.)

b,g,r = img2[:,:,0], img2[:,:,1], img2[:,:,2] # uint16으로 바꾼 이미지 파일을 색깔별로 나누어 b, g, r에 저장한다.
# img2는 3차원 리스트로 [높이, 폭, [b, g, r]]로 저장된다. 
gray = ((b+g+r)/3).astype(np.uint8) # 각각의 색깔의 크기를 더하여 평균을 낸 값을 gray라는 리스트 값에 저장한다. 
# gray는 [높이, 폭, 흑백 색상값]으로 구성된다. 
# gray는 이미지파일이므로 dtype을 uint8로 변경한다.

cv2.imshow("gray", gray) # gray를 "gray"인 창을 톻해 보여준다.

cv2.waitKey()
cv2.destroyAllWindows()

B, G, R = cv2.split(img) #이미지 파일을 색상별로 슬라이스 하여 각각 B,G,R에 저장한다.
zeros = np.zeros(img.shape[:2], dtype ="uint8") # 이미지 크기에 맞는 list값을 0으로 가지고 있는 list를 생성하여 zeros에 저장한다.
cv2.imshow("red", cv2.merge([zeros, zeros, R])) # 이미지에서 빨간색 값만이 나오도록 2차원 리스트를 합하여 3차원리스트로 만든 후(cv2.merge([B,G,R])), "red"라는 이름의 창을 통해 보여준다.
cv2.imshow("green", cv2.merge([zeros, G, zeros])) # 이미지에서 초록색 값만이 나오도록 2차원 리스트를 합하여 3차원리스트로 만든 후, "green"이라는 이름의 창을 통해 보여준다.
cv2.imshow("blue", cv2.merge([B, zeros, zeros])) # 이미지에서 파란색 값만이 나오도록 2차원 리스트를 합하여 3차원리스트로 만든 후, "blue"라는 이름의 창을 통해 보여준다.
cv2.imshow("inverse", cv2.merge([255-B, 255-G, 255-R])) # 각각의 컬러값을 255에서 뺀값을 merge하여 색상이 반전된 이미지를 만든 후, "inverse"라는 이름의 창을 통해 보여준다.

cv2.waitKey()
cv2.destroyAllWindows()

# cv2.cvtColor(이미지파일, 변환방식): 주어진 이미지파일을 설정한 변환방식으로 변환한다.
# 변환방식의 종류: cv2.COLOR_BGR2GRAY(BGR 컬러 이미지를 그레이 스케일로 변환), cv2.COLOR_GRAY2BGR(그레이 스케일 이미지를 BGR 컬러 이미지로 변환),
# cv2.COLOR_BGR2RGB(BGR 컬러 이미지를 RGB 컬러 이미지로 변환), cv2.COLOR_BGR2HSV(BGR 컬러 이미지를 HSV 컬러 이미지로 변환), 
# cv2.COLOR_HSV2BGR(HVS 컬러 이미지를 BGR 컬러 이미지로 변환), cv2.COLOR_BGR2YUV(BGR 컬러 이미지를 YUV 컬러 이미지로 변환), cv2.COLOR_YUV2BGR(YUV 컬러 이미지를 BGR 컬러 이미지로 변환)
GRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # BGR 컬러 이미지를 GRAY 스케일로 변환하여 GRAY에 저장
RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR 컬러 이미지를 RGB 컬러 이미지로 변환하여 RGB에 저장
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # BGR 컬러 이미지를 HSV 컬러 이미지로 변환하여 HSV에 저장
YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) # BGR 컬러 이미지를 YUV 컬러 이미지로 변환하여 YUV에 저장

cv2.imshow("GRAY", GRAY)
cv2.imshow("RGB", RGB)
cv2.imshow("HSV", HSV)
cv2.imshow("YUV", YUV)
cv2.imshow("ORIGIN", img)

cv2.waitKey()
cv2.destroyAllWindows()