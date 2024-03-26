"""
maix.touchscreen module
"""
from __future__ import annotations
import maix._maix.err
__all__ = ['TouchScreen']
class TouchScreen:
    def __init__(self, device: str = '', open: bool = True) -> None:
        ...
    def close(self) -> maix._maix.err.Err:
        """
        close touchscreen device
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def is_opened(self) -> bool:
        """
        Check if touchscreen is opened
        
        Returns: true if touchscreen is opened, false if not
        """
    def open(self) -> maix._maix.err.Err:
        """
        open touchscreen device
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def read(self) -> list[int]:
        """
        read touchscreen device
        
        Returns: Returns a list include x, y, pressed state
        """
