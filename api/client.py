import socket
import threading
import customtkinter as ctk


HOST = "localhost"
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            chatbox.insert("end", message + "\n")
            chatbox.see("end")
        except:
            break


def send_message():
    message = entry.get()
    if message:
        client.sendall(message.encode())
        entry.delete(0, "end")


# GUI
root = ctk.CTk()
root.geometry("500x500")
root.title("Chat Client")

chatbox = ctk.CTkTextbox(root, width=480, height=400)
chatbox.pack(pady=10)

entry = ctk.CTkEntry(root, width=350)
entry.pack(side="left", padx=10, pady=10)

send_button = ctk.CTkButton(root, text="Senden", command=send_message)
send_button.pack(side="left", pady=10)


# Empfangs-Thread starten
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()