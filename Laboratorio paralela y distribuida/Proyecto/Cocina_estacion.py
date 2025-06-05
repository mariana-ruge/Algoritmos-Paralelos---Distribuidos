import socket
import threading
import time
import json
import random

id_estacion = "E1"  # Cambia a E2, E3 en otras instancias
pedidos_en_curso = []
lock = threading.Lock()

def reportar_monitor():
    while True:
        time.sleep(2)
        with lock:
            data = {
                'id': id_estacion,
                'pendientes': len(pedidos_en_curso)
            }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('localhost', 7777))
                s.send(json.dumps(data).encode('utf-8'))
            except:
                pass  # El monitor puede estar apagado

def preparar_pedido(pedido):
    with lock:
        pedidos_en_curso.append(pedido)
    time.sleep(random.uniform(2, 4))
    with lock:
        pedidos_en_curso.remove(pedido)
    print(f"[{id_estacion}] Pedido {pedido} listo.")

def servidor_cocina():
    host = 'localhost'
    port = 9001  # Diferente para cada estación
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[{id_estacion}] Esperando pedidos...")
        while True:
            conn, _ = s.accept()
            data = conn.recv(1024).decode('utf-8')
            pedido = data.strip()
            threading.Thread(target=preparar_pedido, args=(pedido,)).start()

# Iniciar hilos
threading.Thread(target=reportar_monitor, daemon=True).start()
servidor_cocina()
