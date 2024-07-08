import hashlib
import tkinter as tk

def check_seed():
    server_seed = server_seed_entry.get()
    server_seed_hash = server_seed_hash_entry.get()
    client_seed = client_seed_entry.get()
    nonce = nonce_entry.get()

    calculated_seed_hash = hashlib.sha256(server_seed.encode()).hexdigest()

    if calculated_seed_hash == server_seed_hash:
        result_label.config(text="Server seed and server seed hash match!", fg="green")
    else:
        result_label.config(text="Server seed and server seed hash do not match!", fg="red")

def generate_seed_hash():
    server_seed = server_seed_entry.get()
    seed_hash = hashlib.sha256(server_seed.encode()).hexdigest()

    server_seed_hash_value_label.config(text=seed_hash)

def generate_seed_from_hash():
    server_seed_hash = server_seed_hash_entry.get()

    seed_found = False
    seed_value = ""

    for i in range(1000000):
        test_seed = str(i).zfill(6)
        calculated_seed_hash = hashlib.sha256(test_seed.encode()).hexdigest()

        if calculated_seed_hash == server_seed_hash:
            seed_found = True
            seed_value = test_seed
            break

    if seed_found:
        server_seed_value_label.config(text=seed_value)
    else:
        server_seed_value_label.config(text="Seed not found!")

# Create the GUI window
window = tk.Tk()
window.title("Server Seed Checker")

# Calculate the half-screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
half_width = screen_width // 2
half_height = screen_height // 2

# Set window dimensions for half-screen display
window.geometry(f"{half_width}x{half_height}+0+0")

# Create labels and entry boxes using grid layout
server_seed_label = tk.Label(window, text="Server Seed:")
server_seed_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

server_seed_entry = tk.Entry(window, width=80)  # Increase width to 80 characters
server_seed_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

server_seed_hash_label = tk.Label(window, text="Server Seed Hash:")
server_seed_hash_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

server_seed_hash_entry = tk.Entry(window, width=80)  # Increase width to 80 characters
server_seed_hash_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

client_seed_label = tk.Label(window, text="Client Seed:")
client_seed_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

client_seed_entry = tk.Entry(window, width=80)  # Increase width to 80 characters
client_seed_entry.grid(row=3, column=0, padx=5, pady=5, sticky="w")

nonce_label = tk.Label(window, text="Nonce:")
nonce_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

nonce_entry = tk.Entry(window, width=80)  # Increase width to 80 characters
nonce_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Create a button to check the server seed
check_button = tk.Button(window, text="Check", command=check_seed)
check_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Create a button to generate the server seed hash
generate_hash_button = tk.Button(window, text="Generate Hash", command=generate_seed_hash)
generate_hash_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create a button to generate the server seed from the hash
generate_seed_button = tk.Button(window, text="Generate Seed", command=generate_seed_from_hash)
generate_seed_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the generated server seed hash value
server_seed_hash_value_label = tk.Label(window, text="", fg="black")
server_seed_hash_value_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the generated server seed value
server_seed_value_label = tk.Label(window, text="", fg="black")
server_seed_value_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the result
result_label = tk.Label(window, text="", fg="black")
result_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Run the GUI main loop
window.mainloop()

