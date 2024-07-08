import hashlib
import tkinter as tk

def check_seed():
    server_seed = server_seed_entry.get()
    server_seed_hash = server_seed_hash_entry.get()
    client_seed = client_seed_entry.get()
    nonce = nonce_entry.get()

    server_seed_hash_copy = hashlib.sha256(server_seed.encode()).hexdigest()

    hash_object = hashlib.sha256()
    hash_object.update(server_seed.encode())
    server_seed_hash_copy = hash_object.hexdigest()

    if server_seed_hash_copy == server_seed_hash:
        result_label.config(text="Server seed and server seed hash match!", fg="green")
    else:
        result_label.config(text="Server seed and server seed hash do not match!", fg="red")

# Create the GUI window
window = tk.Tk()
window.title("Server Seed Checker")

# Calculate the half-screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
half_width = screen_width 
half_height = screen_height 

# Set window dimensions for half-screen display
window.geometry(f"{half_width}x{half_height}+0+0")

# Create labels and entry boxes using grid layout
server_seed_label = tk.Label(window, text="Server Seed:")
server_seed_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

server_seed_entry = tk.Entry(window, width=80)  # Increase width to 50 characters
server_seed_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

server_seed_hash_label = tk.Label(window, text="Server Seed Hash:")
server_seed_hash_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

server_seed_hash_entry = tk.Entry(window, width=80)  # Increase width to 50 characters
server_seed_hash_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

client_seed_label = tk.Label(window, text="Client Seed:")
client_seed_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

client_seed_entry = tk.Entry(window, width=80)  # Increase width to 50 characters
client_seed_entry.grid(row=3, column=0, padx=5, pady=5, sticky="w")

nonce_label = tk.Label(window, text="Nonce:")
nonce_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

nonce_entry = tk.Entry(window, width=80)  # Increase width to 50 characters
nonce_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Create a button to check the server seed
check_button = tk.Button(window, text="Check", command=check_seed)
check_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the result
result_label = tk.Label(window, text="", fg="black")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Run the GUI main loop
window.mainloop()

