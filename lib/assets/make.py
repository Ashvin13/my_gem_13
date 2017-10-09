import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage.measure import compare_ssim
import imutils

img = cv2.imread('digits.png')

height, width = img.shape[:2]

i = 0
k = 1

# save = img[100:120, 0:20]
# cv2.imwrite('aaa.png', save)

while True:
	j = 0
	while True:
		
		save = img[i:i+20, j:j+20]
		cv2.imwrite('digits/img'+str(k)+'.png', save)
		k += 1
		j += 20
		if j == width:
			break
	i += 20	
	if i == 1000:
		break
	

# cv2.waitKey()