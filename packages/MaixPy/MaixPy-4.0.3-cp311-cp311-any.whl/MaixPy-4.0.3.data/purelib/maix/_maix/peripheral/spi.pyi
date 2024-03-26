"""
maix.peripheral.spi module
"""
from __future__ import annotations
__all__ = ['CLOCK_MODE_0', 'CLOCK_MODE_1', 'CLOCK_MODE_2', 'CLOCK_MODE_3', 'MASTER_MODE', 'SLAVE_MODE', 'SPI']
class SPI:
    def __init__(self, id: int, sclk: int, mosi: int, miso: int, cs: int, freq: int, use_soft_cs: int = -1, mode: int = -1, clock_mode: int = -1) -> None:
        ...
    def cs_high(self) -> int:
        """
        set cs pin to high level
        """
    def cs_low(self) -> int:
        """
        set cs pin to low level
        """
    def is_busy(self) -> bool:
        """
        get busy status of spi
        
        Returns: busy status, bool type
        """
    def read(self, read_len: int) -> list[int]:
        """
        read data from spi
        
        Args:
          - read_len: direction [in], read length, int type
        
        
        Returns: read data, vector<unsigned char> type
        """
    def read_write(self, write_data: list[int] = [], read_len: int = -1) -> list[int]:
        """
        set spi status to high level or low level
        
        Args:
          - write_data: direction [in], write data, vector<unsigned char> type
        the member range of the list is [0,255]
          - read_len: direction [in], read length, int type
        default is -1, means read_len = write_data.size()
        
        
        Returns: read data, vector<unsigned char> type
        """
    def write(self, write_data: list[int] = []) -> int:
        """
        write data to spi
        
        Args:
          - write_data: direction [in], write data, vector<unsigned char> type
        the member range of the list is [0,255]
        
        
        Returns: error code, if write success, return err::ERR_NONE
        """
CLOCK_MODE_0: int = 0
CLOCK_MODE_1: int = 1
CLOCK_MODE_2: int = 2
CLOCK_MODE_3: int = 3
MASTER_MODE: int = 1
SLAVE_MODE: int = 2
