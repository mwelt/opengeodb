# opengeodb
Pythoninterface to OpenGeoDB. Data based on additional tableset 
as described [here](http://opengeodb.org/wiki/OpenGeoDB_-_Umkreissuche).

## usage
```python
import opengeodb

connection = opengeodb.OpengeoDbConnection(
        host='localhost', user='opengeodb',
        passwd='opengeodb', db='opengeodb')

odb = opengeodb.OpengeoDb(connection)

#find locations by zipcode
locs_by_zip = odb.find_locations_by_zip("04205")

#find locations by city name
locs_by_name = odb.find_locations_by_name("Leipzig")

#find locations near by zipcode and distance
locs_nearby = odb.find_locations_nearby_zip("73614", 10)
```


