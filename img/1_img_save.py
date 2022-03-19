import cv2

img_file="arim/img/img.jpeg" # "img_file"에 파일의 경로를 넣는다.
save_file="arim/img/img_gray.jpeg" # 이미지 파일이 저장될 경로를 "save_file"에 넣는다.

# 파일경로에 있는 이미지를 지정된 방식으로 읽어 변수에 저장
# 변수=cv2.imread(파일경로, 읽는 방식)
# 읽는 방식의 종류: cv2.IMREAD_COLOR(컬러스케일로 읽고 투명한 부분 무시, 기본값), cv2.IMREAD_GRAYSCALE(흑백스케일로 읽기), cv2.IMREAD_UNCHANGED(컬러스케일로 읽고 투명한 부분도 읽음)
img_1=cv2.imread(img_file, cv2.IMREAD_COLOR) # "img_file"에 있는 이미지를 컬러로 읽어 "img_1"에 넣는다.
img_2=cv2.imread(img_file, cv2.IMREAD_GRAYSCALE) # "img_file"에 있는 이미지를 흑백으로 읽어 "img_2"에 넣는다.

cv2.imshow("img1", img_1) # img_1를 "img1"인 창에 보여준다.
cv2.imshow("img2", img_2) # img_2를 "img2"인 창에 보여준다.

cv2.imwrite(save_file, img_2) # img_2를 "save_file"에 저장한다.
cv2.waitKey()
cv2.destroyAllWindows()