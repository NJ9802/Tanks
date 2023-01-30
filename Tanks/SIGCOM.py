from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from validations import validate_time, validate_numeric_entry
from db_main import update_darkmode, update_stock, update_gee
from db_main import all_gee, all_tanks, darkmode

from to_excel import write_to_excel


class Aplicacion:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Sistema de Gestion del Combustible')
        self.root.resizable(0, 0)
        self.root.geometry('+0+0')
        self.root.option_add('*tearOff', False)
        self.root.tk.call('lappend', 'auto_path',
                          'themes/tkBreeze-master')
        self.estilo = Style()

        # Tanks Variables
        self.cm = DoubleVar()
        self.localizacion = StringVar(value=all_tanks[0].location)
        self.existencia = DoubleVar()
        self.consumo = DoubleVar()

        self.tank_percent_list = []

        for tank in all_tanks:
            self.tank_percent_list.append(DoubleVar())

        self.existencia_anterior = DoubleVar()
        self.medicion_anterior = DoubleVar()
        self.entrada_litros = DoubleVar()
        self.localizacion_entrada = StringVar(value=all_tanks[0].location)

        # GEE variables
        self.horametros_var_list = []
        for gee in all_gee:
            self.horametros_var_list.append(StringVar(value=gee.horametro))

        self.gee = StringVar(value=all_gee[0])

        self.modo_oscuro = BooleanVar()

        # Chequear si estaba activado el modo oscuro
        if darkmode.on:
            self.estilo.theme_use('breeze-dark')
            self.estilo.configure('variable.TLabel', background='#3b3b3c')
            self.estilo.configure(
                'dark.Vertical.TProgressbar', background='#3e3e3e')
            self.modo_oscuro.set(1)

        else:
            self.estilo.theme_use('breeze')

        # Menu
        barramenu = Menu(self.root)
        self.root['menu'] = barramenu
        menu1 = Menu(barramenu)
        menu2 = Menu(barramenu)
        menu3 = Menu(barramenu)

        barramenu.add_cascade(menu=menu1,
                              label='Archivo')
        barramenu.add_cascade(menu=menu2,
                              label='Opciones')
        barramenu.add_cascade(menu=menu3, label='Estilo')

        menu1.add_command(label='Guardar',
                          command=self.guardar, underline=0,
                          accelerator='Ctrl+g')
        menu1.add_separator()
        menu1.add_command(label='Salir',
                          command=lambda: self.root.destroy(), underline=0,
                          accelerator='Alt+F4')

        menu2.add_command(label='Establecer valor inicial',
                          command=self.valor_inicial)
        menu2.add_command(label='Tablas de Aforo',
                          underline=0, command=self.seleccionar_tablas,
                          accelerator='Ctrl+t')
        menu2.add_command(label='Entrada de Combustible',
                          underline=0, command=self.entrada,
                          accelerator='Ctrl+e')

        menu3.add_checkbutton(label='Modo oscuro', variable=self.modo_oscuro,
                              command=self.switch_darkmode)

        # Barra de estado
        self.mensaje = ' Hecho por Nelson J. Aldazabal Hernandez.'
        self.barra_estado = Label(self.root, text=self.mensaje,
                                  border=1, relief='sunken',
                                  anchor='w')

        # NoteBook y Frames
        notebook = Notebook(self.root)

        tanks_frame = Frame(notebook)
        gee_frame = Frame(notebook)

        notebook.grid()
        tanks_frame.grid()
        gee_frame.grid()

        notebook.add(tanks_frame, text='Tanques')
        notebook.add(gee_frame, text='GEE')

        # Tanks Widgets
        medicion_cm_label = Label(
            tanks_frame, text='Medicion en cm:')
        self.medicion_cm = Entry(
            tanks_frame, textvariable=self.cm, width=6)

        tanques_label = Label(
            tanks_frame, text='Seleccione el Tanque:')

        for index, tank in enumerate(all_tanks):
            Radiobutton(tanks_frame, text=tank.location,
                        variable=self.localizacion, value=tank.location, command=self.actualizar_valores).grid(
                column=1, row=index, padx=10, pady=10, sticky='w')

        existencia_final_label = Label(tanks_frame,
                                       text='Existencia Final:')
        existencia_final = Label(tanks_frame, width=10,
                                 textvariable=self.existencia,
                                 anchor='e', style='variable.TLabel')

        existencia_anterior_label = Label(tanks_frame,
                                          text='Existencia Anterior:')
        existencia_anterior_cm = Label(tanks_frame, width=10,
                                       textvariable=self.existencia_anterior,
                                       anchor='e', style='variable.TLabel')

        medicion_anterior_label = Label(tanks_frame,
                                        text='Medicion Anterior:')
        medicion_anterior_cm = Label(tanks_frame, width=10,
                                     textvariable=self.medicion_anterior,
                                     anchor='e', style='variable.TLabel')

        gasto_combustible_label = Label(tanks_frame,
                                        text='Consumido:')
        gasto_combustible = Label(tanks_frame, width=10,
                                  textvariable=self.consumo,
                                  anchor='e', style='variable.TLabel')

        boton_calcular = Button(tanks_frame, text='Calcular',
                                command=self.calcular)

        for index, tank in enumerate(all_tanks):
            Label(tanks_frame, text=tank.location).grid(
                column=index+3, row=0, padx=5, pady=10)
            Progressbar(tanks_frame, orient='vertical', variable=self.tank_percent_list[index],
                        length=270, style='dark.Vertical.TProgressbar').grid(column=index+3, row=1, padx=5, pady=5,
                                                                             rowspan=10)
        separador1 = Separator(tanks_frame, orient='horizontal')
        separador2 = Separator(tanks_frame, orient='horizontal')
        separador_vertical = Separator(
            tanks_frame, orient='vertical')

        # Tanks Posicion
        tanques_label.grid(column=0, row=0, padx=10, pady=10)

        separador1.grid(column=0, row=index+1, columnspan=2,
                        pady=5, padx=5, sticky="ew")

        medicion_anterior_label.grid(
            column=0, row=index+2, padx=10, pady=10)
        medicion_anterior_cm.grid(column=1, row=index+2, padx=10, pady=10)

        medicion_cm_label.grid(column=0, row=index+3, padx=10, pady=10)
        self.medicion_cm.grid(column=1, row=index+3,
                              sticky='e', padx=10, pady=10)

        separador2.grid(column=0, row=index+4, columnspan=2,
                        padx=5, pady=5, sticky="ew")

        existencia_anterior_label.grid(column=0, row=index+5,
                                       padx=10, pady=10)
        existencia_anterior_cm.grid(column=1, row=index+5,
                                    padx=10, pady=10)

        existencia_final_label.grid(column=0, row=index+6,
                                    padx=10, pady=10)
        existencia_final.grid(column=1, row=index+6,
                              padx=10, pady=10)

        gasto_combustible_label.grid(column=0, row=index+7,
                                     padx=10, pady=10)
        gasto_combustible.grid(column=1, row=index+7, padx=10, pady=10)

        boton_calcular.grid(column=0, row=index+8, padx=10, pady=10,
                            columnspan=2)

        separador_vertical.grid(column=2, row=0, rowspan=index+9,
                                padx=5, pady=5, sticky='ns')

        self.barra_estado.grid(column=0, row=1,
                               columnspan=6, sticky='ew')

        # GEE Widgets
        gee_label = Label(gee_frame, text='Grupos Electrogenos')
        horametro_label = Label(gee_frame, text='Horametro')

        for index, gee in enumerate(all_gee):
            Radiobutton(gee_frame, text=gee, variable=self.gee,
                        value=gee).grid(column=0, row=index+1)
            Label(gee_frame, textvariable=self.horametros_var_list[index]).grid(
                column=1, row=index+1)

        gee_separator = Separator(gee_frame, orient='horizontal')

        operacion_button = Button(
            gee_frame, text='Operacion', command=self.operacion)
        info_button = Button(gee_frame, text='Informacion')

        # GEE position
        gee_label.grid(column=0, row=0, pady=10, padx=10)
        horametro_label.grid(column=1, row=0, pady=10, padx=10)

        gee_separator.grid(
            column=0, row=index+2, columnspan=2, sticky='we', padx=10)

        operacion_button.grid(column=0, row=index+3, padx=10)
        info_button.grid(column=1, row=index+3, padx=10)

        gee_frame.columnconfigure(0, weight=1)
        gee_frame.columnconfigure(1, weight=1)

        for number in range(index+4):
            gee_frame.rowconfigure(number, weight=1)

        # Funciones iniciales

        # Valor inicial de medicion anterior y existencia anterior
        self.medicion_anterior.set(all_tanks[0].height_cm)
        self.existencia_anterior.set(all_tanks[0].stock)

        # Actualizar por ciento en barras
        for index, tank in enumerate(all_tanks):
            self.tank_percent_list[index].set(tank.percent())

        # Enfoque inicial
        self.medicion_cm.focus_set()
        self.cm.set('')

        # Limpiar campo al hacer click
        self.medicion_cm.bind('<Button-1>', lambda _: self.cm.set(''))

        # Calcular al presionar ENTER
        self.medicion_cm.bind('<Return>', lambda _: self.calcular())

        # Guardar
        self.root.bind('<Control-g>', lambda _: self.guardar())

        self.root.bind('<Control-e>', lambda _: self.entrada())

        self.root.bind('<Control-t>', lambda _: self.seleccionar_tablas())

        self.root.mainloop()

    # Metodos de la Aplicacion
    def switch_darkmode(self):
        if not self.modo_oscuro.get():
            self.estilo.theme_use('breeze')
            update_darkmode(False)

        else:
            self.estilo.theme_use('breeze-dark')
            update_darkmode(True)

    def actualizar_valores(self):
        self.existencia.set(0.0)
        self.consumo.set(0.0)
        self.cm.set('')
        self.medicion_cm.focus_set()

        for tank in all_tanks:
            if tank.location == self.localizacion.get():
                self.medicion_anterior.set(tank.height_cm)
                self.existencia_anterior.set(tank.stock)
                break

    def calcular(self):
        try:
            cm = self.cm.get()
        except:
            self.consumo.set('Error!')
            self.existencia.set('Error!')
            self.barra_estado['text'] = 'Medicion en cm tiene que tener un valor numerico'
            self.root.after(4000,
                            lambda: self.barra_estado.config(text=self.mensaje))
            return 1

        for index, tank in enumerate(all_tanks):
            if tank.location == self.localizacion.get():
                actual_stock = tank.volume(cm)

                if type(actual_stock) == str:
                    messagebox.showerror('Error', actual_stock)
                    return 1

                self.consumo.set(
                    round(self.existencia_anterior.get()-actual_stock, 2))
                self.existencia.set(actual_stock)
                self.tank_percent_list[index].set(tank.percent())
                break

    def guardar(self):
        for tank in all_tanks:
            update_stock(tank)

        self.barra_estado['text'] = 'Actualizado correctamente'
        self.root.after(2000,
                        lambda: self.barra_estado.config(text=self.mensaje))

    def entrada(self):
        entrada = Toplevel()
        entrada.title('Entrada')
        entrada.resizable(0, 0)

        entrada_frame = Frame(entrada)
        tanques_label = Label(entrada_frame,
                              text='Seleccione el Tanque:')

        for index, tank in enumerate(all_tanks):
            Radiobutton(entrada_frame, text=tank.location, variable=self.localizacion_entrada,
                        value=tank.location).grid(column=1, row=index, padx=5, pady=5, sticky='w')

        l_entrada = Label(entrada_frame, text='Entrada:')
        e_entrada = Entry(entrada_frame, textvariable=self.entrada_litros,
                          width=10)
        b_aceptar = Button(entrada_frame, text='Confirmar',
                           command=self.confirmar_entrada)
        b_salir = Button(entrada_frame, text='Salir',
                         command=entrada.destroy)
        separador = Separator(entrada_frame, orient='horizontal')

        entrada_frame.grid()

        tanques_label.grid(column=0, row=0, padx=5, pady=5)
        l_entrada.grid(column=0, row=index+1, padx=5, pady=5)
        e_entrada.grid(column=1, row=index+1, padx=5, pady=5)
        separador.grid(column=0, row=index+2, padx=5,
                       pady=5, columnspan=2, sticky='ew')
        b_aceptar.grid(column=0, row=index+3, padx=5, pady=5)
        b_salir.grid(column=1, row=index+3, padx=5, pady=5)

        entrada.transient(self.root)
        entrada.grab_set()
        entrada.bind('<Return>', lambda _: self.confirmar_entrada())

        e_entrada.bind('<Button-1>', lambda _: self.entrada_litros.set(''))

        entrada.focus_set()

        self.root.wait_window(entrada)

    def confirmar_entrada(self):
        try:
            entrada = self.entrada_litros.get()
        except:
            self.barra_estado['text'] = 'Introduzca la entrada en litros'
            self.root.after(4000,
                            lambda: self.barra_estado.config(text=self.mensaje))
            return 1

        for index, tank in enumerate(all_tanks):
            if tank.location == self.localizacion_entrada.get():
                tank.stock += entrada
                update_stock(tank)
                self.tank_percent_list[index].set(tank.percent())
                break

        self.actualizar_valores()
        self.barra_estado['text'] = 'Actualizado correctamente'
        self.root.after(2000,
                        lambda: self.barra_estado.config(text=self.mensaje))

    def valor_inicial(self):
        ventana = Toplevel()
        ventana.title = 'Valor inicial'
        ventana.resizable(0, 0)

        ventana_frame = Frame(ventana)
        label = Label(ventana_frame, text='Establecer valor inicial')

        for index, tank in enumerate(all_tanks):
            Radiobutton(ventana_frame, text=tank.location, variable=self.localizacion_entrada,
                        value=tank.location).grid(column=1, row=index, padx=5, pady=5, sticky='w')

        l_entrada = Label(ventana_frame, text='Valor inicial:')
        e_entrada = Entry(ventana_frame, textvariable=self.entrada_litros,
                          width=10)
        b_aceptar = Button(ventana_frame, text='Confirmar',
                           command=self.establecer_valor_inicial)
        b_salir = Button(ventana_frame, text='Salir',
                         command=ventana.destroy)
        separador = Separator(ventana_frame, orient='horizontal')

        ventana_frame.grid()

        label.grid(column=0, row=0, padx=5, pady=5)
        l_entrada.grid(column=0, row=index+1, padx=5, pady=5)
        e_entrada.grid(column=1, row=index+1, padx=5, pady=5)
        separador.grid(column=0, row=index+2, padx=5,
                       pady=5, columnspan=2, sticky='ew')
        b_aceptar.grid(column=0, row=index+3, padx=5, pady=5)
        b_salir.grid(column=1, row=index+3, padx=5, pady=5)

        ventana.transient(self.root)
        ventana.grab_set()
        ventana.bind('<Return>', lambda _: self.establecer_valor_inicial())

        e_entrada.bind('<Button-1>', lambda _: self.entrada_litros.set(''))

        ventana.focus_set()

        self.root.wait_window(ventana)

    def establecer_valor_inicial(self):
        try:
            entrada = self.entrada_litros.get()
        except:
            self.barra_estado['text'] = 'Introduzca el valor inicial en litros'
            self.root.after(4000,
                            lambda: self.barra_estado.config(text=self.mensaje))
            return 1

        for index, tank in enumerate(all_tanks):
            if tank.location == self.localizacion_entrada.get():
                tank.stock = entrada
                update_stock(tank)
                self.tank_percent_list[index].set(tank.percent())
                break

        self.actualizar_valores()
        self.barra_estado['text'] = 'Actualizado correctamente'
        self.root.after(2000,
                        lambda: self.barra_estado.config(text=self.mensaje))

    def seleccionar_tablas(self):
        ventana = Toplevel()
        ventana.title('Tablas certificadas')
        ventana.resizable(0, 0)

        ventana_frame = Frame(ventana)

        for index, tank in enumerate(all_tanks):
            Radiobutton(ventana_frame, text=f'Tabla de {tank.location}', variable=self.localizacion_entrada,
                        value=tank.location).grid(column=0, row=index, padx=10, pady=10, sticky='we')

        b_ver = Button(ventana_frame, text='Ver', command=self.ver)

        ventana_frame.grid(sticky='swe')

        b_ver.grid(column=0, row=index+1, padx=10, pady=10,
                   sticky='we')

        ventana.columnconfigure(0, weight=1)
        for number in range(index+1):
            ventana.rowconfigure(number, weight=1)

        ventana.bind('<Return>', lambda _: self.ver())

        ventana.transient(self.root)
        ventana.focus_set()

        self.root.wait_window(ventana)

    def ver(self):
        ver = Toplevel()

        for tank in all_tanks:
            if tank.location == self.localizacion_entrada.get():
                title = f'Tabla {tank.location}'
                file = f'tablas/{tank.location}.jpg'
                img = Image.open(file).rotate(270, expand=1)
                break

        ver.title(title)

        heigth = self.root.winfo_screenheight()
        width = self.root.winfo_screenwidth()
        img = ImageTk.PhotoImage(img.resize((width, heigth)))
        l_img = Label(ver, image=img)

        l_img.grid(column=0, row=0)

        ver.focus_set()

        self.root.wait_window(ver)

    # Metodos GEE
    def operacion(self):
        ventana = Toplevel(self.root)
        ventana.title('Operacion')
        ventana.resizable(0, 0)
        ventana.geometry(f'+{round(self.root.winfo_width()+10)}+0')

        # variables
        self.var_hora_inicial = StringVar()
        self.var_hora_final = StringVar()
        self.var_horametro_inicial = StringVar()
        self.var_horametro_final = StringVar()
        self.var_tiempo_horas = DoubleVar()
        self.var_energia_generada = DoubleVar()
        self.var_demanda_liberada = DoubleVar()
        self.var_consumo = DoubleVar()
        self.horametro_roto = BooleanVar()
        self.var_existencia = DoubleVar()

        for gee in all_gee:
            if gee.name == self.gee.get():
                self.gee_obj = gee
                break

        self.var_horametro_inicial.set(self.gee_obj.horametro)

        mt_label = Label(ventana, text=self.gee_obj)
        fecha_label = Label(ventana, text='Fecha')
        tipo_de_operacion = Label(ventana, text='Tipo')
        hora_de_inicio = Label(ventana, text='Hora Inicio (HH:MM)')
        hora_final = Label(ventana, text='Hora Final (HH:MM)')
        horametro_inicial = Label(ventana, text='Horametro inicial')
        horametro_final = Label(ventana, text='Horametro final')
        tiempo_horas = Label(ventana, text='Tiempo Horas', state='readonly')
        energia_generada = Label(ventana, text='Energia Generada')
        demanda_liberada = Label(ventana, text='Demanda Liberada')
        consumo = Label(ventana, text='Consumo')
        l_horametro_roto = Label(ventana, text='Horametro Roto')
        existencia_final = Label(ventana, text='Existencia Final')

        self.e_fecha = DateEntry(
            ventana, state='readonly', width=8, date_pattern='dd/mm/yy')
        e_hora_inicial = Entry(
            ventana, textvariable=self.var_hora_inicial, width=8, validate='key',
            validatecommand=(self.root.register(validate_time), '%P'))
        self.e_hora_final = Entry(
            ventana, textvariable=self.var_hora_final, width=8, state='readonly',
            validate='key',
            validatecommand=(self.root.register(validate_time), '%P'))
        self.e_tipo = Combobox(ventana, values=[
            'PS', 'PC', 'IA', 'LD', 'SS', 'GA', 'RO', 'IU', 'LC', 'LS'], width=3,
            state='readonly')
        self.e_horametro_inicial = Entry(
            ventana, textvariable=self.var_horametro_inicial, width=8, state='readonly')
        self.e_horametro_final = Entry(
            ventana, textvariable=self.var_horametro_final, width=8,
            validate='key',
            validatecommand=(self.root.register(validate_numeric_entry), '%S'))
        e_tiempo_horas = Entry(
            ventana, textvariable=self.var_tiempo_horas, width=8, state='readonly')
        e_energia_generada = Entry(
            ventana, textvariable=self.var_energia_generada, width=8, state='readonly')
        e_demanda_liberada = Entry(
            ventana, textvariable=self.var_demanda_liberada, width=8, state='readonly')
        e_consumo = Entry(ventana, textvariable=self.var_consumo, width=8,
                          validate='key',
                          validatecommand=(self.root.register(validate_numeric_entry), '%S'))
        w_horametro_roto = Checkbutton(
            ventana, variable=self.horametro_roto, command=self.f_horametro_roto)
        e_existencia_final = Entry(
            ventana, textvariable=self.var_existencia, width=8, state='readonly')

        separador1 = Separator(ventana, orient='horizontal')
        separador2 = Separator(ventana, orient='horizontal')
        separador3 = Separator(ventana, orient='horizontal')

        button = Button(ventana, command=self.procesar_datos, text='Procesar')
        self.excel_button = Button(ventana, text='Registrar', state='disabled',
                                   command=self.registrar_datos)

        # Position
        mt_label.grid(column=0, row=0, columnspan=2, pady=10, padx=10)

        separador1.grid(column=0, row=1, padx=10,
                        sticky='we', columnspan=2)

        l_horametro_roto.grid(column=0, row=2, pady=10, padx=10,)

        separador2.grid(column=0, row=3, padx=10,
                        sticky='we', columnspan=2)

        fecha_label.grid(column=0, row=4, pady=10, padx=10, sticky='e')
        tipo_de_operacion.grid(column=0, row=5, pady=10, padx=10, sticky='e')
        hora_de_inicio.grid(column=0, row=6, pady=10, padx=10, sticky='e')
        hora_final.grid(column=0, row=7, pady=10, padx=10, sticky='e')
        horametro_inicial.grid(
            column=0, row=8, pady=10, padx=10, sticky='e')
        horametro_final.grid(
            column=0, row=9, pady=10, padx=10, sticky='e')
        tiempo_horas.grid(column=0, row=10, pady=10, padx=10, sticky='e')
        energia_generada.grid(column=0, row=11, pady=10, padx=10, sticky='e')
        demanda_liberada.grid(column=0, row=12, pady=10, padx=10, sticky='e')
        consumo.grid(column=0, row=13, pady=10, padx=10, sticky='e')
        existencia_final.grid(column=0, row=14, pady=10, padx=10, sticky='e')

        w_horametro_roto.grid(column=1, row=2, padx=10, pady=10)
        self.e_fecha.grid(column=1, row=4, padx=10, pady=10)
        self.e_tipo.grid(column=1, row=5, padx=10, pady=10)
        e_hora_inicial.grid(column=1, row=6, padx=10, pady=10)
        self.e_hora_final.grid(column=1, row=7, padx=10, pady=10)
        self.e_horametro_inicial.grid(column=1, row=8, padx=10, pady=10)
        self.e_horametro_final.grid(column=1, row=9, padx=10, pady=10)
        e_tiempo_horas.grid(column=1, row=10, pady=10, padx=10)
        e_energia_generada.grid(column=1, row=11, padx=10, pady=10)
        e_demanda_liberada.grid(column=1, row=12, padx=10, pady=10)
        e_consumo.grid(column=1, row=13, padx=10, pady=10)
        e_existencia_final.grid(column=1, row=14, padx=10, pady=10)

        separador3.grid(column=0, row=15, padx=10,
                        pady=10, sticky='we', columnspan=2)

        button.grid(column=0, row=16, padx=10, pady=10)
        self.excel_button.grid(column=1, row=16, padx=10, pady=10)

        if self.gee_obj.horametro == 'Roto':
            self.horametro_roto.set(True)
            self.f_horametro_roto()

        e_consumo.bind('<Button-1>', lambda _: self.var_consumo.set(''))
        ventana.grab_set()
        self.root.wait_window(ventana)

    def f_horametro_roto(self):
        if self.horametro_roto.get():
            self.e_horametro_final.configure(state='readonly')
            self.e_hora_final.configure(state='normal')
            self.var_horametro_inicial.set('Roto')
            self.var_horametro_final.set('Roto')

        else:
            self.e_hora_final.configure(state='readonly')
            self.e_horametro_final.configure(state='normal')
            self.var_horametro_inicial.set(self.gee_obj.horametro)
            self.var_horametro_final.set('')

    def procesar_datos(self):
        roto = self.horametro_roto.get()
        tipo = self.e_tipo.get()
        hora_inicial = self.var_hora_inicial.get()
        consumo_s = self.var_consumo.get()

        for index, entry in enumerate([tipo, hora_inicial, consumo_s]):
            if not entry:
                if index == 0:
                    field = 'Tipo'
                elif index == 1:
                    field = 'Hora Inicial'
                else:
                    field = 'Consumo'

                messagebox.showwarning(
                    'Faltan Campos', f'El campo {field} esta vacio')
                return 1

        if roto:
            hora_final = self.var_hora_final.get()

            if not hora_final:
                messagebox.showwarning(
                    'Faltan Campos', 'El campo Hora Final esta vacio')
                return 1

            else:
                processed_data = self.gee_obj.operacion(tipo=tipo, hora_inicial=hora_inicial,
                                                        consumo=consumo_s, horametro_roto=roto, hora_final=hora_final)

        else:
            horametro = self.var_horametro_final.get()
            if not horametro:
                messagebox.showwarning(
                    'Faltan Campos', 'El campo Horamemtro Final esta vacio')
                return 1

            else:
                processed_data = self.gee_obj.operacion(tipo=tipo, hora_inicial=hora_inicial,
                                                        consumo=consumo_s, horametro_roto=roto, horametro_final=horametro)

        if type(processed_data) == str:
            messagebox.showerror('Error', processed_data)

        else:
            self.var_tiempo_horas.set(processed_data['tiempo_horas'])
            self.var_hora_final.set(processed_data['hora_final'])
            self.var_energia_generada.set(processed_data['energia_generada'])
            self.var_demanda_liberada.set(processed_data['demanda_liberada'])
            self.var_existencia.set(self.gee_obj.tank.stock)

            if processed_data['sobreconsumo']:
                messagebox.showwarning(
                    'Sobreconsumo', 'Existe sobreconsumo en la operacion')

            else:
                self.excel_button['state'] = 'normal'

                self.data_to_excel = processed_data
                self.data_to_excel['fecha'] = self.e_fecha.get()

    def registrar_datos(self):
        try:
            write_to_excel(self.data_to_excel)
            messagebox.showinfo('Info', 'Operacion registrada correctamente')
            self.excel_button['state'] = DISABLED

            # Update horametro_final value in database and GUI
            horametro = self.data_to_excel['horametro_final']
            self.horametros_var_list[all_gee.index(
                self.gee_obj)].set(horametro)

            self.gee_obj.horametro = horametro
            update_gee(self.gee_obj)

        except Exception as e:
            messagebox.showerror('Error', f'Existe un error en la operacion')
            print(e)


def main():
    app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
