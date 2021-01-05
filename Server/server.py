from flask import Flask, request, Response
from flask_socketio import SocketIO
import cv2
from webserver import WebServer
from camera import Camera


import eventlet
#
# app = Flask(__name__)
# socketio = SocketIO(app)
# video = cv2.VideoCapture(0)
#
#
# @socketio.on('connect')
# def connect():
#     print('Client connected: ' + request.sid)
#
#
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected: ' + request.sid)
#
#
# @socketio.on('message')
# def handle_message(data):
#     print('Received message: ' + data + ' ' + request.sid)
#
#
# @app.route('/')
# def index():
#     return '''<html>
#   <head>
#     <title>Car Stream</title>
#   </head>
#   <body>
#     <h1>Car Stream</h1>
#     <img src="http://127.0.0.1:5000/video_feed">
#   </body>
# </html>'''
#
#
# def gen(video):
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
#
#
# @app.route('/video_feed'):
#     global video
#     return Response(gen(video), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print('Starting camera')
    camera=Camera(fps=60)
    print('Starting Web Server')
    server = WebServer(camera=camera, log_output=True)

