import cv2
import eventlet
import time
import eventlet
import threading
import time


class Camera:
    def __init__(self, fps=60):
        self.image = None
        self.fps = fps
        # self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.last_access = time.time()
        self.released = True
        self.thread = threading.Thread(target=self.camera_thread)
        self.thread.start()


    def camera_thread(self):
        print("Camera thread running.")
        self.cam = cv2.VideoCapture(0)
        while True:
            _, frame = self.cam.read()
            #frame = self.process_frame(frame)
            _, frame = cv2.imencode('.jpg', frame)
            self.image = frame.tobytes()
            time.sleep(1/self.fps)

    def get_frame(self):
        while True:
            try:
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.image + b'\r\n\r\n')
                eventlet.sleep(1/self.fps)
            except GeneratorExit:
                break

    def playback(self):
        # print("playback enter")
        while True:
            self.timeout = False
            if (self.released):
                self.released = False
                self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.last_access = time.time()
            success, image = self.cam.read()
            image = self.process_frame(image)
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            try:
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except GeneratorExit:
                self.close()
                break
            eventlet.greenthread.sleep(1 / self.fps)

    def process_frame(self, image):
        # print("enter")
        faceCascade = cv2.CascadeClassifier(
            'C:\\Users\\alexc\\PycharmProjects\\piCar\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (0, 0), fx=1, fy=1)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('gray', gray)
        cv2.waitKey(1)
        return image

    def close(self):
        self.timeout = True
        eventlet.sleep(2)
        if self.timeout:
            self.cam.release()
            self.released = True
            cv2.destroyAllWindows()
