#!/usr/bin/python

# Import the modules
import sys
import cv2
from skimage.feature import hog
import numpy as np
import argparse as ap

def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
 
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
 
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
 
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))
 
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

# Get the path of the training set
parser = ap.ArgumentParser()
parser.add_argument("-i", "--image", help="Path to Image", required="True")
args = vars(parser.parse_args())

# Read the input image 
im = cv2.imread(args["image"])

# Convert to grayscale and apply Gaussian filtering
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

# Threshold the image
ret, im_th = cv2.threshold(im_gray, 180, 255, cv2.THRESH_BINARY_INV)

height, width, channels = im.shape

i = 0

crop_cnt = 1

while True:
    
    t = 0
    for j in range(0, width):
        color = int(im_th[i, j])
        if color != 0:
            t = 1
            break

    if t == 1:
        start_x = i
        for k in range(i, height):
            p = 0
            for j in range(0, width):
                color = int(im_th[k, j])
                if color != 0:
                    p = 1
                    break
            if p == 0:
                end_x = k
                i = k
                break;
        dis = str(start_x)
        dis = dis + ' '
        try:
            dis = dis + str(end_x)
        except:
            continue
        # print dis

        # crop_img = np.zeros((height,width,3), np.uint8)
        # crop_img[0:height, 0:width] = (255, 255, 255)
        # crop_start = (height-end_x+start_x)/2
        # crop_img[crop_start:crop_start+end_x-start_x, 0:width] = im[start_x:end_x, 0:width]

        crop_img = np.zeros((height,width+200,3), np.uint8)
        crop_img[0:height, 0:width+200] = (255, 255, 255)
        crop_start = (height-end_x+start_x)/2
        crop_img[crop_start:crop_start+end_x-start_x, 100:width+100] = im[start_x:end_x, 0:width]

        # crop = im[start_x:end_x, 0:width]
        cv2.imwrite('crop/crop'+str(crop_cnt)+'.jpg', crop_img)
        crop_cnt += 1
        # cv2.imshow('crop' + dis, crop)

    i = i + 1

    if i >= height: break

for crop_i in range(1, crop_cnt):

    im = cv2.imread("crop/crop"+(str)(crop_i)+".jpg")

    # Convert to grayscale and apply Gaussian filtering
    if im == True:
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
        break

    # Threshold the image
    ret, im_th = cv2.threshold(im_gray, 180, 255, cv2.THRESH_BINARY_INV)

    # cv2.namedWindow(str(crop_i), cv2.WINDOW_NORMAL)
    # cv2.imshow(str(crop_i), im_th)

    # Find contours in the image
    ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get rectangles contains each contour

    try:
        cnts = sorted(ctrs, key = cv2.contourArea, reverse = True)[:30]
        (cnts, boundingBoxes) = sort_contours(cnts, method="left-to-right")
    except:
        continue

    rects = [cv2.boundingRect(ctr) for ctr in cnts]

    i = 0

    digit = ''

    prev = 0

    score_width = 0
    score_index = 0

    for rect in rects:
        # Draw the rectangles
        temp = (int)(rect[0]) - prev
        if score_width < temp:
            score_width = temp
            score_index = i
        prev = rect[0]
        # res_str = (str)(rect[0]) + ' ' + (str)(rect[1])
        # print res_str
        if rect[2] < 30 and rect[3] < 30:
            continue
        # cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 
        # Make the rectangular region around the digit
        leng = int(rect[3] * 1.6)
        pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
        pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
        roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
        # Resize the image
        try:
            roi = cv2.resize(roi, (20, 20), interpolation=cv2.INTER_AREA)
        except:
            continue
        
        roi = cv2.dilate(roi, (3, 3))
        
        cv2.imwrite("roi/roi" + str(i) + ".png", roi)

        roi = cv2.imread("roi/roi" + str(i) + ".png")

        err = 99999

        fname = ''

        cnt = 5000

        for ii in xrange(1,5000):
            file_name = 'img' + str(ii) + '.png'
            try:
                compare = cv2.imread('digits/'+file_name)
            except:
                continue

            dif = np.sum((roi.astype("float") - compare.astype("float")) ** 2)
            dif /= float(roi.shape[0] * roi.shape[1])

            if err > dif:
                err = dif
                fname = file_name

        res = (int)(fname[3:len(fname)-4])

        if res % 500 == 0:
            digit = digit + (str)(res / 500 - 1) + ' '
        else:
            digit = digit + (str)((int)(res / 500))

        
        # cv2.putText(im, str(i), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
        i += 1

    ret = [(int)(digit[:score_index]), (int)(digit[score_index:])]

    print >> sys.stdout, ret

    digit = digit[:score_index] + ' ' + digit[score_index:]
    # print digit

# cv2.namedWindow("Resulting Image with Rectangular ROIs", cv2.WINDOW_NORMAL)
# cv2.imshow("Resulting Image with Rectangular ROIs", im)
cv2.waitKey()
