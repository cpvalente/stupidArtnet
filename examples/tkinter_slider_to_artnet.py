"""(Very) Simple Example of using Tkinter with StupidArtnet.

It creates a simple window with a slider of value 0-255
This value is streamed in universe 0 channel 1

Note: The example imports stupid artnet locally from
a parent folder, real use import would be simpler

"""

from tkinter import *

from stupidArtnet import StupidArtnet

# Declare globals
stupid = None
window = None


def updateValue(slider_value):
    """Callback from slider onchange.
    Sends the value of the slider to the artnet channel.
    """
    global stupid
    stupid.set_single_value(1, int(slider_value))


def cleanup():
    """Cleanup function for when window is closed.
    Closes socket and destroys object.
    """
    print('cleanup')

    global stupid
    stupid.stop()
    del stupid

    global window
    window.destroy()


# ARTNET CODE
# -------------

# Create artnet object
stupid = StupidArtnet()

# Start persistent thread
stupid.start()


# TKINTER CODE
# --------------

# Create window object
window = Tk()

# Hold value of the slider
slider_val = IntVar()

# Create slider
scale = Scale(window, variable=slider_val,
              command=updateValue, from_=255, to=0)
scale.pack(anchor=CENTER)

# Create label with value
label = Label(window)
label.pack()

# Cleanup on exit
window.protocol("WM_DELETE_WINDOW", cleanup)

# Start
window.mainloop()
