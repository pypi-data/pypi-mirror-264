"""
Some useful functions to manipulate bytes
Author: Mohamed Abdelkader
Contact: mohamedashraf123@gmail.com
"""

def toHex(intval, nbits):
    """
    Converts an integer to hexdecimal.
    Useful for negative integers where hex() doesn't work as expected

    Params
    --
    intaval: [int] Integer number
    nbits: [int] Number of bits

    Returns
    --
    String of the hexdecimal value
    """
    h = format((intval + (1 << nbits)) % (1 << nbits),'x')
    if len(h)==1:
        h="0"+h
    return h

def toInt(hexval):
    """
    Converts hexidecimal value to an integer number, which can be negative
    Ref: https://www.delftstack.com/howto/python/python-hex-to-int/

    Params
    --
    hexval: [string] String of the hex value
    """
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

def format_hex(number, bits=16):
    if number < 0:
        # Compute two's complement for negative numbers
        number = (1 << bits) + number
    # Format the number as hex and remove the '0x' prefix
    hex_str = hex(number)[2:]
    # Ensure the hex string is the correct length
    hex_str = hex_str.zfill(bits // 4)
    return hex_str
