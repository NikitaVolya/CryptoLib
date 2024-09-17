import ctypes
import json

from dualBitTextArray import DualBitTextArray

class CEncripter:

    __lib = ctypes.CDLL('./crypto/CryptoLib.dll')

    __lib.save_as_file.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int, ctypes.c_char_p]
    __lib.save_as_file.restype = ctypes.c_bool

    __lib.get_data_size_in_file.argtypes = [ctypes.c_char_p]
    __lib.get_data_size_in_file.restype = ctypes.c_int64

    __lib.read_file.argtypes = [ctypes.c_char_p]
    __lib.read_file.restype = ctypes.POINTER(ctypes.c_int64)

    @staticmethod
    def save_as_file(text: str, key: str, file_name: str = "output/output_file"):
        encrypt_data = DualBitTextArray.data_from_string(text)
        encrypt_data.encrypt(key)

        data, size = encrypt_data.get_64bit_data()
        
        CEncripter.__lib.save_as_file(data, size, file_name.encode("ascii"))

    @staticmethod
    def load_from_file(file_name: str, key: str) -> str | None:
        file_name = file_name.encode('ascii')

        size = CEncripter.__lib.get_data_size_in_file(file_name) // 64
        if size < 1:
            return None
        
        rep = CEncripter.__lib.read_file(file_name)
        data = DualBitTextArray().set_64bit(rep, size)
        data.decipher(key)
        return data.to_string()

    @staticmethod
    def save_as_json(data, key: str, file_name: str = "output/output_file"):
        text = json.dumps(data)
        CEncripter.save_as_file(text, key, file_name)
    
    def load_from_json(file_name: str, key: str) -> any:
        rep = CEncripter.load_from_file(file_name, key)
        if not rep:
            return None
        return json.loads(rep)


values = {"text": "Hello world", "try": 200}

CEncripter.save_as_json(values, "20061303")
data = CEncripter.load_from_json("output/output_file", "20061303")

print(data)
print(data["try"])