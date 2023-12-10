import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy
from keras.models import load_model

model = load_model('my_model.h5')

# Dictionary to label all traffic signs class.
classes = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Stop',
    4: 'Right Turn'
}

top = tk.Tk()
top.geometry('800x600')
top.title('Traffic sign classification')
top.configure(background='#CDCDCD')


label = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    
    # Check if the image has 4 channels (e.g., RGBA with transparency)
    if image.mode == "RGBA":
        # Convert the 4-channel image to 3-channel (RGB) image
        image = image.convert("RGB")
    
    image = image.resize((30, 30))
    image = numpy.expand_dims(image, axis=0)
    image = numpy.array(image)

    try:
        # Try using model.predict if available (newer Keras versions)
        pred = model.predict(image)
        predicted_class = numpy.argmax(pred)
    except AttributeError:
        # Fall back to model.predict_classes for older Keras versions
        pred = model.predict_classes(image)
        predicted_class = pred[0]

    sign = classes[predicted_class]
    print(sign)
    label.configure(foreground='#011638', text=sign)


def show_classify_button(file_path):
    classify_b = Button(top, text="Classify Image", command=lambda: classify(file_path), padx=10, pady=5)
    classify_b.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
    classify_b.place(relx=0.79, rely=0.46)

def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            uploaded = Image.open(file_path)
            uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25))
            )
            im = ImageTk.PhotoImage(uploaded)

            sign_image.configure(image=im)
            sign_image.image = im
            label.configure(text='')
            show_classify_button(file_path)
    except Exception as e:
        print(e)

upload = Button(top, text="Upload an image", command=upload_image, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
upload.pack(side=BOTTOM, pady=50)
sign_image.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)
heading = Label(top, text="Know Your Traffic Sign", pady=20, font=('arial', 20, 'bold'))
heading.configure(background= '#CDCDCD', foreground='#364156')
heading.pack()

top.mainloop()
