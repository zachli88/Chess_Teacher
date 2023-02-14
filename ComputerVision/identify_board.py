import cv2 as cv
import sys
import numpy as np


def main():
    img = cv.imread('test_data/4.jpg',cv.IMREAD_COLOR)
    
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Convert the image to grayscale
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
    pattern_size = (rows, columns)

    # Find the corners of the chessboard in the image
    found, corners = cv.findChessboardCorners(median, pattern_size, None)

    # if found:
    #     print("found")
    #     # Draw the corners on the image
    #     cv.drawChessboardCorners(img, pattern_size, corners, found)
    # else:
    #     print("not foudn")

    # Use canny edge detection
    edges = cv.Canny(median,50,150,apertureSize=3)
    
    # Apply HoughLinesP method to 
    # to directly obtain line end points
    lines_list =[]
    lines = cv.HoughLinesP(
                edges, # Input edge image
                1, # Distance resolution in pixels
                np.pi/180, # Angle resolution in radians
                threshold=50, # Min number of votes for valid line
                minLineLength=5, # Min allowed length of line
                maxLineGap=15 # Max allowed gap between line for joining them
                )
    
    # Iterate over points
    for points in lines:
        # Extracted points nested in the list
        x1,y1,x2,y2=points[0]
        # Draw the lines joing the points
        # On the original image
        cv.line(median,(x1,y1),(x2,y2),(0,255,0),2)
        # Maintain a simples lookup list for points
        lines_list.append([(x1,y1),(x2,y2)])

    # Show the result
    cv.imshow("Result", median)
    cv.waitKey(0)


if __name__ == '__main__':
    main()