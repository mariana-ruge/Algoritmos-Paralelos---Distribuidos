import threading
import time
import random
import matplotlib.pyplot as plt

registro = []
lock = threading.Lock()
hilos_cocina = []

def preparar_pedido(pedido_id, pedido, cliente_id, tiempo_llegada):
    tiempo_inicio = time.time()
    time.sleep(random.uniform(1.5, 3.5))
    tiempo_fin = time.time()

    with lock:
        registro.append({
            'pedido_id': pedido_id,
            'cliente_id': cliente_id,
            'pedido': pedido,
            'llegada': tiempo_llegada,
            'inicio_preparacion': tiempo_inicio,
            'fin': tiempo_fin
        })
    print(f"[Cocina] Pedido {pedido_id} ({pedido}) para Cliente {cliente_id} listo.")

def manejar_cliente(pedido_id, cliente_id):
    pedidos = ["Capuchino", "Latte", "Americano"]
    pedido = random.choice(pedidos)
    tiempo_llegada = time.time()

    print(f"[Caja] Pedido recibido: {pedido} de Cliente {cliente_id}")
    time.sleep(random.uniform(0.2, 0.5))

    hilo_cocina = threading.Thread(
        target=preparar_pedido,
        args=(pedido_id, pedido, cliente_id, tiempo_llegada)
    )
    hilos_cocina.append(hilo_cocina)  # <--- Guardamos el hilo
    hilo_cocina.start()

def ejecutar_simulacion(num_clientes=5):
    hilos_clientes = []
    for i in range(num_clientes):
        hilo = threading.Thread(target=manejar_cliente, args=(i, i))
        hilos_clientes.append(hilo)
        hilo.start()
        time.sleep(0.3)

    for hilo in hilos_clientes:
        hilo.join()

    for hilo in hilos_cocina:  # <--- Esperamos los hilos de cocina
        hilo.join()

def graficar_resultados():
    if not registro:
        print("No hay datos para graficar.")
        return

    registro.sort(key=lambda r: r['llegada'])

    pedidos = [r['pedido_id'] for r in registro]
    llegadas = [r['llegada'] - registro[0]['llegada'] for r in registro]
    inicios = [r['inicio_preparacion'] - registro[0]['llegada'] for r in registro]
    finales = [r['fin'] - registro[0]['llegada'] for r in registro]

    plt.figure(figsize=(10, 5))
    for i in range(len(registro)):
        plt.plot(
            [llegadas[i], inicios[i]],
            [i, i],
            'r--',
            linewidth=2,
            label='Espera' if i == 0 else None
        )
        plt.plot(
            [inicios[i], finales[i]],
            [i, i],
            'g-',
            linewidth=4,
            label='Preparación' if i == 0 else None
        )

    plt.yticks(range(len(pedidos)), [f"Pedido {i}" for i in pedidos])
    plt.xlabel("Tiempo (segundos)")
    plt.title("Tiempos de espera y preparación de pedidos")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Ejecutar todo
ejecutar_simulacion(6)
graficar_resultados()
