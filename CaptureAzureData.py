from os import listdir, path
from re import search
import tkinter as tk
from tkinter import filedialog
from pyk4a import Config, ImageFormat, PyK4A, PyK4ARecord

root = tk.Tk()
root.withdraw()
window = tk.Toplevel()
window.attributes('-topmost', True)
window.title("Capture Azure Data")

# Initiate parameters
saveFolder = tk.StringVar(value= path.join(path.expanduser("~"), "Documents"))
cameraPath = tk.StringVar(value='C:/Program Files/Azure Kinect SDK v1.4.1/tools')
name = tk.StringVar(value='name')
task = tk.StringVar(value='task')
side = tk.StringVar(value='left')
suffixIndex = tk.StringVar(value=1)
trial = tk.StringVar(value=1)
savedFiles = tk.StringVar(value=listdir(saveFolder.get()))

# Logo
logo = tk.PhotoImage(file="azure_logo.png")

# Buttons
def startCapture():
    global capturing
    capturing = True
            
    config = Config(color_format=ImageFormat.COLOR_MJPG)
    device = PyK4A(config=config, device_id=0)
    device.start()
    
    fileName = name.get() + '_' + task.get() + '_' + side.get() +  '_' + str(trial.get())
    record = PyK4ARecord(device=device, config=config, path=saveFolder.get() + '/' + fileName + '.mkv')
    record.create()
    
    # Toggle button text
    buttonRun.configure(text='Stop capturing', command=stopCapture, bg='#ff7c68')
    
    try:
        print("Recording... Click the 'Stop capturing' button to stop recording.")
        while capturing:
            capture = device.get_capture()
            record.write_capture(capture)
            window.update()  # Update the GUI to respond to button click events
            
    except KeyboardInterrupt:
        print("Recording stopped.")
        
    
    record.flush()
    record.close()
    print(f"{record.captures_count} frames written.")
    device.stop()
    
    # Reset button text and command
    buttonRun.configure(text='Start capturing', command=startCapture)

    # Add incremental numbering
    trial.set(int(trial.get()) + 1)
   
	  
def stopCapture():
    global capturing
    capturing = False
    buttonRun.configure(text='Start capturing', command=stopCapture, bg='#baffc9')
   
def selectFolder():
    folderDir = filedialog.askdirectory()
    saveFolder.set(folderDir)

def setCameraPath():
    folderDir = filedialog.askdirectory()
    cameraPath.set(folderDir)

# Function to update the list of saved files
def update_list():
    files = [f for f in listdir(saveFolder.get()) if path.isfile(path.join(saveFolder.get(), f)) and f.endswith('.mkv')]
    savedFiles.set(files)
    root.after(1000, update_list)
    
# Build the GUI
window.configure(bg='#F6F4F0')
imgLogo = tk.Label(window, image=logo)
imgLogo.grid(row=1, column=1, columnspan=3, padx=20, pady=2)
version = tk.Label(window, text='Version 4, August 2024')
version.grid(row=2, column=1, columnspan=3, padx=20, pady=2)

# Select path to Azure SDK
buttonCameraPath = tk.Button(window, text='Select path to SDK k4arecorder', command=setCameraPath)
buttonCameraPath.grid(row=3, column=1, columnspan=3, padx=20, pady=5)

# Select folder to save files
buttonSaveFolder = tk.Button(window, text='Select folder to save to', command=selectFolder)
buttonSaveFolder.grid(row=4, column=1, columnspan=3, padx=20, pady=5)
labelSaveFolder = tk.Label(window, textvariable=saveFolder)
labelSaveFolder.grid(row=5, column=1, columnspan=3, padx=20, pady=5)

# Enter participants name
tk.Label(window, text='Name:').grid(row=6, column=0, padx=0, pady=10)
entryName = tk.Entry(window, textvariable=name, width=50)
entryName.grid(row=6, column=1, columnspan=3, padx=0, pady=10)

# Enter task name
tk.Label(window, text='Task:').grid(row=7, column=0, padx=0, pady=10)
entryTask = tk.Entry(window, textvariable=task, width=50)
entryTask.grid(row=7, column=1, columnspan=3, padx=0, pady=10)

# Enter trial number
tk.Label(window, text='Trial/rep:').grid(row=8, column=0, padx=0, pady=10)
entryTrial = tk.Entry(window, textvariable=trial, width=50)
entryTrial.grid(row=8, column=1, columnspan=3, padx=0, pady=10)

# Select leg(s) used
tk.Label(window, text='Side:').grid(row=9, column=0, padx=0, pady=10)
side1 = tk.Radiobutton(window, text="Left leg", variable=side, value='left')
side1.grid(row=9, column=1, padx=0, pady=10)
side2 = tk.Radiobutton(window, text="Right leg", variable=side, value='right')
side2.grid(row=9, column=2, padx=0, pady=10)
side3 = tk.Radiobutton(window, text="Both legs", variable=side, value='both')
side3.grid(row=9, column=3, padx=0, pady=10)

# Display list of saved files
labelSavedFiles = tk.Label(window, text="Saved files:")
labelSavedFiles.grid(row=10, column=0, padx=20, pady=5)
listbox = tk.Listbox(window, listvariable=savedFiles, width=50)
listbox.grid(row=10, column=1, columnspan=3, padx=20, pady=5)
listbox.configure(bg='white')

# Start capture button
buttonRun = tk.Button(window, text='Start capturing', command=startCapture, bg='#baffc9')
buttonRun.grid(row=11, column=1, columnspan=3, padx=10, pady=10)

# Exit GUI button
buttonExit = tk.Button(window, text="Exit", command=lambda: [window.destroy(), root.destroy()])
buttonExit.grid(row=12, column=1, columnspan=3, padx=10, pady=20)
    
# Call the update_list function to start the automatic update of the list
update_list()

# Start the main event loop
root.mainloop()

