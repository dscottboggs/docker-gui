"""Update the packages in the container and display a splash-screen."""
from tkinter import Tk
from tkinter.simpledialog import Toplevel, Message
from time import sleep


class StatusMessage(Toplevel):
    def __init__(self, message):
        """Initialize the window."""
        window = self.window = Tk()
        self.message = message
        self.body(window)
        window.update()
        window.update_idletasks()
        super().__init__(window)

    def done(self):
        self.window.destroy()

    def body(self, master):
        return Message(master,
                       text=self.message,
                       anchor='center',
                       padding=75).pack()

d = StatusMessage("Test window, please ignore!")
sleep(3)
d.done()
