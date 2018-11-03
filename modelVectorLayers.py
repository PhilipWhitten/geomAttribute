"""
Creates vector layers as QGIS memory layers.  These layers are intended to demonstrate how the Geometry Attribute Table
renders datasets that have: multi-part, single part, empty, and, null geometries.  A description of the created
layer is included with each method.
"""
# update 03/11/2018


from qgis.core import *

def createMultiPoints(layerName='Multi-part Points'):
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
    prefix = 'MultiPoint'

    # create dictionary of points
    geometries = {}
    geometries['1'] = ['MULTIPOINT ((1 1),(1 2))', 'Mult-point with 2 points']
    geometries['2'] = ['MULTIPOINT ((2 1),(2 2),(2 3),(2 4))', 'Multi-point with 4 points']
    geometries['3'] = ['MULTIPOINT ((3 1))', 'Multi-point with 1 point']
    geometries['4'] = ['POINT (4 1)', 'Point']
    geometries['5'] = [[], 'empty - QGIS erroneously creates a point at (0 0)']
    geometries['6'] = [None, 'null']

    for id, geom in geometries.items():
        record = QgsFeature()
        record.setAttributes([prefix + ' ' + id, geom[1]])
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

def createMultiLines(layerName='Multi-part Lines'):
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
    prefix = 'MultiLine'

    # create dictionary of lines
    geometries = {}
    geometries['1'] = ['MULTILINESTRING ((1 1, 1 3),(2 1, 2 3))', 'Multi-line with 2 lines']
    geometries['2'] = ['MULTILINESTRING ((3 1,3 5),(4 1, 4 5),(5 1,5 5))', 'Multi-line with 3 lines']
    geometries['3'] = ['MULTILINESTRING ((6 1,6 7))', 'Multi-line with 1 line']
    geometries['4'] = ['LINESTRING (7 1, 7 7)', 'Line']
    geometries['5'] = [[], 'empty']
    geometries['6'] = [None, 'null']

    for id, geom in geometries.items():
        record = QgsFeature()
        record.setAttributes([prefix + ' ' + id, geom[1]])
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