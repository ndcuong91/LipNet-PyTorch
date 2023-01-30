from random import random, randint
import numpy as np
import cv2, os


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

def gen_annotation_video(save_name, fps = 25, num_otp = 40, size = (240, 180)):
    '''

    :param save_dir:
    :return:
    '''
    blank_image = np.zeros((size[1], size[0], 3), np.uint8)
    blank_image[:] = (0, 124, 255)

    # font
    org = (int(size[0]/2)-100, int(size[1]/2))
    fontScale = 2
    color = (255, 0, 0)
    thickness = 4

    out = cv2.VideoWriter(save_name, 0, fps, size)
    anno_txt = ''

    bgr_path = '/home/vvn/PycharmProjects/lip_reading/data/bgr/flowers-276014_960_720.jpg'
    intro_img = cv2.imread(bgr_path)
    intro_img = cv2.resize(intro_img, size)
    intro_img = cv2.putText(intro_img, 'READY!', (50,100), 2,
                      fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
    for j in range(int(fps/0.5)):
        out.write(intro_img)
    # cv2.imshow('bgr',intro_img)
    # cv2.waitKey(0)

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

    kk=1


def open_video():
    vid = cv2.VideoCapture('/home/vvn/PycharmProjects/lip_reading/data/gen_otp_video/000.avi')
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20, (480, 480))

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
    vid.release()
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()




if __name__ =='__main__':

    # save_dir = '/home/vvn/PycharmProjects/lip_reading/data/gen_otp_video'
    # for i in range(10):
    #     name = str(i).zfill(3)
    #     save_name = os.path.join(save_dir, name+'.avi')
    #     gen_annotation_video(save_name)

    open_video()