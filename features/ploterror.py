import os
import sys

try: 
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
except ModuleNotFoundError:
    if input(f"matplotlib is required to run this program ({sys.argv[0]}), execute pip install matplotlib? (Y): ").lower().strip() in ["", "y"]:
        os.system(f"pip install matplotlib")
    exit()
from datetime import datetime, timedelta
import threading

unfinished_timestamps = []

def plotError(frame: int or None, hours_mode=True):
    # NOTE: Using default value for argument timestamp in multithreading uses the snaphshot datetime
    global unfinished_timestamps
    timestamps = unfinished_timestamps
    timestamp = datetime.now()
    HOURS = hours_mode
    if HOURS:
        difference = timedelta(days=1)
        error_counts = [
            len([ts for ts in timestamps if ts > timestamp - timedelta(hours=i) and ts <= timestamp - timedelta(hours=i-1)])
            for i in range(24, 0, -1)
        ]
        plots = [datetime.now() - timedelta(hours=i) for i in range(24)]
    else:
        difference = timedelta(minutes=24)
        error_counts = [
            len([ts for ts in timestamps if timestamp - timedelta(minutes=i) < ts <= timestamp - timedelta(minutes=i-1)])
            for i in range(24, 0, -1)
        ]
        plots = [datetime.now() - timedelta(minutes=i) for i in range(24)]
    # Update list of timestamps with this event
    if frame == None: # Means plot_process is not called as the frame is passed as the signature
        timestamps.append(timestamp)
        print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}: Unfinished or blocked')
        # Remove timestamps older than 24 hours to keep only recent data
        period = datetime.now() - difference
        timestamps = [ts for ts in timestamps if ts > period]
    else:
        print(f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}: Update')
    
    plt.clf()
    plt.plot(plots, error_counts, marker='o', color='blue', label='Errors')
    plt.title(f'Number of Errors, period: 24 {"Hours" if HOURS else "Minutes"}')
    plt.xlabel('Hour')
    plt.ylabel('Number of Errors')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return timestamps

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