from PyQt5.QtWidgets import *
from PyQt5 import uic

def agregarsolicitante():
    nombre = ventana.nombre.text()
    apellidos = ventana.apellidos.text()
    expediente = ventana.expediente.text()
    if ventana.BecaSi.isChecked():
        asignada = "S"
    else:
        asignada = "N"
    # Cada registro ocupa 61 bytes (20 + 30 + 10 + 1)
    registro = nombre.ljust(20) + apellidos.ljust(30) + expediente.ljust(10) + asignada
    fichero.write(registro)
    print("Entrada añadida: " + registro)
    ventana.nombre.setText("")
    ventana.apellidos.setText("")
    ventana.expediente.setText("")
    ventana.BecaNo.setChecked(True)


def capacidadarchivo():
    global fichero
    fichero.close()
    fichero = open("solicitantes.txt", "a")
    longitud = fichero.tell() #El final del archivo
    fichero.close()
    fichero = open("solicitantes.txt", "a+")
    return longitud


def muestra(estado):
    final = fichero.tell() - 61
    actual = 0
    fichero.seek(actual)
    if estado == "S":
        titulo = "ALUMNOS CON BECAS ASIGNADAS:"
    else:
        titulo = "ALUMNOS CON BECAS DENEGADAS:"
    texto = "EXPEDIENTE      ALUMNO/A\n".ljust(70, "-") + "\n"
    while actual <= final:
        nombre = fichero.read(20)
        apellidos = fichero.read(30)
        expediente = fichero.read(10)
        asignada = fichero.read(1)
        if asignada == estado:
            texto += expediente.ljust(20) + apellidos.strip() + ", " + nombre.strip() + "\n"
        actual += 61
    mensaje = QMessageBox()
    mensaje.information(ventana, titulo, texto, mensaje.Ok)


def becasasignadas():
    muestra("S")

def becasdenegadas():
    muestra("N")

global fichero
fichero = open("solicitantes.txt", "a+")

app = QApplication([])
ventana = uic.loadUi("ventanaBecas.ui")
ventana.agregar.clicked.connect(agregarsolicitante)
ventana.asignadas.clicked.connect(becasasignadas)
ventana.denegadas.clicked.connect(becasdenegadas)
ventana.show()
app.exec_()



"""

from gi.repository import Gtk


def agregar(boton):
    nombre = conector.get_object("nombre")
    apellidos = conector.get_object("apellidos")
    expediente = conector.get_object("expediente")
    asignada = conector.get_object("asignada")
    # Cada registro ocupa 61 bytes (20 + 30 + 10 + 1)
    registro = nombre.get_text().ljust(20) + apellidos.get_text().ljust(30) + \
    expediente.get_text().ljust(10) + asignada.get_text().ljust(1).upper()
    fichero.write(registro)
    print("Entrada añadida: " + registro)
    nombre.set_text("")
    apellidos.set_text("")
    expediente.set_text("")
    asignada.set_text("")


def muestra(estado):
    final = fichero.tell() - 61
    actual = 0
    fichero.seek(actual)
    if(estado == "S"):
        print("ALUMNOS CON BECAS ASIGNADAS:")
    else:
        print("ALUMNOS CON BECAS DENEGADAS:")
    while(actual <= final):
        nombre = fichero.read(20)
        apellidos = fichero.read(30)
        expediente = fichero.read(10)
        asignada = fichero.read(1)
        if(asignada.upper() == estado):
            print(expediente + " " + apellidos.strip() + ", " + nombre.strip())
        actual += 61


def muestraasignadas(boton):
    muestra("S")


def muestradenegadas(boton):
    muestra("N")


global fichero
fichero = open("becas.txt", "a+")

conector = Gtk.Builder()
conector.add_from_file("becas.glade")

botonagregar = conector.get_object("agregar")
botonagregar.connect("clicked", agregar)

botonasignadas = conector.get_object("asignadas")
botonasignadas.connect("clicked", muestraasignadas)

botondenegadas = conector.get_object("denegadas")
botondenegadas.connect("clicked", muestradenegadas)

ventana = conector.get_object("window1")
ventana.connect("delete-event", Gtk.main_quit)
ventana.show_all()
Gtk.main()
"""