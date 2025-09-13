def crib_drag_attack(guess, cp1, cp2):
    xor_ciphers = ""
    for idx in range(len(cp1)):
        ic1 = ord(cp1[idx])
        ic2 = ord(cp2[idx])
        ic_xor = ic1 ^ ic2
        xor_ciphers += chr(ic_xor)
    # print(xor_ciphers.encode("ascii").hex())

    for idx in range(len(xor_ciphers) - len(guess) + 1):
        slide = xor_ciphers[idx: idx + len(guess)]
        results = ""
        for i in range(len(guess)):
            ig = ord(guess[i])
            id = ord(slide[i])
            ir = ig ^ id
            results += chr(ir)
        print(results)


def match_key(key, data):
    p_size = len(data)
    k_size = len(key)
    # print('P_SIZE: {} -- K_SIZE: {}'.format(p_size, k_size))
    if k_size < p_size:  # if key size is less than p_size, add character
        add_key = p_size - k_size
        for x in range(add_key):
            key = '{}{}'.format(key, key[x])
    else:
        key = '{}'.format(key[:p_size])
    # p_size = len(plaintext)
    # k_size = len(key)
    # print('NEW P_SIZE: {} -- K_SIZE: {}, KEY={}'.format(p_size, k_size, key))
    return key


def encrypt(key, plaintext):
    idx = 0  # Declare index (idx) variable

    key = match_key(key, plaintext)
    ciphertext = ""  # Declare ciphertext variable
    for p in plaintext:  # Take one character at a time in message
        ip = ord(p)  # Convert to Decimal value code
        k = key[idx]  # Take byte value of the key at idx
        ik = ord(k)  # Convert to Decimal value code
        inew = ip ^ ik  # XOR bit-by-bit
        ciphertext += chr(inew)  # Convert to character code and Update ciphertext
        print(p, hex(ip), k, hex(ik), hex(inew))  # print every result
        idx += 1  # Increment idx by 1
    # print("LENGTH CIPHERTEXT: {}".format(len(ciphertext)))
    hexstring = ciphertext.encode("ascii").hex()

    print("\nCheck here...")
    print("{}".format(plaintext, ciphertext))
    print("{}".format(ciphertext))
    print("{}".format(hexstring))

    return ciphertext


def decrypt(key, ciphertext):
    idx = 0  # Declare index (idx) variable
    key = match_key(key, ciphertext)
    plaintext = ""  # Declare plaintext variable
    for c in ciphertext:  # Take one character at a time in message
        ic = ord(c)  # Convert to Decimal value code
        k = key[idx]  # Take byte value of the key at idx
        ik = ord(k)  # Convert to Decimal value code
        inew = ic ^ ik  # XOR bit-by-bit
        plaintext += chr(inew)  # Convert to character code and Update ciphertext
        # print(c, hex(ic), k, hex(ik), hex(inew))  # print every result
        idx += 1  # Increment idx by 1

    print("\n{} --> {}\n".format(plaintext, plaintext.encode("ascii").hex()))
    return plaintext


if __name__ == '__main__':
    message1 = " "
    key = " "

    ciphertextHex1 = ""  # insert between " " the assigned ciphertext in hexstring format
    ciphertextHex2 = ""  # insert between " " the assigned ciphertext in hexstring format

    # Convert the hexstring format to ascii string format. Insert script below.

    guess = input("Guess a word: ")
    crib_drag_attack(guess, ciphertext1, ciphertext2)
