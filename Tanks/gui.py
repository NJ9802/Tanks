from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkcalendar import DateEntry
from cylinder_volume import villa_cuba, casas, morlas, mt_487, mt_488, mt_443, mt_489, mt_452, darkmode
from PIL import Image, ImageTk
from validations import validate_time, validate_numeric_entry
from db_main import update_darkmode, update_stock


class Aplicacion:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Calculo de Combustible en Tanques')
        self.root.resizable(0, 0)
        self.root.option_add('*tearOff', False)
        self.root.tk.call('lappend', 'auto_path',
                          'themes/tkBreeze-master')
        self.estilo = Style()

        # Tanks Variables
        self.cm = DoubleVar()
        self.localizacion = StringVar(value='vc')
        self.existencia = DoubleVar()
        self.consumo = DoubleVar()
        self.vc_percent = DoubleVar()
        self.cs_percent = DoubleVar()
        self.mo_percent = DoubleVar()
        self.existencia_anterior = DoubleVar()
        self.medicion_anterior = DoubleVar()
        self.entrada_litros = DoubleVar()
        self.localizacion_entrada = StringVar(value='vc')

        # GEE variables
        self.horametro_mt487 = DoubleVar()
        self.horametro_mt488 = DoubleVar()
        self.horametro_mt489 = DoubleVar()
        self.horametro_mt443 = DoubleVar()
        self.horametro_mt452 = DoubleVar()

        self.gee = StringVar(value='MT-487')

        self.modo_oscuro = BooleanVar()

        # Chequear si estaba activado el modo oscuro
        if darkmode.on == 1:
            self.estilo.theme_use('breeze-dark')
            self.estilo.configure('variable.TLabel', background='#3b3b3c')
            self.estilo.configure(
                'dark.Vertical.TProgressbar', background='#3e3e3e')
            self.modo_oscuro.set(1)

        else:
            self.estilo.theme_use('breeze')

        # Menu
        self.barramenu = Menu(self.root)
        self.root['menu'] = self.barramenu
        self.menu1 = Menu(self.barramenu)
        self.menu2 = Menu(self.barramenu)
        self.menu3 = Menu(self.barramenu)

        self.barramenu.add_cascade(menu=self.menu1,
                                   label='Archivo')
        self.barramenu.add_cascade(menu=self.menu2,
                                   label='Opciones')
        self.barramenu.add_cascade(menu=self.menu3, label='Estilo')

        self.menu1.add_command(label='Guardar',
                               command=self.guardar, underline=0,
                               accelerator='Ctrl+g')
        self.menu1.add_separator()
        self.menu1.add_command(label='Salir',
                               command=lambda: self.root.destroy(), underline=0,
                               accelerator='Alt+F4')

        self.menu2.add_command(label='Establecer valor inicial',
                               command=self.valor_inicial)
        self.menu2.add_command(label='Tablas de Aforo',
                               underline=0, command=self.seleccionar_tablas,
                               accelerator='Ctrl+t')
        self.menu2.add_command(label='Entrada de Combustible',
                               underline=0, command=self.entrada,
                               accelerator='Ctrl+e')

        self.menu3.add_checkbutton(label='Modo oscuro', variable=self.modo_oscuro,
                                   command=self.switch_darkmode)

        # Barra de estado
        self.mensaje = ' Hecho por Nelson J. Aldazabal Hernandez.'
        self.barra_estado = Label(self.root, text=self.mensaje,
                                  border=1, relief='sunken',
                                  anchor='w')

        # NoteBook y Frames
        self.notebook = Notebook(self.root)

        self.tanks_frame = Frame(self.notebook)
        self.gee_frame = Frame(self.notebook)

        self.notebook.grid()
        self.tanks_frame.grid()
        self.gee_frame.grid()

        self.notebook.add(self.tanks_frame, text='Tanques')
        self.notebook.add(self.gee_frame, text='GEE')

        # Tanks Widgets
        self.medicion_cm_label = Label(
            self.tanks_frame, text='Medicion en cm:')
        self.medicion_cm = Entry(
            self.tanks_frame, textvariable=self.cm, width=6)

        self.tanques_label = Label(self.tanks_frame,
                                   text='Seleccione el Tanque:')
        self.tanque_vc = Radiobutton(self.tanks_frame, text='Villa Cuba',
                                     variable=self.localizacion,
                                     value='vc',
                                     command=self.actualizar_valores)
        self.tanque_cs = Radiobutton(self.tanks_frame, text='Casas',
                                     variable=self.localizacion,
                                     value='cs',
                                     command=self.actualizar_valores)
        self.tanque_mo = Radiobutton(self.tanks_frame, text='Las Morlas',
                                     variable=self.localizacion,
                                     value='mo',
                                     command=self.actualizar_valores)

        self.existencia_final_label = Label(self.tanks_frame,
                                            text='Existencia Final:')
        self.existencia_final = Label(self.tanks_frame, width=10,
                                      textvariable=self.existencia,
                                      anchor='e', style='variable.TLabel')

        self.existencia_anterior_label = Label(self.tanks_frame,
                                               text='Existencia Anterior:')
        self.existencia_anterior_cm = Label(self.tanks_frame, width=10,
                                            textvariable=self.existencia_anterior,
                                            anchor='e', style='variable.TLabel')

        self.medicion_anterior_label = Label(self.tanks_frame,
                                             text='Medicion Anterior:')
        self.medicion_anterior_cm = Label(self.tanks_frame, width=10,
                                          textvariable=self.medicion_anterior,
                                          anchor='e', style='variable.TLabel')

        self.gasto_combustible_label = Label(self.tanks_frame,
                                             text='Consumido:')
        self.gasto_combustible = Label(self.tanks_frame, width=10,
                                       textvariable=self.consumo,
                                       anchor='e', style='variable.TLabel')

        self.boton_calcular = Button(self.tanks_frame, text='Calcular',
                                     command=self.calcular)

        self.vc_label = Label(self.tanks_frame,
                              text='Villa Cuba')
        self.cs_label = Label(self.tanks_frame,
                              text='Casas')
        self.mo_label = Label(self.tanks_frame,
                              text='Las Morlas')
        self.vc_progressbar = Progressbar(self.tanks_frame,
                                          orient='vertical',
                                          variable=self.vc_percent,
                                          length=270, style='dark.Vertical.TProgressbar')
        self.cs_progressbar = Progressbar(self.tanks_frame,
                                          orient='vertical',
                                          variable=self.cs_percent,
                                          length=270, style='dark.Vertical.TProgressbar')
        self.mo_progressbar = Progressbar(self.tanks_frame,
                                          orient='vertical',
                                          variable=self.mo_percent,
                                          length=270, style='dark.Vertical.TProgressbar')

        self.separador1 = Separator(self.tanks_frame, orient='horizontal')
        self.separador2 = Separator(self.tanks_frame, orient='horizontal')
        self.separador_vertical = Separator(
            self.tanks_frame, orient='vertical')

        # GEE Widgets
        self.gee_label = Label(self.gee_frame, text='Grupos Electrogenos')
        self.horametro_label = Label(self.gee_frame, text='Horametro')

        self.mt487_radiobutton = Radiobutton(self.gee_frame, text='MT-487', variable=self.gee,
                                             value='MT-487')
        self.mt488_radiobutton = Radiobutton(self.gee_frame, text='MT-488', variable=self.gee,
                                             value='MT-488')
        self.mt489_radiobutton = Radiobutton(self.gee_frame, text='MT-489', variable=self.gee,
                                             value='MT-489')
        self.mt443_radiobutton = Radiobutton(self.gee_frame, text='MT-443', variable=self.gee,
                                             value='MT-443')
        self.mt452_radiobutton = Radiobutton(self.gee_frame, text='MT-452', variable=self.gee,
                                             value='MT-452')

        self.mt487_horametro_label = Label(
            self.gee_frame, textvariable=self.horametro_mt487)
        self.mt488_horametro_label = Label(
            self.gee_frame, textvariable=self.horametro_mt488)
        self.mt489_horametro_label = Label(
            self.gee_frame, textvariable=self.horametro_mt489)
        self.mt443_horametro_label = Label(
            self.gee_frame, textvariable=self.horametro_mt443)
        self.mt452_horametro_label = Label(
            self.gee_frame, textvariable=self.horametro_mt452)

        self.gee_separator = Separator(self.gee_frame, orient='horizontal')

        self.operacion_button = Button(
            self.gee_frame, text='Operacion', command=self.operacion)
        self.info_button = Button(self.gee_frame, text='Informacion')

        # Tanks Posicion

        self.tanques_label.grid(column=0, row=0, padx=10, pady=10)
        self.tanque_vc.grid(column=1, row=0, padx=10, pady=10, sticky='w')
        self.tanque_cs.grid(column=1, row=1, padx=10, pady=10, sticky='w')
        self.tanque_mo.grid(column=1, row=2, padx=10, pady=10, sticky='w')

        self.separador1.grid(column=0, row=3, columnspan=2,
                             pady=5, padx=5, sticky="ew")

        self.medicion_anterior_label.grid(column=0, row=4, padx=10, pady=10)
        self.medicion_anterior_cm.grid(column=1, row=4, padx=10, pady=10)

        self.medicion_cm_label.grid(column=0, row=5, padx=10, pady=10)
        self.medicion_cm.grid(column=1, row=5, sticky='e', padx=10, pady=10)

        self.separador2.grid(column=0, row=6, columnspan=2,
                             padx=5, pady=5, sticky="ew")

        self.existencia_anterior_label.grid(column=0, row=7,
                                            padx=10, pady=10)
        self.existencia_anterior_cm.grid(column=1, row=7,
                                         padx=10, pady=10)

        self.existencia_final_label.grid(column=0, row=8,
                                         padx=10, pady=10)
        self.existencia_final.grid(column=1, row=8,
                                   padx=10, pady=10)

        self.gasto_combustible_label.grid(column=0, row=9,
                                          padx=10, pady=10)
        self.gasto_combustible.grid(column=1, row=9, padx=10, pady=10)

        self.boton_calcular.grid(column=0, row=10, padx=10, pady=10,
                                 columnspan=2)

        self.separador_vertical.grid(column=2, row=0, rowspan=11,
                                     padx=5, pady=5, sticky='ns')

        self.vc_label.grid(column=3, row=0, padx=5, pady=10)
        self.vc_progressbar.grid(column=3, row=1, padx=5, pady=5,
                                 rowspan=10)
        self.cs_label.grid(column=4, row=0, padx=5, pady=10)
        self.cs_progressbar.grid(column=4, row=1, padx=5, pady=5,
                                 rowspan=10)
        self.mo_label.grid(column=5, row=0, padx=5, pady=10)
        self.mo_progressbar.grid(column=5, row=1, padx=5, pady=5,
                                 rowspan=10)

        self.barra_estado.grid(column=0, row=1,
                               columnspan=6, sticky='ew')

        # GEE position
        self.gee_label.grid(column=0, row=0, pady=10, padx=10)
        self.horametro_label.grid(column=1, row=0, pady=10, padx=10)

        self.mt487_radiobutton.grid(column=0, row=1)
        self.mt488_radiobutton.grid(column=0, row=2)
        self.mt489_radiobutton.grid(column=0, row=3)
        self.mt443_radiobutton.grid(column=0, row=4)
        self.mt452_radiobutton.grid(column=0, row=5)

        self.mt487_horametro_label.grid(column=1, row=1)
        self.mt488_horametro_label.grid(column=1, row=2)
        self.mt489_horametro_label.grid(column=1, row=3)
        self.mt443_horametro_label.grid(column=1, row=4)
        self.mt452_horametro_label.grid(column=1, row=5)

        self.gee_separator.grid(
            column=0, row=6, columnspan=2, sticky='we', padx=10)

        self.operacion_button.grid(column=0, row=7, padx=10)
        self.info_button.grid(column=1, row=7, padx=10)

        self.gee_frame.columnconfigure(0, weight=1)
        self.gee_frame.columnconfigure(1, weight=1)
        self.gee_frame.rowconfigure(0, weight=1)
        self.gee_frame.rowconfigure(1, weight=1)
        self.gee_frame.rowconfigure(2, weight=1)
        self.gee_frame.rowconfigure(3, weight=1)
        self.gee_frame.rowconfigure(4, weight=1)
        self.gee_frame.rowconfigure(5, weight=1)
        self.gee_frame.rowconfigure(6, weight=1)
        self.gee_frame.rowconfigure(7, weight=1)

        # Funciones iniciales

        # Valor inicial de medicion anterior y existencia anterior
        self.medicion_anterior.set(villa_cuba.height_cm)
        self.existencia_anterior.set(villa_cuba.stock)

        # Actualizar por ciento en barras
        self.vc_percent.set(villa_cuba.percent())
        self.cs_percent.set(casas.percent())
        self.mo_percent.set(morlas.percent())

        # Enfoque inicial
        self.medicion_cm.focus_set()
        self.cm.set('')

        # Limpiar campo al hacer click
        self.medicion_cm.bind('<Button-1>', self.limpiar_cm)

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

    def limpiar_cm(self, event):
        self.cm.set('')

    def actualizar_valores(self):
        self.existencia.set(0.0)
        self.consumo.set(0.0)
        self.cm.set('')
        self.medicion_cm.focus_set()

        if self.localizacion.get() == 'vc':
            self.medicion_anterior.set(villa_cuba.height_cm)
            self.existencia_anterior.set(villa_cuba.stock)

        elif self.localizacion.get() == 'cs':
            self.medicion_anterior.set(casas.height_cm)
            self.existencia_anterior.set(casas.stock)

        else:
            self.medicion_anterior.set(morlas.height_cm)
            self.existencia_anterior.set(morlas.stock)

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

        if self.localizacion.get() == 'vc':

            if cm > 189:
                self.consumo.set('Error!')
                self.existencia.set('Error!')
                self.barra_estado['text'] = 'Medicion excedida'
                self.root.after(4000,
                                lambda: self.barra_estado.config(text=self.mensaje))
                return 1

            existencia_anterior = self.existencia_anterior.get()
            volume = villa_cuba.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            self.vc_percent.set(villa_cuba.percent())

        elif self.localizacion.get() == 'cs':
            if cm > 141:
                self.consumo.set('Error!')
                self.existencia.set('Error!')
                self.barra_estado['text'] = 'Medicion excedida'
                self.root.after(4000,
                                lambda: self.barra_estado.config(text=self.mensaje))
                return 1

            existencia_anterior = self.existencia_anterior.get()
            volume = casas.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            self.cs_percent.set(casas.percent())

        else:
            if cm > 141:
                self.consumo.set('Error!')
                self.existencia.set('Error!')
                self.barra_estado['text'] = 'Medicion excedida'
                self.root.after(4000,
                                lambda: self.barra_estado.config(text=self.mensaje))
                return 1

            existencia_anterior = self.existencia_anterior.get()
            volume = morlas.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            self.mo_percent.set(morlas.percent())

    def guardar(self):
        update_stock(villa_cuba)
        update_stock(casas)
        update_stock(morlas)
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
        vc = Radiobutton(entrada_frame, text='Villa Cuba',
                         variable=self.localizacion_entrada,
                         value='vc')
        cs = Radiobutton(entrada_frame, text='Casas',
                         variable=self.localizacion_entrada,
                         value='cs')
        mo = Radiobutton(entrada_frame, text='Las Morlas',
                         variable=self.localizacion_entrada,
                         value='mo')
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
        vc.grid(column=1, row=0, padx=5, pady=5,
                sticky='w')
        cs.grid(column=1, row=1, padx=5, pady=5,
                sticky='w')
        mo.grid(column=1, row=2, padx=5, pady=5,
                sticky='w')
        l_entrada.grid(column=0, row=3, padx=5, pady=5)
        e_entrada.grid(column=1, row=3, padx=5, pady=5)
        separador.grid(column=0, row=4, padx=5, pady=5,
                       columnspan=2, sticky='ew')
        b_aceptar.grid(column=0, row=5, padx=5, pady=5)
        b_salir.grid(column=1, row=5, padx=5, pady=5)

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

        if self.localizacion_entrada.get() == 'vc':
            villa_cuba.stock += entrada
            update_stock(villa_cuba)
            self.vc_percent.set(villa_cuba.percent())

        elif self.localizacion_entrada.get() == 'cs':
            casas.stock += entrada
            update_stock(casas)
            self.cs_percent.set(casas.percent())

        else:
            morlas.stock += entrada
            update_stock(morlas)
            self.mo_percent.set(morlas.percent())

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
        vc = Radiobutton(ventana_frame, text='Villa Cuba',
                         variable=self.localizacion_entrada,
                         value='vc')
        cs = Radiobutton(ventana_frame, text='Casas',
                         variable=self.localizacion_entrada,
                         value='cs')
        mo = Radiobutton(ventana_frame, text='Las Morlas',
                         variable=self.localizacion_entrada,
                         value='mo')
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
        vc.grid(column=1, row=0, padx=5, pady=5,
                sticky='w')
        cs.grid(column=1, row=1, padx=5, pady=5,
                sticky='w')
        mo.grid(column=1, row=2, padx=5, pady=5,
                sticky='w')
        l_entrada.grid(column=0, row=3, padx=5, pady=5)
        e_entrada.grid(column=1, row=3, padx=5, pady=5)
        separador.grid(column=0, row=4, padx=5, pady=5,
                       columnspan=2, sticky='ew')
        b_aceptar.grid(column=0, row=5, padx=5, pady=5)
        b_salir.grid(column=1, row=5, padx=5, pady=5)

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

        if self.localizacion_entrada.get() == 'vc':
            villa_cuba.stock = entrada
            update_stock(villa_cuba)
            self.vc_percent.set(villa_cuba.percent())

        elif self.localizacion_entrada.get() == 'cs':
            casas.stock = entrada
            update_stock(casas)
            self.cs_percent.set(casas.percent())

        else:
            morlas.stock = entrada
            update_stock(morlas)
            self.mo_percent.set(morlas.percent())

        self.actualizar_valores()
        self.barra_estado['text'] = 'Actualizado correctamente'
        self.root.after(2000,
                        lambda: self.barra_estado.config(text=self.mensaje))

    def seleccionar_tablas(self):
        ventana = Toplevel()
        ventana.title('Tablas certificadas')
        ventana.resizable(0, 0)

        ventana_frame = Frame(ventana)

        vc = Radiobutton(ventana_frame, text='Tabla Villa Cuba',
                         variable=self.localizacion_entrada,
                         value='vc')
        cs = Radiobutton(ventana_frame, text='Tabla Las Casas',
                         variable=self.localizacion_entrada,
                         value='cs')
        mo = Radiobutton(ventana_frame, text='Tabla Las Morlas',
                         variable=self.localizacion_entrada,
                         value='mo')

        b_ver = Button(ventana_frame, text='Ver', command=self.ver)

        ventana_frame.grid(sticky='swe')

        vc.grid(column=0, row=0, padx=10, pady=10,
                sticky='we')
        cs.grid(column=0, row=1, padx=10, pady=10,
                sticky='we')
        mo.grid(column=0, row=2, padx=10, pady=10,
                sticky='we')
        b_ver.grid(column=0, row=3, padx=10, pady=10,
                   sticky='we')

        ventana.columnconfigure(0, weight=1)
        ventana.rowconfigure(0, weight=1)
        ventana.rowconfigure(0, weight=1)
        ventana.rowconfigure(1, weight=1)
        ventana.rowconfigure(3, weight=1)

        ventana.bind('<Return>', lambda _: self.ver())

        ventana.transient(self.root)
        ventana.focus_set()

        self.root.wait_window(ventana)

    def ver(self):
        ver = Toplevel()

        if self.localizacion_entrada.get() == 'vc':
            title = 'Tabla Villa Cuba'
            file = 'tablas/vc.jpg'
            img = Image.open(file).rotate(270, expand=1)

        elif self.localizacion_entrada.get() == 'cs':
            title = 'Tabla Las Casas'
            file = 'tablas/cs.jpg'
            img = Image.open(file).rotate(270, expand=1)

        else:
            title = 'Tabla Las Morlas'
            file = 'tablas/mo.jpg'
            img = Image.open(file).rotate(90, expand=1)

        ver.title(title)

        heigth = self.root.winfo_screenheight()
        width = self.root.winfo_screenwidth()
        self.img = ImageTk.PhotoImage(img.resize((width, heigth)))
        l_img = Label(ver, image=self.img)

        l_img.grid(column=0, row=0)

        ver.focus_set()

        self.root.wait_window(ver)

    # Metodos GEE
    def operacion(self):
        ventana = Toplevel()
        ventana.title('Operacion')
        ventana.resizable(0, 0)

        # variables
        self.fecha = StringVar()
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

        mt = self.gee.get()

        if mt == 'MT-487':
            self.gee_obj = mt_487

        elif mt == 'MT-488':
            self.gee_obj = mt_488

        elif mt == 'MT-489':
            self.gee_obj = mt_489

        elif mt == 'MT-443':
            self.gee_obj = mt_443

        else:
            self.gee_obj = mt_452

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

        button = Button(ventana, command=self.run, text='Accept')

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

        button.grid(column=0, row=16, columnspan=2, padx=10, pady=10)

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

    def run(self):
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
                response = self.gee_obj.operacion(tipo=tipo, hora_inicial=hora_inicial,
                                                  consumo=consumo_s, horametro_roto=roto, hora_final=hora_final)

        else:
            horametro = self.var_horametro_final.get()
            if not horametro:
                messagebox.showwarning(
                    'Faltan Campos', 'El campo Horamemtro Final esta vacio')
                return 1

            else:
                response = self.gee_obj.operacion(tipo=tipo, hora_inicial=hora_inicial,
                                                  consumo=consumo_s, horametro_roto=roto, horametro_final=horametro)

        if type(response) == str:
            messagebox.showerror('Error', response)

        else:
            self.var_tiempo_horas.set(response['tiempo_horas'])
            self.var_hora_final.set(response['hora_final'])
            self.var_energia_generada.set(response['energia_generada'])
            self.var_demanda_liberada.set(response['demanda_liberada'])
            self.var_existencia.set(self.gee_obj.tank.stock)

            if response['sobreconsumo']:
                messagebox.showwarning(
                    'Sobreconsumo', 'Existe sobreconsumo en la operacion')


def main():
    app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
