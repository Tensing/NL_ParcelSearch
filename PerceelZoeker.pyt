#***************************************************************************************************************************************
#  Naam:    PerceelZoeker.pyt
#  Auteur:  Egge-Jan Pollé - Tensing - ejpolle@tensing.com
#  Datum:   10 februari 2017
#***************************************************************************************************************************************
import arcpy, re, json

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Zoeken"
        self.alias = "Zoeken"
        self.description = ""

        # List of tool classes associated with this toolbox
        self.tools = [ZoekKadastraalPerceel]

class ZoekKadastraalPerceel(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Zoek Kadastraal Perceel"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        gemCode = arcpy.Parameter(
        displayName="Gemeentecode",
        name="Gemeentecode",
        datatype="Field",
        parameterType="Required",
        direction="Input")

        sec = arcpy.Parameter(
        displayName="Sectie",
        name="Sectie",
        datatype="Field",
        parameterType="Required",
        direction="Input")

        pNum = arcpy.Parameter(
        displayName="Perceelnummer",
        name="Perceelnummer",
        datatype="Field",
        parameterType="Required",
        direction="Input")

        return [gemCode,sec,pNum]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].value:
            GemeenteCode = parameters[0].valueAsText.upper().replace(" ", "")
            parameters[0].value = GemeenteCode
        if parameters[1].value:
            Sectie = parameters[1].valueAsText.upper().replace(" ", "")
            parameters[1].value = Sectie
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if parameters[0].value:
            GemeenteCode = parameters[0].valueAsText
            if not re.match("[A-Z]{3}[0-9]{2}$", GemeenteCode):
                parameters[0].setErrorMessage("Onjuiste Gemeentecode. Een Gemeentecode bestaat uit 3 letters en 2 cijfers.")
            else:
                parameters[0].clearMessage()
        if parameters[1].value:
            Sectie = parameters[1].valueAsText
            if not re.match("[A-Z]{1,2}$", Sectie):
                parameters[1].setErrorMessage("Onjuiste Sectie. Een Sectie bestaat uit 1 of 2 letters.")
            else:
                parameters[1].clearMessage()
        if parameters[2].value:
            Perceelnummer = parameters[2].valueAsText
            if not re.match("[0-9]*$", Perceelnummer):
                parameters[2].setErrorMessage("Onjuist Perceelnummer. Een Perceelnummer bestaat uit cijfers.")
            else:
                parameters[2].clearMessage()
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        GemeenteCode = parameters[0].valueAsText
        Sectie = parameters[1].valueAsText
        Perceelnummer = parameters[2].valueAsText
        
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        sRName = df.spatialReference.name
        if sRName != "RD_New":
            arcpy.AddError("Kaart in onjuist coordinaatsysteem: {}".format(sRName))
            arcpy.AddError("Zoekfunctie werkt alleen voor Nederland met kaart in RD_New (EPSG:28992)")
            arcpy.AddError("Zoeken afgebroken")
            return


        url = "http://basisregistraties.arcgisonline.nl/arcgis/rest/services/DKK/DKK/MapServer/5/query?where=kadastraleGemeente='{}'  and sectie ='{}' and perceelnummer={}&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&outFields=kadastraleaanduiding&returnGeometry=true&f=pjson".format(GemeenteCode,Sectie,Perceelnummer)

        fs = arcpy.FeatureSet()

        fs.load(url)
        desc = arcpy.Describe(fs)
        jsonResponse = json.loads(desc.pjson)

        if (len(jsonResponse["features"]) == 0):
            arcpy.AddError("Geen resultaten gevonden")
            arcpy.AddError("Er bestaat geen perceel {} {} {}".format(GemeenteCode,Sectie,Perceelnummer))
            return
        else:
            aanDuiding = jsonResponse["features"][0]["attributes"]["kadastraleaanduiding"]
            arcpy.AddMessage("Perceel gevonden met kadastrale aanduiding: {}".format(aanDuiding))
            arcpy.AddMessage("Inzoomen naar perceel...")

        polygon = arcpy.AsShape(jsonResponse["features"][0]["geometry"], True)
        ext = polygon.extent
        zoomLevel = "100"
        df.scale = float(zoomLevel)
        df.extent = ext

        return