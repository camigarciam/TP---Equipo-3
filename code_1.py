import random
import json
import time
from datetime import datetime
# from pelis import listapelis


#1.login 
def registrarUsuario(usuario,contra):
    try:
         with open('usuarios.json', 'r') as file:
            contenido = file.read()  # Lee el contenido del archivo
            if contenido:  # Verifica si el contenido no está vacío
                usuarios = json.loads(contenido)  # Carga los usuarios
            else:
                usuarios = []  # Inicializa una lista vacía si el archivo está vacío
    except FileNotFoundError:
        usuarios = []  # Inicializa una lista vacía si el archivo no existe
        
    for u in usuarios:
        if u['nombreUsuario'] == usuario:
            print("El nombre de usuario ya existe")
            return

    nuevo_usuario = {
        "nombreUsuario": usuario,
        "contrasena": contra,
        "peliculas_alquiladas": []
    }
    usuarios.append(nuevo_usuario)

    with open('usuarios.json', 'w') as file:
        json.dump(usuarios, file, indent=4)

    print("Usuario creado con éxito")
    return True

def login_usuario(usuario, contra):
    try:
        with open('usuarios.json', 'r') as file:
            usuarios=json.load(file)
    
    except FileNotFoundError:
        print("No hay usuarios registrados" )
        return False
    
    
     # Verificar si el usuario existe en el diccionario
    usuario_encontrado = None
    for u in usuarios:
        if u["nombreUsuario"] == usuario:
                usuario_encontrado = u
        else:
            print("El nombre de usuario no está registrado. Por favor, regístrese.")
            return False

    # Comprobar la contraseña
    if usuario_encontrado["contrasena"] == contra:
        print("Inicio de sesión exitoso.")

        # Mostrar películas alquiladas y pedir reseña si hay alguna
        if usuario_encontrado["peliculas_alquiladas"]:
            peliculas = ", ".join(usuario_encontrado["peliculas_alquiladas"])
            print(f"Hola, {usuario_encontrado['nombreUsuario']}. La vez pasada alquilaste las películas: {peliculas}.")
            desea_reseña = input(f"¿Te gustaría dejar una reseña sobre {peliculas}? (s/n): ").strip().lower()
            if desea_reseña == 's':
                reseña = input("Escribe tu reseña: ")
                print(f"Gracias por tu reseña sobre '{peliculas}': {reseña}")
        else:
            print(f"Hola, {usuario_encontrado['nombreUsuario']}. No tienes películas alquiladas anteriormente.")
        return True
    else:
        print("Su contraseña es incorrecta.")
        return False
    
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
    while len(nuevacontra) <8 or not any(char.isdigit() for char in nuevacontra) or not any(char.isalpha() for char in nuevacontra):
        nuevacontra=input("Contraseña invalida, ingrese la contraseña nuevamente: ")
    print("Contraseña válida")
    contrasena=input("Confirme su contraseña: ")
    while contrasena != nuevacontra:
        contrasena=input("Las contraseñas no coinciden, ingrese la contraseña nuevamente: ")
    else:
        print("Contraseña confirmada")
    return contrasena


#2. mostrar los titulos de las peliculas 
def Mostrarpelis():
   """
   Muestra el catalogo de películas.

   Parametro/Arg: Ninguno

   Return: Imprime número de índice mas 1 y el título de la película.
   """
   print("Nuestro catálogo es el siguiente")
   for i, peli in enumerate(listapelis):
        print(f"{i+1}. {peli['Titulo']}")
       
   
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
    while numpeli<1 or numpeli>len(listapelis):
        numpeli=int(input("Número de película inválido. Ingrese un número válido: "))
    peli = listapelis[numpeli - 1]
    puntos = lambda rating: "*" * int(rating)
    print(f"{peli['Titulo']}\nGeneros: {', '.join(peli['Generos'])}\nAnio: {peli['Anio']}\nRating: {puntos(peli['Rating'])}")

def selecionar_fechas():
    fecha_inicio = datetime.now()

    while True:
        try:
            fecha_fin = input("Ingrese fecha de finalización del alquiler (dd-mm-aaaa): ")
            fecha_fin = datetime.strptime(fecha_fin, "%d-%m-%Y")
            if fecha_fin > fecha_inicio:
                return fecha_inicio, fecha_fin
            else: 
                print("La fecha de finalización debe ser posterior a la fecha de inicio.")
        except ValueError:
            print("El formato de fecha ingresado no es valido. Porfavor intente de nuevo.")

#4. mostrar disponibilidad y seleccionar 

peliculas_alquiladas = []
indice_alquiler = 1
def Alquilarpeli(numero,usuario):
    """
    Alquila una película si hay unidades disponibles.

    Verifica la disponibilidad de la película seleccionada y, si está disponible, 
    reduce la cantidad y la añade a la lista de películas alquiladas.
    Si no hay disponibilidad, informa al usuario.

    Parametro/Arg: int- Número de la película a alquilar.

    Returns: bool- True si se realiza el alquiler, False si no.
    """
    global indice_alquiler
    with open('usuarios.json', 'r') as file:
                    usuarios = json.load(file)
    peli = listapelis[numero - 1]
    if peli["Disponibilidad"] > 0:
        print(f"Hay {peli['Disponibilidad']} unidades disponibles de '{peli['Titulo']}'")
        confirmacion = input("¿Deseas alquilar esta película? (s/n): ")
        if confirmacion == 's':
            fecha_inicio, fecha_fin = selecionar_fechas()
            peli["Disponibilidad"]-= 1

            usuario_encontrado = None
            for u in usuarios:
                if u["nombreUsuario"] == usuario:
                    usuario_encontrado = u
                    break
            
            # Si el usuario no se encuentra, informa al usuario
            if usuario_encontrado is None:
                print("Error: El usuario no está registrado.")
                return False
            
            # Agrega la película a la lista de películas alquiladas del usuario
            usuario_encontrado["peliculas_alquiladas"].append(peli["Titulo"])
            peliculas_alquiladas.append([indice_alquiler, peli["Titulo"], fecha_inicio, fecha_fin])
            
            # Guarda la lista actualizada de usuarios
            with open('usuarios.json', 'w') as file:
                json.dump(usuarios, file)
            indice_alquiler += 1
            print(f"Has alquilado '{peli['Titulo']}'. Quedan {peli['Disponibilidad']} unidades disponibles.")
        else:
            print("No se ha realizado el alquiler.")
            return False
    else:
        print(f"Lo siento, '{peli['Titulo']}' no está disponible en este momento.")
    return True

