import socketio


class Connection():
    connected = False
    socket = socketio.Client()

    def __init__(self, url):
        self.socket.connect(url)
        while not self.connected:
            pass

    @staticmethod
    @socket.on('connect')
    def on_connect():
        print("Connection to piCar established.")
        Connection.connected = True

    @staticmethod
    @socket.on('disconnect')
    def on_disconnect():
        print("Connection to piCar lost.")
        Connection.connected = False

    def send(self, command):
        if self.connected:
            self.socket.emit('command', command)
            print(f"Send command {command}.")
