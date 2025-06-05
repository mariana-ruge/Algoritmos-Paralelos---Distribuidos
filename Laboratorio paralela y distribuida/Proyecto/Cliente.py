import socket
import threading
import random
import time

def escuchar_cliente(cliente_id, puerto_cliente):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", puerto_cliente))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            mensaje = conn.recv(1024).decode('utf-8')
            print(f"[Cliente {cliente_id}] Notificación de cocina: {mensaje}")

def cliente(cliente_id):
    pedidos = ["Capuchino", "Latte", "Americano"]
    pedido = random.choice(pedidos)
    puerto_cliente = 10000 + cliente_id  # Cada cliente escucha en un puerto diferente

    threading.Thread(target=escuchar_cliente, args=(cliente_id, puerto_cliente)).start()
    time.sleep(0.5)  # Esperar a que el servidor cliente esté escuchando

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 9999))  # Conectarse a Caja
        mensaje = f"{pedido};{cliente_id};localhost;{puerto_cliente}"
        s.send(mensaje.encode('utf-8'))
        respuesta = s.recv(1024).decode('utf-8')
        print(f"[Cliente {cliente_id}] Caja dice: {respuesta}")

# Crear varios clientes
for i in range(3):
    threading.Thread(target=cliente, args=(i,)).start()
