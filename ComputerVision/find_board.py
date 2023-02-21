import cv2
import sys
import numpy as np


def flood_fill(mask):
    # Define a seed point for the flood fill algorithm
    h, w = mask.shape[:2]
    seed_point = (10, 10)

    # Define the fill value and tolerance for the flood fill algorithm
    fill_value = 255
    tolerance = 15

    # Perform the flood fill algorithm
    mask = cv2.floodFill(mask, None, seed_point, fill_value, loDiff=tolerance, upDiff=tolerance)[1]


def blur_color_range(img):
    # Convert the image from RGB to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of brown color in the HSV color space
    lower_brown = np.array([0, 0, 0])
    upper_brown = np.array([100, 200, 200])

    # Threshold the HSV image to get only brown colors
    mask = cv2.inRange(hsv, lower_brown, upper_brown)

    # Apply median blur only to the brown pixels
    blurred = cv2.medianBlur(mask, 3, img)

    return blurred


def proc_frame(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # blurred = cv2.medianBlur(img, 81)
    blurred = blur_color_range(img)
    # flood_fill(blurred)

    gray = np.float32(blurred)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    img[dst>0.01*dst.max()]=[0,0,255]

    # return blurred
    cv2.imshow('Original Image', img)
    cv2.imshow('Blurred Image', blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    img = cv2.imread('test_data/5.jpg',cv2.IMREAD_COLOR)

    # cap = cv2.VideoCapture('sample.mp4')
    # while (cap.isOpened()):
    #     ret, frame = cap.read()
    #     cv2.imshow('Frame', frame)

    proc_frame(img)



if __name__ == '__main__':
    main()