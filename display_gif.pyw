import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class TopLevelGif(tk.Toplevel):
    def __init__(self, gif_path, on_close_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("GIF Viewer")
        self.gif_path = gif_path
        self.on_close_callback = on_close_callback

        self.attributes('-topmost', True)
        self.overrideredirect(1)
        self.wm_attributes('-transparentcolor', 'white')

        self.load_gif()
        self.bind("<Escape>", self.close_window)

        self.bind("<Button-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_move)

    def load_gif(self):
        self.frames = []
        self.durations = []
        self.index = 0

        gif = Image.open(self.gif_path)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            transparency = Image.new('RGBA', gif.size, (255, 255, 255, 0))
            transparency.alpha_composite(gif.convert('RGBA'))
            frame_image = ImageTk.PhotoImage(transparency)
            self.frames.append(frame_image)
            self.durations.append(gif.info['duration'])

        self.label = tk.Label(self, image=self.frames[0], bd=0, bg='white')
        self.label.pack()

        self.update_gif()

    def update_gif(self):
        self.index = (self.index + 1) % len(self.frames)
        self.label.config(image=self.frames[self.index])
        self.after(self.durations[self.index], self.update_gif)

    def on_mouse_down(self, event):
        self.x_offset = event.x_root - self.winfo_rootx()
        self.y_offset = event.y_root - self.winfo_rooty()

    def on_mouse_move(self, event):
        new_x = event.x_root - self.x_offset
        new_y = event.y_root - self.y_offset
        self.geometry(f"+{new_x}+{new_y}")

    def close_window(self, event=None):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

class GifSelectorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GIF Selector")
        self.geometry("250x100")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.selected_gif_label = tk.Label(self, text="")
        self.selected_gif_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.active_gif_count = 0
        self.active_gif_label = tk.Label(self, text=f"Active: {self.active_gif_count}")
        self.active_gif_label.grid(row=1, column=0, columnspan=2)

        self.select_button = tk.Button(self, text="Select GIF", command=self.select_gif)
        self.select_button.grid(row=2, column=0, padx=30, pady=10)

        self.start_button = tk.Button(self, text="Start", command=self.start_gif, state=tk.DISABLED)
        self.start_button.grid(row=2, column=1, padx=30, pady=10)

    def select_gif(self):
        file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
        if not file_path:
            return
        self.selected_gif = file_path
        self.selected_gif_label.config(text=self.selected_gif.split('/')[-1])
        self.start_button.config(state=tk.NORMAL)

    def start_gif(self):
        if self.selected_gif:
            gif_viewer = TopLevelGif(self.selected_gif, on_close_callback=self.on_gif_viewer_closed)
            gif_viewer.geometry("+0+0")  # Position the window at the top-left corner
            self.active_gif_count += 1
            self.update_active_gif_label()

    def on_gif_viewer_closed(self):
        self.active_gif_count -= 1
        self.update_active_gif_label()

    def update_active_gif_label(self):
        self.active_gif_label.config(text=f"Active: {self.active_gif_count}")

def main():
    app = GifSelectorUI()
    app.mainloop()

if __name__ == "__main__":
    main()
