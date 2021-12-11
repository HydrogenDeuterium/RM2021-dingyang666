import time

import cv2
from apriltag import Detector


# from pupil_apriltags import Dcetector


class Camera:
    def __init__(self):
        self.__detector = Detector()
        self.capture = cv2.VideoCapture(0)
        if self.capture.isOpened is False:
            self.capture = cv2.VideoCapture(2)
    
    def __del__(self):
        self.capture.release()
    
    # 拍照
    def __get_photo(self):
        assert self.capture.isOpened() is True
        # 等待0.5秒防止图像抖动导致识别不到图像
        time.sleep(0.5)
        ret, cap = self.capture.read()
        assert ret is True
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        return cap
    
    def auto_anal(self) -> dict:
        """自动拍照并分析各标签位置"""
        img = self.__get_photo()
        result = self.__detector.detect(img=img)
        
        if result:
            img_center = tuple(i_ / 2 for i_ in img.shape[::-1])
            ret = {i.tag_id: tuple(float(res - img) for img, res in zip(img_center, i.center)) for i in result}
            return ret
        return {}


if __name__ == '__main__':
    # Camera
    t0 = time.time_ns()
    camera: Camera = Camera()
    for i in range(100):
        print(camera.auto_anal())
    t = time.time_ns()
    print(f'100次识别总用时 {(t - t0) / 1e9} 秒。\n识别速率：{100 / (t - t0) * 1e9} Hz')
