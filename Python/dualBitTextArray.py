import ctypes



class DualBitTextArray:
        
        __lib = ctypes.CDLL('./crypto/CryptoLib.dll')
        __lib.des_fucntion.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int, ctypes.c_char_p, ctypes.c_bool]
        __lib.des_fucntion.restype = ctypes.POINTER(ctypes.c_int64)

        __lib.uint16_to_uint64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int]
        __lib.uint16_to_uint64.restype = ctypes.POINTER(ctypes.c_int64)

        __lib.uint64_to_uint16.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int]
        __lib.uint64_to_uint16.restype = ctypes.POINTER(ctypes.c_int16)

        def __init__(self, data: ctypes.POINTER = None, size: int = None) -> None:
            self.__data = data
            self.__size = size
        
        @staticmethod
        def __validate_key(key: str) -> bytes:
            """
                Validates the provided key, ensuring it meets the required length and type, then encodes it to bytes.

                Args:
                key (str): The key to validate, which must be a string of exactly 8 characters.

                Returns:
                bytes: The ASCII-encoded version of the input key.

                Raises:
                AssertionError: If the length of the key is not 8 characters.
                TypeError: If the key cannot be encoded to ASCII.
            """
            assert len(key) == 8, "error: length of key must be 8 characters"
            try: key = key.encode('ascii')
            except: raise TypeError("error: key must be an ASCII string")
            return key
        
        @staticmethod
        def __string_to_int16_array(string: str) -> tuple[ctypes.Array, int]:
            """
            Converts a string into an array of 16-bit integers (Unicode code points).
            Pads the array with null characters ('\0') to ensure its length is a multiple of 4.

            Args:
            string (str): The input string to convert.

            Returns:
            tuple[ctypes.Array, int]: 
                - A ctypes array of 16-bit integers representing the Unicode code points of the characters in the string,
                padded with null characters ('\0') to a length multiple of 4.
                - The size of the resulting array.
            """
            rep = [ord(character) for character in string]

            if (space := len(rep) % 4) != 0:
                rep += [ord('\0')] * (4 - space)

            return (ctypes.c_int16 * len(rep))(*rep), len(rep)
    

        @staticmethod
        def data_from_string(text: str) -> "DualBitTextArray":
            data, size = DualBitTextArray.__string_to_int16_array(text)
            return DualBitTextArray(data, size)

        @property
        def data(self) -> ctypes.Array[ctypes.c_int16]:
            return (ctypes.c_int16 * self.__size)(*self.__data)
        
        @property
        def size(self) -> int:
            return self.__size
        
        def get(self, index: str):
            return self.__data[index]

        def set(self, value: ctypes.Array[ctypes.c_int16], size: int) -> "DualBitTextArray":
            self.__data = value
            self.__size = size
            return self

        def set_64bit(self, value: ctypes.Array[ctypes.c_int64], size: int) -> "DualBitTextArray":
            self.__data = DualBitTextArray.__lib.uint64_to_uint16(value, size)
            self.__size = size * 4
            return self

        def to_string(self) -> str:
            rep = ""
            for i in range(self.__size):
                try:
                    symbl = chr(self.__data[i])
                    if symbl == '\0':
                        continue
                    rep += symbl
                except (ValueError, TypeError):
                    rep += "#"
            return rep

        def get_16bit_data(self) -> "DualBitTextArray":
            return self.data

        def get_64bit_data(self) -> tuple[ctypes.Array[ctypes.c_int64], int]:
            data = DualBitTextArray.__lib.uint16_to_uint64(self.__data, self.__size)
            size = self.__size // 4
            return data, size

        def encrypt(self, key: str):
            data_to_encrypt, data_to_encrypt_size = self.get_64bit_data()
            key = self.__validate_key(key)

            rep = DualBitTextArray.__lib.des_fucntion(data_to_encrypt, data_to_encrypt_size, key, True)
            self.set_64bit(rep, data_to_encrypt_size)

            return self
        
        def decipher(self, key: str) -> str:

            data_to_decripter, data_to_decripter_size = self.get_64bit_data()
            key = self.__validate_key(key)

            rep = DualBitTextArray.__lib.des_fucntion(data_to_decripter, data_to_decripter_size, key, False)
            self.set_64bit(rep, data_to_decripter_size)

            return self

        def clone(self):
            return DualBitTextArray(self.data, self.__size)


if __name__ == "__main__":
    data = DualBitTextArray.data_from_string("Hello world!!!")
    data.encrypt("20061303")
    print(data.to_string())
    data.decipher("20061303")
    print(data.to_string())