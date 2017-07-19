# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO,emit
#import legocar_controller  as LegoCar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


#myLegoCar = LegoCar.LegoCarController()


@socketio.on('connect',namespace='/legocar')
def init() :
    print('connected')

@socketio.on('sendMessage',namespace='/legocar')
def recieve_order(order) :

    if order in {'forward','back'}:
       print("accell = " +order)
       testmethod(order)
    elif order in {'break'}:
        print("accell stop = " +order)
        testmethod(order)
    elif order in {'right','left'}:
       print("handle = " +order)
       testmethod(order)
    else:
        pass


@socketio.on('test',namespace='/legocar')
def testmethod(order):
    emit('test',order)



if __name__ == '__main__':
    socketio.run(app)