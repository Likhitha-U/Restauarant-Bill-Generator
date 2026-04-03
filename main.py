from tkinter import *
from PIL import Image, ImageTk
import random
from tkinter import messagebox

root = Tk()
root.geometry("1000x500")
root.title("Bill Management System")
root.resizable(False, False)

thank_you_note = None

# Resize Image
def resize_image(path, size=(150,150)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Frame switching
def show_menu():
    frame_menu.tkraise()

def show_bill():
    frame_bill.tkraise()

def show_welcome():
    frame_welcome.tkraise()

# Reset
def Reset():
    global thank_you_note
    for entry in entry_widgets:
        entry.delete(0, END)

    bill_area.delete("1.0", END)

    if thank_you_note:
        thank_you_note.destroy()
        thank_you_note = None

# Total Function
def Total():
    global thank_you_note

    try:
        quantities = [int(entry.get()) if entry.get() else 0 for entry in entry_widgets]

        if any(q < 0 for q in quantities):
            messagebox.showerror("Error", "Quantity cannot be negative")
            return

        prices = [220, 100, 70, 130, 30, 200, 200]

        subtotal = sum(q * p for q, p in zip(quantities, prices))
        gst = subtotal * 0.05
        final_total = subtotal + gst

        bill_text = "----- BILL RECEIPT -----\n\n"

        for i, q in enumerate(quantities):
            if q > 0:
                bill_text += f"{labels[i]} -{q} = Rs.{q * prices[i]}\n"

        bill_text += f"\nSubtotal: Rs.{subtotal:.2f}"
        bill_text += f"\nGST (5%): Rs.{gst:.2f}"
        bill_text += f"\nTotal: Rs.{final_total:.2f}"

        # Show in Text box
        bill_area.delete("1.0", END)
        bill_area.insert(END, bill_text)

        # Save to file
        with open("bill.txt", "w") as f:
            f.write(bill_text)

        # Thank you message
        thank_you_note = Label(f2, text="Thank you for ordering!", font=('Arial', 18, "bold"), bg="lightyellow", fg="green")
        thank_you_note.place(x=80, y=320)

        # Auto reset after 5 sec
        root.after(5000, Reset)

    except:
        messagebox.showerror("Error", "Enter valid numbers only!")

# Hover effects
def on_enter(e):
    e.widget['bg'] = 'lightgreen'

def on_leave(e):
    e.widget['bg'] = 'lightblue'

# Frames
frame_welcome = Frame(root, bg="lightyellow")
frame_menu = Frame(root)
frame_bill = Frame(root)

for frame in (frame_welcome, frame_menu, frame_bill):
    frame.place(x=0, y=0, width=1000, height=500)

# Welcome Frame
Label(frame_welcome, text="Welcome to Our Restaurant!", font=("Gabriola", 40, "bold"), bg="lightyellow").pack(pady=20)

restaurant_image = resize_image("images/start.jpg", (300,200))
Label(frame_welcome, image=restaurant_image, bg="lightyellow").pack()

btn_next = Button(frame_welcome, text="Next", font=("Arial",16,"bold"), bg="lightblue", command=show_menu)
btn_next.pack(pady=20)
btn_next.bind("<Enter>", on_enter)
btn_next.bind("<Leave>", on_leave)

# Menu Frame
Label(frame_menu, text="Menu", font=("Arial", 28, "bold"), bg="deeppink", fg="white").pack(fill=X)

menu_items = [
    ("Chicken Biryani",220),
    ("Noodles",100),
    ("Manchurian",70),
    ("Egg Fried Rice",130),
    ("Cool Drinks",30),
    ("Chicken Curry",200),
    ("Chicken Fried Rice",200)
]

labels = []
for name, price in menu_items:
    Label(frame_menu, text=f"{name} - Rs.{price}", font=("Arial",14), bg="lavender").pack(anchor='w', padx=20)
    labels.append(name)

# Images
img1 = resize_image("images/chickenbiryani.jpg")
img2 = resize_image("images/manchuria.jpg")
img3 = resize_image("images/noodles.jpeg")

Label(frame_menu, image=img1).place(x=500, y=120)
Label(frame_menu, image=img2).place(x=650, y=120)
Label(frame_menu, image=img3).place(x=800, y=120)

Button(frame_menu, text="Continue", command=show_bill, bg="lightblue").place(x=700,y=400)
Button(frame_menu, text="Back", command=show_welcome, bg="lightblue").place(x=700,y=450)

# Bill Frame
Label(frame_bill, text="Enter Quantity", font=("Arial", 20, "bold"), bg="lightpink").pack(fill=X)

f1 = Frame(frame_bill)
f1.pack(side=LEFT, padx=20)

entry_widgets = []
for i, item in enumerate(labels):
    Label(f1, text=item, font=("Arial",12)).grid(row=i, column=0)
    entry = Entry(f1)
    entry.grid(row=i, column=1)
    entry_widgets.append(entry)

Button(f1, text="Reset", command=Reset).grid(row=8, column=0)
Button(f1, text="Total", command=Total).grid(row=8, column=1)

# Bill Display (TEXT BOX ✅)
f2 = Frame(frame_bill, bg="lightyellow")
f2.pack(side=RIGHT, fill=BOTH, expand=True)

bill_area = Text(f2, font=("Courier", 12), width=40, height=15, bg="white")
bill_area.place(x=20, y=50)

# Scrollbar (optional)
scroll = Scrollbar(f2)
scroll.place(x=380, y=50, height=250)

bill_area.config(yscrollcommand=scroll.set)
scroll.config(command=bill_area.yview)

Button(f2, text="Back", command=show_menu).place(x=300,y=300)

# Start
show_welcome()
root.mainloop()