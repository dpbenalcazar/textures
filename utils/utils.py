import cv2
import numpy as np

def get_mask(img):
    mask_B = img[:,:,0] < 4
    mask_G = img[:,:,1] < 4
    mask_R = img[:,:,2] < 4
    mask = mask_B & mask_G & mask_R
    mask = 255*mask.astype(np.uint8)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask
