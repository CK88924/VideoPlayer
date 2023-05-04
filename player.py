import os
import tkinter as tk
from tkinter import filedialog
import vlc
from tkinter import ttk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        self.root.geometry("800x600")
        
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        
        self.create_buttons()
        self.create_timeline_buttons()
        
        
    
   

    def create_buttons(self):
        self.load_button = tk.Button(self.root, text="Load Video", command=self.load_video)
        self.load_button.pack()

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause, state=tk.DISABLED)
        self.pause_button.pack()

        self.progress = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress.pack(pady=20)

        self.close_button = tk.Button(self.root, text="Close", command=self.close)
        self.close_button.pack(pady=10)

    def create_timeline_buttons(self):
        self.timeline_frame = tk.Frame(self.root)
        self.timeline_frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.timeline_frame)
        self.scrollbar = ttk.Scrollbar(self.timeline_frame, orient="vertical", command=self.canvas.yview)
        self.timeline_buttons_frame = tk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0,0), window=self.timeline_buttons_frame, anchor="nw")
        self.timeline_buttons_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


    def load_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv;*.avi")])

        if self.video_path:
            self.media = self.vlc_instance.media_new(self.video_path)
            self.media.get_mrl()
            self.media_player.set_media(self.media)

            self.load_timeline_buttons()

            self.media_player.play()
            self.pause_button.config(state=tk.NORMAL)
            self.root.after(1000, self.update_progress)

    def pause(self):
        self.media_player.pause()
        state = self.media_player.get_state()
        
        if state == vlc.State.Playing:
            self.pause_button.config(text="Play")
        else:
            self.pause_button.config(text="Pause")
    
    def load_timeline_buttons(self):
        for widget in self.timeline_buttons_frame.winfo_children():
            widget.destroy()
        basename = os.path.basename(self.video_path)
        txt_file = os.path.splitext(basename)[0] + ".txt"
        txt_path = os.path.join("timmer", txt_file)
        if os.path.exists(txt_path):
            with open(txt_path, "r",encoding='utf-8') as file:
                lines = file.readlines()
                buttons_per_row = 5  # 設置每行顯示的按鈕數量
                
                for index, line in enumerate(lines):
                    time_parts = line.strip().split(' ', 1)
                    start_time = time_parts[0].split('-')[0].split('~')[0]
                    text = time_parts[1] if len(time_parts) > 1 else ''
                    button = tk.Button(self.timeline_buttons_frame, text=f"{start_time} {text}", command=lambda t=start_time: self.go_to_time(t))
                
                    row = index // buttons_per_row
                    column = index % buttons_per_row
                    button.grid(row=row, column=column, padx=5, pady=5)

    
    def go_to_time(self, time_str):
        h, m, s = map(int, time_str.split(':'))
        seconds = h * 3600 + m * 60 + s
        self.media_player.set_time(seconds * 1000)
    
    def update_progress(self):
        length = self.media_player.get_length()
        time = self.media_player.get_time()

        if length > 0 and time > 0:
            self.progress["maximum"] = length
            self.progress["value"] = time

        self.root.after(1000, self.update_progress)
    

    def close(self):
        self.media_player.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
