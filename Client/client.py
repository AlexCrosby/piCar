from connection import Connection
from gamepad import Controller

if __name__ == '__main__':
    connection = Connection('http://localhost:5000')
    controller = Controller(connection)
    while True:
        controller.handle_events()
