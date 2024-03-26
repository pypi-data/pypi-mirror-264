"""
maix.peripheral.pwm module
"""
from __future__ import annotations
__all__ = ['PWM']
class PWM:
    def __init__(self, pin: int, freq: int = 1000, duty: int = -1, duty_val: int = -1, align: int = -1, sync: bool = False) -> None:
        ...
    def duty(self, duty: int = -1) -> int:
        """
        set pwm duty
        
        Args:
          - duty: direction [in], pwm duty. int type. default is -1
        duty = [0, 100], set duty
        duty == -1 or not set, return current duty
        
        
        Returns: int type
        when get duty, return current duty
        when set duty, if success, return 0; else return -1
        """
    def duty_val(self, duty_val: int = -1) -> int:
        """
        set pwm duty value
        
        Args:
          - duty_val: direction [in], pwm duty value. int type. default is -1
        duty_val = [0, 65535], set duty_val
        duty_val == -1 or not set, return current duty_val
        
        
        Returns: int type
        when get duty_val, return current duty_val
        when set duty_val, if success, return 0; else return -1
        """
    def enable(self, enable: int = -1) -> int:
        """
        set pwm enable
        
        Args:
          - enable: direction [in], pwm enable. int type. default is -1
        enable == 0, disable pwm
        enable == 1, enable pwm
        enable == -1 or not set, return current enable value
        
        
        Returns: int type
        when get enable, return current enable value
        when set enable, if success, return 0; else return -1
        """
    def freq(self, freq: int = -1) -> int:
        """
        set pwm frequency
        
        Args:
          - freq: direction [in], pwm frequency. int type. default is -1
        freq >= 0, set freq
        freq == -1 or not set, return current freq
        
        
        Returns: int type
        when get freq, return current freq
        when set freq, if success, return 0; else return -1
        """
