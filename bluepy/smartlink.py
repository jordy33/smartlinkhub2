from btle import UUID, Peripheral, BTLEException
import struct
import math
import pexpect
import binascii

if __name__ == "__main__":
    resp=pexpect.spawn('hciconfig hci0 up')
    resp.expect('.*')
    Debugging = False
    devaddr = "f1:99:d1:ce:d9:1d random"
    print("Connecting to:", devaddr)
    a='s'
    while a=='s':
        try:
            conn = Peripheral(devaddr)
            while True:
                n = input("Ponga (s) para salir:")
                try:
                    conn.writeCharacteristic(0x0011,str.encode(n))
                except BTLEException as e:
                    print ("write error:")
                    print (e)
                    print ("Try again? (s/n)")
                    b=input()
                    if b == 's':
                        a='s'
                        break
                else:
                    b='n'
                if n.strip() == 's':
                    a='n'
                    break
            conn.disconnect()
        except BTLEException as e:
            print ("ERROR!!!!")
            print (e)
            print ("desea intentarlo de nuevo (s/n)?")
            a=input()
        finally:
            print ("saliendo")
