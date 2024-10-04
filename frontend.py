import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import llm_backend  

wrap_length = 300

# THIS SHOULD BE AN IMAGE OF THE ENVIRONMENT AT THE BEGINNING OF SIMULATION
current_image_path = "./images/person.jpg"

generated_text = ""

root = tk.Tk()
root.title("Chef and Farmer")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, padx=20, pady=20)

right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, padx=20, pady=20)

llm_label = tk.Label(right_frame, text="LLaMa 3.2 Vision 11B", font=("Arial", 16))
llm_label.grid(row=0, column=0, padx=10, pady=10)

llm_button = tk.Button(right_frame, text="Send Message to LLaMa", command=lambda: have_convo())
llm_button.grid(row=1, column=0, padx=10, pady=10)

llm_row_counter = 2

current_image = Image.open(current_image_path).resize((256, 256))
label_image = ImageTk.PhotoImage(current_image)

def image_uploader():
    global current_image_path
    global llm_image

    file = filedialog.askopenfilename()
    current_image_path = r"{}".format(file)

    current_image = Image.open(current_image_path).resize((256, 256))
    llm_image.image = ImageTk.PhotoImage(current_image)
    llm_image.config(image=llm_image.image)

llm_image = tk.Label(left_frame, image=label_image)
llm_image.grid(row=0, column=0, padx=10, pady=10)

image_button = tk.Button(left_frame, text="Upload Image", command=image_uploader)
image_button.grid(row=1, column=0, padx=10, pady=10)

def have_convo():
    global llm_row_counter
    global generated_text
    
    convo = llm_backend.run_conversation(current_image_path)
    generated_text = convo 
    
    llm_convo_label = tk.Label(right_frame, text=convo, wraplength=wrap_length)
    llm_convo_label.grid(row=llm_row_counter, column=0, padx=10, pady=5, sticky="w")
    llm_row_counter += 1

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(generated_text)
    root.update()

copy_button = tk.Button(right_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=llm_row_counter + 1, column=0, padx=10, pady=10)

# When the model first loads, we want to generate a response so that we can perform future analysis:
have_convo()

root.mainloop()
