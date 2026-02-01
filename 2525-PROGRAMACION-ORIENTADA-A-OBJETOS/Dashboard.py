# Dashboard 
# Aplicación de principios POO:
# - Encapsulación
# - Modularidad

import os
import subprocess

class Proyecto:
    # Se creó la clase Proyecto para encapsular la información general del sistema
    # Gestiona la estructura del proyecto y sus rutas.
    
    def __init__(self):
        self.ruta_base = os.path.dirname(__file__)
        self.unidades = {
            "1": "Unidad 1",
            "2": "Unidad 2"
        }

    def obtener_unidad(self, opcion):
        return self.unidades.get(opcion, None)

class ScriptManager:

    # Esta clase se creó para separar la responsabilidad de leer y ejecutar scripts.
    # Administra la lectura y ejecución de scripts.

    def mostrar_codigo(self, ruta_script):
        try:
            with open(ruta_script, "r", encoding="utf-8") as archivo:
                print("\n--- Código del Script ---\n")
                print(archivo.read())
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    def ejecutar(self, ruta_script):
        try:
            if os.name == "nt":
                subprocess.Popen(["cmd", "/k", "python", ruta_script])
            else:
                subprocess.Popen(["xterm", "-e", "python3", ruta_script])
        except Exception as e:
            print(f"Error al ejecutar el script: {e}")

class Menu:
    # Se creó esta clase para centralizar la lógica de los menús.
    # Maneja la interacción con el usuario.
    

    def mostrar(self, titulo, opciones):
        print(f"\n=== {titulo} ===")
        for clave, valor in opciones.items():
            print(f"{clave}. {valor}")
        print("0. Volver")

        return input("Seleccione una opción: ")

class Dashboard:
    
    # Clase principal que coordina el funcionamiento del sistema.
    

    def __init__(self):
       
       # CAMBIO: composición de objetos (POO)
        self.proyecto = Proyecto()
        self.menu = Menu()
        self.script_manager = ScriptManager()

    def iniciar(self):

       # Método principal que controla la ejecución del programa.
        while True:
            opcion = self.menu.mostrar(
                "MENÚ PRINCIPAL",
                self.proyecto.unidades
            )

            if opcion == "0":
                print("Saliendo del sistema...")
                break

            unidad = self.proyecto.obtener_unidad(opcion)
            if unidad:
                self.gestionar_unidad(unidad)
            else:
                print("Opción inválida.")

    def gestionar_unidad(self, nombre_unidad):

       # Método específico para gestionar una unidad.

        ruta_unidad = os.path.join(self.proyecto.ruta_base, nombre_unidad)
        temas = [d.name for d in os.scandir(ruta_unidad) if d.is_dir()]

        opciones = {str(i + 1): tema for i, tema in enumerate(temas)}

        opcion = self.menu.mostrar("TEMAS", opciones)
        if opcion in opciones:
            self.gestionar_scripts(os.path.join(ruta_unidad, opciones[opcion]))

    def gestionar_scripts(self, ruta_tema):

        # Método encargado únicamente de manejar los scripts.
        scripts = [
            f.name for f in os.scandir(ruta_tema)
            if f.name.endswith(".py")
        ]

        opciones = {str(i + 1): s for i, s in enumerate(scripts)}

        opcion = self.menu.mostrar("SCRIPTS", opciones)
        if opcion in opciones:
            ruta_script = os.path.join(ruta_tema, opciones[opcion])
            self.script_manager.mostrar_codigo(ruta_script)

            ejecutar = input("¿Desea ejecutar el script? (s/n): ")
            if ejecutar.lower() == "s":
                self.script_manager.ejecutar(ruta_script)

# Punto de entrada claramente definido del programa
if __name__ == "__main__":
    app = Dashboard()
    app.iniciar()


