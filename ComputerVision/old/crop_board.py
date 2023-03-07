import cv2 as cv
import sys
import numpy as np

CIRCLE_RES = 10

img = cv.imread('test_data/4.jpg',cv.IMREAD_COLOR)
crop_points = []


def warp():
    global crop_points

    size = 1000
    src_vertices = np.array([[crop_points[0][0], crop_points[0][1]], 
                            [crop_points[1][0], crop_points[1][1]], 
                            [crop_points[2][0], crop_points[2][1]], 
                            [crop_points[3][0], crop_points[3][1]]], dtype=np.float32)
    dst_vertices = np.array([[0, 0], [size, 0], [size, size], [0, size]], dtype=np.float32)
    crop_points = np.array(src_vertices)

    # calculate the perspective transformation matrix
    M = cv.getPerspectiveTransform(src_vertices, dst_vertices)

    # apply transformation to the original image
    dst = cv.warpPerspective(img, M, (size, size))

    cv.imwrite('tranformed_image.jpg', dst)


def crop(): 
    # mask with white pixels
    mask = np.ones(img.shape, dtype=np.uint8)
    mask.fill(255)

    roi_corners = np.array([crop_points], dtype=np.int32)
    cv.fillPoly(mask, roi_corners, 0)
    
    masked_image = cv.bitwise_or(img, mask)
    cv.imshow("select corners", masked_image)

    warp()


def on_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(param, (x, y), CIRCLE_RES, (0, 255, 0), 3)
        cv.imshow("select corners", param)
        crop_points.append((x, y))

    if len(crop_points) == 4:
        crop()


def main():
    img = cv.imread('test_data/4.jpg',cv.IMREAD_COLOR)
    selector = img.copy()
    cv.namedWindow("select corners")
    cv.setMouseCallback('select corners', on_mouse, param=selector)
    cv.imshow("select corners", selector)
    cv.waitKey(0)
    cv.destroyAllwindows()


if __name__ == '__main__':
    main()
