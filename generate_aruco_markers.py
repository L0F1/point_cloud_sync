import cv2
import numpy as np

if __name__ == "__main__":
    # load the ArUCo dictionary
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    id = 1

    # allocate memory for the output ArUCo tag and then draw the ArUCo
    # tag on the output image
    tag = np.zeros((300, 300, 1), dtype="uint8")
    cv2.aruco.drawMarker(arucoDict, id, 300, tag, 1)

    # write the generated ArUCo tag to disk and then display it to our
    # screen
    cv2.imwrite("C:\\Users\\trien\\Desktop\\markers\\DICT_4X4_50_id1.png", tag)
    cv2.imshow("ArUCo Tag", tag)
    cv2.waitKey(0)