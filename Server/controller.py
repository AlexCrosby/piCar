class Controller:
    dev = False

    def __init__(self, camera, offset=0):

        self.camera = camera
        self.forward = 0
        self.backward = 0
        self.left = 0
        self.right = 0
        self.offset = offset

        if not Controller.dev:
            self.servo = Servo(0)
            self.left_wheel = Motor(17, offset=0)
            self.right_wheel = Motor(27, offset=0)
            self.pwm = PCA9685.PWM(bus_number=1)
            self.left_wheel.pwm = self.set_pwm_a
            self.right_wheel.pwm = self.set_pwm_b
            self.update_turn(offset)

    def set_pwm_a(self, value):
        pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
        self.pwm.write(4, 0, pulse_wide)

    def set_pwm_b(self, value):
        pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
        self.pwm.write(5, 0, pulse_wide)

    def handle_command(self, command, value):
        if command in ['DPadUp', 'DPadDown']:
            self.change_fps(value)
        elif command in ['RT', 'KeyW']:
            self.forward = value
            self.update_speed(self.forward - self.backward)
        elif command in ['LT', 'KeyS']:

            self.backward = value
            self.update_speed(self.forward - self.backward)
        elif command == 'LeftStickX':
            self.update_turn(value)
        elif command == 'KeyA':
            self.left = value
            self.update_turn(self.right - self.left)
        elif command == 'KeyD':
            self.right = value
            self.update_turn(self.right - self.left)

    def change_fps(self, value):
        if value == 1:
            self.camera.increase_fps()
        elif value == -1:
            self.camera.decrease_fps()

    def update_speed(self, speed):

        speed = self.map(speed, -1, 1, -100, 100)
        # print(f'Speed set to {speed}')
        if not Controller.dev:
            for motor in [self.left_wheel, self.right_wheel]:
                if speed >= 0:
                    motor.forward()
                else:
                    motor.backward()
                motor.speed = abs(speed)

    def update_turn(self, turn):

        turn = self.map(turn, -1, 1, 45, 135)
        # print(f'Turn set to {turn} ({turn+self.offset})')
        turn += self.offset
        if not Controller.dev:
            self.servo.write(turn)

    @staticmethod
    def map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


try:
    from servo import Servo
    from TB6612 import Motor
    import PCA9685
except ImportError:
    print("Development mode.")
    Controller.dev = True
