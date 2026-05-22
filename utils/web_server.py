print("\n") # separate logs from default messages of editor

from machine import Pin, PWM
from utime import sleep
from json import dumps, loads
import socket

from utils.create_web_page import create_web_page
from utils.connect_to_wifi import connect_to_wifi
from utils.led import ceiling_led, shop_led

def send_response(conn, body, content_type = "text/plain"):
    if isinstance(body, str):
        body = body.encode("utf-8")

    header = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: " + content_type.encode("utf-8") + b"\r\n"
        b"Content-Length: " + str(len(body)).encode("utf-8") + b"\r\n"
        b"Connection: close\r\n"
        b"\r\n"
    )

    conn.sendall(header + body)


def web_server(station):

    # create web socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((station.ifconfig()[0], 80))
    s.listen(5) # max 5 socket connections // max possible should be 16


    # blink leds to signal its ready
    for _ in range(3):
        ceiling_led.set(0)
        shop_led.set(0)
        sleep(0.5)

        ceiling_led.set(100)
        shop_led.set(100)
        sleep(0.5)



    while True:
        conn, addr = s.accept()
        # print(f"got a connection from '{addr}'")

        try:
            # recieve data (of infinite length)
            request = b""
            while b"\r\n\r\n" not in request:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                request += chunk

            header_bytes, body = request.split(b"\r\n\r\n", 1)

            header_text = header_bytes.decode("utf-8")
            header_lines = header_text.split("\r\n")

            method, path, protocol = header_lines[0].split()

            headers = {}
            for line in header_lines[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip().lower()] = value.strip()

            content_type = headers.get("content-type")
            content_length = int(headers.get("content-length", "0"))

            # Read remaining body bytes, if recv() did not get all of it
            while len(body) < content_length:
                body += conn.recv(content_length - len(body))

            print("recieved request:", method, path, content_type)
            if content_type == 'application/json':
                data = loads(body.decode("utf-8"))
                print(data)

                if "ceiling" in data:
                    if data["ceiling"]:
                        ceiling_led.on()
                    else: ceiling_led.off()

                if "shop" in data:
                    if data["shop"]:
                        shop_led.on()
                    else: shop_led.off()

                if data.get("ceiling-toggle", False):
                    ceiling_led.toggle()

                if data.get("shop-toggle", False):
                    shop_led.toggle()

                if "ceiling-brightness" in data:
                    ceiling_led.set(data["ceiling-brightness"])
                if "shop-brightness" in data:
                    shop_led.set(data["shop-brightness"])

                response = dumps({"ok": True})
                send_response(conn, response, "application/json")

            else:
                response = create_web_page()
                send_response(conn, response, "text/html")



        except Exception as e:
            print("server error:", e)
            try:
                send_response(conn, dumps({"ok": False, "error": str(e)}), "application/json")
            except:
                pass

        finally:
            conn.close()
            sleep(0.01)


if __name__ == "__main__":

    station = connect_to_wifi()
    web_server(station)








