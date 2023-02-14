import cv2 as cv
import sys
import numpy as np

CIRCLE_RES = 10

img = cv.imread('test_data/4.jpg',cv.IMREAD_COLOR)
crop_points = []


def warp(target_corners):
    global crop_points

    # Define the vertices of the original quadrilateral
    # src_vertices = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)

    # Define the vertices of the square that the quadrilateral should be transformed into
    size = 1000
    src_vertices = np.array([[crop_points[0][0], crop_points[0][1]], 
                            [crop_points[1][0], crop_points[1][1]], 
                            [crop_points[2][0], crop_points[2][1]], 
                            [crop_points[3][0], crop_points[3][1]]], dtype=np.float32)
    dst_vertices = np.array([[0, 0], [size, 0], [size, size], [0, size]], dtype=np.float32)
    crop_points = np.array(src_vertices)

    print(crop_points)
    print(dst_vertices)

    # Calculate the perspective transformation matrix
    M = cv.getPerspectiveTransform(src_vertices, dst_vertices)

    # Apply the transformation to the original image
    dst = cv.warpPerspective(img, M, (size, size))

    cv.imwrite('tranformed_image.jpg', dst)


def gen_square_target(length):
    print(length)
    return np.array([[0,0], [length, 0], [length, length], [0, length]])


def crop(): 
    #mask with white pixels
    mask = np.ones(img.shape, dtype=np.uint8)
    mask.fill(255)

    roi_corners = np.array([crop_points], dtype=np.int32)
    cv.fillPoly(mask, roi_corners, 0)
    
    masked_image = cv.bitwise_or(img, mask)
    cv.imshow("select corners", masked_image)

    target = gen_square_target(crop_points[1][0] - crop_points[0][0])

    warp(target)
    #four_point_transform(img, target)
    cv.imshow("select corners", target)


def on_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), CIRCLE_RES, (0, 255, 0), 3)
        cv.imshow("select corners", img)
        crop_points.append((x, y))

    if len(crop_points) == 4:
        crop()


def main():
    img = cv.imread('test_data/4.jpg',cv.IMREAD_COLOR)
    cv.namedWindow("select corners")
    cv.setMouseCallback('select corners', on_mouse)
    cv.imshow("select corners", img)
    cv.waitKey(0)
    cv.destroyAllwindows()


if __name__ == '__main__':
    main()
