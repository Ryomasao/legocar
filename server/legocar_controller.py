# -*- coding: utf-8 -*-
import wiringpi as pi
import sys

class LegoCarController:
    '''
    レゴカーを動かすためのクラス
    前進と後退するためのDCモーター、ステアリング処理を行うサーボモータを制御している。
    制御するためのGPIOは、初期処理で固定で決めている。
    '''
    def __init__(self):

        pi.wiringPiSetupGpio()
        #DCモーターを制御するクラス
        self.dcmotor = DCmotor_DRV8835(motor_pin1=14, motor_pin2=15, motor_pin3=20, motor_pin4=21)
        #サーボモータを制御するクラス
        self.servo_motor = ServoMotor(18)

    def accelerator(self, order):
        '''
        orderの値をもとに、前進と後退を制御する。
        :param order:
        :return:
        '''
        if order == b'w' :
            #前進
            self.moveForward()
        elif order == b's':
            #後退
            self.moveBack()
        elif order == (b'a'):
            #ステアリングの命令は無視
            pass
        elif order == (b'd'):
            #ステアリングの命令は無視
            pass
        elif order == (b'h'):
            #クレーンの命令は無視
            pass
        elif order == (b'j'):
            #クレーンの命令は無視
            pass
        else:
            #止まる
            self.stop()


    def moveForward(self):
       self.dcmotor.forwardAmotor()

    def moveBack(self):
        self.dcmotor.reverseAmotor()

    def stop(self):
        self.dcmotor.stopAmotor()

    def handle(self, order):
        '''
        orderの値をもとに、まがる。
        TODO:サーボモータの制御はコピペで全然理解してないの後で整理する。とりあえず40度回転で固定。
        :param order:
        :return:
        '''
        if order == b'd' :
            #右
            self.servo_motor.right()
        elif order == b'a':
            #左
            self.servo_motor.left()
        else:
            pass

    def crane(self,order):
        if order == b'h' :
            #右
            self.dcmotor.forwardBmotor()
        elif order == b'j':
            #左
            self.dcmotor.reverseBmotor()
        elif order == (b'a'):
            #ステアリングの命令は無視
            pass
        elif order == (b'd'):
            #ステアリングの命令は無視
            pass
        elif order == (b'w'):
            #アクセルの命令は無視
            pass
        elif order == (b's'):
            #アクセルの命令は無視
            pass
        else:
            self.dcmotor.stopBmotor()

class DCmotor_DRV8835:
    '''
    DRV8835メモ
    ModeはPMW
        AIN1:PHASE:PMW:motor_pin1
        AIN2:ENABLE:motor_pin2
        BIN1:PAHSE:motor_pin3
        BIN2:ENABLE:motor_pin4
    '''
    def __init__(self,motor_pin1, motor_pin2, motor_pin3, motor_pin4):
        self.motor_pin1 = motor_pin1
        self.motor_pin2 = motor_pin2
        self.motor_pin3 = motor_pin3
        self.motor_pin4 = motor_pin4


        pi.pinMode(self.motor_pin1, 1)
        pi.pinMode(self.motor_pin2, 1)
        pi.pinMode(self.motor_pin3, 1)
        pi.pinMode(self.motor_pin4, 1)

    def forwardAmotor(self):
        '''
        正転
        :return:
        '''
        print("{0},{1},forwardA".format(self.motor_pin1,self.motor_pin2))
        pi.digitalWrite(self.motor_pin1,1)
        pi.digitalWrite(self.motor_pin2,1)

    def reverseAmotor(self):
        '''
        逆転
        :return:
        '''
        print("{0},{1},reverseA".format(self.motor_pin1,self.motor_pin2))
        pi.digitalWrite(self.motor_pin1,0)
        pi.digitalWrite(self.motor_pin2,1)

    def stopAmotor(self):
        '''
        停止
        :return:
        '''
        print("{0},{1},forward".format(self.motor_pin1,self.motor_pin2))
        pi.digitalWrite(self.motor_pin1,0)
        pi.digitalWrite(self.motor_pin2,0)

    def forwardBmotor(self):
        '''
        正転
        :return:
        '''
        print("{0},{1},forwardA".format(self.motor_pin3,self.motor_pin4))
        pi.digitalWrite(self.motor_pin3,1)
        pi.digitalWrite(self.motor_pin4,1)

    def reverseBmotor(self):
        '''
        逆転
        :return:
        '''
        print("{0},{1},forward".format(self.motor_pin3,self.motor_pin4))
        pi.digitalWrite(self.motor_pin3,0)
        pi.digitalWrite(self.motor_pin4,1)

    def stopBmotor(self):
        '''
        停止
        :return:
        '''
        print("{0},{1},forward".format(self.motor_pin3,self.motor_pin4))
        pi.digitalWrite(self.motor_pin3,0)
        pi.digitalWrite(self.motor_pin4,0)




