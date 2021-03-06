import numpy
import cv2
import os
import shutil
from tqdm import tqdm

class Storyboard_Wizard:
    def __init__(self):
        self.__output_directory = "Output"
        self.__captured_video = cv2.VideoCapture()
        self.__frame_number = 0
        self.__video_is_opened = False

    def open(self, path):
        if os.path.exists(path):
            self.__captured_video = cv2.VideoCapture(path)
            self.__frame_number = self.__captured_video.get(cv2.CAP_PROP_FRAME_COUNT)
            self.__video_is_opened = True
        return self.__video_is_opened

    def change_output_directory(self, path):
        self.__output_directory = path
        self.__captured_video.get(cv2.CAP_PROP_FRAME_COUNT)

    def get_frame_number(self):
        return self.__frame_number

    def get_storyboard(self):
        self.__remake_output_directory__()
        self.__write_all_frames__()
        
    def close(self):
        self.__captured_video.release()
        self.__video_is_opened = False

    def __remake_output_directory__(self):
        if os.path.exists(self.__output_directory):
            shutil.rmtree(self.__output_directory, True)
        os.mkdir(self.__output_directory) 

    def __get_frame__(self, captured_video, index_of_frame):
        ret, frame = captured_video.read()
        return frame

    def __write_image__(self, image_name, image):
        cv2.imwrite(image_name, image)

    def __write_all_frames__(self):
        for current_frame in tqdm(range(int(self.__frame_number)), ascii=True, unit="frame", ncols=150):
            image = self.__get_frame__(self.__captured_video, 2)
            self.__write_image__("{}/{}.jpg".format(self.__output_directory, current_frame), image)

if __name__ == "__main__":
    video_name = input('\n' + "Please give the video name including its extension" + '\n')
    storyboard_wizard = Storyboard_Wizard()
    video_is_opened = storyboard_wizard.open(video_name)
    if video_is_opened:
        print("\n Video opened! It has {} frames".format(storyboard_wizard.get_frame_number()))
        storyboard_wizard.get_storyboard()
        storyboard_wizard.close()
        print("Done!")
    else:
        print("\n Can't find that file!")
    input()