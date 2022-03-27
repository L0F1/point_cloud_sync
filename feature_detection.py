import cv2
import numpy as np


def surf_detection(color_image):
    img = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    surf = cv2.xfeatures2d.SURF_create(1000)
    kp, des = surf.detectAndCompute(img, None)
    return cv2.drawKeypoints(img, kp, None, (255, 0, 0), 4)


def sift_detection(color_image):
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create(400)
    kp = sift.detect(gray, None)
    return cv2.drawKeypoints(gray, kp, color_image)


def fast_detection(color_image):
    fast = cv2.FastFeatureDetector_create(15)
    kp = fast.detect(color_image, None)
    return cv2.drawKeypoints(color_image, kp, None, color=(255, 0, 0))


def brief_detection(color_image):
    # Initiate FAST detector
    star = cv2.xfeatures2d.StarDetector_create()
    # Initiate BRIEF extractor
    brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
    # find the keypoints with STAR
    kp = star.detect(color_image, None)
    # compute the descriptors with BRIEF
    kp, des = brief.compute(color_image, kp)
    return cv2.drawKeypoints(color_image, kp, None, color=(255, 0, 0))


def orb_detection_show(color_image):
    kp, des = orb_detection(color_image)
    # draw only keypoints location,not size and orientation
    return cv2.drawKeypoints(color_image, kp, None, color=(255, 0, 0))


def orb_detection(color_image):
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    # compute the descriptors with ORB
    return orb.detectAndCompute(gray, None)


def match_features(color_image_1, color_image_2):
    kp1, des1 = orb_detection(color_image_1)
    kp2, des2 = orb_detection(color_image_2)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1, des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    # Draw first 10 matches.
    return cv2.drawMatches(color_image_1, kp1, color_image_2, kp2, matches[:10], None,
                           flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


# def show_features(detection_alg):
#     return cv2.drawKeypoints(color_image, kp, None, color=(255, 0, 0))


def laplacian_filter(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplas = cv2.Laplacian(gray, cv2.CV_64F, ksize=7)
    return gray - laplas
