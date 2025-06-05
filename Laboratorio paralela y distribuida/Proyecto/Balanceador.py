import socket
import threading
import random

estaciones = [("localhost", 9001), ("localhost", 9002), ("localhost", 9003)]

def manejar_pedido(conn):
    data = conn.recv(1024).decode('utf-8')
    print(f"[Balanceador] Pedido recibido: {data}")
    
    # Selección aleatoria o basada en política (ej. round-robin o carga)
    host, port = random.choice(estaciones)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(data.encode('utf-8'))

def balanceador():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 8888))
        s.listen()
        print("[Balanceador] Esperando pedidos de Caja...")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=manejar_pedido, args=(conn,)).start()

balanceador()
