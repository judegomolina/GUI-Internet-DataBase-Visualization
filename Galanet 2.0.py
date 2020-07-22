from tkinter import *
from tkinter import messagebox as Messagebox
import sqlite3


class Table:
    
    def __init__(self, root, rows, columns, content):
        
        for i in range(rows):
            for j in range(columns):
                
                self.e = Entry(root, width=20, fg='black', justify='center')
                self.e.grid(row=i+1, column=j)
                self.e.insert(END, content[i][j] if content[i][j] \
                              is not None else '')


bg_color = 'white'
button_color = 'light blue'


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))

def buscar_ip():
    global output_frame2
    global output_frame
    
    output_frame2.destroy()
    output_frame2 = Frame(output_frame, bg=bg_color)
    output_frame2.pack(anchor='n')
    cols = ['ID','NODO', 'RED', 'IP', 'VLAN admin', 'VLAN']
    for i,n in enumerate(cols):
        Label(output_frame2, bg=bg_color, text=n, width=20).\
            grid(row=0, column=i)
    
    conexion = sqlite3.connect('Galanet-IPs.sqlite')
    cursor = conexion.cursor()
    val = (nodo_var.get(),)
    cursor.execute("SELECT * FROM 'Nodos Galanet' WHERE nodo=? AND \
                   [CLIENTE ] IS NULL", val)
    valores = cursor.fetchall()
    ips_disp.set(str(len(valores)))
    conexion.commit()
    conexion.close()
    Table(output_frame2, rows=len(valores), columns=6, \
          content=valores)
    


