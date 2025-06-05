import socket
import threading
import time
import random

# Lista de estaciones disponibles (puedes ampliarla)
ESTACIONES = [9001, 9002]  # Puertos de las estaciones

def enviar_a_estacion(pedido):
    for puerto in ESTACIONES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as estacion:
                estacion.connect(('localhost', puerto))
                estacion.send(pedido.encode('utf-8'))
                print(f"[Cocina] Pedido enviado a estación en puerto {puerto}")
                return  # Se envió exitosamente
        except Exception as e:
            print(f"[Cocina] No se pudo conectar a estación {puerto}: {e}")
    print("[Cocina] Ninguna estación disponible.")

def preparar_pedido(data):
    try:
        print(f"[Cocina] Reenviando pedido a estación...")
        enviar_a_estacion(data)
        # Aquí ya no se prepara ni notifica al cliente directamente
    except Exception as e:
        print("[Cocina] Error al reenviar pedido:", e)

def servidor_cocina():
    host = 'localhost'
    port = 8888
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("[Cocina] Esperando pedidos...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                threading.Thread(target=preparar_pedido, args=(data,)).start()

servidor_cocina()


