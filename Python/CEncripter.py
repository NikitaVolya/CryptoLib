import ctypes
import json

from DESEncryptedString import UnicodeDESEncryptedString

class CEncripter:

    __lib = ctypes.CDLL('./crypto/CryptoLib.dll')

    __lib.save_as_file.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int, ctypes.c_char_p]
    __lib.save_as_file.restype = ctypes.c_bool

    __lib.get_data_size_in_file.argtypes = [ctypes.c_char_p]
    __lib.get_data_size_in_file.restype = ctypes.c_int64

    __lib.read_file.argtypes = [ctypes.c_char_p]
    __lib.read_file.restype = ctypes.POINTER(ctypes.c_int16)

    @staticmethod
    def save_as_file(text: str, key: str, file_name: str = "output/output_file"):
        encrypt_text = UnicodeDESEncryptedString.data_from_string(text)
        encrypt_text.encrypt(key)

        CEncripter.__lib.save_as_file(encrypt_text.data, encrypt_text.size, file_name.encode("ascii"))

    @staticmethod
    def load_from_file(file_name: str, key: str) -> str | None:
        file_name = file_name.encode('ascii')

        size = CEncripter.__lib.get_data_size_in_file(file_name) // 16
        if size < 1:
            return None
        
        rep = CEncripter.__lib.read_file(file_name)
        data = UnicodeDESEncryptedString().set(rep, size)
        data.decipher(key)
        return data.to_string()


    @staticmethod
    def file_cripting(file_name: str, key: str, output_name: str):
        file_name = file_name.encode('ascii')

        rep = CEncripter.__lib.read_file(file_name)
        size = CEncripter.__lib.get_data_size_in_file(file_name) // 16

        data = UnicodeDESEncryptedString(rep, size)
        data.encrypt(key)
        CEncripter.__lib.save_as_file(data.data, data.size, output_name.encode("ascii"))

    @staticmethod
    def file_decripting(file_name: str, key: str, output_name: str):
        file_name = file_name.encode('ascii')

        rep = CEncripter.__lib.read_file(file_name)
        size = CEncripter.__lib.get_data_size_in_file(file_name) // 16

        data = UnicodeDESEncryptedString(rep, size)
        data.decipher(key)
        CEncripter.__lib.save_as_file(data.data, data.size, output_name.encode("ascii"))

    @staticmethod
    def save_as_json(data, key: str, file_name: str = "output/output_file"):
        text = json.dumps(data)
        CEncripter.save_as_file(text, key, file_name)
    
    def load_from_json(file_name: str, key: str) -> any:
        rep = CEncripter.load_from_file(file_name, key)
        if not rep:
            return None
        return json.loads(rep)


CEncripter.file_cripting("output\\test_table.xlsx", "20061303", "output\\test_table")
CEncripter.file_decripting("output\\test_table", "20061303", "output\\test_table_output.xlsx")