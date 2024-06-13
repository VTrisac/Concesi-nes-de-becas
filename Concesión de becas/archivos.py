from PyQt5.QtWidgets import *
from PyQt5 import uic
import os


def borrarregistro():
    global fichero
    try:
        ultimo = capacidadarchivo() - 50
        actual = 0
        fichero.seek(actual)
        # Obtenemos el nombre y le añadimos los espacios igual que al guardar
        nombre_saltar = ventana.nombre.text().ljust(20)
        ficherotemp = open("agendatemporal.txt", "w")
        localizado = False #Suponemos inicialmente que no lo encontrará
        while actual <= ultimo:
            nombre = fichero.read(20)
            email = fichero.read(30)
            # Si no coinciden los nombres, lo guardamos en el archivo temporal
            if nombre != nombre_saltar:
                ficherotemp.write(nombre + email)
            else:
                localizado = True
            actual += 50
        # Cerramos los dos y hacemos el cambio del temporal por el original
        fichero.close()
        ficherotemp.close()
        if localizado:
            os.remove("agenda.txt")
            os.rename("agendatemporal.txt", "agenda.txt")
            # Lo dejamos como estaba
            fichero = open("agenda.txt", "a+")
            mensaje(ventana.nombre.text() + " eliminado, operación finalizada.")
            ventana.nombre.setText("")
        else:
            os.remove("agendatemporal.txt")
            mensaje("No se ha encontrado el nombre indicado.")
    except NameError:
        mensaje("ERROR: El archivo no se ha abierto aun!")


def capacidadarchivo():
    global fichero
    fichero.close()
    fichero = open("agenda.txt", "a")
    longitud = fichero.tell() #El final del archivo
    fichero.close()
    fichero = open("agenda.txt", "a+")
    return longitud


def listado():
    try:
        # restamos 50 del último carácter para saber donde comienza el último registro
        final = capacidadarchivo() - 50
        actual = 0
        fichero.seek(actual)
        frase = "contenido de la agenda".upper().center(30, "=") + "\n"
        while actual <= final:
            nombre = fichero.read(20)
            email = fichero.read(30)
            frase += "\nNombre: " + nombre + "\nEmail: " + email + "\n".ljust(45, "-")
            actual += 50
        mensaje(frase)
    except NameError:
        mensaje("ERROR: El archivo no se ha abierto aun!")


def agregardatos():
    minombre = ventana.nombre.text()
    miemail = ventana.email.text()
    registro = minombre.ljust(20) + miemail.ljust(30)
    try:
        fichero.write(registro)
        frase = "Registro añadido: #" + registro + "#"
        print(frase)  # Para dejar constancia en la consola
        mensaje(frase)
        ventana.nombre.setText("")
        ventana.email.setText("")
    except NameError:
        mensaje("ERROR: El archivo no se ha abierto aun!")


def eliminararchivo():
    try:
        if fichero.closed is False:
            fichero.close()
            mensaje("El archivo estaba abierto, ha habido que cerrarlo.")
        os.remove(fichero.name)
        mensaje("Archivo eliminado.")
    except NameError:
        mensaje("ERROR: El archivo no se ha definido aun!")

def creararchivo():
    global fichero
    fichero = open("agenda.txt", "a+")
    frase = "archivo "+ fichero.name + " preparado."
    if fichero.closed:
        frase += "\nEstá cerrado."
    else:
        frase += "\nEstá abierto. Modo de apertura: " + fichero.mode
    mensaje(frase)


def mensaje(texto):
    mensaje = QMessageBox()
    mensaje.information(ventana, "Resultado", texto, mensaje.Ok)


app = QApplication([])
ventana = uic.loadUi("ventanaArchivo.ui")
ventana.crear.clicked.connect(creararchivo)
ventana.eliminar.clicked.connect(eliminararchivo)
ventana.agregar.clicked.connect(agregardatos)
ventana.listar.clicked.connect(listado)
ventana.borrar.clicked.connect(borrarregistro)
ventana.show()
app.exec_()
