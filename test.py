import cv2

cap = cv2.VideoCapture(0)

while(True):
    _, frame = cap.read()
    cv2.imshow("test", frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (20,100,100),(35,255,255))

    # cv2.dilate(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    cv2.imshow("mask", mask)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break