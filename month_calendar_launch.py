import subprocess
import os
import signal

# Define the directory where the server will be started
server_directory = "/home/pi/eink_tools/calendar/"

# Change the current working directory to the server directory
os.chdir(server_directory)

# Start the HTTP server in a separate process
server_process = subprocess.Popen(["python", "-m", "http.server"])

try:
    # Execute your shell command here
    command = ["firefox", "--headless", "--screenshot", "--dpr", "2", "--window-size=800,480", "http://0.0.0.0:8000/month.html"]
    # Run the command
    subprocess.run(command)
    # Execute the other script
    subprocess.run(['python', "/home/pi/Pimoroni/inky/examples/7color/image.py", "screenshot.png"])
finally:
    # Terminate the server after the shell command completes
    os.kill(server_process.pid, signal.SIGINT)
