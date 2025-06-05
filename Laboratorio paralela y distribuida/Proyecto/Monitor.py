import socket
import threading
import json
import time

estado_estaciones = {}
lock = threading.Lock()

def manejar_reporte(conn):
    data = conn.recv(1024).decode('utf-8')
    reporte = json.loads(data)
    with lock:
        estado_estaciones[reporte['id']] = reporte
    conn.close()

def monitor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 7777))  # Puerto del monitor
        s.listen()
        print("[Monitor] Esperando reportes de estaciones...")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=manejar_reporte, args=(conn,)).start()

def mostrar_estado():
    while True:
        time.sleep(2)
        with lock:
            print("\n[CARGA ACTUAL]")
            for estacion, datos in estado_estaciones.items():
                print(f"Estación {estacion}: {datos['pendientes']} pedidos en curso")
            print("-" * 30)

# Ejecutar en hilos paralelos
threading.Thread(target=monitor, daemon=True).start()
mostrar_estado()
