from utils.connect_to_wifi import connect_to_wifi
from utils.create_web_page import create_web_page

from json import loads

station = connect_to_wifi()

# create socket
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((station.ifconfig()[0], 80))
s.listen(5) # max 5 socket connections // max possible should be 16

print(station.ifconfig())

starting_up = False
while True:
    conn, addr = s.accept()
    

    # recieve data
    response = None
    request = str(conn.recv(1024))
    #print('Content = %s' % str(request))

    
    method, path, protocol = request.split(r'\r\n')[0].split()
    headers = dict(x.split(': ') for x in request.split(r'\r\n')[1:-2])
    content_type = headers.get('Content-Type')
    
    #print(method)
    
    if content_type == 'application/json':
        #print(request.split('\r\n\r\n'))
        data = str(request).split('\\r\\n\\r\\n')[1][:-1] # :-1 to remove apices
        data = loads(data)
        print(f"{addr[0]}: {data['msg']}")
        

    
    response = create_web_page()

    
    # Create a socket reply and close
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()