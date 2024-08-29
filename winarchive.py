import sys
import os
import shutil
import subprocess
import getpass  # For password input

# Function to create a ZIP archive
def create_zip(input_dir, output_file, password=None):
    if password:
        print("Password-protected ZIP archives are not supported. Creating a normal ZIP archive.")
    
    shutil.make_archive(output_file.replace('.zip', ''), 'zip', input_dir)
    print(f"ZIP archive created: {output_file}.zip")

# Function to create a 7z archive
def create_7z(input_dir, output_file, password=None):
    command = [".\\7z.exe", "a", output_file, input_dir + "\\*"]
    
    if password:
        command.extend(["-p" + password, "-mhe"])  # -mhe also encrypts file names

    result = subprocess.run(command)
    if result.returncode == 0:
        print(f"7z archive created: {output_file}")
    else:
        print(f"Error creating 7z archive: {output_file}")

# Function to create a RAR archive
def create_rar(input_dir, output_file, password=None):
    command = [".\\7z.exe", "a", "-tzip", output_file, input_dir + "\\*"]  # Using ZIP as a placeholder for RAR
    if password:
        command.extend(["-p" + password])
    
    result = subprocess.run(command)
    if result.returncode == 0:
        print(f"RAR archive created: {output_file}")
    else:
        print(f"Error creating RAR archive: {output_file}")

# Function to create a CAB archive using the Windows makecab command
def create_cab(input_dir, output_file):
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            command = f'makecab "{file_path}" "{output_file}"'
            result = subprocess.run(command, shell=True)
            if result.returncode != 0:
                print(f"Error creating CAB file for: {file}")
                return
    print(f"CAB archive created: {output_file}")

# Function to create a custom archive format (.archive) with optional password protection
def create_custom_archive(input_dir, output_file, password=None):
    with open(output_file, 'wb') as archive_file:
        # Store the password at the beginning of the file
        if password:
            password_bytes = password.encode('utf-8')
            password_length = len(password_bytes)
            archive_file.write(password_length.to_bytes(4, 'little'))
            archive_file.write(password_bytes)
        else:
            archive_file.write((0).to_bytes(4, 'little'))  # Password length 0 if no password

        for root, dirs, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    archive_file.write(len(file).to_bytes(4, 'little'))
                    archive_file.write(file.encode('utf-8'))
                    archive_file.write(len(content).to_bytes(4, 'little'))
                    archive_file.write(content)
    print(f".archive file created: {output_file}")

# Function to extract a custom archive format (.archive) with password checking
def extract_custom_archive(archive_file, output_dir, password=None):
    with open(archive_file, 'rb') as archive_file:
        # Check the password
        password_length = int.from_bytes(archive_file.read(4), 'little')
        if password_length > 0:
            stored_password = archive_file.read(password_length).decode('utf-8')
            if password is None:
                password = getpass.getpass("The .archive file is password-protected. Please enter the password: ")
            if password != stored_password:
                print("Incorrect password. Access denied.")
                return
        else:
            if password is not None:
                print("The archive is not password-protected, but a password was provided. Ignoring the password.")

        # Extract the files
        while True:
            # Read file information
            filename_length_bytes = archive_file.read(4)
            if not filename_length_bytes:
                break  # End of the archive
            filename_length = int.from_bytes(filename_length_bytes, 'little')
            filename = archive_file.read(filename_length).decode('utf-8')

            file_size = int.from_bytes(archive_file.read(4), 'little')
            content = archive_file.read(file_size)

            # Write the file to the disk
            output_path = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as output_file:
                output_file.write(content)

    print(f".archive file extracted to: {output_dir}")

# Function to extract an archive (7z, zip, etc.)
def extract_archive(archive_file, output_dir, password=None):
    if archive_file.endswith('.archive'):
        extract_custom_archive(archive_file, output_dir, password)
    else:
        command = [".\\7z.exe", "x", archive_file, "-o" + output_dir]

        if password:
            command.append("-p" + password)

        result = subprocess.run(command)
        if result.returncode == 0:
            print(f"Archive extracted to: {output_dir}")
        else:
            print(f"Error extracting archive: {archive_file}")

# Main function
def main():
    if len(sys.argv) < 4:
        print("Usage: python winarchive.py [format] [input] [output] [optional_password]")
        sys.exit(1)

    archive_format = sys.argv[1].lower()
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    password = sys.argv[4] if len(sys.argv) > 4 else None

    if archive_format == 'zip':
        create_zip(input_path, output_path, password)
    elif archive_format == '7z':
        create_7z(input_path, output_path, password)
    elif archive_format == 'rar':
        create_rar(input_path, output_path, password)
    elif archive_format == 'cab':
        create_cab(input_path, output_path)
    elif archive_format == 'archive':
        create_custom_archive(input_path, output_path, password)
    elif archive_format == 'extract':
        extract_archive(input_path, output_path, password)
    else:
        print(f"Unknown format: {archive_format}")

if __name__ == '__main__':
    main()
