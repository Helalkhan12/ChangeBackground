from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser, filedialog

class ColorPickerDialog(tk.Toplevel):
    def __init__(self, parent, image):
        super().__init__(parent)
        self.title("Color Picker")
        self.color = None
        self.init_ui(image)

    def init_ui(self, image):
        self.canvas = tk.Canvas(self, width=image.width, height=image.height)
        self.canvas.pack()

        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        pixel = self.photo._PhotoImage__photo.zoom(1, 1).get(x, y)
        self.color = tuple(pixel[:3])
        self.destroy()

def change_background(image, target_color, new_color):
    modified_image = image.copy()

    for y in range(image.height):
        for x in range(image.width):
            pixel_color = image.getpixel((x, y))
            if pixel_color == target_color:
                modified_image.putpixel((x, y), new_color)

    return modified_image

def select_output_path():
    output_path = filedialog.asksaveasfilename(title="Save the modified image", defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg")])

    if output_path:
        return output_path
    else:
        print("No output file selected.")
        return None

def main():
    root = tk.Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if image_path:
        image = Image.open(image_path)

        color_picker = ColorPickerDialog(root, image)
        color_picker.wait_window()

        target_color = color_picker.color

        if target_color:
            new_color = colorchooser.askcolor(title="Select the new color")[0]

            if new_color:
                output_path = select_output_path()

                if output_path:
                    new_image = change_background(image, target_color, tuple(map(int, new_color)))
                    new_image.save(output_path)
                    print("Modified image saved successfully.")

if __name__ == "__main__":
    main()