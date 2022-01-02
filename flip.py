"""
Read in a binary file and flip the bit ordering of all the bytes (while
keeping the byte order the same).
Usage:
    python flip_bits.py infile outfile
"""
import sys


def flip_bits(b):
    """
    Reverse the bits of byte `b`.  `b` must be an int in the range [0, 255]
    From https://stackoverflow.com/a/2602885/125507
    """
    b = (b & 0xF0) >> 4 | (b & 0x0F) << 4
    b = (b & 0xCC) >> 2 | (b & 0x33) << 2
    b = (b & 0xAA) >> 1 | (b & 0x55) << 1
    return b


def test_flip_bits():
    for n in range(256):
        assert(f'{n:>08b}'[::-1] == f'{flip_bits(n):>08b}')


# TODO: There are more efficient ways to process files 1 byte at a time:
# https://stackoverflow.com/a/59013806/125507

fin = open(sys.argv[1], 'rb')
fout = open(sys.argv[2], 'wb')

while True:
    byte = fin.read(1)

    # Quit at end of file
    if byte == b'':
        break

    # Flip bits
    flipped = flip_bits(byte[0])

    # Write flipped int to output file
    fout.write(bytes((flipped,)))

fin.close()
fout.close()

