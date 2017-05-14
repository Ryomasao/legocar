# -*- coding: utf-8 -*-
import sys
import termios
import tty
import socket

def send_order(host):
    '''
    キーボードから入力した文字を一文字ごと、ソケット通信で通信先に送る。
    qを押すと終了する。
    参考サイト：
    キー入力
    http://qiita.com/tortuepin/items/e6c72f48115f20744ace
    socket
    http://qiita.com/nadechin/items/28fc8970d93dbf16e81b
    :return:
    '''

    #標準入力のファイルディスクリプタを取得する
    fd = sys.stdin.fileno()

    #処理が終わった後に元に戻すよう
    old = termios.tcgetattr(fd)

    #接続先の情報
    port = 37564

    #接続した状態のソケットを取得する
    mysocket = connect_socket(host, port)

    #接続できなかった場合、処理を終える
    if mysocket == None:
        return

    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            ch = sys.stdin.read(1)

            if ch == "q":
                break

            #メッセージ送信処理
            send_message(mysocket, ch)

    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
        mysocket.close()



def connect_socket(host, port):
    '''
    socket通信で引数で指定した接続先に接続します。
    その後、接続した状態のソケットを返却します。

    接続処理でエラーがあった場合、Noneを返します。

    :param host:
    :param port:
    :return:接続した状態のソケット、接続に失敗するとNoneを返します。
    '''

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #タイムアウト時間の設定(秒)、設定しなければデフォルト120秒？
    mysocket.settimeout(5)

    #接続処理
    try:
        mysocket.connect((host, port))
    except socket.error as e:
        print("Socket Error! {0}".format(e))
        return None

    return mysocket

def send_message(socket, messeage):
   '''
   接続した状態のsocketを受け取って、messageを接続先に送ります。
   :param socket:
   :param messeage:
   :return:
   '''

   #送信メッセージの全体長
   len_messeage = len(messeage)

   #送信したデータの長さ
   total_sent = 0

  #送信したデータが全部送りおえるまで送信処理を行う。
   while total_sent < len_messeage:
       #送信処理、utfにエンコードしてあげなきゃいけないみたい
       len_sent = socket.send(messeage.encode('utf-8'))
       print(messeage)

       if len_sent == 0:
           raise OSError

       total_sent += len_sent

if __name__ == '__main__':

    #接続先ホストアドレスがない場合終了
    if len(sys.argv ) != 2:
        print("Need Host Address")
        sys.exit()

    host = sys.argv[1]

    #命令送信処理
    send_order(host)
