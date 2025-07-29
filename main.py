import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Signal generation functions
def generate_signal(signal_type, t, freq=1, amplitude=1):
    if signal_type == 'Sine':
        return amplitude * np.sin(2 * np.pi * freq * t)
    elif signal_type == 'Square':
        return amplitude * np.sign(np.sin(2 * np.pi * freq * t))
    elif signal_type == 'Sawtooth':
        return amplitude * (2 * (t * freq - np.floor(0.5 + t * freq)))
    elif signal_type == 'Triangle':
        return amplitude * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)
    else:
        return np.zeros_like(t)

# Mathematical operations
def apply_operation(signal, operation):
    if operation == 'None':
        return signal
    elif operation == 'Scale x2':
        return 2 * signal
    elif operation == 'Add 1':
        return signal + 1
    elif operation == 'Subtract 1':
        return signal - 1
    elif operation == 'Differentiate':
        return np.gradient(signal)
    elif operation == 'Integrate':
        return np.cumsum(signal)
    else:
        return signal

class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Signal Processing GUI')
        self.root.geometry('800x600')

        # Controls
        self.signal_type = tk.StringVar(value='Sine')
        self.operation = tk.StringVar(value='None')
        self.freq = tk.DoubleVar(value=1.0)
        self.amp = tk.DoubleVar(value=1.0)

        control_frame = ttk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(control_frame, text='Signal Type:').pack(side=tk.LEFT)
        ttk.Combobox(control_frame, textvariable=self.signal_type, values=['Sine', 'Square', 'Sawtooth', 'Triangle'], width=10).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text='Operation:').pack(side=tk.LEFT, padx=10)
        ttk.Combobox(control_frame, textvariable=self.operation, values=['None', 'Scale x2', 'Add 1', 'Subtract 1', 'Differentiate', 'Integrate'], width=12).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text='Frequency:').pack(side=tk.LEFT, padx=10)
        ttk.Entry(control_frame, textvariable=self.freq, width=5).pack(side=tk.LEFT)

        ttk.Label(control_frame, text='Amplitude:').pack(side=tk.LEFT, padx=10)
        ttk.Entry(control_frame, textvariable=self.amp, width=5).pack(side=tk.LEFT)

        ttk.Button(control_frame, text='Plot', command=self.plot_signal).pack(side=tk.LEFT, padx=20)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def plot_signal(self):
        t = np.linspace(0, 1, 500)
        try:
            freq = float(self.freq.get())
            amp = float(self.amp.get())
        except ValueError:
            messagebox.showerror('Input Error', 'Frequency and Amplitude must be numbers.')
            return
        signal = generate_signal(self.signal_type.get(), t, freq, amp)
        processed = apply_operation(signal, self.operation.get())
        self.ax.clear()
        self.ax.plot(t, signal, label='Original Signal')
        self.ax.plot(t, processed, label='Processed Signal', linestyle='--')
        self.ax.set_title(f'{self.signal_type.get()} Signal with {self.operation.get()}')
        self.ax.legend()
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()
