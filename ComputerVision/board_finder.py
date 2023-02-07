import cv2 as cv
import sys

def main():
    #POC: get board from image file
    image = cv.imread(cv.samples.findFile("test_data/3.jpg"))

    if image is None:
        sys.exit("Could not read the image.")
    
    image = cv.fastNlMeansDenoisingColored(image,None,20,10,7,21)

    # Convert image to grayscale
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
  
    # Use canny edge detection
    edges = cv.Canny(gray,50,150,apertureSize=3)
  
    # Apply HoughLinesP method to 
    # to directly obtain line end points
    lines_list =[]
    lines = cv.HoughLinesP(
                edges, # Input edge image
                1, # Distance resolution in pixels
                3.14/180, # Angle resolution in radians
                threshold=100, # Min number of votes for valid line
                minLineLength=100, # Min allowed length of line
                maxLineGap=10 # Max allowed gap between line for joining them
    )
  
    # Iterate over points
    for points in lines:
        # Extracted points nested in the list
        x1,y1,x2,y2=points[0]
        # Draw the lines joing the points
        # On the original image
        cv.line(image,(x1,y1),(x2,y2),(0,255,0),2)
        # Maintain a simples lookup list for points
        lines_list.append([(x1,y1),(x2,y2)])
        
    # Save the result image
    # cv2.imwrite('detectedLines.png',image)
    cv.imshow("Display window", image)
    k = cv.waitKey(0)
    # if k == ord("s"):
        # cv.imwrite("starry_night.png", img)




if __name__ == '__main__':
    main()