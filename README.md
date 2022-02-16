# Shroomery

## General Concept

### Data from Sensors

Sensors for: Humidity, C02, Temperature

RPi writes data to json file -> update file on nextcloud -> frontend reads data from nextcloud and displays

### Configuration

Possible configurations:
    * Temperature
        * min/max fruiting chamber
        * min/max fruiting chamber
    * C02 level
        * min/max fruiting chamber
        * min/max fruiting chamber
    * Debuggin Phase:
        * Thresholds
            * max C02 -> start Fan

### Frontend

What to display -> prepared SQL queries? (last days, last week, last month, last x days, all):
    * Humidity
    * C02
    * Temperature

## Code Concept

ShroomRoom/ShroomChmaber 
    -> incubation chamber 
    -> fruiting chamber
    * get measurements

## Frontend

First iteration jupyter notebook reading nextcloud file

