import cv2
import numpy as np

global stx ## 그래프 기준점 

setnm = [1,400,380,780]
nmnm = []
stx = 0

cap1 = cv2.imread("many.png")

## 파장계산(구현예정)
global ihatethis

iht = [0,0,0,0]

def waca():     

    global setnm,nmnm,cap1

    sx = setnm[0]
    bx = setnm[1]
    sn = setnm[2]
    bn = setnm[3]

    
    px1 = (bn-sn)/(bx-sx) ## 1픽셀당 파장(= nm/px)

    def cpx(nm):
        px = nm/px1
        return int(px)

    stx = sx - cpx((sn-380)) ## 파장 시작 이미지 픽셀 위치 
    stn = 380                ## 이미지 시작 파장 
    if stx<=1:
        stx = 1
        stn = int(sn - px1*(sx-stx))


    btx = bx + cpx((780-bn)) ## 파장 끝 이미지 픽셀 위치
    enn = 780               ## 이미지 끝 파장 
    if btx>=400:
        btx = 400                  ## 파장 끝 이미지 픽셀 위치
        enn = int(bn + (400-bx)*px1)    ## 이미지 끝에서의 파장 
    
    iht[0] = stx 
    iht[1] = stn
    iht[2] = btx
    iht[3] = enn


    sketch1 = np.zeros((300,btx-stx,3),dtype=np.uint8)
    sketch1[0:300,0:btx-stx] = cap1[0:300,stx:btx]
    if stn == 380 and enn == 780:
        sketch1 = cv2.resize(sketch1,(400,300))
        return sketch1

    else:
        sketch2 = np.zeros((300,400,3),dtype=np.uint8)
        sketch1 = cv2.resize(sketch1,(enn-stn,300))
        sketch2[0:300,stn-380:enn-380]=sketch1[0:300,0:enn-stn]
        return sketch2

    ## 이미지 시작위치 구하기 