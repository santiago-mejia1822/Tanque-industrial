"""
Quiz #3
Realizado por: Daniel Francisco Lebro y Santiago Mejía.
Nos basamos en tus videos y en otros videos de desarrollo similar.
Gracias.
"""
#Librerías a emplear para el desarrollo de la aplicación
import numpy as np
import matplotlib.pyplot as plt
import os

#Creación de la clase para establecer un molde del objeto.
class Tanque:
    """Clase que simula el tanque de agua"""

    @staticmethod #Método estático que le pide al usuario por una altura inicial del tanque.
    def solicitar_altura_inicial():
        while True: #Control de datos de entrada.
            try:
                altura = float(input("Ingrese la altura inicial del tanque (en metros): "))
                if altura < 0:
                    print("La altura no puede ser negativa. Intente nuevamente.")
                    continue
                return altura
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico válido.")

    @staticmethod #Método estático que le pide al usuario por una área en m^2 del tanque.
    def solicitar_area_tanque():
        while True: #Control de datos de entrada.
            try:
                area = float(input("Ingrese el área del tanque (en metros cuadrados): "))
                if area <= 0:
                    print("El área debe ser un valor positivo mayor que cero. Intente nuevamente.")
                    continue
                return area
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico válido.")

    @staticmethod #Método estático que le pide al usuario por una cte de la primera válvula del tanque.
    def solicitar_constante_valvula_entrada():
        while True: #Control de datos de entrada.
            try:
                k1 = float(input("Ingrese la constante de la válvula de entrada: "))
                if k1 <= 0:
                    print("La constante de la válvula de entrada debe ser un valor positivo mayor que cero. Intente nuevamente.")
                    continue
                return k1
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico válido.")

    @staticmethod #Método estático que le pide al usuario por una cte de la segunda válvula del tanque.
    def solicitar_constante_valvula_salida(): 
        while True: #Control de datos de entrada.
            try:
                k2 = float(input("Ingrese la constante de la válvula de salida: "))
                if k2 <= 0:
                    print("La constante de la válvula de salida debe ser un valor positivo mayor que cero. Intente nuevamente.")
                    continue
                return k2
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico válido.")

    @staticmethod #Método estático que le pide al usuario por un diferencial de tiempo de simulación de la aplicación.
    def solicitar_tiempo_simulacion():
        while True: #Control de datos de entrada.
            try:
                tiempo = int(input("Ingrese el tiempo total de la simulación en segundos: "))
                if tiempo <= 0:
                    print("El tiempo de simulación debe ser un valor positivo mayor que cero. Intente nuevamente.")
                    continue
                return tiempo
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico entero válido.")

    @staticmethod #Método estático que le pide al usuario por un valor de tiempo para el paso de flujo del tanque.
    def solicitar_paso_tiempo():
        while True: #Control de datos de entrada.
            try:
                paso_tiempo = int(input("Ingrese el paso de tiempo en segundos: "))
                if paso_tiempo <= 0:
                    print("El paso de tiempo debe ser un valor positivo mayor que cero. Intente nuevamente.")
                    continue
                return paso_tiempo
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico entero válido.")

    @staticmethod #Método estático que le pide al usuario por una constante alpha que conforma la isoporcentual del tanque.
    def solicitar_constante_alpha():
        while True: #Control de datos de entrada.
            try:
                alpha = int(input("Ingrese la constante alpha para la válvula isoporcentual (10 o 100): "))
                if alpha not in [10, 100]:
                    print("La constante alpha debe ser 10 o 100. Intente nuevamente.")
                    continue
                return alpha
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico entero válido.")

    @staticmethod #Método estático que le pide al usuario por un valor de apertura (0 ó 1) de las válvulas. del tanque.
    def solicitar_apertura_valvula_entrada():
        while True: #Control de datos de entrada.
            try:
                apertura = float(input("Ingrese la apertura de la válvula de entrada (entre 0 y 1): "))
                if not 0 <= apertura <= 1:
                    print("La apertura debe estar en el rango de 0 a 1. Intente nuevamente.")
                    continue
                return apertura
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico válido.")

    @staticmethod #Método estático que le pide al usuario por un valor de cerradura (0 ó 1) de las válvulas del tanque.
    def solicitar_apertura_valvula_salida():
        while True: #Control de datos de entrada.
            try:
                apertura = float(input("Ingrese la apertura de la válvula de salida (entre 0 y 1): "))
                if not 0 <= apertura <= 1:
                    print("La apertura debe estar en el rango de 0 a 1. Intente nuevamente.")
                    continue
                return apertura
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un valor numérico válido.")


    def __init__(self, h0, A, k1, k2, t, p, alpha, a1, a2): #Origen de método constructor con atributos del objeto.
        self.h0 = h0  #Altura inicial del tanque
        self.A = A  #Área transversal del tanque
        self.k1 = k1  #Constante de la válvula de entrada
        self.k2 = k2  #Constante de la válvula de salida
        self.t = t  #Tiempo total de la simulación
        self.p = p  #Paso de tiempo
        self.alpha = alpha  #Constante alpha para la válvula isoporcentual
        self.a1 = a1  #Apertura de la válvula de entrada
        self.a2 = a2  #Apertura de la válvula de salida
        #Funciones de Numpy.
        self.x = np.arange(0, self.t + 1, self.p)  #Vector de tiempo
        self.y = np.zeros(self.t + 1)  #Altura del tanque para válvula lineal
        self.y1 = np.zeros(self.t + 1)  #Altura del tanque para válvula de abertura rápida
        self.y2 = np.zeros(self.t + 1)  #Altura del tanque para válvula isoporcentual

    def valvula_lineal(self):
        """Simulación del tanque con válvula lineal"""
        self.y[0] = self.h0 #Lógica operativa para establecer en la gráfica.
        for i in range(1, len(self.x)):
            self.y[i] = self.y[i - 1] + (
                (self.p * (1 / self.A)) * (self.k1 * self.a1 - self.k2 * self.a2 * self.y[i - 1])
            )

    def valvula_abertura_rapida(self):
        """Simulación del tanque con válvula de abertura rápida"""
        self.y1[0] = self.h0 #Lógica operativa para establecer en la gráfica.
        for i in range(1, len(self.x)):
            self.y1[i] = self.y1[i - 1] + (
                (self.p * (1 / self.A)) * (self.k1 * np.sqrt(self.a1) - self.k2 * self.a2 * self.y1[i - 1])
            )

    def valvula_abertura_lenta_o_isoporcentual(self):
        """Simulación del tanque con válvula de abertura lenta o isoporcentual"""
        self.y2[0] = self.h0 #Lógica operativa para establecer en la gráfica.
        for i in range(1, len(self.x)):
            self.y2[i] = self.y2[i - 1] + (
                (self.p * (1 / self.A)) * (self.k1 * self.alpha**((self.a1 - 1)) - self.k2 * self.a2 * self.y2[i - 1])
            )

    def grafica_altura_tanque(self): #Con los equivalentes anteriores se emplean para esta función a continuar.
        """Genera la gráfica de la altura del tanque para las tres configuraciones de válvula"""
        plt.plot(self.x, self.y, label="Válvula Lineal", color="red", linestyle=":")
        plt.plot(self.x, self.y1, label="Válvula Abertura Rápida", color="green", linestyle="--")
        plt.plot(self.x, self.y2, label="Válvula Abertura Lenta o Isoporcentual", color="blue", linestyle="-")
        plt.legend(loc="best")
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Altura (m)')
        plt.title('Nivel del Tanque')
        plt.grid(True)
        #plt.gca().set_yticks(np.arange(0, max(self.y1) + 0.5, 0.2))
        plt.show()

