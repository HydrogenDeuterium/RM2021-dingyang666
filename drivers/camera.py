import apriltag
from typing import List

import cv2
from apriltag import Detector


class Camera:
    def __init__(self):
        self.__detector = Detector()
        self.capture = cv2.VideoCapture(0)
    
    # 拍照
    def __get_photo(self):
        # os.system('libcamera-jpeg -o tmp.jpg')
        # return cv2.imread('tmp.jpg', cv2.IMREAD_GRAYSCALE)
        ret, cap = self.capture.read()
        assert ret is True
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        return cap
    
    def __anal_photo(self) -> dict:
        img = self.__get_photo()
        result: List[apriltag.Detection] = self.__detector.detect(img=img)
        
        if result:
            img_center = (i / 2 for i in img.shape)
            return {i.tag_id: tuple(res - img for img, res in zip(img_center, i.center))
                    for i in result}
        return {}