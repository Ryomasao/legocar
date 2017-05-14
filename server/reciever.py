# -*- coding: utf-8 -*-
import socket
import legocar_controller  as LegoCar

def recieve_order():
   '''
   クライアントsocketからデータを受け取ります。
   受け取るデータは、ASCの1文字を想定しています。
   受け取ったデータは、wirigpiを実装しているモジュールに渡します。

   TODO：ブロックキングのシングルスレッドで実装している。
         レゴカーのアクセルとハンドルは別スレッドで処理したほうがよいかも
   参考にさせていただいたサイト
   http://blog.amedama.jp/entry/2017/03/29/080000
   :return:
   '''

   serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

   #サーバ側のIPアドレスを入力
   host = ''

   port = 37564
   serversocket.bind((host,port))
   serversocket.listen(1)

   myLegoCar = LegoCar.LegoCarController()

   while True:
      clientsocket , (client_address,client_port) = serversocket.accept()
      print('New client: {0}:{1}'.format(client_address, client_port))

      while True:
         try:
            message = clientsocket.recv(1)
            print('Recv:{}'.format(message))
            #レゴカーのアクセル(前と後ろ)
            myLegoCar.accelerator(message)
            #レゴカーのハンドル(右と左)
            myLegoCar.handle(message)
         except OSError:
            print('OSError')
            myLegoCar.stop()
            break

         if len(message) == 0:
            #切断時は、レゴカーを止める
            myLegoCar.stop()
            break



      # 後始末
      clientsocket.close()
      print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


if __name__ == '__main__':
    recieve_order()