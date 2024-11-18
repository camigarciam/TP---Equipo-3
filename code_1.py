import random
import json
import time
import re
from datetime import datetime
# from pelis import listapelis

#1.login 
def cargar_datos(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

usuarios = cargar_datos('usuarios.json')
listapelis = cargar_datos('pelis.json')

def actualizar_datos(nombre_archivo, datos):
    with open(nombre_archivo, 'w') as file:
        json.dump(datos, file, indent=4)

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
            print("\n\nEl nombre de usuario ya existe")
            return False
 
    #Pedir al usuario ingrese su saldo incial
    saldo_inicial = float(input("\n\nIngrese su saldo incial: $"))

    nuevo_usuario = {
        "nombreUsuario": usuario,
        "contrasena": contra,
        "peliculas_alquiladas": [],
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
    usuario_encontrado = encontrar_usuario(usuario, usuarios)

    # Si no se encontró el usuario, mostrar mensaje de error
    if not usuario_encontrado:
        print("\n\nEl nombre de usuario no está registrado. Por favor, regístrese.")
        return False

    # Comprobar la contraseña
    if usuario_encontrado["contrasena"] != contra:
        print("\n\nContrasena incorrecta. (◣_◢)")
        return False

    print(f"\n\nInicio de sesión exitoso. Bienvenid@, {usuario_encontrado['nombreUsuario']} (^◔ᴥ◔^)")
    print(f"\n\nTu saldo actual es: ${usuario_encontrado['saldo']:.2f}")

    # Mostrar películas alquiladas y pedir reseña si hay alguna
    if usuario_encontrado["peliculas_alquiladas"]:
        peliculas = ", ".join([pelicula["Titulo"] for pelicula in usuario_encontrado["peliculas_alquiladas"]])
        print(f"Hola, {usuario_encontrado['nombreUsuario']}. La vez pasada alquilaste las películas: {peliculas}.")
        desea_res = input(f"¿Te gustaría dejar una reseña sobre {peliculas}? (s/n): ").strip().lower()
        if desea_res == 's':
            resenia = input("Escribe tu reseña: ")
            print(f"Gracias por tu reseña sobre '{peliculas}'")
    else:
        print("No tienes películas alquiladas anteriormente.")
    return True
    

    
def validarusuario(usuario):
        """
        Verifica si el valor del nombre del usuario ingresado es valido.
        Nombre del usuario debe tener 6 caracteres o mas para ser valido.
        Si es muy corto, se le pide al usuario ingresar uno nuevo.

        Parametro/Arg: Usuario ingresado

        Return: str- 'El nombre de usuario es valido'
        """
        while len(usuario)<6:
            print("El nombre de usuario debe contener al menos 6 caracteres")
            usuario=input("Ingrese su nombre de usuario: ")
        print("El nombre de usuario es válido")
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
        nuevacontra=input("Contraseña invalida, ingrese la contraseña nuevamente: ")
    print("Contraseña válida")
    contrasena=input("Confirme su contraseña: ")
    while contrasena != nuevacontra:
        contrasena=input("Las contraseñas no coinciden, ingrese la contraseña nuevamente: ")
    else:
        print("Contraseña confirmada")
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
            indice_pelicula = int(input("\n\n¿Qué película deseas devolver? (Ingrese el número): ")) - 1
            
            if indice_pelicula < 0 or indice_pelicula >= len(data_usuario["peliculas_alquiladas"]):
                print("\n\nOpción no válida. Intenta de nuevo. ξ(｡◕ˇ◊ˇ◕｡)ξ")
                continue
        
            pelicula = data_usuario["peliculas_alquiladas"][indice_pelicula]
            fecha_fin = datetime.strptime(pelicula['FechaFin'], "%d-%m-%Y")
        
            bandera = True
            while bandera:
                try:
                    fecha_actual = datetime.strptime(input("\n\nIngrese la fecha del día de hoy: (dd- mm- aaaa)"), "%d-%m-%Y")
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
                devolver_otra = input("\n\n¿Desea devolver otra pelicula? (s/n): ")
                if (devolver_otra == 's'):
                    for i, alquiler in enumerate(data_usuario["peliculas_alquiladas"], 1):
                        print(f"\n\n{i}. {alquiler['Titulo']} (Devolver antes de: {alquiler['FechaFin']})")
                while devolver_otra not in ['s', 'n']:
                    print("\n\nRespuesta no válida, intente de nuevo.")
                    devolver_otra = input("\n\n¿Desea devolver otra pelicula? (s/n): ")
            else: print("\n\nYa no hay peliculas para devolver.~(‾▿‾)~ ( ˘▽˘)っ")
    
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
   print("Nuestro catálogo es el siguiente")
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
            fecha_fin = input("\n\nIngrese fecha de finalización del alquiler (dd-mm-aaaa): ")
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
        confirmacion = input("\n\n¿Deseas alquilar esta película? (s/n): ")
        if confirmacion == 's':
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
        print(f"\n\nLo siento, '{peli['Titulo']}' no está disponible en este momento. (ó﹏ò｡)")
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
            
    for pregunta, generos in preguntas:
        respuesta = input(f"{pregunta} (s/n): ").strip().lower()
        while respuesta not in ["s", "n"]:
            print("\nRespuesta no válida. Por favor, responda con 's' o 'n'.")
            respuesta = input(f"{pregunta} (s/n): ").strip().lower()

        if respuesta == 's':
            for genero in generos:
                puntos_por_genero[genero] += 1

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
def calcular_total(peliculas_alquiladas, cargo_extra):
    """
    Calcula el total a pagar por las películas alquiladas, incluyendo cargos por retraso.

    Parámetros:
        peliculas_alquiladas (list): Lista de películas alquiladas con fechas.
        cargo_extra (int): Cargo adicional por retraso, si lo hay.

    Retorna:
        float: El total a pagar, incluyendo cargos adicionales.
    """
    if len(peliculas_alquiladas) == 0:
        print("No hay películas seleccionadas para alquilar.")    
        return 0  # Devuelve 0 si no hay alquileres

    total_a_pagar = 0
    print("Detalles de tu compra:")
    for alquiler in peliculas_alquiladas:
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
        total_a_pagar += costo
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
        opcion_pago = input("Selecciona método de pago (1, 2, 3): ")

        if opcion_pago in ['1', '2', '3']:
            cantidad_agregar = None
            while cantidad_agregar is None:
                try:
                    cantidad_agregar = float(input("\n\nIngrese la cantidad de dinero que desea agregar a su cuenta: $"))
                    if cantidad_agregar <= 0:
                        print("\n\nError, el monto debe ser mayor a cero.")
                        cantidad_agregar = None
                except ValueError:
                    print("\nIngrese un número válido.")

            usuario_encontrado["saldo"] += cantidad_agregar
            actualizar_datos('usuarios.json', usuarios)

            print(f"\nSe han agregado ${cantidad_agregar} a tu saldo. Tu nuevo saldo es: ${usuario_encontrado['saldo']:.2f}")
            metodo_pago_valido = True 
        else:
            print("\nOpción no válida. Por favor, selecciona una opción válida (1, 2, 3).")

# Función para procesar el pago
def realizar_pago(total_a_pagar, usuario):

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
    while usuario_encontrado["saldo"] < total_a_pagar:
        diferencia = total_a_pagar - usuario_encontrado["saldo"]
        print(f"\n\nEl saldo no es suficiente para realizar el pago. Te faltan ${diferencia:.2f} (ʘдʘ╬)")
        agregar_dinero = input("\n¿Desea agregar dinero a su cuenta? (s/n): ").strip().lower()

        if agregar_dinero == 's':
            agregar_saldo(usuario_encontrado, usuarios)

        else:
            print("\n\nSe ha cancelado la compra debido a saldo insuficiente. >(#｀皿´)")
            return  # Salimos de la función si no se agrega dinero

    # El saldo es suficiente para pagar
    usuario_encontrado["saldo"] -= total_a_pagar
    print("\nSaldo suficiente, procesando pago...")
    time.sleep(2)

    # Guardar el saldo actualizado en el archivo
    actualizar_datos('usuarios.json', usuarios)

    print(f"\n\nCompra realizada con éxito! ╰(*´︶`*)╯♡. Tu saldo restante es: ${usuario_encontrado['saldo']:.2f}")

def datos_tarjeta():
    pass

#7. finalizar
def Finalizar(usuario,usuarios):
    """
    Imprime un mensaje de agradecimiento y muestra una lista de las películas que el usuario ha alquilado durante la sesión. 
    Si no se alquiló ninguna película, informa al usuario.

    Returns:
        None: La función imprime un mensaje en la maquina y no retorna ningún valor.
    """
    data_usuario = encontrar_usuario(usuario, usuarios)
    peliculas_alquiladas = data_usuario.get("peliculas_alquiladas", [])
    
    if len(peliculas_alquiladas) != 0:
        print("Películas que alquilaste en esta sesión:")
        for alquiler in peliculas_alquiladas:
            # Desempaquetar el alquiler en variables
            titulo, fecha_inicio_str, fecha_fin_str = alquiler["Titulo"], alquiler["FechaInicio"], alquiler["FechaFin"]
            # Convertir las fechas de cadena a datetime
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%d-%m-%Y")
            fecha_fin = datetime.strptime(fecha_fin_str, "%d-%m-%Y")
            print(f"\n{titulo} (Desde: {fecha_inicio.strftime('%d-%m-%Y')} Hasta: {fecha_fin.strftime('%d-%m-%Y')})")
        print("\n\nGracias por usar nuestro sistema de alquiler de películas, ¡hasta la próxima! \n❤ (ɔˆз(ˆ⌣ˆc)" )
    else:
        print("\nNo alquilaste ninguna película en esta sesión.")

#programa principal
def Main():
        
    sesion_iniciada = True #controla estado
    while sesion_iniciada == True:  #estado = no se inició sesión
        try:
            print("\nBienvenido al videoclub!（●＞ω＜●）\n")
            loginregistro = int(input("Si desea registrarse, pulse 1. Si desea iniciar sesión, pulse 2."))
            
            if loginregistro == 1:
                usuario = input("\n\nCree su nombre de usuario: ")
                usuario = validarusuario(usuario)
                nuevacontra = input("\n\nCree su contraseña, debe contener al menos 8 caracteres y un número: ")
                nuevacontra = validarcontraseña(nuevacontra)
                registrarUsuario(usuario, nuevacontra)
                print("\n\nRegistro exitoso. Ahora inicie sesión para continuar.")

                #Solicita nombre usuario y contrasena de nuevo.
                usuario = input("\n\nIngrese su nombre de usuario: ")
                contra = input("\n\nIngrese su contraseña para iniciar sesión: ")
                if login_usuario(usuario, contra,usuarios):  # Intentar iniciar sesión
                    sesion_iniciada = False  # Cambiar el estado para salir del ciclo

            elif loginregistro == 2:
                usuario = input("\n\nIngrese su nombre de usuario: ")
                contra = input("\n\nIngrese su contraseña: ")
                if login_usuario(usuario, contra, usuarios):  # devuekve True
                    sesion_iniciada = False  # Cambiar el estado para salir del ciclo

            else:
                print("Opción no válida. Intente nuevamente.")

        except ValueError:
            print("Por favor, ingrese un número válido.")

    
    cargo_extra = 0
    devolver_opcion = input("\n\n¿Te gustaría devolver alguna película? (s/n): ").strip().lower()
    if devolver_opcion == 's':
        cargo_extra = devolver_pelis(usuario)
   
    # Recomendación de película
    respuesta_valida = True

    while respuesta_valida == True:  #estado = no se ha respondido
        recomendada = input("\n\n¿Desea responder un test de 10 preguntas para que le recomendemos una película? (s/n): ").strip().lower()
        
        if recomendada == "s":
            print("¡Comienza el test!")
            Recomendacion()
            respuesta_valida = False # Cambia el estado para terminar el bucle
        elif recomendada == "n":
            print("\nNo hay problema!.")
            respuesta_valida = False  # Cambia el estado para terminar el bucle
        else:
            print("\nRespuesta no válida. Por favor, responda con 's' o 'n'. (ｏ・_・)ノ”(ノ_<、)")

     # Mostrar películas
    Mostrarpelis()

    # Comprobar disponibilidad y alquilar
    bandera = True 
    while bandera:
        try:
            numero = int(input("\n\nIngrese el número de película sobre la que desea obtener más información: "))
            
            # Validar el número antes de llamar a Infopeli
            if numero < 1 or numero > len(listapelis):
                print(f"\nNúmero de película inválido. Por favor, ingrese un número entre 1 y {len(listapelis)}")
            else:
                Infopeli(numero)  # Llamar a Infopeli solo si el número es válido
                
                if Alquilarpeli(numero, usuario):
                    continuar = input("\n¿Desea alquilar otra película? (s/n): ")
                    if continuar.lower() != 's':
                        bandera = False
                else:
                    Mostrarpelis()
        except ValueError:
            print("\nPor favor, ingrese un número.")
    
    #Realizar pago
    total_a_pagar = calcular_total(peliculas_alquiladas, cargo_extra)
    realizar_pago(total_a_pagar, usuario)
    Finalizar(usuario, usuarios)

# Ejecutar la función principal
Main()


