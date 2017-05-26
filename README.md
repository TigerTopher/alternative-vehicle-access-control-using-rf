# Vehicle Access Control Framework using RF Technology
## Alias: AVra-Cardabra
### ToDo: Add documentation & setup tutorial.

# Setup Tutorial
* Install Pycrypto
```
sudo apt-get install libgmp-dev
sudo apt-get update
sudo apt-get install python-dev
sudo pip install pycrypto
```

* Setup NFC Module
To run MFRC522.py, you first need to setup SPI-Py
```
git clone https://github.com/lthiery/SPI-Py
cd SPI-Py
python setup.py
```
After installing SPI-Py, you should be able to run MFRC522.py

* SWIG
The following is how to setup SWIG in your Raspberry PI and use it to create a wrapper file for your C code. This would then allow you to call your C functions in your python code [interfacing C/C++ to Python].

Install SWIG:
`sudo apt-get install swig`

You're SWIG is now installed. 

* Hooking to CRONTAB
ToDo.

* Pins used
ToDo.

# Resources
Ultrasonic Sensor Module
https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
