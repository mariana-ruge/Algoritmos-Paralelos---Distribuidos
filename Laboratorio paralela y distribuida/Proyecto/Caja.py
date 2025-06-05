import socket
import threading

def manejar_cliente(conn):
    data = conn.recv(1024).decode('utf-8')
    print(f"[Caja] Pedido recibido: {data}")
    conn.send("Tu pedido fue enviado a la cocina. Espera notificación.".encode('utf-8'))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cocina:
        cocina.connect(('localhost', 8888))  # Conectar con la Cocina
        cocina.send(data.encode('utf-8'))  # Reenviar datos completos

def servidor_caja():
    host = 'localhost'
    port = 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("[Caja] Esperando clientes...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=manejar_cliente, args=(conn,)).start()

servidor_caja()
