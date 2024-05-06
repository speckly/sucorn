import os
import sys

try: 
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
except ModuleNotFoundError:
    if input(f"matplotlib is required to run this program ({sys.argv[0]}), execute pip install matplotlib? (Y): ").lower().strip() in ["", "y"]:
        os.system("pip install matplotlib")
    exit()
from datetime import datetime, timedelta
import threading
from typing import Optional
from typing import Optional, Union

unfinished_timestamps = []
def plotError(frame: Optional[Union[int, None]]=None, hours_mode: bool=True):
    # Add an indented block of code here
    pass

def plot_process():
    ani = FuncAnimation(plt.gcf(), plotError, interval=100000) # ms interval for checking
    plt.show()

def plot_thread():
    animation_thread = threading.Thread(target=plot_process)
    animation_thread.start()

if __name__ == "__main__":
    ts = []
    animation_thread = threading.Thread(target=plot_process, args=(ts,))
    animation_thread.start()