import hashlib
import os
import json

def hash_file(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()

def traverse_directory(directory):
    file_hashes = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hashes[filepath] = hash_file(filepath)

    return file_hashes

def generate_table(directory):
    file_hashes = traverse_directory(directory)

    with open("hash_table.json", "w") as json_file:
        json.dump(file_hashes, json_file, indent=4)

    print("Hash table generated")


def validate_hash(directory):
    with open("hash_table.json", "r") as json_file:
        old_hashes = json.load(json_file)

    new_hashes = traverse_directory(directory)

    for filepath, old_hash in old_hashes.items():
        if filepath not in new_hashes:
            print(f"{filepath} has been deleted")
        elif new_hashes[filepath] == old_hash:
            print(f"{filepath} hash is valid")
        else:
            print(f"{filepath} hash is invalid")

    for filepath in new_hashes:
        if filepath not in old_hashes:
            print(f"{filepath} is a new file")

def main():
    print("1. Generate a new hash table")
    print("2. Verify hashes")

    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        directory = input("Enter the directory path: ")
        generate_table(directory)

    elif choice == "2":
        directory = input("Enter the directory path: ")
        validate_hash(directory)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()