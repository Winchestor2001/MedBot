import base64


def create_hash(data):
    chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
             '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8',
             '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
             'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    key = ['d', '~', 'x', '4', ':', 'b', 't', '|', '?', '*', '6', 'R', '^', 'M', 'D', 'p', '/', 'w', 'K', '\\', 'a',
           'j', 'r', 'g', ']', 'B', ';', 'W', 'J', 'k', 'S', 'q', 'e', '8', 'U', 'v', '(', '1', 'G', 'z', ')', 'P', '{',
           '0', '&', '2', 'I', 'm', '9', "'", 'N', 'Y', 'C', '%', 'F', 'L', '<', '$', 'H', '+', '}', 's', '[', 'y', '.',
           'u', ',', '"', 'h', '3', '7', 'E', 'i', '`', 'Z', '#', ' ', '>', 'o', 'T', 'l', 'c', 'A', 'n', 'X', '-', 'Q',
           '=', 'V', 'O', '!', '5', 'f', '_', '@']

    plain_text = str(data)
    cipher_text = ""

    for letter in plain_text:
        index = chars.index(letter)
        cipher_text += key[index]

    item = str(cipher_text).encode('utf-8')
    base64_bytes = base64.b64encode(item)
    base64_string = base64_bytes.decode("utf-8")

    return base64_string
