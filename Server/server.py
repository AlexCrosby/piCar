from webserver import WebServer
from camera import Camera
from controller import Controller

if __name__ == '__main__':
    print('Starting camera')
    camera = Camera(fps=30)
    print('Starting controller')
    controller = Controller(camera=camera)
    print('Starting Web Server')
    server = WebServer(camera=camera, controller=controller, log_output=True)
