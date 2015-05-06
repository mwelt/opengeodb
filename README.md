# opengeodb
Interface in python to OpenGeoDB. Data based on additional table *zip_coordinates* 
as described [here](http://opengeodb.org/wiki/OpenGeoDB_-_Umkreissuche).

## installation 

You can either use precalculated data from a dump i took a while ago, or
build *zip_coordinates* table from scratch.

### with dump

* Download my *zip_coordinates* dump from [here](https://dl.dropboxusercontent.com/u/26156549/zip_coordinates-02627_2013-09-18.sql)
  the dump is based on latest OpenGeoDB data from 2013/09/18. 
  Import it to your MySql database (change user and db name according 
  to your settings) with:

```bash
$ mysql -uopengeodb -p opengeodb < zip_coordinates-02627_2013-09-18.sql
```
  
### from scratch

* Download latest opengeodb dump [here](http://www.fa-technik.adfc.de/code/opengeodb/dump/),
  and import it to your MySql database (change user and db name according
  to your settings) with:
  
```bash
$ mysql -uopengeodb -p opengeodb < opengeodb-02627_2013-09-18.sql
```

* Go get some sleep, this may take a while. 
* create additional database *zip_coordinates*:

```sql
CREATE TABLE `zip_coordinates` (
    zc_id INT NOT NULL auto_increment PRIMARY KEY,
    zc_loc_id INT NOT NULL ,
    zc_zip VARCHAR( 10 ) NOT NULL ,
    zc_location_name VARCHAR( 255 ) NOT NULL ,
    zc_lat DOUBLE NOT NULL ,
    zc_lon DOUBLE NOT NULL
)
```

* and fill it with data:

```sql
INSERT INTO zip_coordinates (zc_loc_id, zc_zip, zc_location_name, zc_lat, zc_lon)
SELECT gl.loc_id, plz.text_val, name.text_val, coord.lat, coord.lon
FROM geodb_textdata plz
LEFT JOIN geodb_textdata name     ON plz.loc_id = name.loc_id
LEFT JOIN geodb_locations gl      ON plz.loc_id = gl.loc_id
LEFT JOIN geodb_hierarchies tier  ON plz.loc_id = tier.loc_id
LEFT JOIN geodb_coordinates coord ON plz.loc_id = coord.loc_id
WHERE plz.text_type  = 500300000 /* Postleitzahl */
AND   name.text_type = 500100000 /* Name */
AND   tier.id_lvl1 = 104
AND   tier.id_lvl2 = 105 /* Bundesrepublik Deutschland */
AND   name.text_locale = "de" /* deutschsprachige Version */
AND   gl.loc_type IN ( 100600000 /* pol. Gliederung */, 100700000 /* Ortschaft */ );
```

### install opengeodb module with pip:

```bash
$ pip install git+https://github.com/mwelt/opengeodb
```


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