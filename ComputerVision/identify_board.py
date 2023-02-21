import cv2 as cv
import sys
import numpy as np


def main():
    img = cv.imread('test_data/4.jpg',cv.IMREAD_COLOR)
    
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Threshold the image to get only the black pixels
    _, mask = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Invert the mask to get all non-black pixels
    # mask = cv.bitwise_not(mask)

    # Create a white image
    white = np.full(img.shape, 255, dtype=np.uint8)

    # Make everything else white
    result = cv.bitwise_and(white, white, mask=mask)

    median = cv.medianBlur(result,3)

    rows = 3
    columns = 3

    # Define the chessboard pattern size
    # pattern_size = (rows, columns)

    # Find the corners of the chessboard in the image
    # found, corners = cv.findChessboardCorners(median, pattern_size, None)

    # if found:
    #     print("found")
    #     # Draw the corners on the image
    #     cv.drawChessboardCorners(img, pattern_size, corners, found)
    # else:
    #     print("not foudn")

    # gray = cv.cvtColor(gray, cv.COLOR_BGR2GRAY)

    # Show the result
    cv.imshow("Result", median)
    cv.waitKey(0)


if __name__ == '__main__':
    main()