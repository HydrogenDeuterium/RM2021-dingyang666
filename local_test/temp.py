import cv2

for i in range(65536):
    camera = cv2.VideoCapture(i)
    if camera.isOpened():
        print(i)
        break
