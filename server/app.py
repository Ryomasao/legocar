# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO,emit
import legocar_controller  as LegoCar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


myLegoCar = LegoCar.LegoCarController()


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
       print("handle = " +order)
       #レゴカーのハンドル(右)
       myLegoCar.handle(b"d")
       testmethod(order)
    elif order in {'left'}:
        print("handle = " +order)
        #レゴカーのハンドル(右と左)
        myLegoCar.handle(b"a")
        testmethod(order)
    elif order in {'crane_left'}:
        print("handle = " +order)
        #クレーンの左回転
        myLegoCar.crane(b"h")
        testmethod(order)
    elif order in {'crane_left'}:
        print("handle = " +order)
        #クレーンの右回転
        myLegoCar.crane(b"j")
        testmethod(order)
    elif order in {'crane_left'}:
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
    socketio.run(app,host='0.0.0.0',port=5000)