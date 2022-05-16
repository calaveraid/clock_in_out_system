#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import os
from empresa import *
from config import *
import RPi.GPIO as GPIO
from time import sleep
import mfrc522

empr = empresa(EMPR_CIF, EMPR_NAME)

if os.path.isfile(EMPL_FILE):
    f = open(EMPL_FILE)
    lineas = f.readlines()
    for linea in lineas:
        l = linea.rstrip().split(',')
        empr.add_empleado(empleado(l[0], l[1], l[2]))
else:
    f = open(EMPL_FILE, 'w')
f.close()

if os.path.isfile(REG_FILE):
    f = open(REG_FILE)
    lineas = f.readlines()
    for linea in lineas:
        l = linea.rstrip().split(',')
        empr.find_by_dni(l[0]).add_registro({'datetime': datetime.strptime(l[1], '%d/%m/%Y - %H:%M:%S'), 'tipo': l[2]})
else:
    f = open(REG_FILE, 'w')
f.close()

MIFAREReader = mfrc522.MFRC522()
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
block = 4
dni = ''
print('\nEn espera...')

try:
    while True:
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print ("UID: {:X} {:X} {:X} {:X}".format(uid[0], uid[1], uid[2], uid[3]))

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                buffdni = MIFAREReader.MFRC522_Read(4)
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print("Authentication error")

            for b in buffdni:
                dni = dni + chr(b)
            dni = dni.strip(chr(0))
            print(dni)

            empl = empr.find_by_dni(dni)
            if empl:
                print('\n{} {}'.format(empl.nombre, empl.apellidos))
                if empl.add_registro({'datetime': datetime.now()}):
                    print('ENTRADA REGISTRADA')
                else:
                    print('SALIDA REGISTRADA')
                for reg in empl.registro[-6:]:
                    print(reg['datetime'].strftime('%d/%m/%Y - %H:%M:%S') +', '+ reg['tipo'])
            else:
                print('\nDNI no encontrado')

            sleep(2)
            dni = ''
            print('\nEn espera...')

except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nGuardando registros...')
    f = open(REG_FILE, 'w')
    for empl in empr.empleados:
        for reg in empl.registro:
            f.write(empl.dni +','+ reg['datetime'].strftime('%d/%m/%Y - %H:%M:%S') +','+ reg['tipo'] +'\n')
    f.close()
    print('Listo')
