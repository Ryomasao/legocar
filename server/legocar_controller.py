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
        #self.servo_motor = ServoMotor(18)
        self.servo_motor = NewServoMotor(18)

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

    def handle(self, order, degree):
        '''
        orderの値をもとに、まがる。
        TODO:サーボモータの制御はコピペで全然理解してないの後で整理する。とりあえず40度回転で固定。
        :param order:
        :return:
        '''
        if order == b'd' :
            #右
            #self.servo_motor.right(degree)
            self.servo_motor.plusRotation()
        elif order == b'a':
            #左
            #self.servo_motor.left(degree)
            self.servo_motor.minusRotation()
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


    def right(self, degree=10):
        '''
        右に10度固定でまげる
        :param degree:
        :return:
        '''

        tmp = int(float(ServoMotor.SERVO_MAX_VALUE - ServoMotor.SERVO_MIN_VALUE) / 180.0 * float(degree + 90)) + ServoMotor.SERVO_MIN_VALUE
        target = ServoMotor.SERVO_MAX_VALUE + ServoMotor.SERVO_MIN_VALUE - tmp
        pi.pwmWrite(self.motor_pin1, target)

    def left(self, degree=-10):
        '''
        左に10度固定でまげる
        :param degree:
        :return:
        '''

        tmp = int(float(ServoMotor.SERVO_MAX_VALUE - ServoMotor.SERVO_MIN_VALUE) / 180.0 * float(degree + 90)) + ServoMotor.SERVO_MIN_VALUE
        target = ServoMotor.SERVO_MAX_VALUE + ServoMotor.SERVO_MIN_VALUE - tmp
        pi.pwmWrite(self.motor_pin1, target)


class NewServoMotor:
    '''
    サーボモータを制御するクラス
    少しだけ仕組みを理解した上で、かいてみる
    SG5010、SG90のサーボモータに対応している。
    具体的には以下の仕様に依存している。

        制御パルス:0.5ms〜2.4ms
        PWMサイクル:20ms

    '''

    #制御パルス、PWMサイクル、pwmWrite関数の仕様により求められるduty比
    MIN_DUTY = 26;   #-90度
    MAX_DUTY = 123;  # 90度
    MID_DUTY =  MAX_DUTY - MIN_DUTY   # 0度

    #サーボモータを曲げる角度を定義しておく。
    # 大胆に曲げたい場合は、この数字を大きくしよう。最大90度かな。
    # 細かく制御したい場合は、この数字を小さくしよう。最小1度かな。
    ANGLE_BEND = 10;

    #ANGLE_BENDが全体(180度)に対して占める割合
    RATIO_OF_ANGLE_BEND = int( 180 / ANGLE_BEND)

    #ANGLE_BENDを実現するためduty比
    ANGLE_BEND_DUTY = int( (MAX_DUTY - MIN_DUTY) / RATIO_OF_ANGLE_BEND)

    #もしduty比が1未満になっちゃったらduty比1としよう。
    if ANGLE_BEND_DUTY == 0 : ANGLE_BEND_DUTY = 1



    def __init__(self, servo_motor_pin1):
        self.motor_pin1 = servo_motor_pin1
        #ピンの割り当て
        pi.pinMode( self.motor_pin1, pi.GPIO.PWM_OUTPUT )

        #duty比を変更すると周波数がかわってしまうので、固定するための設定、あまりわかってない。
        pi.pwmSetMode( pi.GPIO.PWM_MODE_MS )

        #周波数を50Hzにすると、18750/周波数=375 あまりわかってない。
        pi.pwmSetClock(375)

        #起動時にタイヤをまっすぐにしとく
        self.dutyState = NewServoMotor.MID_DUTY;
        pi.pwmWrite(self.motor_pin1,self.dutyState);


    def minusRotation(self):
        '''
        マイナス側にサーボモータを回転させる。
        曲がる角度は、クラス変数 ANGLE_BENDで指定した角度。
        :return:
        '''
        self.dutyState -= NewServoMotor.ANGLE_BEND_DUTY;
        print(NewServoMotor.ANGLE_BEND_DUTY)
        print(self.dutyState)

        #限界(-90度)を超える場合は、-90度とする
        if(self.dutyState < NewServoMotor.MIN_DUTY):
            self.dutyState =  NewServoMotor.MIN_DUTY

        pi.pwmWrite(self.motor_pin1,self.dutyState);

    def plusRotation(self):
        '''
        プラス側にサーボモータを回転させる。
        minusRotationと同様。
        :return:
        '''
        self.dutyState += NewServoMotor.ANGLE_BEND_DUTY;
        print(self.dutyState)

        #限界(90度)を超える場合は、90度とする
        if(self.dutyState > NewServoMotor.MAX_DUTY):
            self.dutyState =  NewServoMotor.MAX_DUTY

        pi.pwmWrite(self.motor_pin1,self.dutyState);



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


