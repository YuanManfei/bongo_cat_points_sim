import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Controller, Key
from datetime import datetime, timedelta
import time
import threading
from PIL import Image, ImageTk
import os
import sys

class AutoTypeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bongo Cat Auto Typer")
        self.root.geometry("600x500")  # Reduced height to eliminate blank space at bottom
        
        # Define modern gentle color scheme inspired by Bongo Cat
        self.colors = {
            'bg': '#FDF6E3',           # Soft cream background
            'frame_bg': '#FFF8DC',     # Light cream
            'primary': '#DDA0DD',      # Gentle plum
            'secondary': '#AFD3E2',    # Soft blue
            'accent': '#E3BAA8',       # Warm peach
            'text': '#5D4E46',         # Dark brown for text
            'highlight': '#F9CB9C',    # Soft yellow highlight
            'progress_bg': '#ECE3CE',  # Light beige for progress bar
            'progress_fg': '#AFD3E2',  # Blue for progress bar fill
            'warning': '#FF6B6B'       # Red for warnings
        }
        
        # Apply custom styles
        self.setup_styles()
        
        # Set window icon if available
        self.set_window_icon()
        
        # Removed Bongo Cat image - no longer loading or displaying it
        
        self.keyboard = Controller()
        
        # Create variables (removed press_duration_var since we use a fixed value now)
        self.times_var = tk.IntVar(value=5000)
        self.interval_var = tk.DoubleVar(value=0.05)
        self.status_var = tk.StringVar(value="Ready to start typing! 🎵")
        
        # Create UI elements
        self.create_widgets()
        
        # Thread control
        self.type_thread = None
        self.is_running = False

    def setup_styles(self):
        """Configure modern gentle styles for widgets"""
        self.style = ttk.Style()
        
        # Configure widget styles
        self.style.theme_use('clam')  # Use a modern theme
        
        # Configure custom styles
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'], font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', background=self.colors['bg'], foreground=self.colors['text'], font=('Comic Sans MS', 16, 'bold'))
        self.style.configure('Warning.TLabel', background=self.colors['bg'], foreground=self.colors['warning'], 
                             font=('Segoe UI', 10, 'bold'))
        self.style.configure('TButton', background=self.colors['secondary'], foreground=self.colors['text'], 
                             font=('Segoe UI', 10, 'bold'), borderwidth=1, focuscolor='none',
                             lightcolor=self.colors['highlight'], darkcolor=self.colors['accent'])
        self.style.map('TButton', background=[('active', self.colors['primary'])])
        
        self.style.configure('Accent.TButton', background=self.colors['primary'], foreground='white', 
                             font=('Segoe UI', 10, 'bold'), borderwidth=1, focuscolor='none')
        self.style.map('Accent.TButton', background=[('active', self.colors['accent'])])
        
        self.style.configure('Stop.TButton', background='#FF6B6B', foreground='white', 
                             font=('Segoe UI', 10, 'bold'), borderwidth=1, focuscolor='none')
        self.style.map('Stop.TButton', background=[('active', '#FF5252')])
        
        self.style.configure('TEntry', fieldbackground='white', foreground=self.colors['text'], width=10)
        self.style.configure('TProgressbar', thickness=15, background=self.colors['progress_fg'], 
                             troughcolor=self.colors['progress_bg'], bordercolor=self.colors['bg'])
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
    def set_window_icon(self):
        """Set window icon if available"""
        try:
            # Try to load icon from resources when packaged as exe
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                icon_path = os.path.join(sys._MEIPASS, 'bongo_cat.ico')
            else:
                # Running as script
                icon_path = 'bongo_cat.ico'
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            # If icon doesn't exist or fails to load, continue without it
            pass

    def create_widgets(self):
        # Main frame with padding and background color
        main_frame = ttk.Frame(self.root, padding="15", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Bongo Cat header
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="🐱 Bongo Cat Auto Typer 🥁🎵", 
                               style='Header.TLabel')
        title_label.pack()
        
        # Removed Bongo Cat image - keeping only the header text
        # If no image, show a text alternative with cat emoji
        img_placeholder = ttk.Label(header_frame, text="🎵 Type Along with Bongo Cat! 🎵", 
                                   font=("Comic Sans MS", 12, "bold"), 
                                   background=self.colors['bg'], foreground=self.colors['primary'])
        img_placeholder.pack(pady=10)
        
        # Warning about F13 usage
        warning_frame = ttk.Frame(main_frame, style='TFrame')
        warning_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        warning_label = ttk.Label(warning_frame, 
                                  text="⚠️ WARNING: Avoid using F13 key as a macro while running this application ⚠️", 
                                  style='Warning.TLabel')
        warning_label.pack()
        
        # Type Settings header
        settings_header = ttk.Label(main_frame, text="Type Settings", 
                                   font=("Segoe UI", 12, "bold"), 
                                   foreground=self.colors['primary'],
                                   background=self.colors['bg'])
        settings_header.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 10))

        # Settings container frame
        settings_frame = ttk.Frame(main_frame, style='TFrame')
        settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        settings_frame.columnconfigure(1, weight=1)
        
        # Times input
        times_label = ttk.Label(settings_frame, text="Number of types:", style='TLabel')
        times_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        times_entry = ttk.Entry(settings_frame, textvariable=self.times_var, width=12, style='TEntry')
        times_entry.grid(row=0, column=1, pady=(0, 10), padx=(10, 0), sticky=tk.W)
        
        # Interval input
        interval_label = ttk.Label(settings_frame, text="Interval between types (seconds):", style='TLabel')
        interval_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        interval_entry = ttk.Entry(settings_frame, textvariable=self.interval_var, width=12, style='TEntry')
        interval_entry.grid(row=1, column=1, pady=(0, 10), padx=(10, 0), sticky=tk.W)
        
        # Removed press duration input - no longer showing in the interface
        # Press duration is now fixed at 0.05 seconds
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame, style='TFrame')
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        buttons_frame.columnconfigure((0, 1, 2), weight=1, uniform='button_col')
        
        # Estimate button
        estimate_btn = ttk.Button(buttons_frame, text="🎵 Estimate Time 🎵", 
                                 command=self.estimate_completion, style='TButton')
        estimate_btn.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        
        # Start button
        start_btn = ttk.Button(buttons_frame, text="⌨️ Start Typing ⌨️", 
                              command=self.start_typing, style='Accent.TButton')
        start_btn.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Stop button
        stop_btn = ttk.Button(buttons_frame, text="✋ Stop 🛑", 
                             command=self.stop_typing, style='Stop.TButton')
        stop_btn.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E))
        
        # Estimated completion label
        self.eta_label = ttk.Label(main_frame, text="", foreground="#6A5ACD", 
                                  font=("Segoe UI", 10, "italic"), style='TLabel')
        self.eta_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Status label
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Segoe UI", 11, "bold"), 
                                foreground=self.colors['text'], style='TLabel')
        status_label.grid(row=6, column=0, columnspan=2, pady=(10, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate', style='TProgressbar')
        self.progress.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5), padx=20)
        self.progress['value'] = 0

    def estimate_completion(self):
        try:
            times = int(self.times_var.get())
            interval = float(self.interval_var.get())
            # Fixed press duration at 0.05 seconds instead of using the variable
            press_duration = 0.05
            
            if times <= 0:
                total_seconds = 0
            else:
                # Fixed calculation to properly account for both press duration and intervals between types
                total_seconds = (times * press_duration) + ((times - 1) * interval)
            
            eta = datetime.now() + timedelta(seconds=total_seconds)
            # Format time nicely - showing hours, minutes, seconds if needed
            if total_seconds >= 3600:
                duration_str = str(timedelta(seconds=int(total_seconds)))
            elif total_seconds >= 60:
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                duration_str = f"{minutes} min {seconds} sec"
            else:
                duration_str = f"{round(total_seconds, 1)} seconds"
            
            # Format the end time
            end_time = eta.strftime('%I:%M %p').replace(' 0', ' ').strip()
            date_str = eta.strftime('%m/%d')
            
            self.eta_label.config(text=f"🎵 Est. duration: {duration_str} | End time: {date_str} {end_time} 🎵")
        except ValueError:
            self.eta_label.config(text="Please enter valid numbers")
    
    def start_typing(self):
        if not self.is_running:
            self.is_running = True
            self.type_thread = threading.Thread(target=self.run_typing)
            self.type_thread.daemon = True
            self.type_thread.start()
    
    def stop_typing(self):
        self.is_running = False
    
    def run_typing(self):
        try:
            times = int(self.times_var.get())
            interval = float(self.interval_var.get())
            # Fixed press duration at 0.05 seconds instead of using the variable
            press_duration = 0.05
            
            self.status_var.set("Bongo Cat is typing... 🥁🎵")
            self.progress['maximum'] = times
            self.progress['value'] = 0
            
            for i in range(1, times + 1):
                if not self.is_running:
                    break
                
                # Press and release F13
                self.keyboard.press(Key.f13)
                time.sleep(press_duration)
                self.keyboard.release(Key.f13)
                
                # Update progress
                self.progress['value'] = i
                self.status_var.set(f"Bongo Cat typed {i}/{times} times! 🥁")
                
                # If not the last iteration, wait for the specified interval
                if i < times and self.is_running:
                    time.sleep(interval)
            
            if self.is_running:
                self.status_var.set(f"Bongo Cat finished {times} types! 🎉🎵")
            else:
                self.status_var.set("Stopped by user 🛑")
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.is_running = False

def main():
    root = tk.Tk()
    app = AutoTypeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()