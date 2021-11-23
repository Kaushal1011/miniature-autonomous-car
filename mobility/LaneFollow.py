#########################################
# import camera funcs
# find heading angle change and return it
# check interscetion/turn and return it
#########################################

from vision.Camera import *
import cv2
import os
import numpy as np

control_image = []

thresholded_image = []

angle_arr = []


def find_steering_angle(img, roi=[[0, 600], [0, 300], [800, 300], [800, 600]]):
    anew = cv2.rotate(img, cv2.ROTATE_180)
    anew2= cv2.cvtColor(anew, cv2.COLOR_BGR2GRAY)
    # anew=cv2.rotate(a, cv2.ROTATE_90_CLOCKWISE)
    s, masked_img = roi_func(
        anew2, roi)
    lines = find_lanes(masked_img)
    thresholded_image.append(draw_line(anew, lines))

    sloped_lines = average_slope_intercept(anew2, lines)
    imgnew = display_lines(anew, sloped_lines)
    angle = compute_steering_angle(anew2, sloped_lines)
    global angle_arr
    angle_arr.append(angle)

    imgnew2 = display_heading_line(imgnew, angle)
    control_image.append(imgnew2)
    return angle


def stabilise(img):
    pass


def save_videos():
    height, width, _ = control_image[0].shape
    size = (width, height)
    out2 = cv2.VideoWriter(
        'slopesandheading.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
    for i in range(len(control_image)):
        # print(control_image[i].shape)
        out2.write(control_image[i])

    out2.release()
    out3 = cv2.VideoWriter(
        'detections.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
    for i in range(len(thresholded_image)):
        # print(control_image[i].shape)
        out3.write(thresholded_image[i])

    out3.release()
