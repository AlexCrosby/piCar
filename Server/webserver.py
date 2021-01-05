from flask import Flask, request, Response
from flask_socketio import SocketIO
import cv2
import eventlet


class WebServer:

    def __init__(self,camera, log_output):
        self.camera=camera
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.video = cv2.VideoCapture(0)
        self.setup_routes()
        self.setup_socketio()
        self.socketio.run(self.app, log_output=log_output)

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)

    def setup_socketio(self):
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('disconnect', self.disconnect)
        self.socketio.on_event('command', self.handle_command)

    # ==================== ------ API Calls ------- ====================

    @staticmethod
    def index():
        return '''<html>
      <head>
        <title>Car Stream</title>
      </head>
      <body>
        <h1>Car Stream</h1>
        <img src="http://127.0.0.1:5000/video_feed">
      </body>
    </html>'''

    def video_feed(self):

        #return Response(self.camera.playback(), mimetype='multipart/x-mixed-replace; boundary=frame')
        return Response(self.camera.get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # ==================== ------ Socket Calls ------- ====================

    # def gen(self, video):
    #     while True:
    #         try:
    #             success, image = video.read()
    #             ret, jpeg = cv2.imencode('.jpg', image)
    #             frame = jpeg.tobytes()
    #             yield (b'--frame\r\n'
    #                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    #             fps = 60
    #             eventlet.greenthread.sleep(1 / fps)
    #         except ConnectionAbortedError:
    #             pass

    def connect(self):
        print('Client connected: ' + request.sid)

    def disconnect(self):
        print('Client disconnected: ' + request.sid)

    def handle_command(self, data):
        print(f"Received command: {data} " + request.sid)


