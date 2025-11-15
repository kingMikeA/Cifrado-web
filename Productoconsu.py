# productor_consumidor.py
import threading
import time
import random
from queue import Queue, Empty
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

class Buffer:
    """Buffer thread-safe para el problema productor-consumidor"""
    
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.queue = Queue(maxsize=tamaño)
        self.items_producidos = 0
        self.items_consumidos = 0
        self.lock_stats = threading.Lock()
    
    def producir(self, item, productor_id):
        """Produce un item en el buffer"""
        self.queue.put(item, block=True)  # Bloquea si está lleno
        
        with self.lock_stats:
            self.items_producidos += 1
        
        logging.info(f"Productor {productor_id} produjo item {item}. "
                     f"Buffer size: {self.queue.qsize()}")
    
    def consumir(self, consumidor_id, timeout=None):
        """Consume un item del buffer"""
        try:
            item = self.queue.get(block=True, timeout=timeout)
            
            with self.lock_stats:
                self.items_consumidos += 1
            
            logging.info(f"Consumidor {consumidor_id} consumió item {item}. "
                         f"Buffer size: {self.queue.qsize()}")
            
            self.queue.task_done()
            return item
            
        except Empty:
            return None
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del buffer"""
        with self.lock_stats:
            return {
                'items_producidos': self.items_producidos,
                'items_consumidos': self.items_consumidos,
                'buffer_actual': self.queue.qsize(),
                'buffer_tamaño': self.tamaño
            }

class Productor(threading.Thread):
    """Clase productor que hereda de Thread"""
    
    def __init__(self, id_productor, buffer, items_a_producir, tiempo_min=0.1, tiempo_max=0.5):
        super().__init__(name=f"Productor-{id_productor}")
        self.id = id_productor
        self.buffer = buffer
        self.items_a_producir = items_a_producir
        self.tiempo_min = tiempo_min
        self.tiempo_max = tiempo_max
    
    def run(self):
        """Método que se ejecuta cuando inicia el hilo"""
        logging.info(f"Iniciado")
        
        for i in range(self.items_a_producir):
            # Generar item
            item = f"P{self.id}-Item{i+1}-{random.randint(1, 100)}"
            
            # Producir item
            self.buffer.producir(item, self.id)
            
            # Simular tiempo de producción
            tiempo_espera = random.uniform(self.tiempo_min, self.tiempo_max)
            time.sleep(tiempo_espera)
        
        logging.info(f"Terminado - Produjo {self.items_a_producir} items")

class Consumidor(threading.Thread):
    """Clase consumidor que hereda de Thread"""
    
    def __init__(self, id_consumidor, buffer, tiempo_limite=None, tiempo_min=0.2, tiempo_max=0.8):
        super().__init__(name=f"Consumidor-{id_consumidor}")
        self.id = id_consumidor
        self.buffer = buffer
        self.tiempo_limite = tiempo_limite
        self.tiempo_min = tiempo_min
        self.tiempo_max = tiempo_max
        self.items_consumidos = 0
    
    def run(self):
        """Método que se ejecuta cuando inicia el hilo"""
        logging.info(f"Iniciado")
        
        tiempo_inicio = time.time()
        
        while True:
            # Verificar límite de tiempo
            if self.tiempo_limite and (time.time() - tiempo_inicio) > self.tiempo_limite:
                break
            
            # Consumir item
            item = self.buffer.consumir(self.id, timeout=2)
            
            if item is None:
                logging.info(f"Timeout - No hay items disponibles")
                break
            
            self.items_consumidos += 1
            
            # Simular tiempo de procesamiento
            tiempo_espera = random.uniform(self.tiempo_min, self.tiempo_max)
            time.sleep(tiempo_espera)
        
        logging.info(f"Terminado - Consumió {self.items_consumidos} items")

def ejecutar_simulacion():
    """Ejecuta la simulación completa"""
    print("=== SIMULACIÓN PRODUCTOR-CONSUMIDOR ===")
    
    # Configuración
    tamaño_buffer = 5
    num_productores = 3
    num_consumidores = 2
    items_por_productor = 10
    tiempo_simulacion = 20
    
    print(f"Configuración:")
    print(f"  Buffer size: {tamaño_buffer}")
    print(f"  Productores: {num_productores} (c/u produce {items_por_productor} items)")
    print(f"  Consumidores: {num_consumidores}")
    print(f"  Tiempo límite: {tiempo_simulacion} segundos")
    print()
    
    # Crear buffer compartido
    buffer = Buffer(tamaño_buffer)
    
    # Crear productores
    productores = []
    for i in range(num_productores):
        productor = Productor(i+1, buffer, items_por_productor)
        productores.append(productor)
    
    # Crear consumidores
    consumidores = []
    for i in range(num_consumidores):
        consumidor = Consumidor(i+1, buffer, tiempo_simulacion)
        consumidores.append(consumidor)
    
    # Iniciar todos los hilos
    inicio_simulacion = time.time()
    
    for productor in productores:
        productor.start()
    
    for consumidor in consumidores:
        consumidor.start()
    
    # Monitorear progreso
    while any(p.is_alive() for p in productores) or any(c.is_alive() for c in consumidores):
        stats = buffer.obtener_estadisticas()
        print(f"\nEstado actual:")
        print(f"  Items producidos: {stats['items_producidos']}")
        print(f"  Items consumidos: {stats['items_consumidos']}")
        print(f"  En buffer: {stats['buffer_actual']}/{stats['buffer_tamaño']}")
        print(f"  Threads activos: {threading.active_count()}")
        
        time.sleep(2)
    
    # Esperar a que terminen todos los hilos
    for productor in productores:
        productor.join()
    
    for consumidor in consumidores:
        consumidor.join()
    
    fin_simulacion = time.time()
    
    # Estadísticas finales
    stats_finales = buffer.obtener_estadisticas()
    print(f"\n=== RESULTADOS FINALES ===")
    print(f"Tiempo total: {fin_simulacion - inicio_simulacion:.2f} segundos")
    print(f"Items producidos: {stats_finales['items_producidos']}")
    print(f"Items consumidos: {stats_finales['items_consumidos']}")
    print(f"Items restantes en buffer: {stats_finales['buffer_actual']}")
    
    # Estadísticas por consumidor
    print(f"\nItems consumidos por consumidor:")
    for consumidor in consumidores:
        print(f"  {consumidor.name}: {consumidor.items_consumidos} items")
    
    # Verificar balance
    total_esperado = num_productores * items_por_productor
    total_procesado = stats_finales['items_consumidos'] + stats_finales['buffer_actual']
    
    if stats_finales['items_producidos'] == total_esperado:
        print("✓ Todos los items fueron producidos correctamente")
    else:
        print(f"⚠ Discrepancia en producción: esperado {total_esperado}, real {stats_finales['items_producidos']}")
    
    if total_procesado == stats_finales['items_producidos']:
        print("✓ Balance correcto: producidos = consumidos + en_buffer")
    else:
        print(f"⚠ Error de balance detectado")

if __name__ == "__main__":
    ejecutar_simulacion()