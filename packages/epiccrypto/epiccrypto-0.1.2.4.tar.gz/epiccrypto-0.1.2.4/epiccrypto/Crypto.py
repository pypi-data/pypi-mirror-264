import hashlib
from epicfilemanager import File

class Crypto:
    alphabet = list("abcdefghijklmnopqrstuvwxyzäöüßẞ.,/\#;:-_?! 1234567890")
    def hash_string(string : str):
        encoded_string = string.encode("utf-8")
        hasher = hashlib.sha256()
        hasher.update(encoded_string)
        return hasher.hexdigest()



    def getIndex(key : str):
        return [Crypto.alphabet.index(f) for f in key]  

    def encode(data : str, key : str):
        hashed_key = Crypto.hash_string(str.lower(key))
        shifts = Crypto.getIndex(hashed_key)
        index_data = Crypto.getIndex(str.lower(data))
        coded_data = []
        keyIndex = 0
        for i in range(0, len(index_data)):
            index = index_data[i]
            index += shifts[keyIndex]
            if index > len(Crypto.alphabet)-1:
                index -= len(Crypto.alphabet)
            coded_data.append(Crypto.alphabet[index])
            keyIndex += 1
            if keyIndex > len(shifts)-1:
                keyIndex = 0
        return "".join(coded_data)

    def decode(data : str, key: str):
        hashed_key = Crypto.hash_string(str.lower(key))
        shifts = Crypto.getIndex(hashed_key)
        index_data = Crypto.getIndex(str.lower(data))
        coded_data = []
        keyIndex = 0
        for i in range(0, len(index_data)):
            index = index_data[i]
            index -= shifts[keyIndex]
            if index < 0:
                index += len(Crypto.alphabet)
            coded_data.append(Crypto.alphabet[index])
            keyIndex += 1
            if keyIndex > len(shifts)-1:
                keyIndex = 0
        return "".join(coded_data)
    
    def encodeFile(path : str, key : str):
        file = File(path)
        print(file.path)
        data = file.read()
        if not file.exists or data == False:
            return False
        encoded = Crypto.encode(data, key)
        print(encoded)
        
    def decodeFile(path : str, key : str):
        file = File(path)
        data = file.read()
        if not file.exists or data == False:
            return False
        decoded = Crypto.encode(data, key)
        print(decoded)
        
        
        
        
        
        
        
        