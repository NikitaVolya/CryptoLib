import ctypes



class UnicodeDESEncryptedString:
        
        __lib = ctypes.CDLL('./crypto/CryptoLib.dll')
        __lib.des_fucntion.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int, ctypes.c_char_p, ctypes.c_bool]
        __lib.des_fucntion.restype = ctypes.POINTER(ctypes.c_int16)

        def __init__(self, data: ctypes.POINTER, size: int) -> None:
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
        def __to_char(value: int):
            if value == ord('\0'):
                    return ""
            try:
                return chr(value)
            except (ValueError, TypeError):
                return "#"

        @staticmethod
        def data_from_string(text: str) -> "UnicodeDESEncryptedString":
            data, size = UnicodeDESEncryptedString.__string_to_int16_array(text)
            return UnicodeDESEncryptedString(data, size)

        @property
        def data(self) -> ctypes.Array[ctypes.c_int16]:
            tmp = [self.__data[i] for i in range(self.__size)]
            return (ctypes.c_int16 * self.__size)(*tmp)
        
        @property
        def size(self) -> int:
            return self.__size
        

        def get(self, index: str):
            return self.__data[index]

        def set(self, value: ctypes.Array[ctypes.c_int16], size: int) -> "UnicodeDESEncryptedString":
            self.__data = value
            self.__size = size
            return self


        def encrypt(self, key: str):
            data_to_encrypt, data_to_encrypt_size = self.__data, self.__size
            key = self.__validate_key(key)
            
            
            rep = UnicodeDESEncryptedString.__lib.des_fucntion(data_to_encrypt, data_to_encrypt_size, key, True)
            self.set(rep, data_to_encrypt_size)

            return self
        
        def decipher(self, key: str) -> str:

            data_to_decripter, data_to_decripter_size = self.__data, self.__size
            key = self.__validate_key(key)

            rep = UnicodeDESEncryptedString.__lib.des_fucntion(data_to_decripter, data_to_decripter_size, key, False)
            self.set(rep, data_to_decripter_size)

            for i in range(self.size - 1, -1, -1):
                if self.__data[i] != ord('\0'):
                    break
                self.__size -= 1
            self.__data = self.__data[:self.__size]

            return self


        def clone(self):
            return UnicodeDESEncryptedString(self.data, self.__size)
        
        def to_string(self) -> str:
            rep = ""
            for i in range(self.__size):
                rep += self.__to_char(self.__data[i])
            return rep

        def __str__(self) -> str:
            return self.to_string()
        
        def __repr__(self) -> str:
            return self.to_string()

        def __getitem__(self, key: int) -> chr:
            return self.__to_char(self.get(key))

if __name__ == "__main__":
    a = UnicodeDESEncryptedString.data_from_string("Hello world!!!")


    print(a.encrypt("20061303"))
    print(a[0])
    print(a.decipher("20061303"))
    for i in range(a.size):
        print(a[i])