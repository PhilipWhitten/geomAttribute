"""
Creates vector layers with a QGIS memory layer data source.  These layers are intended to demonstrate how the Geometry Attribute Table
plugin renders datasets that have: multi-part, single part, *empty*, and, *null* geometries.  A description of the created layer is included with each method.
"""
# update 03/11/2018


from qgis.core import *
from PyQt5.QtGui import QColor

def createMultiPoints(layerName='Multi-Part Points'):
    """
    A geometry collection of multi-part points and points (single part constrained).

    For an *empty* point, QGIS creates erroneously creates a point with the coordinates (0 0).

    Args:
        layerName (str): The name of the layer that is loaded into QGIS.

    Returns:
        A QGIS memory data source vector layer containing features with the following geometries: 2 point multi-point; 4 point multi-point,
        1 point multi-point, point, *empty* multi-point, and, *null*.

    """
    """Creates a model single line dataset that also contains empty lines and null lines.  Constructed by function as
     it does not require methods not provided by QGSVectorLayer"""


    layer=QgsVectorLayer('MultiPoint?crs=epsg:4326&field=id:string&field=Description:string', layerName, "memory")

    pr=layer.dataProvider()

    # create dictionary of points
    geometries = {}
    geometries['1'] = ['MULTIPOINT ((1 1),(1 2))', '1. Multi-Point (2X)']
    geometries['2'] = ['MULTIPOINT ((2 1),(2 2),(2 3),(2 4))', '2. Multi-Point (4X)']
    geometries['3'] = ['MULTIPOINT ((3 1))', '3. Multi-Point (1X)']
    geometries['4'] = ['POINT (4 1)', '4. Point']
    geometries['5'] = [[], '5. Empty']
    geometries['6'] = [None, '6. null']

    for id, geom in geometries.items():
        record = QgsFeature()
        record.setAttributes([id, geom[1]])
        #create 'null' geometry
        if geom[0] is None:
            pass
        #create empty geometry
        elif len(geom[0]) == 0:
            #Below gives a null geometry
            #record.setGeometry(QgsGeometry.fromWkt('MULTIPOINT (())'))
            record.setGeometry(QgsGeometry.fromMultiPointXY([QgsPointXY()]))
        #create geometry with verticies
        else:
            record.setGeometry(QgsGeometry.fromWkt(geom[0]))

        pr.addFeature(record)

    layer.updateExtents()
    return layer

def createMultiLines(layerName='Multi-Part Lines'):
    """A geometry collection of multi-part lines and lines (single part constrained).

    Args:
        layerName (str): The name of the layer that is loaded into QGIS.

    Returns:
        A memory vector layer containing features with the following geometries: 2 part multi-line; 3 part multi-line,
        1 part multi-line, line, Empty multi-line, and, Null.

    """

    #The constructor is one of: 'Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', or 'MultiPolygon'."""
    layer=QgsVectorLayer('MultiLineString?crs=epsg:4326&field=ID:string&field=Description:string', layerName, "memory")

    pr=layer.dataProvider()

    # create dictionary of lines
    geometries = {}
    geometries['1'] = ['MULTILINESTRING ((1 6, 3 6), (1 7, 3 7))', '1. Multi-Line (2 parts)']
    geometries['2'] = ['MULTILINESTRING ((1 3, 4 3), (1 4, 4 4), (1 5, 4 5))', '2. Multi-Line (3 parts)']
    geometries['3'] = ['MULTILINESTRING ((1 2, 5 2))', '3. Multi-Line (1 part)']
    geometries['4'] = ['LINESTRING (1 1, 6 1)', '4. Line']
    geometries['5'] = [[], '5. Empty']
    geometries['6'] = [None, '6. null']

    categories = []
    colorList = [
        [140, 81, 10],
        [216, 179, 101],
        [246, 232, 195],
        [199, 234, 229],
        [90, 180, 172],
        [1, 102, 94]
    ]

    i = 0
    for id, geom in geometries.items():
        record = QgsFeature()
        record.setAttributes([id, geom[1]])
        #create 'null' geometry
        if geom[0] is None:
            pass
        #create empty geometry
        elif len(geom[0]) == 0:
            record.setGeometry(QgsGeometry.fromWkt('MULTILINESTRING (())'))
        #create geometry if not null or empty
        else:
            record.setGeometry(QgsGeometry.fromWkt(geom[0]))

        pr.addFeature(record)

        #Rendering each line
        #lineSymbol needs to be instantiated within For group, not before it.
        lineSymbol = QgsLineSymbol.createSimple({
            'capstyle': 'round',
            'width': '3.5'
        })
        lineSymbol.setColor(QColor(colorList[i][0], colorList[i][1], colorList[i][2]))
        category = QgsRendererCategory(id, lineSymbol, geom[1])
        categories.append(category)
        i += 1

    layer.updateExtents()

    renderer = QgsCategorizedSymbolRenderer('ID',categories)
    layer.setRenderer(renderer)

    text_format = QgsTextFormat()
    label = QgsPalLayerSettings()
    label.fieldName = 'Description'
    label.enabled = True
    label.setFormat(text_format)
    #label.placement = QgsPalLayerSettings.OnLine
    #label.OnLine = True
    #label.Size = 10
    labeler = QgsVectorLayerSimpleLabeling(label)
    layer.setLabelsEnabled(True)
    layer.setLabeling(labeler)
    layer.triggerRepaint()

    return layer

if __name__ == '__main__':

    name = "Model Lines"
    line_load = createMultiLines(name)
    print("Printing name")
    print(line_load.sourceName())