#5. recomendacion de una pelicula por si no sabes qué elegir! 
def Recomendacion():
    """
    Hace una recomendación de manera aleatoria.
    Selecciona una película de la lista de películas disponibles y muestra su información. Si no hay películas disponibles, informa al usuario.

    Returns:
        int or None: El índice de la película recomendada en la lista de películas, o None si no hay películas disponibles.
    """

    preguntas = [
        ("¿Estás dispuesto a buscar el amor a través de aplicaciones de citas?", ["Romance"]),
        ("¿Solés viajar en transporte público en hora pico?", ["Acción", "Aventura", "Drama"]),
        ("¿Te subirías a una nave espacial sin preguntar a dónde va?", ["Ciencia Ficción", "Aventura"]),
        ("¿Te intrigan las relaciones amorosas de la gente que te rodea? ", ["Drama", "Romance"]),
        ("¿Investigarías un ruido extraño en otra habitación?", ["Suspenso", "Acción"]),
        ("¿Te gustaría ser un dragón o algún bicho gigante por un día?", ["Animación", "Aventura"]),
        ("¿Aceptarías hacer un viaje improvisado a un lugar desconocido?", ["Aventura"]),
        ("¿Te gusta la idea de viajar por el mundo y conocer nuevos países?", ["Acción", "Aventura"]),
        ("¿Considerás que mirar el atardecer es un plan ideal?", ["Romance"]),
        ("¿Si estás de viaje en una zona montañosa, te agrada la idea de dormir afuera mirando las estrellas?", ["Romance", "Aventura"])
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
        while respuesta not in ['s', 'n']:
            print("Respuesta no válida. Por favor, responda con 's' o 'n'.")
            respuesta = input(f"{pregunta} (s/n): ").strip().lower()

        if respuesta == 's':
            for genero in generos:
                puntos_por_genero[genero] += 1

    max_puntos = max(puntos_por_genero.values())
    generos_maximos = [genero for genero, puntos in puntos_por_genero.items() if puntos == max_puntos]

    # Si hay empate
    genero_recomendado = random.choice(generos_maximos)

    peliculas_recomendadas = [
        peli["Titulo"] for peli in listapelis
        if genero_recomendado in peli["Generos"] and peli["Disponibilidad"] > 0
    ]

    if peliculas_recomendadas:
        print(f"Películas recomendadas en el género {genero_recomendado}:")
        for pelicula in peliculas_recomendadas:
            print(f"- {pelicula}")
    else:
        print(f"No hay películas disponibles en el género {genero_recomendado}.")

    return peliculas_recomendadas

#6. Pago
def Pago(peliculas_alquiladas):
    if not peliculas_alquiladas:  
        print("No hay películas seleccionadas para alquilar.")
        return  
    
    total_a_pagar = 0
    for indice, titulo, fecha_inicio, fecha_fin in peliculas_alquiladas:
        dias_alquilados = (fecha_fin - fecha_inicio).days
        costo = dias_alquilados * 1200
        total_a_pagar += costo
        print("Detalles de tu compra:")
        print(f"Película: {titulo}, Días alquilados: {dias_alquilados}, Costo: ${costo}")
    print(f"El total a pagar es: ${total_a_pagar}")

    opcion_valida = False 

    while not opcion_valida: 
        print("Métodos de pago disponibles:\n1. Tarjeta de crédito\n2. Mercado Pago\n3. Tarjeta de debito")
        opcion_pago = input("Seleccione método de pago (1, 2, 3): ")

        if opcion_pago == '1':
            print("Procesando pago...")
            time.sleep(3)
            print("Pago con tarjeta de crédito realizado con éxito.")
            opcion_valida = True  
        elif opcion_pago == '2':
            print("Procesando pago...")
            time.sleep(3)
            print("Pago con Mercado Pago realizado con éxito.")
            opcion_valida = True  
        elif opcion_pago == '3':
            print("Procesando pago...")
            time.sleep(3)
            print("Pago con Tarjeta de debito realizado con éxito.")
            opcion_valida = True  
        else:
            print("Opción seleccionada incorrecta. Por favor, seleccione una opción válida (1, 2, 3).")



#7. finalizar
def Finalizar():
    """
    Imprime un mensaje de agradecimiento y muestra una lista de las películas que el usuario ha alquilado durante la sesión. 
    Si no se alquiló ninguna película, informa al usuario.

    Returns:
        None: La función imprime un mensaje en la maquina y no retorna ningún valor.
    """
    print("Gracias por usar el programa de alquiler de películas.")
    if peliculas_alquiladas:
        print("Películas que alquilaste en esta sesión:")
        for indice, titulo, fecha_inicio, fecha_fin in peliculas_alquiladas:
            print(f"{indice}. {titulo} (Desde: {fecha_inicio.strftime('%d-%m-%Y')} Hasta: {fecha_fin.strftime('%d-%m-%Y')})")
        print ("Gracias por usar nuestro sistema de alquier de peliculas, hasta la próxima!")
    else:
        print("No alquilaste ninguna película en esta sesión.")




with open('pelis.json', 'r') as file:
        listapelis = json.load(file)



#programa principal
def Main():

    
     sesion_iniciada = False #controla estado

    while sesion_iniciada == False:  #estado= no se inició sesión
        try:
            loginregistro = int(input("Si desea registrarse, pulse 1. Si desea iniciar sesión, pulse 2. "))
            
            if loginregistro == 1:
                usuario = input("Cree su nombre de usuario: ")
                usuario = validarusuario(usuario)
                nuevacontra = input("Cree su contraseña, debe contener al menos 8 caracteres y un número: ")
                nuevacontra = validarcontraseña(nuevacontra)
                registrarUsuario(usuario, nuevacontra)
                print("Registro exitoso. Ahora inicie sesión para continuar.")

                #Solicita nombre usuario y contrasena de nuevo.
                usuario = input("Ingrese su nombre de usuario: ")
                contra = input("Ingrese su contraseña para iniciar sesión: ")
                if login_usuario(usuario, contra):  # Intentar iniciar sesión
                    sesion_iniciada = True  # Cambiar el estado para salir del ciclo

            elif loginregistro == 2:
                usuario = input("Ingrese su nombre de usuario: ")
                contra = input("Ingrese su contraseña: ")
                if login_usuario(usuario, contra):  # devuekve True
                    print("Inicio de sesión exitoso.")
                    sesion_iniciada = True  # Cambiar el estado para salir del ciclo

            else:
                print("Opción no válida. Intente nuevamente.")

        except ValueError:
            print("Por favor, ingrese un número válido.")

    # Mostrar películas
    Mostrarpelis()

    # Recomendación de película
    recomendada = input("¿Desea responder un test de 10 preguntas para que le recomendemos una película? (s/n): ")
    if recomendada.lower() == "s":
        print("Comienza el test!:")
        Recomendacion()

    # Comprobar disponibilidad y alquilar
    bandera = True
    while bandera:
        try:
            numero = int(input("Ingrese el número de película sobre la que desea obtener más información: "))
            Infopeli(numero)
            if Alquilarpeli(numero,usuario):
                continuar = input("¿Desea alquilar otra película? (s/n): ")
                if continuar.lower() != 's':
                    bandera = False
            else:
                Mostrarpelis()
        except ValueError:
            print("Por favor, ingrese un número.")
    
    #Pago
    Pago(peliculas_alquiladas)

# Ejecutar la función principal
Main()
Finalizar()


