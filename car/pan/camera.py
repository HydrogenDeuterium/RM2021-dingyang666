import time
from typing import Dict, Tuple

import cv2
from apriltag import Detector


class Camera(Detector):
    def __init__(self):
        Detector.__init__(self)
        self.capture = cv2.VideoCapture(0)
    
    def __del__(self):
        self.capture.release()
    
    # 拍照
    def get_photo(self):
        assert self.capture.isOpened() is True
        # 等待0.5秒防止图像抖动导致识别不到图像
        time.sleep(0.5)
        ret, cap = self.capture.read()
        assert ret is True
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        return cap
    
    def auto_anal(self) -> Dict[int, Tuple[float, float]]:
        """自动拍照并分析各标签位置"""
        img = self.get_photo()
        result = self.detect(img=img)
        
        if result:
            img_center = img.shape[1], img.shape[0]
            ret = {i_.tag_id: (i_.center[0] - img_center[0],
                               i_.center[1] - img_center[1])
                   for i_ in result}
            return ret
        return {}


if __name__ == '__main__':
    # Camera
    t0 = time.time_ns()
    camera: Camera = Camera()
    for i in range(50):
        print(camera.auto_anal())
    t = time.time_ns()
    print(f'100次识别总用时 {(t - t0) / 1e9} 秒。\n识别速率：{100 / (t - t0) * 1e9} Hz')