class DCmotor:
    '''
    TA7291のモータドライバーを使用する前提のクラス
    http://akizukidenshi.com/download/ta7291p.pdf

    TODO:
    PWM信号にすることで、モーターの電圧を擬似的にアプリ側から制御できる。
    pi.sofPWMCreate()
    pi.sotPWMWrite()
    モーターのスピードを変更できてもいいかもしれない


    '''
    def __init__(self, motor_pin1, motor_pin2):

        self.motor_pin1 = motor_pin1
        self.motor_pin2 = motor_pin2

        pi.pinMode(self.motor_pin1, 1)
        pi.pinMode(self.motor_pin2, 1)


    def forward(self):
        '''
        正転
        :return:
        '''
        print("{0},{1},forward".format(self.motor_pin1,self.motor_pin2))
        pi.digitalWrite(self.motor_pin1,1)
        pi.digitalWrite(self.motor_pin2,0)

    def reverse(self):
        '''
        逆転
        :return:
        '''
        print("{0},{1},reverse".format(self.motor_pin1,self.motor_pin2))
        pi.digitalWrite(self.motor_pin1,0)
        pi.digitalWrite(self.motor_pin2,1)

    def stop(self):
        '''
        停止
        :return:
        '''
        print("{0},{1},stop".format(self.motor_pin1,self.motor_pin2))
        pi.digitalWrite(self.motor_pin1,0)
        pi.digitalWrite(self.motor_pin2,0)


class ServoMotor:
    '''
    サーボモーターを制御するクラス
    TODO:全般的に理解してない
    '''

    RANGE = 2000
    CYCLE = 20  # Unit : ms
    SERVO_MIN = 0.5  # Unit : ms
    SERVO_MAX = 2.5  # Unit : ms

    clock = int( 19.2 / float(RANGE) * CYCLE * 1000 )

    SERVO_MIN_VALUE = int(SERVO_MIN * RANGE / CYCLE)
    SERVO_MAX_VALUE = int(SERVO_MAX * RANGE / CYCLE)

    def __init__(self, servo_motor_pin1):
        self.motor_pin1 = servo_motor_pin1

        pi.pinMode( self.motor_pin1, pi.GPIO.PWM_OUTPUT )
        pi.pwmSetMode( pi.GPIO.PWM_MODE_MS )
        pi.pwmSetRange( ServoMotor.RANGE )
        pi.pwmSetClock( ServoMotor.clock )


    def right(self, degree=60):
        '''
        右に40度固定でまげる
        :param degree:
        :return:
        '''

        tmp = int(float(ServoMotor.SERVO_MAX_VALUE - ServoMotor.SERVO_MIN_VALUE) / 180.0 * float(degree + 90)) + ServoMotor.SERVO_MIN_VALUE
        target = ServoMotor.SERVO_MAX_VALUE + ServoMotor.SERVO_MIN_VALUE - tmp
        pi.pwmWrite(self.motor_pin1, target)

    def left(self, degree=-60):
        '''
        左に40度固定でまげる
        :param degree:
        :return:
        '''

        tmp = int(float(ServoMotor.SERVO_MAX_VALUE - ServoMotor.SERVO_MIN_VALUE) / 180.0 * float(degree + 90)) + ServoMotor.SERVO_MIN_VALUE
        target = ServoMotor.SERVO_MAX_VALUE + ServoMotor.SERVO_MIN_VALUE - tmp
        pi.pwmWrite(self.motor_pin1, target)



if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Need Argument:motor or servo")
        sys.exit()

    if sys.argv[1] == "motor":
        dcmotor = DCmotor(motor_pin1=14,motor_pin2=15)
        dcmotor.forward()

    if sys.argv[1] == "stop":
        dcmotor = DCmotor(motor_pin1=14,motor_pin2=15)
        dcmotor.stop()


