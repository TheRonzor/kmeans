import tkinter as tk
import kmaf

ANCHOR = tk.N + tk.E

LBL_H  = 2
PADX   = 10

# The function that runs when we push the button
def Go():
    kmaf.KMeansAnim(n_clusters  = int(input_k.get()),
                    n_points    = int(input_n.get()),
                    method      = method_value.get(),
                    seed        = int(input_seed.get())
                    ).Go()
    return

# The main window
main = tk.Tk()
main.geometry('400x100')
main.title('Just what do you think you are doing, Dave?')

# Interface frame
inter = tk.Frame(main)
inter.rowconfigure(0, weight=1) # For the settings
inter.rowconfigure(1, weight=1) # For the Go button

# Settings frame goes inside interface frame
settings = tk.Frame(inter)
settings.rowconfigure(0, weight=1)
settings.rowconfigure(1, weight=1)
settings.rowconfigure(2, weight=1)
settings.grid(row=0)

# How many clusters?
label_k = tk.Label(settings, text='k = ', height=LBL_H)
label_k.grid(row=0, column=0, sticky = ANCHOR)
input_k = tk.Entry(settings, width=5)
input_k.grid(row=0, column=1, sticky = ANCHOR)
input_k.insert(0, 3)

# How many points?
label_n = tk.Label(settings, text='n = ', height=LBL_H)
label_n.grid(row=1, column=0, sticky = ANCHOR)
input_n = tk.Entry(settings, width=5)
input_n.grid(row=1, column=1, sticky = ANCHOR)
input_n.insert(0, 100)

# Methods
label_meth = tk.Label(settings, text='Method = ', height=LBL_H)
label_meth.grid(row=0, column=2, padx=PADX, sticky = ANCHOR)

method_value = tk.StringVar()
options_methods = ['naive', 'from_data', 'k++']
method_value.set(options_methods[0])

input_meth = tk.OptionMenu(settings, method_value, *options_methods)
input_meth.grid(row=0, column=3)

# Random seed
label_seed = tk.Label(settings, text='Seed = ', height=LBL_H)
label_seed.grid(row=1, column=2, padx=PADX, sticky=ANCHOR)
input_seed = tk.Entry(settings, width=5)
input_seed.grid(row=1, column=3, padx=PADX, sticky=ANCHOR)

seed = kmaf.np.random.randint(1000)
input_seed.insert(0, seed)


# The Go button
go = tk.Button(inter, text="Let's go!", command=Go, height=3)
go.grid(row=1, sticky=tk.S)

# Pack it up
inter.pack(pady=20, padx=20)

# Ship it out
main.mainloop()