import random
import json
import time
import segno
import re
import os
from datetime import datetime
# from pelis import listapelis

#1.login 
def cargar_datos(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

usuarios = cargar_datos('usuarios.json')
listapelis = cargar_datos('pelis.json')
resenias=cargar_datos('resenias.json')

def actualizar_datos(nombre_archivo, datos):
    with open(nombre_archivo, 'w') as file:
        json.dump(datos, file, indent=4)

def user_input(mensaje):
    respuesta = input(mensaje).strip().lower()
    if respuesta == "exit":
        time.sleep(1)
        print("\nHas cerrado sesión. ¡Portate bien! (・∀・)! \n\n\n")
        Main()  
    return respuesta

def registrarUsuario(usuario,contra):
    """
    Registra un nuevo usuario con un saldo inicial si el nombre de usuario no existe.

    Parámetros:
        usuario (str): El nombre de usuario.
        contra (str): La contraseña del usuario.

    Retorna:
        bool: True si el registro es exitoso, False si el usuario ya existe.
    """
    for u in usuarios:
        if u['nombreUsuario'] == usuario:
            print("\n\nEl nombre de usuario ya existe. ༼ง=ಠ益ಠ=༽ง")
            return False
 
    saldo_inicial = 0.0

    nuevo_usuario = {
        "nombreUsuario": usuario,
        "contrasena": contra,
        "peliculas_alquiladas": [],
        "peliculas_a_pagar":[],
        "saldo": saldo_inicial
    }
    usuarios.append(nuevo_usuario)

    actualizar_datos('usuarios.json', usuarios)

    print("Usuario creado con éxito")
    return True

def encontrar_usuario(usuario, usuarios):
    for index_usuario in usuarios:
        if index_usuario['nombreUsuario'] == usuario:
            return index_usuario
    return None

def login_usuario(usuario, contra, usuarios):
    """
    Inicia sesión de un usuario y muestra información sobre su saldo y películas alquiladas.

    Verifica que el usuario exista y que la contraseña sea correcta.
    Si el usuario tiene películas alquiladas, muestra las películas y permite dejar una reseña.

    Parámetros:
        usuario (str): El nombre de usuario.
        contra (str): La contraseña del usuario.
        usuarios (dict): El diccionario con la información de los usuarios registrados.

    Retorna:
        bool: True si el inicio de sesión es exitoso, False si hay algún error en el proceso.
    """
    # Verificar si el usuario existe en el diccionario
    global usuario_encontrado
    usuario_encontrado = encontrar_usuario(usuario, usuarios)

    # Si no se encontró el usuario, mostrar mensaje de error
    if not usuario_encontrado:
        print("\n\nEl nombre de usuario no está registrado. Por favor, regístrese.")
        return False

    # Comprobar la contraseña
    if usuario_encontrado["contrasena"] != contra:
        print("\n\nContrasena incorrecta. (◣_◢)")
        return False
    
    print("Iniciando sesión...")
    time.sleep(2)
    limpiarpantalla()
    print("\n\n\n=============================================")
    print("\n")
    print(f"\nInicio de sesión exitoso. Bienvenid@, {usuario_encontrado['nombreUsuario']} ヽ༼࿃っ࿃༽ﾉ\n")
    print("Puede cerrar sesión en cualquier momento usando la palabra clave 'exit'")
    print(f"\n\nTu saldo actual es: {usuario_encontrado['saldo']:.2f}")
    time.sleep(2)

    return True
    

def resenia(usuario):

    data_usuario = encontrar_usuario(usuario, usuarios)
    peliculas = data_usuario.get("peliculas_alquiladas",[])

    if peliculas:
        
        print(f"{usuario}, has alquilado las siguientes películas:")

        
        for i, pelicula in enumerate(peliculas, start=1):
            print(f"{i}. {pelicula['Titulo']}")

        bandera = True  
        while bandera:
            try:
                seleccion = int(user_input("\nIngrese el número de la película para dejar una reseña (o 0 para salir): "))
                
                if seleccion == 0:

                    print("\nLa humanidad no podrá sobrevivir sin tus opiniones... (￣ ￣|||)")
                    time.sleep(2)
                    bandera = False  
                    menuprincipal(usuario, usuarios)
                elif 1 <= seleccion <= len(peliculas):
                    pelicula_seleccionada = peliculas[seleccion - 1]  
                    print(f"\nHas seleccionado '{pelicula_seleccionada['Titulo']}'.")

                    resenia = user_input(f"Escribe tu reseña sobre '{pelicula_seleccionada['Titulo']}': ")
                    pelicula_seleccionada["Resenia"] = resenia  
                    resenia_nueva = {
                        "usuario": usuario,
                        "resenia": resenia
                    }

                    if pelicula_seleccionada['Titulo'] not in resenias:
                        
                        resenias[pelicula_seleccionada['Titulo']] = []
                    
                    resenias[pelicula_seleccionada['Titulo']].append(resenia_nueva)
                    
    
                    actualizar_datos("resenias.json", resenias)
                    print(f"\nGracias por tu reseña sobre '{pelicula_seleccionada['Titulo']}'.")
                    
                else:
                    print(f"Por favor, selecciona un número válido entre 1 y {len(peliculas)}.")
            except ValueError:
                print("Por favor, ingresa un número.")
    else:
        print("\nNo tienes películas alquiladas anteriormente.")    

    
def validarusuario(usuario):
        """
        Verifica si el valor del nombre del usuario ingresado es valido.
        Nombre del usuario debe tener 6 caracteres o mas para ser valido.
        Si es muy corto, se le pide al usuario ingresar uno nuevo.

        Parametro/Arg: Usuario ingresado

        Return: str- 'El nombre de usuario es valido'
        """
        while len(usuario)<6:
            print("(－‸ლ) El nombre de usuario debe contener al menos 6 caracteres")
            usuario=user_input("Ingrese su nombre de usuario: ")
        print("El nombre de usuario es válido ୧༼✿ ͡◕ д ◕͡ ༽୨")
        return usuario

def validarcontraseña(nuevacontra):
    """ 
    Verifica si la contraseña ingresada por el usuario es válida.
    
    La contraseña debe tener 8 caracteres o más y al menos un número para ser válida.
    Si no se cumple esta condición, se le pide al usuario ingresar una nueva.
    Luego, se le solicita al usuario que confirme la contraseña.
    Si las contraseñas no coinciden, se le pedirá que la ingrese nuevamente hasta que coincidan.

    Parametro/Arg: Contraseña ingresada

    Return: str- 'Contraseña confirmada'
    """
    while not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', nuevacontra):
        nuevacontra=user_input("/nContraseña invalida, ingrese la contraseña nuevamente: ")
    print("Contraseña válida")
    contrasena=user_input("\nConfirme su contraseña: ")
    while contrasena != nuevacontra:
        contrasena=user_input("/nLas contraseñas no coinciden, ingrese la contraseña nuevamente: ")
    else:
        print("Contraseña confirmada ༼ ◔ ͜ʖ ◔ ༽")
    return contrasena

def devolver_pelis(usuario):
    """
    Permite al usuario devolver películas alquiladas, calculando cargos por retraso si aplica.

    Parámetros:
        usuario (str): El nombre del usuario.

    Retorna:
        int: Cargo por retraso, o 0 si no hubo retraso.
    """
    # Verificar si el usuario tiene películas alquiladas
    data_usuario = encontrar_usuario(usuario, usuarios)
    if not data_usuario["peliculas_alquiladas"]:
        print("\n\nNo tienes películas alquiladas para devolver.")
        return
    
    # Mostrar las películas alquiladas
    print("Estas son tus películas alquiladas:")
    for i, alquiler in enumerate(data_usuario["peliculas_alquiladas"], 1):
        print(f"\n\n{i}. {alquiler['Titulo']} (Devolver antes de: {alquiler['FechaFin']})")
    
    devolver_otra = 's'
    cargo_extra = 0

    while devolver_otra == 's' and len(data_usuario["peliculas_alquiladas"]) > 0:
        try:
            # Solicitar al usuario la película que desea devolver
            indice_pelicula = int(user_input("\n\n¿Qué película deseas devolver? (Ingrese el número 0 para salir: ")) - 1

            if indice_pelicula == -1:
                print("Volviendo al menú principal...")
                time.sleep(2)
                limpiarpantalla()
                menuprincipal(usuario, usuarios)
            else:
                if indice_pelicula < 0 or indice_pelicula >= len(data_usuario["peliculas_alquiladas"]):
                    print("\n\nOpción no válida. Intenta de nuevo. ξ(｡◕ˇ◊ˇ◕｡)ξ")
                    continue

            pelicula = data_usuario["peliculas_alquiladas"][indice_pelicula]
            fecha_fin = datetime.strptime(pelicula['FechaFin'], "%d-%m-%Y")
        
            bandera = True
            while bandera:
                try:
                    fecha_actual = datetime.now()
                    bandera = False
                except ValueError:
                    print("\n\nEl formato de la fecha ingresado no es válido. Por favor intente de nuevo.")

            # Verificar si se devuelve tarde
            if fecha_actual > fecha_fin:
                dias_retraso = (fecha_actual - fecha_fin).days
                print(f"\n\nLa película '{pelicula['Titulo']}' se devuelve con {dias_retraso} día(s) de retraso.")
                cargo_extra = dias_retraso * 1500
                print(f"\n\nSe aplicará un cargo adicional de ${cargo_extra} por el retraso.")


            # Eliminar la película de las películas alquiladas
            data_usuario["peliculas_alquiladas"].pop(indice_pelicula)
            actualizar_datos('usuarios.json', usuarios)
            print(f"\n\nHas devuelto la película '{pelicula['Titulo']}' con éxito.")

            # Pregunta al usuario si desea devolver otra pelicula
            if len(data_usuario["peliculas_alquiladas"]) > 0:
                devolver_otra = user_input("\n\n¿Desea devolver otra pelicula? (s/n): ")
                if (devolver_otra == 's'):
                    for i, alquiler in enumerate(data_usuario["peliculas_alquiladas"], 1):
                        print(f"\n\n{i}. {alquiler['Titulo']} (Devolver antes de: {alquiler['FechaFin']})")
                while devolver_otra not in ['s', 'n']:
                    print("\n\nRespuesta no válida, intente de nuevo.")
                    devolver_otra = user_input("\n\n¿Desea devolver otra pelicula? (s/n): ")
            else: 
                print("\n\nYa no hay peliculas para devolver.~(‾▿‾)~ ( ˘▽˘)っ")
                menuprincipal(usuario, usuarios)
    
        except ValueError:
            print("\nPor favor, ingrese un número válido.")
    return cargo_extra

#2. mostrar los titulos de las peliculas 
def Mostrarpelis():
   """
   Muestra el catalogo de películas.

   Parametro/Arg: Ninguno

   Return: Imprime número de índice mas 1 y el título de la película.
   """
   print("Cargando catálogo... (•ᴗ•,, )")
   time.sleep(2)
   limpiarpantalla()
   print("Nuestro catálogo es el siguiente ≽^-⩊-^≼")
   for i, peli in enumerate(listapelis):
        print(f"\n{i+1}. {peli['Titulo']}")
       
   
#3. elegir una peli y mostrar detalles 
def Infopeli(numpeli):
    """
    Muestra información detallada sobre una película basadandose en el número seleccionado por el usuario.
    Si el número de película no es válido, solicita al usuario que ingrese uno nuevamente hasta que cumpla la condición.

    Parametro:
        numpeli (int): Número de la película, ingresado por el usuario, de la cual se desea tener información.

    Returns: 
            None: La función imprime la información de la película en la maquina y no retorna ningún valor.
    """
    peli = listapelis[numpeli - 1]
    puntos = lambda rating: "*" * int(rating)
    print(f"\n\n{peli['Titulo']}\n\nGeneros: {', '.join(peli['Generos'])}\n\nAnio: {peli['Anio']}\n\nRating: {puntos(peli['Rating'])}")

def selecionar_fechas():
    fecha_inicio = datetime.now()

    while True:
        try:
            fecha_fin = user_input("\n\nIngrese fecha de finalización del alquiler (dd-mm-aaaa): ")
            fecha_fin = datetime.strptime(fecha_fin, "%d-%m-%Y")
            if fecha_fin > fecha_inicio:
                return fecha_inicio, fecha_fin
            else: 
                print("\n\nLa fecha de finalización debe ser posterior a la fecha de inicio.")
        except ValueError:
            print("\nEl formato de fecha ingresado no es valido. Porfavor intente de nuevo.")


#4. mostrar disponibilidad y seleccionar 

peliculas_alquiladas = []
indice_alquiler = 1
def Alquilarpeli(numero,usuario):
    """
    Alquila una película si hay unidades disponibles, reduce la cantidad 
    y la añade a las películas alquiladas del usuario. 

    Verifica la disponibilidad de la película y, si el usuario confirma, 
    actualiza el inventario y los registros del usuario.

    Parametro/Arg:  int- Número de la película a alquilar. 
                    str- El nombre de usuario que realiza el alquiler.

    Returns: bool- True si se realiza el alquiler, False si no hay disponibilidad o el alquiler es cancelado..
    """
    global indice_alquiler, peliculas_alquiladas  

    if numero < 1 or numero > len(listapelis):
        print("\n\nNúmero de película inválido. Por favor, ingrese un número entre 1 y", len(listapelis))
        return False

    peli = listapelis[numero - 1]
    if peli["Disponibilidad"] > 0:
        print(f"\nHay {peli['Disponibilidad']} unidades disponibles de '{peli['Titulo']}'")
        confirmacion = user_input("\n\n¿Deseas alquilar esta película? (s/n): ")
        if confirmacion == 's':
            print("\n༼✷ɷ✷༽  ༼ԾɷԾ༽ ୧༼ ͡◉ل͜ ͡◉༽୨ ヽ༼௵ل͜௵༽ﾉ\n")
            fecha_inicio, fecha_fin = selecionar_fechas()
            peli["Disponibilidad"] -= 1

            # Convertir las fechas a formato de cadena
            fecha_inicio_str = fecha_inicio.strftime("%d-%m-%Y")
            fecha_fin_str = fecha_fin.strftime("%d-%m-%Y")

            # Encontrar y actualizar usuario
            data_usuario = encontrar_usuario(usuario, usuarios)
            info_alquiler = {
                "Titulo": peli["Titulo"],
                "FechaInicio": fecha_inicio_str,
                "FechaFin": fecha_fin_str
            }
            data_usuario["peliculas_alquiladas"].append(info_alquiler)
            data_usuario["peliculas_a_pagar"].append(info_alquiler["Titulo"])

            # Actualizar la lista global de peliculas_alquiladas
            peliculas_alquiladas = data_usuario["peliculas_alquiladas"]

            # Guardar cambios en los archivos JSON
            actualizar_datos('usuarios.json', usuarios)
            actualizar_datos('pelis.json', listapelis)

            print(f"Has alquilado '{peli['Titulo']}' ♡(ŐωŐ人). Quedan {peli['Disponibilidad']} unidades disponibles.")

            return True
        else:
            print("\nNo se ha realizado el alquiler. (〒﹏〒)\n\n\n")
            return False
    else:
        print(f"\n\nLo sentimos, '{peli['Titulo']}' no está disponible en este momento. (ó﹏ò｡)")
        time.sleep(2)
        limpiarpantalla()
        return False
    
# Recomendacion de una pelicula por si no sabes qué elegir! 
def Recomendacion():

    """
    Realiza una recomendación de película basada en las respuestas del usuario. 
    Filtra y ordena las películas por rating según el género preferido. 
    Si no hay películas disponibles, informa al usuario.

    Returns:
        lista: Películas recomendadas o lista vacía si no hay opciones disponibles.
    """
    print("Comienza el test! (｡・//ε//・｡)")
    print("Recuerde que puede omitir el test en cualquier momento ingresando el número '0'")


    preguntas = [
        ("\n¿Estás dispuesto a buscar el amor a través de aplicaciones de citas?", ["Romance"]),
        ("\n¿Solés viajar en transporte público en hora pico?", ["Acción", "Aventura", "Drama"]),
        ("\n¿Te subirías a una nave espacial sin preguntar a dónde va?", ["Ciencia Ficción", "Aventura"]),
        ("\n¿Te intrigan las relaciones amorosas de la gente que te rodea? ", ["Drama", "Romance"]),
        ("\n¿Investigarías un ruido extraño en otra habitación?", ["Suspenso", "Acción"]),
        ("\n¿Te gustaría ser un dragón o algún bicho gigante por un día?", ["Animación", "Aventura"]),
        ("\n¿Aceptarías hacer un viaje improvisado a un lugar desconocido?", ["Aventura"]),
        ("\n¿Te gusta la idea de viajar por el mundo y conocer nuevos países?", ["Acción", "Aventura"]),
        ("\n¿Considerás que mirar el atardecer es un plan ideal?", ["Romance"]),
        ("\n¿Si estás de viaje en una zona montañosa, te agrada la idea de dormir afuera mirando las estrellas?", ["Romance", "Aventura"])
    ]

    puntos_por_genero = {
        "Romance": 0,
        "Acción": 0,
        "Fantasía": 0,
        "Drama": 0,
        "Ciencia Ficción": 0,
        "Suspenso":0,
        "Animación":0,
        "Aventura":0
    }
    banderatest=True
    while banderatest:       
        for pregunta, generos in preguntas:
            if not banderatest: 
                print("Volviendo al menú principal...")
                time.sleep(2)
                limpiarpantalla()
                menuprincipal(usuario_encontrado["nombreUsuario"],usuarios) 
            respuesta = user_input(f"{pregunta} (s/n): ").strip().lower()
            while respuesta not in ["s", "n", "0"]:
                print("\nRespuesta no válida. Por favor, responda con 's' o 'n'.")
                respuesta = user_input(f"{pregunta} (s/n): ").strip().lower()

            if respuesta == 's':
                for genero in generos:
                    puntos_por_genero[genero] += 1
            if respuesta=="0":
                banderatest=False
                
                
                

        max_puntos = max(puntos_por_genero.values())
        generos_maximos = [genero for genero, puntos in puntos_por_genero.items() if puntos == max_puntos]

        # Si hay empate
        genero_recomendado = random.choice(generos_maximos)

        peliculas_recomendadas = [
            peli for peli in listapelis
            if genero_recomendado in peli["Generos"] and peli["Disponibilidad"] > 0
        ]

        if peliculas_recomendadas:
            n = len(peliculas_recomendadas)

            # metodo de burbujeo
            for i in range(n):
                for j in range(0, n-i-1):  
                    if peliculas_recomendadas[j]["Rating"] < peliculas_recomendadas[j+1]["Rating"]:
                    
                        peliculas_recomendadas[j], peliculas_recomendadas[j+1] = peliculas_recomendadas[j+1], peliculas_recomendadas[j]

            print(f"\n\n (人ﾟ∀ﾟ) Fin del test! ＠＾▽＾＠ \nPareces ser un aficionado del género {genero_recomendado}. \n Estas son nuestras recomendaciones, ordenadas por rating: ")
            for pelicula in peliculas_recomendadas:
                print(f"- {pelicula['Titulo']}")
        else:
            print(f"\nNo hay películas disponibles en el género {genero_recomendado}.")

        return peliculas_recomendadas

#6. Pago
# Función para calcular el total a pagar
def calcular_total(usuario, cargo_extra):
    """
    Calcula el total a pagar por las películas alquiladas, incluyendo cargos por retraso.

    Parámetros:
        cargo_extra (int): Cargo adicional por retraso, si lo hay.

    Retorna:
        float: El total a pagar, incluyendo cargos adicionales.
    """
    data_usuario = encontrar_usuario(usuario, usuarios)
    peliculas_a_pagar = data_usuario.get("peliculas_a_pagar", [])
    
    if len(peliculas_a_pagar) == 0:
        print("No hay películas seleccionadas para alquilar.")  
        menuprincipal(usuario_encontrado, usuarios)  
        return 0  # Devuelve 0 si no hay alquileres

    total_a_pagar = 400
    print("Detalles de tu compra:")
    for alquiler in usuario_encontrado["peliculas_alquiladas"]:
        # Acceder a los valores del diccionario por clave
        titulo = alquiler["Titulo"]
        fecha_inicio_str = alquiler["FechaInicio"]
        fecha_fin_str = alquiler["FechaFin"]

        # Convertir las fechas de cadena a datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d-%m-%Y")
        fecha_fin = datetime.strptime(fecha_fin_str, "%d-%m-%Y")

        # Calcular los días alquilados
        dias_alquilados = (fecha_fin - fecha_inicio).days
        costo = dias_alquilados * 1200  # Suponiendo que el costo es 1200 por día
        total_a_pagar +=  costo
        print(f"Película: {titulo}\n Días alquilados: {dias_alquilados}\n Costo: ${costo}")
    
    if cargo_extra is None:
        cargo_extra = 0

    if cargo_extra > 0:
        print(f"\n\nSe le va a cobrar un cargo adicional de ${cargo_extra} por devolución tardia. (⁄ ⁄•⁄ω⁄•⁄ ⁄)")
        total_a_pagar += cargo_extra

    print(f"\n\nEl total a pagar es: ${total_a_pagar} ヽ(･ω･ゞ)")
    

    return total_a_pagar

# Función para agregar saldo a la cuenta del usuario
def agregar_saldo(usuario_encontrado, usuarios):
    """
    Permite agregar saldo a la cuenta del usuario a través de diferentes métodos de pago.

    Solicita al usuario seleccionar un método de pago y la cantidad a agregar. Si la cantidad es válida, se actualiza el saldo del usuario.

    Parámetros:
        usuario_encontrado (dict): El diccionario con la información del usuario.
        usuarios (list): Lista de usuarios registrados.

    Retorna:
        None
    """
    metodo_pago_valido = False
    while not metodo_pago_valido:
        print("Métodos para agregar dinero:")
        print("1. Tarjeta de crédito")
        print("2. Mercado Pago")
        print("3. Tarjeta de débito")
        print("4. Salir")
        opcion_pago = user_input("Selecciona método de pago (1, 2, 3): ")

        if opcion_pago in ['1', '2', '3']:
            cantidad_agregar = None
            while cantidad_agregar is None:
                try:
                    cantidad_agregar = float(user_input("\n\nIngrese la cantidad de dinero que desea agregar a su cuenta: $"))
                    if cantidad_agregar <= 0:
                        print("\n\nError, el monto debe ser mayor a cero.")
                        cantidad_agregar = None
                except ValueError:
                    print("\nIngrese un número válido.")



            if opcion_pago == '2':  # Generar y mostrar código QR para Mercado Pago
                # Crear el código QR con información relevante
                qr_data = f"Mercado Pago - Usuario: {usuario_encontrado['nombreUsuario']} - Monto: ${cantidad_agregar:.2f}"
                qr = segno.make(qr_data)
                
                # Mostrar el QR en la terminal
                print("\nCódigo QR para Mercado Pago:")
                qr.terminal(compact=True)  # Compacta el QR y lo invierte (opcional)
                time.sleep(2)
            
            elif opcion_pago == '1'or opcion_pago == '3':  # Tarjeta de crédito o débito
                tarjeta = {}

    # Solicitar número de tarjeta
                valido_numero = False
                while not valido_numero:
                    numero_tarjeta = user_input("Ingrese el número de su tarjeta (16 dígitos): ")
                    if len(numero_tarjeta) == 16 and numero_tarjeta.isdigit():
                        tarjeta['numero'] = numero_tarjeta
                        valido_numero = True
                    else:
                        print("Número de tarjeta inválido. Debe tener 16 dígitos.")

                # Solicitar fecha de vencimiento
                valido_fecha = False
                while not valido_fecha:
                    fecha_vencimiento = input("Ingrese la fecha de vencimiento (MM/AA): ")
                    if len(fecha_vencimiento) == 5 and fecha_vencimiento[2] == '/' and fecha_vencimiento[:2].isdigit() and fecha_vencimiento[3:].isdigit():
                        try:
                            # Parsear mes y año
                            mes = int(fecha_vencimiento[:2])
                            anio = int(fecha_vencimiento[3:]) + 2000  # Convertir AA a AAAA

                            # Validar si la fecha es válida y no está vencida
                            hoy = datetime.now()
                            fecha_vencimiento_dt = datetime(anio, mes, 1)

                            if fecha_vencimiento_dt >= hoy.replace(day=1):
                                tarjeta['fecha_vencimiento'] = fecha_vencimiento
                                valido_fecha = True
                                print("\nTarjeta aprobada, procesando pago...")
                                time.sleep(2)
                            else:
                                print("La tarjeta está vencida. Por favor, ingrese una fecha válida.")
                        except ValueError:
                            print("Fecha de vencimiento inválida. Debe estar en formato MM/AA y representar una fecha válida.")
                    else:
                        print("Fecha de vencimiento inválida. Debe estar en formato MM/AA.")
            else:
                print("Opción no válida. Por favor, selecciona una opción válida (1, 2, 3).")    

            usuario_encontrado["saldo"] += cantidad_agregar
            actualizar_datos('usuarios.json', usuarios)
            print(f"\nSe han agregado ${cantidad_agregar} a tu saldo. Tu nuevo saldo es: ${usuario_encontrado['saldo']:.2f}")
            metodo_pago_valido = True
        elif opcion_pago == '4':
            print("\n\nSaliendo del menú de agregar saldo...")
            limpiarpantalla()
            menuprincipal(usuario_encontrado["nombreUsuario"], usuarios)
        else:
            print("\nOpción no válida. Por favor, selecciona una opción válida (1, 2, 3).")

# Función para procesar el pago
def realizar_pago(total_a_pagar, usuario):
    """
    Realiza el proceso de pago, verificando que el usuario tenga saldo suficiente.
    Si no tiene suficiente saldo, se le ofrece agregar dinero a su cuenta.
    Si el pago es exitoso, se procesa la compra y actualiza el saldo.
    """
    
    bandera=True
    with open('usuarios.json', 'r') as file:
        usuarios = json.load(file)

    usuario_encontrado = None
    while bandera:
        for u in usuarios:
            if u["nombreUsuario"] == usuario:
                usuario_encontrado = u
                bandera=False
        if usuario_encontrado is None:
            print("\nUsuario no encontrado.")
            return


    # Verificar si hay saldo suficiente
    if usuario_encontrado["saldo"] < total_a_pagar:
        diferencia = total_a_pagar - usuario_encontrado["saldo"]
        print(f"\n\nEl saldo no es suficiente para realizar el pago. Te faltan ${diferencia:.2f} (ʘдʘ╬)")
        
        # Opción para agregar dinero
        agregar_dinero = user_input("\n¿Desea agregar dinero a su cuenta? (s/n): ").strip().lower()
        if agregar_dinero == 's':
            agregar_saldo(usuario_encontrado, usuarios)
        else:
            print("\n\nSe ha cancelado el pago debido a saldo insuficiente. >(#｀皿´)")
            menuprincipal(usuario,usuarios)  # Volver al menu ppal
    
    # Si el saldo es suficiente, realizar el pago
    usuario_encontrado["saldo"] -= total_a_pagar
    print("\nSaldo suficiente, procesando pago...")
    time.sleep(2)

    usuario_encontrado["peliculas_a_pagar"]=[]
    

    # Guardar los cambios en el archivo
    actualizar_datos('usuarios.json', usuarios)

    print(f"\n\nCompra realizada con éxito! ╰(*´︶`*)╯♡. Tu saldo restante es: ${usuario_encontrado['saldo']:.2f}")


    # Preguntar si desea finalizar sesión
    finalizar = user_input("\n¿Desea finalizar la sesión? (s/n): ")
    while finalizar not in ['s', 'n']:
        print("\nRespuesta no válida. Por favor, responda con 's' o 'n'.")
        finalizar = user_input("\n¿Desea finalizar la sesión? (s/n): ")

    if finalizar == 's':
        Finalizar(usuario, usuarios)  # Llamar a Finalizar si se desea terminar la sesión
    else:
        print("\nRedirigiendo al menú principal...\n")
        menuprincipal(usuario, usuarios)

#7. finalizar
def Finalizar(usuario, usuarios):
    """
    Imprime un mensaje de agradecimiento y muestra una lista de las películas que el usuario ha alquilado durante la sesión. 
    Si no se alquiló ninguna película, informa al usuario.
    """

    # Buscar el usuario en la lista
    data_usuario = encontrar_usuario(usuario, usuarios)
    peliculas_alquiladas = data_usuario.get("peliculas_alquiladas", [])

    if peliculas_alquiladas:
        print("Películas que alquilaste en esta sesión:")
        for alquiler in peliculas_alquiladas:
            # Desempaquetar alquiler
            titulo, fecha_inicio_str, fecha_fin_str = alquiler["Titulo"], alquiler["FechaInicio"], alquiler["FechaFin"]
            
            # Convertir las fechas de cadena a datetime
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%d-%m-%Y")
            fecha_fin = datetime.strptime(fecha_fin_str, "%d-%m-%Y")
            print(f"\n{titulo} (Desde: {fecha_inicio.strftime('%d-%m-%Y')} Hasta: {fecha_fin.strftime('%d-%m-%Y')})")
        
        print("\n\nGracias por usar nuestro sistema de alquiler de películas, ¡hasta la próxima! \n❤ (ɔˆз(ˆ⌣ˆc)" )
        time.sleep(2)
        Main()
    else:
        print("\nNo alquilaste ninguna película en esta sesión.")

def ver_resenia(usuario, usuarios):
    peliculas_con_resenias = [titulo for titulo in resenias.keys()]
    if peliculas_con_resenias:
        # Show the list of movies with their index
        for i, titulo in enumerate(peliculas_con_resenias, start=1):
            print(f"{i}. {titulo}")
                # Ask the user to choose a movie
        try:
            seleccion = int(user_input("\nIngrese el número de la película para ver las reseñas (o 0 para salir): "))
            
            if seleccion == 0:
                print("Volviendo al menú principal...")
                time.sleep(2)
                limpiarpantalla()
                menuprincipal(usuario, usuarios)
            
            if 1 <= seleccion <= len(peliculas_con_resenias):
                titulo_pelicula = peliculas_con_resenias[seleccion - 1]
                print(f"\nReseñas para la película '{titulo_pelicula}':")
                
                for i, resenia in enumerate(resenias[titulo_pelicula], start=1):
                    print(f"\nReseña #{i}:")
                    print(f"Usuario: {resenia['usuario']}")
                    print(f"Reseña: {resenia['resenia']}")
            else:
                print("\nPor favor, seleccione un número válido.")
        except ValueError:
            print("\nPor favor, ingrese un número válido.")
    else:
        print("\nNo hay películas con reseñas disponibles.")


def obtener_peliculas_por_devolver(usuario):
    """Devuelve las películas pendientes por devolver, ordenadas por fecha de vencimiento ."""
    data_usuario = encontrar_usuario(usuario, usuarios)
    if data_usuario is None:
        raise ValueError(f"El usuario '{usuario}' no fue encontrado.")
    peliculas = data_usuario.get("peliculas_alquiladas",[])

    # `filter` incluye todas las pelis 
    hoy = datetime.now()
    peliculas_pendientes = list(
        filter(lambda p: datetime.strptime(p["FechaFin"], "%d-%m-%Y") >= hoy, peliculas)
    )

    # Ordenamiento manual por fecha de vencimiento x burbujeo
    for i in range(len(peliculas_pendientes)):
        for j in range(0, len(peliculas_pendientes) - i - 1):
            fecha_j = datetime.strptime(peliculas_pendientes[j]["FechaFin"], "%d-%m-%Y")
            fecha_j1 = datetime.strptime(peliculas_pendientes[j + 1]["FechaFin"], "%d-%m-%Y")
            if fecha_j > fecha_j1:
                peliculas_pendientes[j], peliculas_pendientes[j + 1] = peliculas_pendientes[j + 1], peliculas_pendientes[j]

    return peliculas_pendientes



def limpiarpantalla():
    # Verificamos el sistema operativo del usuario para emplear el comando correcto
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')



def menuprincipal(usuario, usuarios):
    """Muestra el menú principal y las películas por devolver al inicio."""


    # Mostrar películas pendientes por devolver
    peliculas_pendientes = obtener_peliculas_por_devolver(usuario)
    if peliculas_pendientes:
        
        print(f"\n{usuario}, estas son tus películas pendientes por devolver (  •̀ - •́  ) (ordenadas por fecha de vencimiento):\n")
        for i, pelicula in enumerate(peliculas_pendientes, start=1):
            print(f"{i}. {pelicula['Titulo']} - Fecha de vencimiento: {pelicula['FechaFin']}")
    else:
        print("\nNo tienes películas pendientes por devolver ٩(ˊᗜˋ*)و .")
    
    print("\n")
    time.sleep(4)
    print("=============================================")
    print("\n")
    print("Puede manejarse a través del menú con el teclado")
    print("\n")
   
    time.sleep(2)

    print("=============================================")
    print("૮ ˶ᵔ ᵕ ᵔ˶ ა   MENÚ PRINCIPAL   (˶˃ ᵕ ˂˶) .ᐟ.ᐟ")
    print("=============================================")
    print("\n     1.Ver nuestro catálogo y alquilar una película")
    print("\n     2.Devolver una peli")
    print("\n     3.Dejar una reseña sobre alguna peli que alquilaste")
    print("\n     4.Ver reseñas de otros usuarios")
    print("\n     5.Agregar Saldo")
    print("\n     6.Obtener una recomendación")
    print("\n     7.Pagar y Finalizar")
    print("\n")
    usuario_encontrado = encontrar_usuario(usuario, usuarios)
    banderamenu=True
    while banderamenu:
        try:
            navegacion=int(user_input("Ingrese el num deseado: "))
            if navegacion==1:
                Mostrarpelis()

                # Comprobar disponibilidad y alquilar
                bandera = True 
                while bandera:
                    try:
                        numero = int(user_input("\n\nIngrese el número de película sobre la que desea obtener más información (o 0 para salir): "))
                        if numero == 0:
                            print("Volviendo al menú principal...")
                            time.sleep(2)
                            limpiarpantalla()

                            menuprincipal(usuario, usuarios)
                        else:
                        # Validar el número antes de llamar a Infopeli
                            if numero < 1 or numero > len(listapelis):
                                print(f"\nNúmero de película inválido. Por favor, ingrese un número entre 1 y {len(listapelis)}")
                            else:
                                Infopeli(numero)  # Llamar a Infopeli solo si el número es válido

                                if Alquilarpeli(numero, usuario):
                                    continuar = user_input("\n¿Desea alquilar otra película? (s/n): ")
                                    if continuar.lower() != 's':
                                        menuprincipal(usuario, usuarios)
                                        bandera = False
                                else:
                                    Mostrarpelis()
                    except ValueError:
                        print("\nPor favor, ingrese un número.")

            elif navegacion==2:
                cargo_extra = devolver_pelis(usuario)
            
            elif navegacion==3:
                resenia(usuario)
            
            elif navegacion == 4:
                ver_resenia(usuario, usuarios)
            elif navegacion == 5:
                agregar_saldo(usuario_encontrado, usuarios)
            
            elif navegacion==6:
                
                print("El test está por comenzar...")
                time.sleep(2)
                
                limpiarpantalla()
                
                Recomendacion()
            
            cargo_extra = 0

            if navegacion == 7:
                total_a_pagar = calcular_total(usuario, cargo_extra)
                realizar_pago(total_a_pagar, usuario)
                Finalizar(usuario, usuarios)
                banderamenu=False

            elif navegacion>7 or navegacion<0:
                print("Por favor, ingrese un número válido")
                
                   
        except ValueError:
            print("Por favor, ingrese un número válido")
            
    
    



#programa principal
def Main():
        
    sesion_iniciada = True #controla estado
    while sesion_iniciada == True:  #estado = no se inició sesión
        try:
            print("\n")
            print("\n===============================================\n")
            print("\nヽ(*・ω・)ﾉ Bienvenido al videoclub!（●＞ω＜●）\n")
            print("\n===============================================\n")
            loginregistro = int(input("Si desea registrarse, pulse 1. Si desea iniciar sesión, pulse 2. "))
            
            if loginregistro == 1:
                usuario = input("\n\nCree su nombre de usuario: ")
                usuario = validarusuario(usuario)
                nuevacontra = input("\n\nCree su contraseña, debe contener al menos 8 caracteres y un número: ")
                nuevacontra = validarcontraseña(nuevacontra)

                # Intentar registrar al usuario y verificar si es exitoso
                registro_exitoso = registrarUsuario(usuario, nuevacontra)
                if not registro_exitoso:  # Si el registro falla, volver al menú
                    time.sleep(2)
                    continue

                print("\n\nRegistro exitoso. Ahora inicie sesión para continuar.")

                # Solicitar nombre de usuario y contraseña de nuevo
                usuario = input("\n\nIngrese su nombre de usuario: ")
                contra = input("\n\nIngrese su contraseña para iniciar sesión: ")
                if login_usuario(usuario, contra, usuarios):  # Intentar iniciar sesión
                    sesion_iniciada = False  # Cambiar el estado para salir del ciclo
                    usuario_obj = encontrar_usuario(usuario, usuarios)

            elif loginregistro == 2:
                
                usuario = input("\n\nIngrese su nombre de usuario: ")
                contra = input("\n\nIngrese su contraseña: ")
                if login_usuario(usuario, contra, usuarios):  # devuekve True
                    sesion_iniciada = False  # Cambiar el estado para salir del ciclo
                    usuario_obj = encontrar_usuario(usuario, usuarios)

            else:
                print("Opción no válida. Intente nuevamente.")

        except ValueError:
            print("Por favor, ingrese un número válido.")

    
    menuprincipal(usuario,usuarios)
    


# Ejecutar la función principal
Main()


    
        
    
    