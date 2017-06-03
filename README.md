# shp2gmt
A python script that extract the features in a shapefile by using pyshp library.
## Feature
An interact version that allow user to select the interest field and then output to a gmt (psxy) file.
## Python version:
* Pyhton Version: should be work on python 2.7 and 3.X. Tested in 3.5  
* Required library : pyshp ([Official github](https://github.com/GeospatialPython/pyshp))
## Usage
_$python3 shp2gmt input.shp_
## Sample output:
_The given shapefile contains the following fields:  
[1] AREA  
[2] PERIMETER  
[3] C69A1PL_  
[4] C69A1PL_ID  
[5] DATA_ID  
[6] CODE  
[7] AGE_CODE  
[8] AGE_C  
[9] AGE_E  
[10] ST_C  
[11] ST_E  
[12] ABBREV  
[13] CHAR_C  
[14] CHAR_E  
[15] MAP_ID  
[16] LAYER_ID  
Please select one field from above.  
Input "id" instead of the name of the field.  
Your selection >>>__9__   
Selected field: AGE_E  
The specified field '['AGE_E', 'C', 50, 0]' has the following field  
[0] Holocene  
[1] Latest Middle - Late Miocene  
[2] Middle Miocene  
[3] Late Miocene - Pleistocene  
[4] Pleistocene  
[5] Early Pliocene - Early Pleistocene  
Please use the 'ID' to select your interested content of field or type 'all' to output all the data from shapefile.  
Your selection >>>__3__  
Selected field content:Late Miocene - Pleistocene  
GMT file saved to:  
./SHP/Hengchun.shp.gmt  
_
