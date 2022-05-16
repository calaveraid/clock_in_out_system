# clock_in_out_system
Clocking system for companies using a **Raspberry Pi** and a **RFID-RC522 Module**.

The application is in a very early phase, just for testing RFID tags.
The next step is to develop a web service for data synchronization and on which to run queries.

In this early version, you need a .csv file with the employes data with this structure:
*`id_number,Name Surname`*

* `main.py`: Run the Clock In - Clock Out System.
* `write_new_dni.py`: Use for write a new ID in a RFID tag.

## Prerequisites
* Install mfrc522 library with `sudo pip install mfrc522` (or using `pip3`)
* Active SPI Interface in `sudo raspi-config`
* RPi library is included with Raspberry OS. Just update (you know, `sudo apt update` -> `sudo apt upgrade`)
* Run scripts using python 3.x

This is the pin configuration for RFID-RC522 Module:

  | RC522 Pin	| RaspPi Pin |
  |-----------|------------|
  |3.3V	| Pin 1 |
  | RST | Pin 22 |
  | GND | Pin 6	|
  | MISO | Pin 21 |
  | MOSI | Pin 19 |
  | SCK	| Pin 23 |
  | SDA	| Pin 24 |

 > "If you walk in front my door and don't even say goodbye,  
 > what you leave me you take, you are not better than me."  
 > — Vladimir Tkachenko
