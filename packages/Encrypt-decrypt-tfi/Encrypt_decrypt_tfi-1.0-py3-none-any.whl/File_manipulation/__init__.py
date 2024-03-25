#TEXT FILE ENCRYPTION
def encrypt_textfile(file1, file2=None):

    # Define the message to be written at the beginning of the file
    message = "#This file has been encrypted with FILE_MANIPULATION by Wahid Hussain\n\n"

    # Reading the file
    with open(file1, 'rb') as f1:
        read1 = f1.read()

    # Encrypting the message
    incryp_lst = []
    increment = 967
    for byte in read1:
        encrypted_byte = byte + increment
        increment += 247
        incryp_lst.append(str(encrypted_byte))

    # If file2 is not provided, set it to file1
    if file2 is None:
        file2 = file1

    # Writing the file
    with open(file2, 'wb') as f:
        # Write the message at the beginning of the file
        f.write(message.encode())

        # Write the encrypted data
        w_row = f.write(b' '.join(map(bytes, map(str.encode, incryp_lst))))

#TEXT FILE DECRYPTION       
def decrypt_textfile(file1,file2=None):

    # Reading the text file
    with open(file1,'rb') as f1:
        f1.readline()
        f1.readline()
        read = f1.read()
    lst = read.split()
    
    # Decode bytes literals into integers
    lst = [int(byte) for byte in lst]

    # Decrypting the value into ASCII
    decry_lst = []
    decrement = 967
    for i in lst:
        decremented_value = i - decrement
        decrement += 247
        decry_lst.append(decremented_value)

    english_translation = ''.join(chr(char) for char in decry_lst)

    # If file two none
    if file2 is None:
        file2 = file1

    # Writting into the file
    with open(file2,'w') as f2:
        f2.write(english_translation)
    
#IMAGE FILE ENCRYPTION 
def encrypt_imagefile(file1, file2=None):

    # Define the message to be written at the beginning of the file
    message = "#This file has been encrypted with FILE-MANIPULATION by Wahid Hussain\n\n"

    # Reading the file
    with open(file1, 'rb') as f1:
        read1 = f1.read()

    # Encrypting the message
    incryp_lst = []
    increment = 967
    for byte in read1:
        encrypted_byte = byte + increment
        increment += 247
        incryp_lst.append(str(encrypted_byte))

    # If file2 is not provided, set it to file1
    if file2 is None:
        # If file2 is not provided, construct the output filename
        file2 = file1.replace('.jpg', '.txt')  # Change the suffix to .txt

    # Writing the file
    with open(file2, 'wb') as f:
        # Write the message at the beginning of the file
        f.write(message.encode())

        # Write the encrypted data
        w_row = f.write(b' '.join(map(bytes, map(str.encode, incryp_lst))))

#IMAGE FILE DECRYPTION
def decrypt_imagefile(file1, file2=None):
    # Reading the file
    with open(file1, 'rb') as f1:
        f1.readline()  # Skip the message
        f1.readline()  # Skip the newline after the message
        read = f1.read()

    lst = read.split()

    # Decrypting the value into bytes
    decrypted_bytes = []
    decrement = 967
    for byte in lst:
        decrypted_byte = int(byte) - decrement
        decrement += 247
        decrypted_bytes.append(decrypted_byte)

    decrypted_data = bytes(decrypted_bytes)

    # Determine the output filename
    if file2 is None:
        # If file2 is not provided, construct the output filename
        file2 = file1.replace('.txt', '.jpg')  # Change the suffix to .jpg

    # Writing the file
    with open(file2, 'wb') as f2:
        f2.write(decrypted_data)
