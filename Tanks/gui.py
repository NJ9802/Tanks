from tkinter import *
from tkinter.ttk import *

from cylinder_volume import villa_cuba, casas, morlas
from db_scripts import update_existencia, extract_existencia


class Aplicacion:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title('Calculo de Combustible en Tanques')
        self.root.resizable(0, 0)
        
        # Variables
        self.cm = DoubleVar()
        self.localizacion = StringVar(value='vc')
        self.existencia = DoubleVar()
        self.consumo = DoubleVar()
        self.vc_percent = DoubleVar()
        self.cs_percent = DoubleVar()
        self.mo_percent = DoubleVar()

        # Widgets
        self.medicion_cm_label = Label(self.root, text='Medicion en cm:')
        self.medicion_cm = Entry(self.root, textvariable=self.cm, width=6)

        self.tanques_label = Label(self.root,
                                   text='Seleccione el Tanque:')
        self.tanque_vc = Radiobutton(self.root, text='Villa Cuba',
                                     variable=self.localizacion,
                                     value='vc')
        self.tanque_cs = Radiobutton(self.root, text='Casas',
                                     variable=self.localizacion,
                                     value='cs')
        self.tanque_mo = Radiobutton(self.root, text='Las Morlas',
                                     variable=self.localizacion,
                                     value='mo')

        self.existencia_final_label = Label(self.root,
                                            text='Existencia Final:')
        self.existencia_final = Label(self.root, width=10,
                                      textvariable=self.existencia,
                                      foreground='yellow', anchor='e',
                                      background='black')
        self.gasto_combustible_label = Label(self.root,
                                             text='Consumido:')
        self.gasto_combustible = Label(self.root, width=10,
                                       textvariable=self.consumo,
                                       foreground='yellow', anchor='e',
                                       background='black')

        self.boton_calcular = Button(self.root, text='Calcular',
                                     command=self.calcular)
        self.boton_salir = Button(self.root, text='Salir',
                                  command=quit)

        self.vc_label = Label(self.root,
                              text='Villa Cuba')
        self.cs_label = Label(self.root,
                              text='Casas')
        self.mo_label = Label(self.root,
                              text='Las Morlas')
        self.vc_progressbar = Progressbar(orient='vertical',
                                          variable=self.vc_percent,
                                          length=220)
        self.cs_progressbar = Progressbar(orient='vertical',
                                          variable=self.cs_percent,
                                          length=220)
        self.mo_progressbar = Progressbar(orient='vertical',
                                          variable=self.mo_percent,
                                          length=220)

        self.separador1 = Separator(self.root, orient='horizontal')
        self.separador2 = Separator(self.root, orient='horizontal')
        self.separador_vertical = Separator(self.root, orient='vertical')

        # Posicion

        self.tanques_label.grid(column=0, row=0, padx=10, pady=10)
        self.tanque_vc.grid(column=1, row=0, padx=10, pady=10, sticky='w')
        self.tanque_cs.grid(column=1, row=1, padx=10, pady=10, sticky='w')
        self.tanque_mo.grid(column=1, row=2, padx=10, pady=10, sticky='w')

        self.separador1.grid(column=0, row=3, columnspan=2,
                             pady=5, padx=5, sticky="ew")

        self.medicion_cm_label.grid(column=0, row=4, padx=10, pady=10)
        self.medicion_cm.grid(column=1, row=4, padx=10, pady=10)

        self.separador2.grid(column=0, row=5, columnspan=2,
                             padx=5, pady=5, sticky="ew")

        self.gasto_combustible_label.grid(column=0, row=6,
                                          padx=10, pady=10)
        self.gasto_combustible.grid(column=1, row=6, padx=10, pady=10)

        self.existencia_final_label.grid(column=0, row=7,
                                         padx=10, pady=10)
        self.existencia_final.grid(column=1, row=7,
                                   padx=10, pady=10)

        self.boton_calcular.grid(column=0, row=8, padx=10, pady=10)
        self.boton_salir.grid(column=1, row=8, padx=10, pady=10)

        self.separador_vertical.grid(column=2, row=0, rowspan=9,
                                     padx=5, pady=5, sticky='ns')

        self.vc_label.grid(column=3, row=0, padx=5, pady=10)
        self.vc_progressbar.grid(column=3, row=1, padx=5, pady=5,
                                 rowspan=8)
        self.cs_label.grid(column=4, row=0, padx=5, pady=10)
        self.cs_progressbar.grid(column=4, row=1, padx=5, pady=5,
                                 rowspan=8)
        self.mo_label.grid(column=5, row=0, padx=5, pady=10)
        self.mo_progressbar.grid(column=5, row=1, padx=5, pady=5,
                                 rowspan=8)

        # Funciones iniciales

        # no funciona todavia
        self.vc_percent.set(self.calcular_porciento_de_tanques(villa_cuba))
        self.cs_percent.set(self.calcular_porciento_de_tanques(casas))
        self.mo_percent.set(self.calcular_porciento_de_tanques(morlas))

        # Enfoque inicial
        self.medicion_cm.focus_set()
        self.cm.set('')

        # Limpiar campo al hacer click
        self.medicion_cm.bind('<Button-1>', self.limpiar_cm)

        # Calcular al presionar ENTER
        self.root.bind('<Return>', self.enter)

        self.root.mainloop()

    # Metodos de la Aplicacion
    def limpiar_cm(self, event):
        self.cm.set('')

    def enter(self, event):
        self.calcular()

    def calcular_porciento_de_tanques(self, tank):
        return tank.percent()

    def calcular(self):
        try:
            cm = self.cm.get()
        except:
            self.consumo.set('Error!')
            self.existencia.set('Error!')
            print('Medicion en cm tiene q tener un valor numerico')
            return 1

        if self.localizacion.get() == 'vc':
            if cm > 189:
                self.consumo.set('Error!')
                self.existencia.set('Error!')
                print('Medicion excedida')
                return 1

            existencia_anterior = extract_existencia(villa_cuba)
            volume = villa_cuba.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            update_existencia(villa_cuba, volume)

        elif self.localizacion.get() == 'cs':
            if cm > 141:
                self.consumo.set('Error!')
                self.existencia.set('Error!')
                print('Medicion excedida')
                return 1

            existencia_anterior = extract_existencia(casas)
            volume = casas.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            update_existencia(casas, volume)

        else:
            if cm > 141:
                self.consumo.set('Error!')
                self.existencia.set('Error!')
                print('Medicion excedida')
                return 1

            existencia_anterior = extract_existencia(morlas)
            volume = morlas.volume(cm)

            self.existencia.set(volume)
            self.consumo.set(round(existencia_anterior-volume))
            update_existencia(morlas, volume)


def main():
    app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
