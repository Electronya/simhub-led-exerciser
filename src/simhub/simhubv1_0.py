from serial import Serial
from time import sleep


def unlockUpload(dev: str) -> bytes:
    """
    The unlock upload query.

    Params
        dev: The serial device to use.

    Return
        The SimHub device answer.
    """
    pkt = bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, ord('u'),
                 ord('n'), ord('l'), ord('o'), ord('c'), ord('k')])
    serial = Serial(port=dev, baudrate=115200, timeout=1000)
    serial.write(pkt)
    response = serial.read_until(size=17)
    serial.close()
    return response


def getProtoVersion(dev: str) -> bytes:
    """
    Get the protocole version.

    Params:
        dev: The serial device to use.

    Return
        The SimHub device answer.
    """
    pkt = bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, ord('p'),
                 ord('r'), ord('o'), ord('t'), ord('o')])
    serial = Serial(port=dev, baudrate=115200, timeout=1000)
    serial.write(pkt)
    response = serial.read_until(size=12)
    serial.close()
    return response


def getLedCount(dev: str) -> int:
    """
    Get the LED count.

    Params:
        dev: The serial device.

    Return
        The SimHub device LED count.
    """
    pkt = bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff, ord('l'),
                 ord('e'), ord('d'), ord('s'), ord('c')])
    serial = Serial(port=dev, baudrate=115200, timeout=1000)
    serial.write(pkt)
    response = serial.read_until(size=5)
    ledCountStr = response.decode()
    return int(ledCountStr)


def generatedLedData(dev: str, ledCount: int, iteration: int) -> None:
    """
    Generate LED data.

    Params:
        dev: The serial device.
        ledCount: The LED count of the SimHub device for which to generate the
                  data.
        iteration: The number of iteration of data generation.
    """
    serial = Serial(port=dev, baudrate=115200, timeout=1000)
    footer = [0xff, 0xfe, 0xfd]
    red = [0x0f, 0x00, 0x00]
    green = [0x00, 0x0f, 0x00]
    blue = [0x00, 0x00, 0x0f]
    yellow = [0x0f, 0x0f, 0x00]
    colors = [red, green, blue, yellow]
    for seq in range(iteration):
        ledData = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, ord('s'),
                   ord('l'), ord('e'), ord('d'), ord('s')]
        color = seq % 4
        for _ in range(ledCount):
            ledData.extend(colors[color])
        ledData.extend(footer)
        serial.write(bytes(ledData))
        sleep(1)
    serial.close()
