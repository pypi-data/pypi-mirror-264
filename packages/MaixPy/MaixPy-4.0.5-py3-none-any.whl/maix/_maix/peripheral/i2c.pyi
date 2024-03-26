"""
maix.peripheral.i2c module
"""
from __future__ import annotations
__all__ = ['FAST_SPEED', 'I2C', 'MASTER', 'SEVEN_BIT', 'SLAVE', 'STANDARD_SPEED', 'TEN_BIT']
class I2C:
    def __init__(self, id: int, scl: int, sda: int, freq: int = -1, mode: int = -1, bit: int = -1, speed_mode: int = -1) -> None:
        ...
    def readfrom(self, addr: int, len: int) -> list[int]:
        """
        read data from i2c slave
        
        Args:
          - addr: direction [in], i2c slave address, int type
          - len: direction [in], data length to read, int type
        
        
        Returns: the list of data read from i2c slave, vector<unsigned char> type
        """
    def readfrom_mem(self, addr: int, start_addr: int, len: int) -> list[int]:
        """
        read data from i2c slave
        
        Args:
          - addr: direction [in], i2c slave address, int type
          - start_addr: direction [in], start address of i2c slave, int type
          - len: direction [in], data length to read, int type
        
        
        Returns: the list of data read from i2c slave, vector<unsigned char> type
        """
    def scan(self) -> list[int]:
        """
        scan all i2c address
        
        Returns: the list of i2c address, vector<int> type
        """
    def writeto(self, addr: int, data: list[int]) -> int:
        """
        write data to i2c slave
        
        Args:
          - addr: direction [in], i2c slave address, int type
          - data: direction [in], data to write, vector<unsigned char> type.
        Note: The member range of the list is [0,255]
        
        
        Returns: if success, return 0, else return -1
        """
    def writeto_mem(self, addr: int, start_addr: int, data: list[int]) -> int:
        """
        write data to i2c slave
        
        Args:
          - addr: direction [in], i2c slave address, int type
          - start_addr: direction [in], start address of i2c slave, int type
          - data: direction [in], data to write, vector<unsigned char> type.
        Note: The member range of the list is [0,255]
        
        
        Returns: if success, return 0, else return -1
        """
FAST_SPEED: int = 32
MASTER: int = 4
SEVEN_BIT: int = 1
SLAVE: int = 8
STANDARD_SPEED: int = 16
TEN_BIT: int = 2
