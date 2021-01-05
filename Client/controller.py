import inputs


class Controller:

    def __init__(self, connection):
        self.connection = connection
        try:
            self.gamepad = inputs.devices.gamepads[0]
        except IndexError:
            raise inputs.UnpluggedError("No gamepad found.")
        self.button_translation = {'BTN_SOUTH': 'A', 'BTN_EAST': 'B', 'BTN_WEST': 'X', 'BTN_NORTH': 'Y', 'BTN_TL': 'LB',
                                   'BTN_TR': 'RB', 'BTN_START': 'SELECT', 'BTN_SELECT': 'START', 'ABS_HAT0X': 'DX',
                                   'ABS_HAT0Y': 'DY', 'ABS_X': 'LSX', 'ABS_Y': 'LSY', 'ABS_RX': 'RSX', 'ABS_RY': 'RSY',
                                   'ABS_Z': 'LT', 'ABS_RZ': 'RT', 'BTN_THUMBR': 'RSB', 'BTN_THUMBL': 'LSB'}
        self.state = {'A': 0, 'B': 0, 'X': 0, 'Y': 0, 'LB': 0, 'RB': 0, 'START': 0, 'SELECT': 0, 'DX': 0, 'DY': 0,
                      'LT': 0, 'RT': 0, 'LSX': 0, 'LSY': 0, 'LSB': 0, 'RSX': 0, 'RSY': 0, 'RSB': 0}

    def handle_events(self):
        events = self.gamepad.read()
        for event in events:
            if event.ev_type == 'Key' or event.ev_type == 'Absolute':
                self.update_state(event.code, event.state)

    def update_state(self, key, value):
        if key in self.button_translation:
            key = self.button_translation[key]
        if key in ['LSX', 'LSY', 'RSX', 'RSY']:
            old_value = self.state[key]
            if -5000 < value < 5000:
                value = 0
            elif value >30000:
                value = 32767
            elif value < -30000:
                value = -32767
            difference = abs(old_value - value)
            if difference < 2000:
                return
        elif key == 'DY':
            value = -value

        self.state[key] = value

        self.command_to_send(key, value)

    def command_to_send(self, key, value):
        if key in ['LSX', 'LSY', 'RSX', 'RSY', 'LT', 'RT']:

            if key in ['LT', 'RT']:
                value = round(value/255,2)
            else:
                value = round(value/32767,2)
            self.send_filter(key,value)
        elif value != 0:
            self.send_filter(key,value)

    def send_filter(self,key,value):
        if key in ['LT','RT', 'LSX','A','B','X','Y']:
            self.connection.send({key: value})