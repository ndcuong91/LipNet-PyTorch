from random import random, randint
import numpy as np
import cv2, os
from datetime import datetime


def split_video(video_path, output_dir):
    '''
    cắt video thành 2,3 phần rồi save vào output_dir
    :param video_path:
    :param output_dir:
    :return:
    '''

    kk=1

def random_slow_fast_video(video_path, min_speed = 0.5, max_speed = 2.0):
    '''

    :param video_path:
    :param min_speed:
    :param max_speed:
    :return:
    '''

    ran_speed = random.uniform(min_speed, 2 -min_speed)
    if ran_speed >1: ran_speed = 1+(max_speed-1)*(ran_speed-1)/(1-min_speed)

def merge_video(input_dir, output_video_path):
    '''

    :param input_dir:
    :param output_video_path:
    :return:
    '''
    nn=1

def open_video():
    vid = cv2.VideoCapture('000.avi')
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20, (480, 360))

    # Check if camera opened successfully
    if (vid.isOpened() == False) or (cap.isOpened() == False):
        print("Error opening and capturing video file")

    while (vid.isOpened() and cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = vid.read()
        ret_cap, frame_cap = cap.read()
        if ret_cap:
            # Display the resulting frame
            cv2.imshow('Frame', frame)
            cv2.imshow('Frame cap', frame_cap)

            out.write(frame_cap)

            # Press Q on keyboard to exit
            if cv2.waitKey(40) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    out.release()
    vid.release()
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


def gen_annotation_video(save_name, fps = 0.25, num_otp = 40, size = (480, 360)):
    '''

    :param save_dir:
    :return:
    '''
    blank_image = np.zeros((size[1], size[0], 3), np.uint8)
    blank_image[:] = (0, 124, 255)

    # font
    org = (int(size[0]/2)-200, int(size[1]/2))
    fontScale = 3
    color = (255, 0, 0)
    thickness = 4

    out = cv2.VideoWriter(save_name, 0, fps, size)
    anno_txt = ''

    bgr_path = 'bgr.jpg'
    intro_img = cv2.imread(bgr_path)
    intro_img = cv2.resize(intro_img, size)
    intro_img = cv2.putText(intro_img, 'READY!', (100,200), 2,
                      fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
    for j in range(int(fps/0.25)):
        out.write(intro_img)

    for i in range(num_otp):
        img = blank_image.copy()
        otp = str(randint(100000, 999999))
        img = cv2.putText(img, otp, org, 2,
                        fontScale, color, thickness, cv2.LINE_AA)
        anno_txt+=otp+'\n'
        for j in range(int(fps/0.25)):
            out.write(img)

    out.release()
    anno_txt = anno_txt.rstrip('\n')

    with open(save_name.replace('.avi','.txt'), mode='w') as f:
        f.write(anno_txt)

def new_capture():
    # Python program to save a

    video = cv2.VideoCapture(0)

    if (video.isOpened() == False):
        print("Error reading video file")

    size = (640, 480)
    result = cv2.VideoWriter('filename.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             25, size)

    start = False
    while (True):
        ret, frame = video.read()
        if ret == True:

            # Write the frame into the
            # file 'filename.avi'

            # Display the frame
            # saved in the file
            if cv2.waitKey(10) & 0xFF == ord('s'):
                start = True

                frame = cv2.putText(frame, 'START', (300,240), 2,
                                  3, (0,255,0), 2, cv2.LINE_AA)
                cv2.imshow('start', frame)
                cv2.waitKey(0)
            cv2.imshow('Frame', frame)
            if start:
                result.write(frame)

            if cv2.waitKey(40) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    video.release()
    result.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    print("The video was successfully saved")


if __name__ =='__main__':

    save_dir = r'data/otp/{}'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(save_dir)
    for i in range(50):
        name = str(i).zfill(3)
        save_name = os.path.join(save_dir, name+'.avi')
        gen_annotation_video(save_name)
    #
    # open_video()
    # new_capture()