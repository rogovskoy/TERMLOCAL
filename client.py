import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Ошибка при получении данных!")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input('')
        client_socket.send(message.encode('utf-8'))

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))

    nickname = input("Введите ваш ник: ")
    client.send(nickname.encode('utf-8'))

    # Запустим потоки для получения и отправки сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

if __name__ == "__main__":
    start_client()