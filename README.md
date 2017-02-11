# NL_ParcelSearch

## Python Toolbox PerceelZoeker.pyt (ArcMap 10.x)

The search functionaliuty in this toolbox uses an ArcGIS Map Service hosted by Esri Nederland:
[http://basisregistraties.arcgisonline.nl/arcgis/rest/services/DKK/DKK/MapServer](http://basisregistraties.arcgisonline.nl/arcgis/rest/services/DKK/DKK/MapServer)

Please read - and agree to - the [Esri Nederland Terms of Use](http://www.esri.nl/overig/terms-of-use) before using this toolbbox.

Each cadastral parcel in the Netherlands is identified by a unique code consisting of 3 elements:  the municipality (Gemeentecode), a section (Sectie) and the actual parcel number (Perceelnummer). If you enter **ASD04**, **F** and **2749** respectively, you will zoom in to the Royal Palace at Dam Square in Amsterdam.

The geometry returned by the Map Service is in EPSG:28992, hence the limitation that the tool will only work when the Coordinate System of the map is set to RD_New.

The dialog and the help documentation are in Dutch.

The tool has been developed using ArcMap 10.1 and tested using ArcMap 10.3.

To use the toolbox in ArcMap: copy the *.pyt file, including the 2 corresponding *.xml files, to a folder of your choice and open it from the Catalog window in ArcMap.

![alt text](https://github.com/Tensing/NL_ParcelSearch/blob/master/image/ZoekKadastraalPerceel.png "The tool's dialog box")