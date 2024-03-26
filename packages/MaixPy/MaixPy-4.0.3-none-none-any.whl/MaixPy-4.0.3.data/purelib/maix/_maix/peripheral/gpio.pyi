"""
maix.peripheral.gpio module
"""
from __future__ import annotations
__all__ = ['GPIO', 'IN', 'OFF', 'ON', 'OUT', 'OUT_OD', 'PULL_DOWN', 'PULL_NONE', 'PULL_UP']
class GPIO:
    def __init__(self, pin: int, mode: int = -1, pull: int = -1) -> None:
        ...
    def high(self) -> None:
        """
        set gpio high
        """
    def low(self) -> None:
        """
        set gpio low
        """
    def off(self) -> None:
        """
        set gpio off
        """
    def on(self) -> None:
        """
        set gpio on
        """
    def read(self) -> int:
        """
        get gpio read
        
        Returns: int type
        return 0, means gpio is low level
        return 1, means gpio is high level
        return other, means error
        """
    def toggle(self) -> None:
        """
        gpio toggle
        """
    def value(self, value: int = -1) -> int:
        """
        write/read gpio value
        
        Args:
          - value: direction [in], gpio value. int type.
        value == 0, means write gpio to low level
        value == 1, means write gpio to high level
        
        
        Returns: int type
        if success, return 0; else return -1
        """
    def write(self, value: int) -> int:
        """
        get gpio write
        
        Args:
          - value: direction [in], gpio value. int type.
        value == 0, means write gpio to low level
        value == 1, means write gpio to high level
        value == -1 or not set, means read gpio value
        
        
        Returns: int type
        when read gpio value, return gpio value
        when write gpio value, if success, return 0; else return -1
        """
IN: int = 1
OFF: int = 0
ON: int = 1
OUT: int = 2
OUT_OD: int = 3
PULL_DOWN: int = 6
PULL_NONE: int = 4
PULL_UP: int = 5