#Función que lo identifica como programa principal.
if __name__ == "__main__":
    #Parámetros iniciales

    #Solicitar la altura inicial del tanque
    h0 = Tanque.solicitar_altura_inicial()

    #Solicitar el área del tanque
    A = Tanque.solicitar_area_tanque()

    #Solicitar la constante de la válvula de entrada
    k1 = Tanque.solicitar_constante_valvula_entrada()

    #Solicitar la constante de la válvula de salida
    k2 = Tanque.solicitar_constante_valvula_salida()

    #Solicitar el tiempo total de la simulación
    t = Tanque.solicitar_tiempo_simulacion()

    #Solicitar el paso de tiempo
    p = Tanque.solicitar_paso_tiempo()

    #Solicitar la constante alpha para la válvula isoporcentual
    alpha = Tanque.solicitar_constante_alpha()

    #Solicitar la apertura de la válvula de entrada
    a1 = Tanque.solicitar_apertura_valvula_entrada()

    #Solicitar la apertura de la válvula de salida
    a2 = Tanque.solicitar_apertura_valvula_salida()

    #Crear objeto Tanque
    tanque = Tanque(h0, A, k1, k2, t, p, alpha, a1, a2)

    #Ejecutar simulaciones
    tanque.valvula_lineal()
    tanque.valvula_abertura_rapida()
    tanque.valvula_abertura_lenta_o_isoporcentual()

    #Generar la gráfica de resultados
    tanque.grafica_altura_tanque()

print("\n\nGracias por usar nuestra aplicación. Buen día.") #La buena mi papá-ya.
