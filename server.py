import socket
import threading

def handle_client(client_socket, clients):
    nickname = client_socket.recv(1024).decode('utf-8')
    print(f"[Новый Подключившийся] {nickname}")
    broadcast(f"[{nickname} присоединился к чату]".encode('utf-8'), clients)
    while True:
        try:
            message = client_socket.recv(1024)
            broadcast(f"{nickname}: ".encode('utf-8') + message, clients)
        except:
            # Удаляем клиента из списка и сообщаем о его отключении
            clients.remove(client_socket)
            broadcast(f"[{nickname} покинул чат]".encode('utf-8'), clients)
            client_socket.close()
            break

def broadcast(message, clients):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen()
    print("[Запуск] Сервер запущен и ожидает подключения клиентов...")

    clients = []
    
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, clients))
        thread.start()

if __name__ == "__main__":
    start_server()