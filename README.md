# Air Quality Network Sensor - Mobile version

## Urbanova

Source code and documentation for a mobile air quality sensor based on the Raspberry Pi computer and low-cost retail sensors. The Hologram Nova USB device allows the sensor to record data via an integrated cellular phone. Measurements are converted into JSON strings, then transferred and store to the Hologram Cloud using the Nova.

* Environmental measurements
	* Temperature, Pressure and Relative Humidity - TPU sensor (BME280 breakout; Adafruit)
    <https://www.adafruit.com/product/2652>
	* Particulate Matter (PM) in 16 bins including PM1, PM2.5 and PM10 - Particulate sensor (OPC-N2; Alphasense)
    <http://www.alphasense.com/index.php/products/optical-particle-counter/>

* Supporting hardware
	* Single-board computer (Raspberry Pi 3 - Model B)
    <https://www.adafruit.com/product/3055>
	* Hologram Nova
    <https://www.hologram.io/products/nova>


### Documentation

* [Initial setup](doc/install/)

* [Connect to hologram.io](docs/setup/Hologram_connectivity.md)
