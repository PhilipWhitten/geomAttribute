"""
Creates vector layers as QGIS memory layers.  These layers are intended to demonstrate how the Geometry Attribute Table
renders datasets that have: multi-part, single part, empty, and, null geometries.  A description of the created
layer is included with each method.
"""
# update 03/11/2018


from qgis.core import *

def createMultiPoints(layerName='Multi-Part Points'):
    """A geometry collection of multi-part points and points (single part constrained).

    For an empty point, QGIS creates erroneously creates a point with the coordinates (0 0).

    Args:
        layerName (str): The name of the layer that is loaded into QGIS.

    Returns:
        A memory vector layer containing features with the following geometries: 2 point multi-point; 4 point multi-point,
        1 point multi-point, line, Empty multi-line, and, Null.

    """
    """Creates a model single line dataset that also contains empty lines and null lines.  Constructed by function as
     it does not require methods not provided by QGSVectorLayer"""


    layer=QgsVectorLayer('MultiPoint?crs=epsg:4326&field=id:string&field=type:string', layerName, "memory")

    pr=layer.dataProvider()

    # create dictionary of points
    geometries = {}
    geometries['1'] = ['MULTIPOINT ((1 1),(1 2))', '1 - Multi-Point (2X)']
    geometries['2'] = ['MULTIPOINT ((2 1),(2 2),(2 3),(2 4))', '2 - Multi-Point (4X)']
    geometries['3'] = ['MULTIPOINT ((3 1))', '3 - Multi-Point (1X)']
    geometries['4'] = ['POINT (4 1)', '4 - Point']
    geometries['5'] = [[], '5 - Empty']
    geometries['6'] = [None, '6 - null']

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
    layer=QgsVectorLayer('MultiLineString?crs=epsg:4326&field=id:string&field=type:string', layerName, "memory")

    pr=layer.dataProvider()

    # create dictionary of lines
    geometries = {}
    geometries['1'] = ['MULTILINESTRING ((1 1, 1 3),(2 1, 2 3))', '1 - Multi-Line (2X)']
    geometries['2'] = ['MULTILINESTRING ((3 1,3 5),(4 1, 4 5),(5 1,5 5))', '2 - Multi-Line (3X)']
    geometries['3'] = ['MULTILINESTRING ((6 1,6 7))', '3 - Multi-Line (1X)']
    geometries['4'] = ['LINESTRING (7 1, 7 7)', '4 - Line']
    geometries['5'] = [[], '5 - Empty']
    geometries['6'] = [None, '6 - null']

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

    layer.updateExtents()
    return layer

if __name__ == '__main__':

    name = "Model Lines"
    line_load = createMultiLines(name)
    print("Printing name")
    print(line_load.sourceName())