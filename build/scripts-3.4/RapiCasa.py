__author__ = 'bhernandezsouto'
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Image
from reportlab.pdfgen import canvas
import sqlite3 as dbapi
from gi.repository import Gtk
import os.path
import PDF


# Clase Principal en esta clase se muestran los datos y contiene los metodos necesarios para la ejecucion de
# las funciones del programa (agregar, eliminar, modificar y actualizar)
class Principal:
    # Creacion de la ventana y de los valores iniciales de esta
    def __init__(self):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        self.window = Gtk.Window()
        self.window.resize(700, 500)
        fichero = "widgetPrincipal.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(fichero)
        self.bPrincipal = self.builder.get_object("bPrincipal")

        self.vista = self.builder.get_object("tCliente")
        self.vista1 = self.builder.get_object("tPiso")
        senal = {"on_añadirCliente_clicked": self.on_añadirCliente_clicked,
                 "on_eliminarCliente_clicked": self.on_eliminarCliente_clicked,
                 "on_tCliente_row_activated": self.on_tCliente_row_activated,
                 "on_añadirPiso_clicked": self.on_añadirPiso_clicked,
                 "actualizar": self.actualizara,
                 "on_eliminarPiso_clicked": self.on_eliminarPiso_clicked,
                 "on_editarC_clicked": self.on_editarC_clicked,
                 "on_pdf_clicked": self.imprimir,
                 "on_editarP_clicked": self.on_editarP_clicked,
                 }
        self.builder.connect_signals(senal)
        render = Gtk.CellRendererText()
        columna1 = Gtk.TreeViewColumn("DNI", render, text=0)
        columna2 = Gtk.TreeViewColumn("Nombre", render, text=1)
        columna3 = Gtk.TreeViewColumn("Apellidos", render, text=2)
        columna4 = Gtk.TreeViewColumn("Direccion", render, text=3)
        columna5 = Gtk.TreeViewColumn("Telefono", render, text=4)
        columna6 = Gtk.TreeViewColumn("F_Nacimiento", render, text=5)
        columna7 = Gtk.TreeViewColumn("Propietario", render, text=0)
        columna8 = Gtk.TreeViewColumn("EnVenta", render, text=1)
        columna9 = Gtk.TreeViewColumn("EnAlquiler", render, text=2)
        columna10 = Gtk.TreeViewColumn("Direccion", render, text=3)
        columna11 = Gtk.TreeViewColumn("Pre Venta", render, text=4)
        columna12 = Gtk.TreeViewColumn("Pre Alquiler", render, text=5)
        columna13 = Gtk.TreeViewColumn("Superficie", render, text=6)
        columna14 = Gtk.TreeViewColumn("Habitaciones", render, text=7)
        columna15 = Gtk.TreeViewColumn("Baños", render, text=8)
        columna16 = Gtk.TreeViewColumn("Otros Servicios", render, text=9)

        self.vista.append_column(columna1)
        self.vista.append_column(columna2)
        self.vista.append_column(columna3)
        self.vista.append_column(columna4)
        self.vista.append_column(columna5)
        self.vista.append_column(columna6)
        self.vista1.append_column(columna7)
        self.vista1.append_column(columna8)
        self.vista1.append_column(columna9)
        self.vista1.append_column(columna10)
        self.vista1.append_column(columna11)
        self.vista1.append_column(columna12)
        self.vista1.append_column(columna13)
        self.vista1.append_column(columna14)
        self.vista1.append_column(columna15)
        self.vista1.append_column(columna16)

        self.window.add(self.bPrincipal)
        self.window.show()
        self.actualizar()

        # metodo que realiza la conexion a la base

    def coneccion(self):
        self.bbdd = dbapi.connect("basedatos.dat")
        self.cursor = self.bbdd.cursor()
        self.bbdd.commit()

    # metodo que crea la base si esta no existe
    def crearbd(self):
        self.bbdd = dbapi.connect("basedatos.dat")
        self.cursor = self.bbdd.cursor()
        self.bbdd.commit()
        self.cursor.execute("CREATE TABLE CLIENTE (DNI VARCHAR(7) PRIMARY KEY NOT NULL,"
                            "NOMBRE VARCHAR(20) NOT NULL,"
                            "APELLIDOS VARCHAR(30) NOT NULL,"
                            "DIRECCION VARCHAR(50) ,"
                            "TELEFONO VARCHAR(30),"
                            "FNACIMIENTO VARCHAR(10))")
        self.cursor.execute("CREATE TABLE PISO (PROPIETARIO VARCHAR(7) NOT NULL,"
                            "ENVENTA VARCHAR(2),"
                            "ENALQUILER VARCHAR(2),"
                            "DIRECCION VARCHAR(50) ,"
                            "PVENTA VARCHAR(20),"
                            "PALQUILER VARCHAR(20),"
                            "SUPERFICIE VARCHAR(20),"
                            "HABITACIONES VARCHAR(20) ,"
                            "BANOS VARCHAR(20) ,"
                            "OTROS VARCHAR(100))")

        self.bbdd.commit()

    def imprimir(self, control):
        obj = PDF.PDF()
        obj.pdf()

    # metodo que abre la ventana agregar
    def on_añadirCliente_clicked(self, control):
        fichero = "fCliente.glade"
        self.builderCliente = Gtk.Builder()
        self.builderCliente.add_from_file(fichero)
        self.fCliente = self.builderCliente.get_object("fCliente")

        senal = {"on_aceptarCliente_clicked": self.on_aceptarCliente_clicked,
                 "on_cancelar_clicked": self.on_cancelar_clicked
                 }
        self.builderCliente.connect_signals(senal)
        self.bPrincipal.pack_start(self.fCliente, False, False, 0)
        self.window.show()

    def on_aceptarCliente_clicked(self, control):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        dni = self.builderCliente.get_object("dni").get_text()
        nombre = self.builderCliente.get_object("nombre").get_text()
        apellidos = self.builderCliente.get_object("apellidos").get_text()
        direccion = self.builderCliente.get_object("direccion").get_text()
        telefono = self.builderCliente.get_object("telefono").get_text()
        fnacimiento = self.builderCliente.get_object("fnacimiento").get_text()
        registro = (dni, nombre, apellidos, direccion, telefono, fnacimiento)
        if len(dni)==9 and telefono.isdigit and len(telefono)==9:
            self.condicion = True
        else:
            self.emergente("Datos invalidos. ")
            self.condicion = False

        if(self.condicion):
            try:
                self.cursor.execute(
                    "INSERT INTO CLIENTE(DNI,NOMBRE,APELLIDOS,DIRECCION,TELEFONO,FNACIMIENTO) VALUES (?,?,?,?,?,?)", registro)
                self.bbdd.commit()
                self.cursor.close()
                self.bbdd.close()
                self.fCliente.hide()
                self.emergente("Cliente Agregado")
                self.actualizar()
                self.window.resize(700, 500)
            except dbapi.IntegrityError:
                self.emergente("El Cliente ya existe")

    def on_cancelar_clicked(self, control):
        self.fpiso.hide()
        self.fCliente.hide()
        self.window.resize(700, 500)

    def on_eliminarCliente_clicked(self, control):

        self.coneccion()
        selection = self.vista.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.dni = model[selec][0]
            self.cursor.execute("DELETE FROM CLIENTE WHERE DNI ='" + self.dni + "'")
            self.bbdd.commit()
            self.emergente("Borrado")
            self.actualizar()
        self.cursor.close()
        self.bbdd.close()

    def on_tCliente_row_activated(self, path, column,user_data):
        self.coneccion()
        selection = self.vista.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.dni = model[selec][0]
            lista = Gtk.ListStore(str, str, str, str, str, str,str,str,str,str)
            self.cursor.execute("SELECT * FROM PISO WHERE PROPIETARIO = " + self.dni)
            for fila in self.cursor:
                lista.append(fila)
                self.vista1.set_model(lista)
                self.vista1.show()

    def on_añadirPiso_clicked(self, control):
        fichero = "fPiso.glade"
        self.builderPiso = Gtk.Builder()
        self.builderPiso.add_from_file(fichero)
        self.fpiso = self.builderPiso.get_object("fPiso")

        senal = {"on_aceptarPiso_clicked": self.on_aceptarPiso_clicked,
                 "on_cancelarP_clicked": self.on_cancelar_clicked
                 }
        self.builderPiso.connect_signals(senal)
        self.bPrincipal.pack_start(self.fpiso, False, False, 0)

        self.window.show()

    def on_aceptarPiso_clicked(self, control):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        propietario = self.builderPiso.get_object("propietario").get_text()
        benventa = self.builderPiso.get_object("enventa")
        if benventa.get_active():
            enventa = "si"
        else:
            enventa = "no"
        benalquiler = self.builderPiso.get_object("enalquiler")
        if benalquiler.get_active():
            enalquiler = "si"
        else:
            enalquiler = "no"
        direccion = self.builderPiso.get_object("direccion").get_text()
        pventa = int(self.builderPiso.get_object("pventa").get_text())
        palquiler = self.builderPiso.get_object("palquiler").get_text()
        superficie = self.builderPiso.get_object("superficie").get_text()
        habitaciones = int(self.builderPiso.get_object("habitaciones").get_text())
        banos = self.builderPiso.get_object("banos").get_text()
        otros = self.builderPiso.get_object("otros").get_text()
        registro = (
            propietario, enventa, enalquiler, direccion, pventa, palquiler, superficie, habitaciones, banos, otros)
        if len(propietario)==9:
            self.condicion = True
        else:
            self.emergente("Datos invalidos. ")
            self.condicion = False

        if(self.condicion):
                self.cursor.execute(
                    "INSERT INTO PISO(PROPIETARIO,ENVENTA,ENALQUILER,DIRECCION,PVENTA,PALQUILER,SUPERFICIE,HABITACIONES,BANOS,OTROS) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    registro)
                self.bbdd.commit()
                self.cursor.close()
                self.bbdd.close()
                self.fpiso.hide()
                self.emergente("Piso Agregado")
                self.actualizar()
                self.window.resize(700, 500)

    def on_eliminarPiso_clicked(self, control):
        self.coneccion()
        selection = self.vista1.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.dni = model[selec][0]
            self.cursor.execute("DELETE FROM PISO WHERE PROPIETARIO ='" + self.dni + "'")
            self.bbdd.commit()
            self.emergente("Borrado")
            self.actualizar()
        self.cursor.close()
        self.bbdd.close()

    def on_cancelar_clicked(self, control):
        self.fCliente.hide()
        self.window.resize(700, 500)

    def on_cancelarP_clicked(self, control):
        self.fpiso.hide()
        self.window.resize(700, 500)

    def on_cancelarA_clicked(self, control):
        self.faCliente.hide()
        self.window.resize(700, 500)

    def on_cancelarAp_clicked(self, control):
        self.faPiso.hide()
        self.window.resize(700, 500)

    def on_editarC_clicked(self, control):
        self.coneccion()
        selection = self.vista.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.dni = model[selec][0]
            nombre = model[selec][1]
            apellidos = model[selec][2]
            direccion = model[selec][3]
            telefono = str(model[selec][4])
            fnacimiento = model[selec][5]
            fichero3 = "faCliente.glade"
            self.builderClienteA = Gtk.Builder()
            self.builderClienteA.add_from_file(fichero3)
            self.faCliente = self.builderClienteA.get_object("faCliente")
            self.builderClienteA.get_object("dni").set_text(self.dni)
            self.builderClienteA.get_object("nombre").set_text(nombre)
            self.builderClienteA.get_object("apellidos").set_text(apellidos)
            self.builderClienteA.get_object("direccion").set_text(direccion)
            self.builderClienteA.get_object("telefono").set_text(telefono)
            self.builderClienteA.get_object("fnacimiento").set_text(fnacimiento)

            senal = {"on_actualizarCliente_clicked": self.on_actualizarCliente_clicked,
                     "on_cancelarA_clicked": self.on_cancelarA_clicked
                     }
            self.builderClienteA.connect_signals(senal)
            self.bPrincipal.pack_start(self.faCliente, False, False, 0)
            self.faCliente.show()
            self.window.show()

        self.cursor.close()
        self.bbdd.close()

    def on_actualizarCliente_clicked(self, control):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        dni = self.builderClienteA.get_object("dni").get_text()
        nombre = self.builderClienteA.get_object("nombre").get_text()
        apellidos = self.builderClienteA.get_object("apellidos").get_text()
        direccion = self.builderClienteA.get_object("direccion").get_text()
        telefono = int(self.builderClienteA.get_object("telefono").get_text())
        fnacimiento = self.builderClienteA.get_object("fnacimiento").get_text()
        dnia = self.dni
        if len(dni)==9 and telefono.isdigit and len(telefono)==9:
            self.condicion = True
        else:
            self.emergente("Datos invalidos. ")
            self.condicion = False

        if(self.condicion):
            try:
                self.cursor.execute(
                    "UPDATE CLIENTE SET DNI=@dni,NOMBRE=@nombre,APELLIDOS=@apellidos,DIRECCION=@direccion,TELEFONO=@telefono,FNACIMIENTO=@fnacimiento WHERE DNI = @dnia",
                    [dni, nombre, apellidos, direccion, telefono, fnacimiento, dnia])
                self.bbdd.commit()
                self.cursor.close()
                self.bbdd.close()
                self.faCliente.hide()
                self.emergente("Cliente modificado")
                self.actualizar()
                self.window.resize(700, 500)
            except dbapi.IntegrityError:
                self.emergente("El Cliente ya existe")


    def on_editarP_clicked(self, control):
        self.coneccion()
        selection = self.vista1.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.propietario = model[selec][0]
            enventa = model[selec][1]
            enalquiler = model[selec][2]
            direccion = model[selec][3]
            pventa = str(model[selec][4])
            palquiler = model[selec][5]
            superficie = model[selec][6]
            habitaciones = model[selec][7]
            banos = model[selec][8]
            otros = model[selec][9]
            fichero3 = "faPiso.glade"
            self.builderP = Gtk.Builder()
            self.builderP.add_from_file(fichero3)
            self.faPiso = self.builderP.get_object("faPiso")
            self.builderP.get_object("propietario").set_text(self.propietario)
            venta = self.builderP.get_object("enventa")
            if enventa == "si":
                venta.set_active(True)
            else:
                venta.set_active(False)
            alquiler = self.builderP.get_object("enalquiler")
            if enalquiler == "si":
                alquiler.set_active(True)
            else:
                alquiler.set_active(False)
            self.builderP.get_object("direccion").set_text(direccion)
            self.builderP.get_object("pventa").set_text(pventa)
            self.builderP.get_object("palquiler").set_text(palquiler)
            self.builderP.get_object("superficie").set_text(superficie)
            self.builderP.get_object("habitaciones").set_text(habitaciones)
            self.builderP.get_object("banos").set_text(banos)
            self.builderP.get_object("otros").set_text(otros)
            senal = {"on_actualizarPiso_clicked": self.on_actualizarPiso_clicked,
                     "on_cancelarP_clicked": self.on_cancelarAp_clicked
                     }
            self.builderP.connect_signals(senal)
            self.bPrincipal.pack_start(self.faPiso, False, False, 0)
            self.faPiso.show()
            self.window.show()
        self.cursor.close()
        self.bbdd.close()

    def on_actualizarPiso_clicked(self, control):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        propietario = self.builderP.get_object("propietario").get_text()
        benventa = self.builderP.get_object("enventa")
        if benventa.get_active():
            enventa = "si"
        else:
            enventa = "no"
        benalquiler = self.builderP.get_object("enalquiler")
        if benalquiler.get_active():
            enalquiler = "si"
        else:
            enalquiler = "no"
        direccion = self.builderP.get_object("direccion").get_text()
        pventa = int(self.builderP.get_object("pventa").get_text())
        palquiler = self.builderP.get_object("palquiler").get_text()
        superficie = self.builderP.get_object("superficie").get_text()
        habitaciones = int(self.builderP.get_object("habitaciones").get_text())
        banos = self.builderP.get_object("banos").get_text()
        otros = self.builderP.get_object("otros").get_text()
        propietarioa = self.propietario
        if len(propietario)==9:
            self.condicion = True
        else:
            self.emergente("Datos invalidos. ")
            self.condicion = False

        if(self.condicion):
            self.cursor.execute(
                "UPDATE PISO SET PROPIETARIO=@propietario,ENVENTA=@enventa,ENALQUILER=@enalquiler,DIRECCION=@direccion,PVENTA=@pventa,"
                "PALQUILER=@palquiler,SUPERFICIE=@superficie,HABITACIONES=@habitaciones,BANOS=@banos,OTROS=@otros WHERE PROPIETARIO = @propietarioa",
                [propietario, enventa, enalquiler, direccion, pventa, palquiler, superficie, habitaciones, banos, otros,
                 propietarioa])
            self.bbdd.commit()
            self.cursor.close()
            self.bbdd.close()
            self.faPiso.hide()
            self.emergente("Piso modificado")
            self.actualizar()
            self.window.resize(700, 500)
    def actualizar(self):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        lista = Gtk.ListStore(str, str, str, str, str, str)
        self.cursor.execute("SELECT * FROM CLIENTE")
        for fila in self.cursor:
            lista.append(fila)
        self.vista.set_model(lista)
        self.vista.show()
        lista1 = Gtk.ListStore(str, str, str, str, str, str, str,str,str,str)
        self.cursor.execute("SELECT * FROM PISO")
        for fila in self.cursor:
            lista1.append(fila)
        self.vista1.set_model(lista1)
        self.vista1.show()
        self.bbdd.commit()
        self.cursor.close()
        self.bbdd.close()

    def actualizara(self,control):
        if os.path.exists("basedatos.dat"):
            self.coneccion()
        else:
            self.crearbd()
        lista = Gtk.ListStore(str, str, str, str, str, str)
        self.cursor.execute("SELECT * FROM CLIENTE")
        for fila in self.cursor:
            lista.append(fila)
        self.vista.set_model(lista)
        self.vista.show()
        lista1 = Gtk.ListStore(str, str, str, str, str, str, str,str,str,str)
        self.cursor.execute("SELECT * FROM PISO")
        for fila in self.cursor:
            lista1.append(fila)
        self.vista1.set_model(lista1)
        self.vista1.show()
        self.bbdd.commit()
        self.cursor.close()
        self.bbdd.close()

    def emergente(self, mensaje):  # Ventana emergente de error.
        vent_emergente = Gtk.Window(title="MENSAJE")
        vent_emergente.set_size_request(500, 100)
        vent_emergente.set_resizable(False)
        caja = Gtk.Box()
        label = Gtk.Label()
        label.set_text("    " + mensaje)
        vent_emergente.add(caja)
        caja.add(label)
        vent_emergente.show_all()


w = Principal()
Gtk.main()
