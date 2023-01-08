from tkinter import *
from tkinter.ttk import *
from db_scripts import update_existencia
from cylinder_volume import villa_cuba, casas, morlas
from PIL import Image, ImageTk


class Aplicacion:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Calculo de Combustible en Tanques')
        self.root.resizable(0, 0)
        self.root.option_add('*tearOff', False)
        self.root.tk.call('lappend', 'auto_path',
                          'themes/tkBreeze-master')
        self.estilo = Style()
        self.estilo.theme_use('breeze-dark')
        self.estilo.configure('variable.TLabel', background='#3b3b3c')
        self.estilo.configure('dark.Vertical.TProgressbar', background='#3e3e3e')

        # Variables
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

        # Menu
        barramenu = Menu(self.root)
        self.root['menu'] = barramenu
        self.menu1 = Menu(barramenu)
        self.menu2 = Menu(barramenu)

        barramenu.add_cascade(menu=self.menu1,
                              label='Archivo')
        barramenu.add_cascade(menu=self.menu2,
                              label='Opciones')

        self.menu1.add_command(label='Guardar',
                               command=self.guardar, underline=0,
                               accelerator='Ctrl+g')
        self.menu1.add_separator()
        self.menu1.add_command(label='Salir',
                               command=quit, underline=0,
                               accelerator='Alt+F4')

        self.menu2.add_command(label='Establecer valor inicial',
                               command=self.valor_inicial)
        self.menu2.add_command(label='Tablas de Aforo',
                               underline=0, command=self.seleccionar_tablas,
                               accelerator='Ctrl+t')
        self.menu2.add_command(label='Entrada de Combustible',
                               underline=0, command=self.entrada,
                               accelerator='Ctrl+e')

        # Barra de estado
        self.mensaje = 'Hecho por Nelson J. Aldazabal Hernandez. Colaborador Maykel'
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

        # Widgets
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

        # Posicion

        self.tanques_label.grid(column=0, row=0, padx=10, pady=10)
        self.tanque_vc.grid(column=1, row=0, padx=10, pady=10, sticky='w')
        self.tanque_cs.grid(column=1, row=1, padx=10, pady=10, sticky='w')
        self.tanque_mo.grid(column=1, row=2, padx=10, pady=10, sticky='w')

        self.separador1.grid(column=0, row=3, columnspan=2,
                             pady=5, padx=5, sticky="ew")

        self.medicion_anterior_label.grid(column=0, row=4, padx=10, pady=10)
        self.medicion_anterior_cm.grid(column=1, row=4, padx=10, pady=10)

        self.medicion_cm_label.grid(column=0, row=5, padx=10, pady=10)
        self.medicion_cm.grid(column=1, row=5, padx=10, pady=10)

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
        self.root.bind('<Return>', self.enter)

        # Guardar
        self.root.bind('<Control-g>', lambda _: self.guardar())

        self.root.bind('<Control-e>', lambda _: self.entrada())

        self.root.bind('<Control-t>', lambda _: self.seleccionar_tablas())

        self.root.mainloop()

    # Metodos de la Aplicacion
    def limpiar_cm(self, event):
        self.cm.set('')

    def enter(self, event):
        self.calcular()

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

            existencia_anterior = casas.stock
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

            existencia_anterior = morlas.stock
            volume = morlas.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            self.mo_percent.set(morlas.percent())

    def guardar(self):
        update_existencia(villa_cuba, villa_cuba.stock, villa_cuba.height_cm)
        update_existencia(casas, casas.stock, casas.height_cm)
        update_existencia(morlas, morlas.stock, morlas.height_cm)
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
            update_existencia(villa_cuba, villa_cuba.stock,
                              villa_cuba.height_cm)

        elif self.localizacion_entrada.get() == 'cs':
            casas.stock += entrada
            update_existencia(casas, casas.stock, casas.height_cm)

        else:
            morlas.stock += entrada
            update_existencia(morlas, morlas.stock, morlas.height_cm)

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
            update_existencia(villa_cuba, villa_cuba.stock,
                              villa_cuba.height_cm)

        elif self.localizacion_entrada.get() == 'cs':
            casas.stock = entrada
            update_existencia(casas, casas.stock, casas.height_cm)

        else:
            morlas.stock = entrada
            update_existencia(morlas, morlas.stock, morlas.height_cm)

        self.actualizar_valores()
        self.barra_estado['text'] = 'Actualizado correctamente'
        self.root.after(2000,
                        lambda: self.barra_estado.config(text=self.mensaje))

    def seleccionar_tablas(self):
        ventana = Toplevel()
        ventana.title('Tablas cerificadas')
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


def main():
    app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
