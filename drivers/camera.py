import time

import apriltag
from typing import List

import cv2
from apriltag import Detector


class Camera:
    def __init__(self):
        self.__detector = Detector()
        self.capture = cv2.VideoCapture(0)
    
    def __del__(self):
        self.capture.release()
    
    # 拍照
    def __get_photo(self):
        # os.system('libcamera-jpeg -o tmp.jpg')
        # return cv2.imread('tmp.jpg', cv2.IMREAD_GRAYSCALE)
        assert self.capture.isOpened() is True
        ret, cap = self.capture.read()
        assert ret is True
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        return cap
    
    def anal_photo(self) -> dict:
        img = self.__get_photo()
        result: List[apriltag.Detection] = self.__detector.detect(img=img)
        
        if result:
            img_center = tuple(i / 2 for i in img.shape)
            return {i.tag_id: tuple(float(res - img) for img, res in zip(img_center, i.center))
                    for i in result}
        return {}


if __name__ == '__main__':
    # Camera
    t0 = time.time_ns()
    camera: Camera = Camera()
    for i in range(100):
        print(camera.anal_photo())
    t = time.time_ns()
    print(f'100次识别总用时 {(t - t0) / 1e9} 秒。\n识别速率：{100 / (t - t0) * 1e9} Hz')
