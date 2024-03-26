import snap7
from snap7 import util
import struct
class client(object):
    client_s7 = snap7.client.Client()
    db_num = None

    @classmethod
    def connect(cls, ip_plc, db_num):
        cls.db_num = db_num
        cls.client_s7.connect(ip_plc, 0, 1)
    
    @classmethod
    def disconnect(cls):
        cls.client_s7.disconnect()
    
    @classmethod
    def read_bit(self, db_point, bit):
        data =  self.client_s7.db_read(self.db_num, db_point, 1)
        return util.get_bool(data, 0, bit)

    @classmethod    
    def bool_list(self, db_point):
        data = bytearray(1)
        data =  self.client_s7.db_read(self.db_num, db_point, 1)
        bool_values = [util.get_bool(data, 0, i) for i in range(8)]
        return bool_values
    
    @classmethod 
    def read_array(self, db_point, byte_num):
        bytes = list(self.client_s7.db_read(self.db_num, db_point, byte_num))
        return [[bool((byte >> i) & 1) for i in range(8)] for byte in bytes]
    
    @classmethod
    def read_usint(self, db_point):
        return util.get_usint(self.client_s7.db_read(self.db_num, db_point, 1), 0)
    
    @classmethod
    def read_byte(self, db_point):
        return util.get_byte(self.client_s7.db_read(self.db_num, db_point, 1), 0)
    
    @classmethod
    def read_sint(self, db_point):
        return util.get_sint(self.client_s7.db_read(self.db_num, db_point, 1), 0)
    
    @classmethod
    def read_uint(self, db_point):
        return util.get_uint(self.client_s7.db_read(self.db_num, db_point, 2), 0)
    
    @classmethod
    def read_int(self, db_point):
        return util.get_int(self.client_s7.db_read(self.db_num, db_point, 2), 0)
    
    @classmethod
    def read_word(self, db_point):
        return util.get_word(self.client_s7.db_read(self.db_num, db_point, 2), 0)
    
    @classmethod
    def read_udint(self, db_point):
        return util.get_udint(self.client_s7.db_read(self.db_num, db_point, 4), 0)
    
    @classmethod
    def read_dword(self, db_point):
        return util.get_dword(self.client_s7.db_read(self.db_num, db_point, 4), 0)
    
    @classmethod
    def read_bytes(self, db_point, byte_num):
        return self.client_s7.db_read(self.db_num, db_point, byte_num)
    
    @classmethod
    def read_dint(self, db_point):
        return util.get_dint(self.client_s7.db_read(self.db_num, db_point, 4), 0)
    
    @classmethod
    def read_real(self, db_point):
        return util.get_real(self.client_s7.db_read(self.db_num, db_point, 4), 0)
    
    @classmethod
    def read_lreal(self, db_point):
        return util.get_lreal(self.client_s7.db_read(self.db_num, db_point, 4), 0)
    
    @classmethod
    def read_string(self, db_point, size = 254):
        return util.get_string(self.client_s7.db_read(self.db_num, db_point, size + 2), 0)
    
    @classmethod
    def set_bit(self, db_point, bit, value):
        self.client_s7.db_write(self.db_num, db_point, util.set_bool(self.client_s7.db_read(self.db_num, db_point, 1), 0, bit, value))
    
    @classmethod
    def set_bool_list(self, db_point, bool_list):
        data_value = bytearray(1)
        for i, value in enumerate(bool_list):
            util.set_bool(data_value, 0, i, value)
        self.client_s7.db_write(self.db_num, db_point, data_value)
        
    @classmethod
    def set_array(self, db_point, data_byte):
        self.client_s7.db_write(self.db_num, db_point, bytes([sum(bit << i for i, bit in enumerate(bits)) for bits in data_byte]))
    
    @classmethod
    def set_usint(self, db_point, data_usint):
        data_value = bytearray(1)
        util.set_usint(data_value, 0, data_usint)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_byte(self, db_point, data_byte):
        data_value = bytearray(1)
        util.set_usint(data_value, 0, data_byte)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_bytes(self, db_point, data_byte):
        self.client_s7.db_write(self.db_num, db_point, data_byte)
    
    @classmethod
    def set_sint(self, db_point, data_sint):
        data_value = bytearray(1)
        util.set_sint(self, data_value, 0, data_sint)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_uint(self, db_point, data_uint):
        data_value = bytearray(2)
        util.set_uint(data_value, 0, data_uint)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_int(self, db_point, data_int):
        data_value = bytearray(2)
        util.set_int(data_value, 0, data_int)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_word(self, db_point, data_word):
        data_value = bytearray(2)
        util.set_int(data_value, 0, data_word)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_udint(self, db_point, data_udint):
        data_value = bytearray(4)
        util.set_dint(data_value, 0, data_udint)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_dword(self, db_point, data_dword):
        data_value = bytearray(4)
        util.set_dint(data_value, 0, data_dword)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_dint(self, db_point, data_dint):
        data_value = bytearray(4)
        util.set_dint(data_value, 0, data_dint)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_real(self, db_point, data_real):
        data_value = bytearray(4)
        util.set_real(data_value, 0, data_real)
        self.client_s7.db_write(self.db_num, db_point, data_value)
        
    @classmethod
    def set_lreal(self, db_point, data_lreal):
        data_value = struct.pack('>d', data_lreal)
        self.client_s7.db_write(self.db_num, db_point, data_value)
    
    @classmethod
    def set_string(self, db_point, data_string):
        data_value = bytearray(len(data_string) + 2)
        util.set_string(data_value, 0, data_string, len(data_string))
        self.client_s7.db_write(self.db_num, db_point, data_value)
        