def ubicar_ip():
    global output_frame2
    global output_frame
    
    ips_disp.set('')
    
    ubicar_ip = Toplevel(bg=bg_color)
    ubicar_ip.title('Ubicar una IP disponible')
    ubicar_ip.geometry('900x700')
    ubicar_ip.resizable(0,1)
    
    input_frame = Frame(ubicar_ip, bg=bg_color)
    input_frame.pack(anchor='n')
    Label(input_frame, text='Seleccione un nodo:', bg=bg_color).grid(row=0, column=0)
    
    conexion = sqlite3.connect('Galanet-IPs.sqlite')
    cursor = conexion.cursor()
    cursor.execute("SELECT nodo FROM 'Nodos Galanet' ")
    nodos = cursor.fetchall()
    nodos = tuple(set(nodos))
    nodos_tupla = (i[0] for i in nodos)
    conexion.commit()
    conexion.close()
    
    nodo_var.set('Nodo')
    option = OptionMenu (input_frame, nodo_var, *nodos_tupla)
    option.grid(row=0, column=1)
    Button(input_frame, bg=button_color, fg=bg_color, text='Buscar',\
           command=buscar_ip).grid(row=0, column=2)
        
    pre_output_frame = Frame(ubicar_ip, bg=bg_color)
    pre_output_frame.pack(anchor='n')
    Label(pre_output_frame, bg=bg_color, text='IPs disponibles: ').\
        grid(row=0, column=0)
    Label(pre_output_frame, bg=bg_color, textvar=ips_disp).grid(row=0, column=1)
    canvas = Canvas(ubicar_ip, bg=bg_color)
    canvas.pack(fill='both', expand=True, anchor='e')
    output_frame = Frame(canvas, bg=bg_color)
    output_frame.pack(anchor='n')
    scroll = Scrollbar(output_frame, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    canvas.create_window((0,0), window=output_frame)
    output_frame.bind('<Configure>', lambda event, canvas=canvas : \
                      onFrameConfigure(canvas))
    output_frame2 = Frame(output_frame, bg=bg_color, width=900)
    output_frame2.pack()
    
    
def buscar_cliente():
    global output_frame_clientes
    global output_frame2_clientes

    output_frame2_clientes.destroy()
    output_frame2_clientes = Frame(output_frame_clientes, bg=bg_color, width=1200, height=650)
    output_frame2_clientes.pack(fill='both', expand=True, anchor='n')

    conexion = sqlite3.connect('Galanet-IPs.sqlite')
    cursor = conexion.cursor()
    val = (cliente.get().upper(),)
    cursor.execute("SELECT * FROM 'Nodos Galanet' WHERE [CLIENTE ]=?", val)
    cols = [i[0] for i in cursor.description]
    valores = cursor.fetchall()
    num_clientes.set(str(len(valores)))
    conexion.commit()
    conexion.close()
    
    for i,n in enumerate(cols):
        Label(output_frame2_clientes, bg=bg_color, text=n, width=20).\
                grid(row=0, column=i)
    Table(output_frame2_clientes, rows=len(valores), columns=len(valores[0]), \
          content=valores)


def ubicar_cliente():
    
    global output_frame_clientes
    global output_frame2_clientes
    
    cliente.set('')
    num_clientes.set('')
    
    ubicar_cliente = Toplevel(bg=bg_color)
    ubicar_cliente.title('Ubicar un Cliente')
    ubicar_cliente.resizable(0,0)
    
    input_frame = Frame(ubicar_cliente, bg=bg_color)
    input_frame.pack(anchor='n')
    Label(input_frame, text='Indique un cliente:', bg=bg_color).grid(row=0, column=0)
    Entry(input_frame, bg=bg_color, textvar=cliente).grid(row=0, column=1)
    Button(input_frame, bg=button_color, fg=bg_color, text='Buscar',\
           command=buscar_cliente).grid(row=0, column=2)
        
    pre_output_frame = Frame(ubicar_cliente, bg=bg_color)
    pre_output_frame.pack(anchor='n')
    Label(pre_output_frame, bg=bg_color, text='Clientes encontrados: ').\
        grid(row=0, column=0)
    Label(pre_output_frame, bg=bg_color, textvar=num_clientes).grid(row=0, column=1)
    canvas_frame = Frame(ubicar_cliente, bg=bg_color)
    canvas_frame.pack()
    canvas = Canvas(canvas_frame, bg=bg_color, width=1150, height=550)
    scrollv = Scrollbar(canvas_frame, orient='vertical', \
                        command=canvas.yview)
    canvas.configure(yscrollcommand=scrollv.set)
    scrollv.grid(row=0, column=1, sticky=NSEW)
    scrollh = Scrollbar(canvas_frame, orient='horizontal', \
                        command=canvas.xview)
    canvas.configure(xscrollcommand=scrollh.set)
    scrollh.grid(row=1, column=0, sticky=NSEW)
    canvas.grid(row=0, column=0)
    canvas.pack_propagate(0)
    output_frame_clientes = Frame(canvas, bg=bg_color)
    output_frame_clientes.pack(anchor='n')
    canvas.create_window((0,0), window=output_frame_clientes)
    output_frame_clientes.bind('<Configure>', lambda event, canvas=canvas : \
                      onFrameConfigure(canvas))
    output_frame2_clientes = Frame(output_frame_clientes, bg=bg_color)
    output_frame2_clientes.pack(anchor='n')
    

def about():
    Messagebox.showinfo('Acerca de la Aplicación', 'Versión: 0.1 \n\
Desarrollada por Juan Molina \nPara Fractal Group C.A. y Galanet C.A.')


root = Tk()
root.title('Galanet 2.0')
root.resizable(0,0)
root.config(bg=bg_color)
#root.geometry('300x190')

frame_logos = Frame(root)
frame_logos.pack()
frame_logos.config(bg=bg_color)
logo_galanet = PhotoImage(file='logo galanet.gif')
logo_galanet = logo_galanet.subsample(2,2)
Label(frame_logos, image=logo_galanet).pack()

frame_opciones = Frame(root)
frame_opciones.pack()
frame_opciones.config(bg=bg_color)
Label(frame_opciones, bg=bg_color).pack()
Button(frame_opciones, text='Ubicar una IP disponbible', command=ubicar_ip, \
       bg=button_color, fg=bg_color).pack()
Label(frame_opciones, bg=bg_color).pack()
Button(frame_opciones, text='Ubicar un cliente', command=ubicar_cliente, \
       bg=button_color, fg=bg_color).pack()
Label(frame_opciones, bg=bg_color).pack()
Label(frame_opciones, bg=bg_color).pack()
Label(frame_opciones, bg=bg_color).pack()
Button(frame_opciones, text='Acerca de la aplicación', command=about, \
       bg=button_color, fg=bg_color).pack()
Label(frame_opciones, bg=bg_color).pack()

frame_logos2 = Frame(root)
frame_logos2.pack()
frame_logos2.config(bg=bg_color)
logo_fractal = PhotoImage(file='logo fractal.gif')
logo_fractal = logo_fractal.subsample(4, 4)
Label(frame_logos2, image=logo_fractal).pack()
    
nodo_var = StringVar()
ips_disp = StringVar()
cliente = StringVar()
num_clientes = StringVar()

root.mainloop()