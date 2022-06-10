from __future__ import annotations

import ctypes, struct, libnacl

class Scalar:
    def __init__(self, scalar = None):
        self.value = ctypes.create_string_buffer(libnacl.crypto_box_SECRETKEYBYTES)
        if scalar != None:
            if len(scalar) != libnacl.crypto_box_SECRETKEYBYTES:
                raise ValueError('Invalid scalar')
            ext = ctypes.create_string_buffer(64)
            ext[0:32] = scalar
            libnacl.nacl.crypto_core_ed25519_scalar_reduce(self.value, ext)
            
    def add(self, b: Scalar) -> Scalar:
        result = Scalar()
        libnacl.nacl.crypto_core_ed25519_scalar_add(result.value, self.value, b.value)
        return result
    
    def mul(self, b: Scalar) -> Scalar:
        result = Scalar()
        libnacl.nacl.crypto_core_ed25519_scalar_mul(result.value, self.value, b.value)
        return result
    
    def set_int(self, v: int) -> Scalar:            
        struct.pack_into('<q', self.value, 0, abs(v))
        if v < 0:
            libnacl.nacl.crypto_core_ed25519_scalar_negate(self.value, self.value)
        return Scalar(self.value)
    
    def to_int(self) -> int:
        a = Scalar(self.value)
        b = Scalar().set_int(100000)
        return struct.unpack_from('<q', self.add(b).value, 0)[0] - 100000
    
    def rnd(self) -> Scalar:
        libnacl.nacl.crypto_core_ed25519_scalar_random(self.value)
        return self

    def hex(self) -> str:
        return bytes(self.value).hex()

    def __print__(self):
        print("Ed25519Scalar(", bytes(self.value).hex(),")")
    

class Point:
    def __init__(self, point = None):
        self.value = ctypes.create_string_buffer(libnacl.crypto_box_PUBLICKEYBYTES)
        if point != None:
            if len(point) != libnacl.crypto_box_PUBLICKEYBYTES:
                raise ValueError('Invalid point')                
            self.value = point
            
    def add(self, b: Point) -> Point:
        if self.is_zero():
            return Point(b.value)
        if b.is_zero():
            return Point(self.value)
        
        result = Point()
        libnacl.nacl.crypto_core_ed25519_add(result.value, self.value, b.value)
        return result

    def sub(self, b: Point) -> Point:
        if self.is_zero():
            raise ValueError("Cannot subtract from 0")
        if b.is_zero():
            return Point(self.value)
        
        result = Point()
        libnacl.nacl.crypto_core_ed25519_sub(result.value, self.value, b.value)
        return result
    
    def is_zero(self) -> bool:
        return self.hex() == "0100000000000000000000000000000000000000000000000000000000000000"
    
    def scalarmult(self, b: Scalar) -> Point:
        result = Point()
        if libnacl.nacl.crypto_scalarmult_ed25519_noclamp(result.value, b.value, self.value):
            raise libnacl.CryptError('Failed to compute scalar product')
        return result
    
    def hex(self) -> str:
        return bytes(self.value).hex()
    
    def __print__(self):
        print("Ed25519Point(", bytes(self.value).hex(), ")")
    
    # The following methods, set_int and get_int, are specially used here for the homomorphic tests.
    
    def set_int(self, i: int) -> Point:
        if i == 0:
            a = Point().set_int(1)
            self.value = a.sub(a).value
        else:
            a = Scalar().set_int(i)
            self.value = Point.scalarmult_base(a).value
            
        return self

    def get_int(self) -> int:
        result = Point()
        # Zig-zag search for the correct number
        for i in range(1, 1000):
            j = i // 2
            if i % 2 == 0:
                j *= -1
            result.set_int(j)
            if bytes(result.value).hex() == bytes(self.value).hex():
                return j

        raise ValueError('No value found')

    @staticmethod
    def scalarmult_base(b: Scalar) -> Point:
        result = Point()
        if libnacl.nacl.crypto_scalarmult_ed25519_base_noclamp(result.value, b.value):
            raise libnacl.CryptError('Failed to compute scalar product')
        return result
    
