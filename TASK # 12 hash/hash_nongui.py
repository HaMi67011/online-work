import hashlib

server_seed = "5f692b19314055dc74cd10374"
server_seed_hash = "5f692b19314055dc74cd10374"

hash_object = hashlib.sha256()

hash_object.update(server_seed.encode())

server_seed_hash_copy = hash_object.hexdigest()
print(server_seed_hash_copy)

encrypted_server_seed = hashlib.sha256(server_seed.encode()).hexdigest()
print(encrypted_server_seed )

if server_seed_hash_copy == encrypted_server_seed:
    print("Server seed and server seed hash match!")
else:
    print("Server seed and server seed hash do not match.")


