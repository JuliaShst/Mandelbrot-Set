import tkinter as tk
from turtle import RawTurtle, TurtleScreen, ScrolledCanvas
import time

MAX_ITER = 100
WIDTH = 400
HEIGHT = 300

RE_START = -2
RE_END = 1
IM_START = -1.5
IM_END = 1.5

root = tk.Tk()
root.title("Mandelbrot Fractal - Click to zoom in")

canvas = ScrolledCanvas(master=root, width=WIDTH, height=HEIGHT)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

screen = TurtleScreen(canvas)


screen.colormode(255)
screen.tracer(0, 0) 

def IsInMandelbrot(c):
    """Determine if a complex number is in the Mandelbrot set.
        Calculate the number of iterations required to determine 
        if a complex number is in the Mandelbrot set.
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n = n + 1
    return n

def draw_mandelbrot():
    """Draw the Mandelbrot fractal."""
    start_time = time.time()
    
    screen.tracer(0, 0) 
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            real = RE_START + (RE_END - RE_START) * x / (WIDTH - 1) 
            imag = IM_END - (IM_END - IM_START) * y / (HEIGHT - 1) 

            c = complex(real, imag) 

            m = IsInMandelbrot(c) 

            if m == MAX_ITER: 
                color = (0, 0, 0) 
            else: 
                color = (m % 8 * 32, m % 16 * 16, m % 32 * 8)

            t = RawTurtle(screen) 
            t.penup() 
            t.setpos(x - WIDTH / 2, HEIGHT / 2 - y) 
            t.pencolor(color) 
            t.dot() 
        
        # Print progress bar    
        if x % 50 == 0 or x == WIDTH - 1:
            progress_bar_length = 20
            percentage_progress = min(100, round(x / WIDTH * 100))
            completed_blocks = round(progress_bar_length * percentage_progress / 100)
            remaining_blocks = progress_bar_length - completed_blocks
            progress_bar = '[' + '=' * completed_blocks + ' ' * remaining_blocks + f'] {percentage_progress}%'
            print(progress_bar)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time} seconds")

    screen.update() 

def handle_click(x, y):
    """Handle the click event."""
    global RE_START, RE_END, IM_START, IM_END

    center_real = RE_START + (RE_END - RE_START) * x / WIDTH
    center_imag = IM_END - (IM_END - IM_START) * y / HEIGHT

    zoomed_width = (RE_END - RE_START) / 16  
    zoomed_height = (IM_END - IM_START) / 16  

    RE_START = center_real - zoomed_width
    RE_END = center_real + zoomed_width
    IM_START = center_imag - zoomed_height
    IM_END = center_imag + zoomed_height

    draw_mandelbrot()

# Initial draw
draw_mandelbrot()

# Bind the click event to the handle_click function
canvas.bind('<Button-1>', lambda event: handle_click(event.x, event.y))

screen.mainloop()
