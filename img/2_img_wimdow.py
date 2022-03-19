import cv2

file_path="arim/img/img.jpeg" 
img = cv2.imread(file_path, cv2.IMREAD_COLOR)
img_gray= cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# "창이름"을 가진 창을 지정된 창타입에 맞추어 만듦
# cv.namedWindow("창이름", 창타입)
# 창타입: cv2.WINDOW_AUTOSIZE(이미지와 같은 크기의 창, 창의 크기에 따라 이미지의 크기가 변하지 않음), cv2.WINDOW_NORMAL(임의의 크기의 창, 창의 크기에 따라 이미지의 크기가 변함)
cv2.namedWindow("origin", cv2.WINDOW_AUTOSIZE) # "origin"이라는 이름으로 창 생성 (창 타입:cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("gray", cv2.WINDOW_NORMAL) # "gray"라는 이름으로 창 생성 (창 타입: cv2.WINDOW_NORMAL)

cv2.imshow("origin", img) # "origin"창에 "img"에 저장된 이미지 표시하기
cv2.imshow("gray", img_gray) # "gray"창에 "img_gray"에 저장된 이미지 표시하기

# cv2.moveWindow("창이름", x, y)
# "창이름" 창을 (x,y) 위치로 옮기기
cv2.moveWindow("origin", 0, 0) # "origin"창의 위치를 (0,0)으로 옮긴다.
cv2.moveWindow("gray", 100, 100) # "gray"창의 위치를 (100,100)으로 옮긴다.

cv2.waitKey()
# cv2.resizeWindow("창이름", width, height)
# "창이름" 창의 크기를 가로 width, 세로 height로 바꿈
cv2.resizeWindow("origin", 400,400) # "origin" 창의 크기를 (400,400)으로 변경한다. 
cv2.resizeWindow("gray", 100,100) # "gray" 창의 크기를 (100,100)으로 변경한다.

cv2.waitKey()
cv2.destroyAllWindows()