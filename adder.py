import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import sys
import subprocess

class ParentalAdvisoryAdder:
    def __init__(self, root):
        self.root = root
        self.root.title("Parental Advisory Adder")
        self.root.geometry("600x500")
        self.root.configure(bg="white")

        # Set ttk style for a clean white look
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass  # fallback to default if 'clam' is not available
        style.configure('TFrame', background='white')
        style.configure('TLabelFrame', background='white', foreground='#222')
        style.configure('TLabel', background='white', foreground='#222')
        style.configure('TButton', background='white', foreground='#222')
        style.configure('TRadiobutton', background='white', foreground='#222')
        style.configure('Horizontal.TScale', background='white')
        style.configure('TProgressbar', background='white')

        self.selected_files = []
        self.position_var = tk.StringVar(value="bottom_left")
        self.logo_size_var = tk.IntVar(value=100)
        self.crop_mode_var = tk.StringVar(value="crop")
        
        try:
            self.pa_logo = Image.open("parental.png")
        except FileNotFoundError:
            messagebox.showerror("Error", "Parental Logo not found in the same directory!")
            root.destroy()
            return
        
        self.setup_ui()

    def setup_ui(self):
        # File selection
        file_frame = ttk.LabelFrame(self.root, text="Select Images")
        file_frame.pack(fill='x', padx=10, pady=10)
        
        self.file_entry = ttk.Entry(file_frame, width=50)
        self.file_entry.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        browse_btn = ttk.Button(file_frame, text="Browse Files", command=self.browse_files)
        browse_btn.pack(side='right', padx=5, pady=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(self.root, text="Logo Settings")
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        pos_label = ttk.Label(settings_frame, text="Position:")
        pos_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        positions = [
            ("Bottom Left", "bottom_left"),
            ("Bottom Middle", "bottom_middle"),
            ("Bottom Right", "bottom_right")
        ]
        for i, (text, value) in enumerate(positions):
            rb = ttk.Radiobutton(settings_frame, text=text, variable=self.position_var, value=value, style='TRadiobutton', command=self.update_preview)
            rb.grid(row=0, column=i+1, padx=5, pady=5)
        
        size_label = ttk.Label(settings_frame, text="Logo Width:")
        size_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        size_scale = ttk.Scale(settings_frame, from_=50, to=200, orient='horizontal', variable=self.logo_size_var, command=self.update_size_label, style='Horizontal.TScale')
        size_scale.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        self.size_value_label = ttk.Label(settings_frame, text="100 px")
        self.size_value_label.grid(row=1, column=3, padx=5, pady=5)
        settings_frame.columnconfigure(2, weight=1)
        
        # Crop mode option
        crop_mode_label = ttk.Label(settings_frame, text="Crop Mode:")
        crop_mode_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        crop_modes = [("Crop to Center", "crop"), ("Stretch to Square", "stretch")]
        for i, (text, value) in enumerate(crop_modes):
            rb = ttk.Radiobutton(settings_frame, text=text, variable=self.crop_mode_var, value=value, style='TRadiobutton', command=self.update_preview)
            rb.grid(row=2, column=i+1, padx=5, pady=5)
        
        # Preview
        preview_frame = ttk.LabelFrame(self.root, text="Preview")
        preview_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.preview_canvas = tk.Canvas(preview_frame, bg='white', height=220, highlightthickness=0)
        self.preview_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        self.preview_canvas.bind('<Configure>', lambda event: self.update_preview())
        
        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=10, pady=10)
        preview_btn = ttk.Button(btn_frame, text="Refresh Preview", command=self.update_preview)
        preview_btn.pack(side='left', padx=5)
        process_btn = ttk.Button(btn_frame, text="Process Images", command=self.process_images)
        process_btn.pack(side='right', padx=5)
        
        # Progress
        self.progress = ttk.Progressbar(self.root, mode='determinate', style='TProgressbar')
        self.progress.pack(fill='x', padx=10, pady=(0,10))
        self.status_label = ttk.Label(self.root, text="Ready.", style='TLabel')
        self.status_label.pack(padx=10, pady=(0,10))
        
        self.update_preview()

    def browse_files(self):
        files = filedialog.askopenfilenames(title="Select Album Cover Images",
                                           filetypes=[
                                               ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                                               ("All Files", "*.*")
                                           ])
        if files:
            self.selected_files = list(files)
            if len(self.selected_files) == 1:
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, os.path.basename(self.selected_files[0]))
            else:
                self.file_entry.delete(0, tk.END)
                self.file_entry.insert(0, f"{len(self.selected_files)} files selected")
            self.update_preview()

    def update_size_label(self, val):
        self.size_value_label.config(text=f"{int(float(val))} px")
        self.update_preview()

    def update_preview(self):
        self.preview_canvas.delete("all")
        canvas_width = self.preview_canvas.winfo_width() or 400
        canvas_height = self.preview_canvas.winfo_height() or 220
        if self.selected_files:
            try:
                img = Image.open(self.selected_files[0]).copy()
                img_width, img_height = img.size
                min_side = min(img_width, img_height)
                preview_size = min(canvas_width-20, canvas_height-20)
                if self.crop_mode_var.get() == "crop":
                    left = (img_width - min_side) // 2
                    top = (img_height - min_side) // 2
                    img = img.crop((left, top, left+min_side, top+min_side))
                    img = img.resize((preview_size, preview_size), Image.LANCZOS)
                else:  # stretch
                    img = img.resize((preview_size, preview_size), Image.LANCZOS)
                # Match processing logic: composite logo in RGBA
                logo_width = max(10, min(self.logo_size_var.get(), preview_size // 3))
                orig_w, orig_h = self.pa_logo.size
                aspect_ratio = orig_h / orig_w
                logo_height = max(10, int(logo_width * aspect_ratio))
                if logo_width <= 0 or logo_height <= 0:
                    logo_width = 20
                    logo_height = int(logo_width * aspect_ratio)
                logo_resized = self.pa_logo.resize((logo_width, logo_height), Image.LANCZOS)
                logo_with_bg = Image.new("RGBA", (logo_width, logo_height), (0, 0, 0, 255))
                logo_with_bg.paste(logo_resized, (0, 0), logo_resized)
                position = self.position_var.get()
                if position == "bottom_left":
                    x = 10
                    y = preview_size - logo_height - 10
                elif position == "bottom_middle":
                    x = (preview_size - logo_width) // 2
                    y = preview_size - logo_height - 10
                else:
                    x = preview_size - logo_width - 10
                    y = preview_size - logo_height - 10
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                img.paste(logo_with_bg, (x, y), logo_with_bg)
                # End compositing
                # Determine if the processed image will be PNG (with transparency) or JPEG (no transparency)
                ext = os.path.splitext(self.selected_files[0])[1].lower()
                will_be_png = (img.mode in ["RGBA", "LA"] or ext == ".png")
                if not will_be_png:
                    # Composite onto white background for preview, as in JPEG output
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
                    img = bg
                preview_img = ImageTk.PhotoImage(img)
                cx = (canvas_width - preview_size) // 2
                cy = (canvas_height - preview_size) // 2
                self.preview_canvas.create_image(cx, cy, anchor='nw', image=preview_img)
                self.preview_canvas.image = preview_img
            except Exception:
                self.preview_canvas.create_text(canvas_width//2, canvas_height//2, text="Error loading preview", fill='red')
        else:
            sample_size = min(canvas_width-20, canvas_height-20)
            x = (canvas_width - sample_size) // 2
            y = (canvas_height - sample_size) // 2
            self.preview_canvas.create_rectangle(x, y, x+sample_size, y+sample_size, fill='#fafafa', outline='#ccc')
            self.preview_canvas.create_text(canvas_width//2, canvas_height//2, text="Select images to see preview", fill='#888')
            self.draw_logo_preview(x, y, sample_size)

    def draw_logo_preview(self, img_x, img_y, img_size):
        # Ensure minimum logo size and prevent negative/zero dimensions
        logo_width = max(10, min(self.logo_size_var.get(), img_size // 3))
        orig_w, orig_h = self.pa_logo.size
        aspect_ratio = orig_h / orig_w
        logo_height = max(10, int(logo_width * aspect_ratio))
        
        # Ensure both dimensions are valid
        if logo_width <= 0 or logo_height <= 0:
            logo_width = 20
            logo_height = int(logo_width * aspect_ratio)
        
        logo_resized = self.pa_logo.resize((logo_width, logo_height), Image.LANCZOS)
        logo_with_bg = Image.new("RGBA", (logo_width, logo_height), (0, 0, 0, 255))
        logo_with_bg.paste(logo_resized, (0, 0), logo_resized)
        logo_photo = ImageTk.PhotoImage(logo_with_bg)
        position = self.position_var.get()
        if position == "bottom_left":
            x = img_x + 10
            y = img_y + img_size - logo_height - 10
        elif position == "bottom_middle":
            x = img_x + (img_size - logo_width) // 2
            y = img_y + img_size - logo_height - 10
        else:
            x = img_x + img_size - logo_width - 10
            y = img_y + img_size - logo_height - 10
        self.preview_canvas.create_image(x, y, anchor='nw', image=logo_photo)
        self.preview_canvas.logo = logo_photo

    def process_images(self):
        if not self.selected_files:
            messagebox.showerror("Error", "Please select files first!")
            return
        image_files = self.selected_files
        result = messagebox.askyesno("Confirm", f"Found {len(image_files)} image(s).\nAdd parental advisory logo to all images?\nProcessed images will be saved with '_modified' suffix.")
        if not result:
            return
        self.progress['maximum'] = len(image_files)
        self.progress['value'] = 0
        processed_count = 0
        last_new_path = None
        for i, image_path in enumerate(image_files):
            try:
                self.status_label.config(text=f"Processing: {os.path.basename(image_path)}")
                self.root.update()
                # Always work on a copy, never modify the original
                img = Image.open(image_path).copy()
                img_width, img_height = img.size
                min_side = min(img_width, img_height)
                if self.crop_mode_var.get() == "crop":
                    left = (img_width - min_side) // 2
                    top = (img_height - min_side) // 2
                    img = img.crop((left, top, left+min_side, top+min_side))
                else:  # stretch
                    img = img.resize((min_side, min_side), Image.LANCZOS)
                logo_width = max(10, self.logo_size_var.get())
                orig_w, orig_h = self.pa_logo.size
                aspect_ratio = orig_h / orig_w
                logo_height = max(10, int(logo_width * aspect_ratio))
                if logo_width <= 0 or logo_height <= 0:
                    logo_width = 20
                    logo_height = int(logo_width * aspect_ratio)
                logo_resized = self.pa_logo.resize((logo_width, logo_height), Image.LANCZOS)
                logo_with_bg = Image.new("RGBA", (logo_width, logo_height), (0, 0, 0, 255))
                logo_with_bg.paste(logo_resized, (0, 0), logo_resized)
                position = self.position_var.get()
                img_width, img_height = img.size
                if position == "bottom_left":
                    x = 10
                    y = img_height - logo_height - 10
                elif position == "bottom_middle":
                    x = (img_width - logo_width) // 2
                    y = img_height - logo_height - 10
                else:
                    x = img_width - logo_width - 10
                    y = img_height - logo_height - 10
                # Always work in RGBA for compositing
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                img.paste(logo_with_bg, (x, y), logo_with_bg)
                # Save as new file with _modified before extension
                base, ext = os.path.splitext(image_path)
                new_path = base + "_modified" + ext
                # If original has alpha or is PNG, save as PNG to preserve transparency
                if (img.mode == "RGBA" or img.mode == "LA" or ext.lower() == ".png"):
                    img.save(new_path, format="PNG")
                else:
                    img = img.convert("RGB")
                    img.save(new_path)
                processed_count += 1
                last_new_path = new_path
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {os.path.basename(image_path)}: {str(e)}")
            self.progress['value'] = i + 1
            self.root.update()
        self.status_label.config(text=f"Completed! Processed {processed_count} images.")
        messagebox.showinfo("Success", f"Successfully processed {processed_count} images!\nProcessed images have '_modified' suffix.")
        # Open folder and select the last processed image
        if last_new_path and os.path.exists(last_new_path):
            folder = os.path.dirname(os.path.abspath(last_new_path))
            if sys.platform == "darwin":
                subprocess.run(["open", "-R", last_new_path])
            elif sys.platform == "win32":
                subprocess.run(["explorer", "/select,", last_new_path])
            elif sys.platform.startswith("linux"):
                # Try with xdg-open, will just open the folder
                subprocess.run(["xdg-open", folder])

def main():
    root = tk.Tk()
    app = ParentalAdvisoryAdder(root)
    root.mainloop()

if __name__ == "__main__":
    main() 