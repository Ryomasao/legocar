# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO,emit
import legocar_controller  as LegoCar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


myLegoCar = LegoCar.LegoCarController()

#ハンドルの角度をコントロールするために、ここにdegreeを持っておく。
#この変数はrecieve_order関数内から更新・参照される。
Degree = 0

#Flask限定の話なのかよくわからないけれども、関数内でDegreeを使うときは、global 変数名　と宣言した後にDegreeを使う。
#https://stackoverflow.com/questions/35309042/python-how-to-set-global-variables-in-flask
@socketio.on('connect',namespace='/legocar')
def init() :
    print('connected')

@socketio.on('sendMessage',namespace='/legocar')
def recieve_order(order) :
#TODO ひどいコードなので直したい
    if order in {'forward'}:
       print("accell forward " +order)
       #レゴカーのアクセル(前)
       myLegoCar.accelerator(b"w")
       testmethod(order)
    elif order in {'back'}:
        print("accell back " +order)
        #レゴカーのアクセル(後)
        myLegoCar.accelerator(b"s")
        testmethod(order)
    elif order in {'break'}:
        print("accell stop " +order)
        myLegoCar.accelerator(b"f")
        testmethod(order)
    elif order in {'right'}:
       global Degree
       Degree += 10
       print("handle = " +order)
       #レゴカーのハンドル(右)
       myLegoCar.handle(b"d",Degree)
       testmethod(order)
    elif order in {'left'}:
        print("handle = " +order)
        global Degree
        Degree -= 10
        #レゴカーのハンドル(右と左)
        myLegoCar.handle(b"a",Degree)
        testmethod(order)
    elif order in {'crane_left'}:
        print("handle = " +order)
        #クレーンの左回転
        myLegoCar.crane(b"h")
        testmethod(order)
    elif order in {'crane_right'}:
        print("handle = " +order)
        #クレーンの右回転
        myLegoCar.crane(b"j")
        testmethod(order)
    elif order in {'crane_stop'}:
        print("handle = " +order)
        #クレーンストップ
        myLegoCar.crane(b"g")
        testmethod(order)
    else:
        pass


@socketio.on('test',namespace='/legocar')
def testmethod(order):
    emit('test',order)



if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=6677)
