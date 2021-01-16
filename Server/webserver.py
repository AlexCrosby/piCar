from flask import Flask, request, Response
from flask_socketio import SocketIO
import cv2


class WebServer:

    def __init__(self, camera, controller, log_output):
        self.camera = camera
        self.controller = controller
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.setup_routes()
        self.setup_socketio()
        self.socketio.run(self.app, log_output=log_output, host='0.0.0.0')

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        if self.camera is not None:
            self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)

    def setup_socketio(self):
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('disconnect', self.disconnect)
        self.socketio.on_event('command', self.handle_command)

    def get_state(self):
        status = {}
        if self.camera is not None:
            status['fps'] = self.camera.fps
        self.socketio.emit('status', status)

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
        # return Response(self.camera.playback(), mimetype='multipart/x-mixed-replace; boundary=frame')
        if self.camera is not None:
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
        self.controller.stop_car()

    def handle_command(self, data):
        print(f"Received command: {data} " + request.sid)
        for command, value in data.items():
            self.controller.handle_command(command, value)
