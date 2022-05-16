#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import mfrc522

MIFAREReader = mfrc522.MFRC522()
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
data = [0x00 for i in range(16)]
block = 4
dni = ''
continua = True

try:
    dni = input('\nIntroduce el nuevo DNI: ')
    print('\nAcerca nueva tarjeta...')
    while continua:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                # Fill the data with 0xFF
                for i in range(len(dni)):
                    data[i] = ord(dni[i])

                print("\nGrabando DNI en tarjeta...")
                # Write the data
                MIFAREReader.MFRC522_Write(block, data)

                print("Bloque grabado:")
                # Check to see if it was written
                print(MIFAREReader.MFRC522_Read(block))

                # Stop
                MIFAREReader.MFRC522_StopCrypto1()

            else:
                print("Error de autenticación")# Scan for cards    

            continua = False
            GPIO.cleanup()
            print('\nListo')


except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nListo')
