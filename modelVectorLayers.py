"""
Creates vector layers as QGIS memory layers.  A description of the layers are included with each method
"""
# update 03/11/2018


from qgis.core import *

def ModelLines(lay_name='Single Lines'):

    """Creates a model single line dataset that also contains empty lines and null lines.  Constructed by function as
     it does not require methods not provided by QGSVectorLayer"""

    layer=QgsVectorLayer('LineString?crs=epsg:4326&field=id:string&field=type:string', lay_name, "memory")

    pr=layer.dataProvider()

    # create dictionary of lines
    lines = {}
    lines['Line1'] = [[(1, 1), (3, 1)], 'linestring(1 3, 1 1)']
    lines['Line2'] = [[(2, 2), (5, 2)], 'linestring(2 2, 5 2)']
    lines['Line3'] = [[(5, 1), (7, 1)], 'linestring(5 1, 7 1)']
    lines['Line4'] = [[], 'empty']
    lines['Line5'] = [None, 'null']

    for id, line in lines.items():
        ln = QgsFeature()
        ln.setAttributes([id, line[1]])
        if line[0] is None:
            pass
        elif len(line[0]) == 0:
            ln.setGeometry(QgsGeometry(QgsLineString()))
        else:
            ln.setGeometry(QgsGeometry(QgsLineString([QgsPoint(line[0][0][0], line[0][0][1]),
                                                          QgsPoint(line[0][1][0], line[0][1][1])])))
        pr.addFeature(ln)

    layer.updateExtents()
    return layer

def ModelPoints(lay_name='Single Points'):

    """Creates a model single line dataset that also contains empty lines and null lines.  Constructed by function as
     it does not require methods not provided by QGSVectorLayer"""

    """The constructor is one of: 'Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString',
     or 'MultiPolygon'."""
    layer=QgsVectorLayer('Point?crs=epsg:4326&field=id:string&field=type:string', lay_name, "memory")

    pr=layer.dataProvider()
    prefix = 'Point'

    # create dictionary of lines
    geometries = {}
    geometries['1'] = [[(1, 1)], 'point(1 3)']
    geometries['2'] = [[(2, 2)], 'point(2 2)']
    geometries['3'] = [[(5, 1)], 'point(5 1)']
    geometries['4'] = [[], 'empty']
    geometries['5'] = [None, 'null']

    for id, geom in geometries.items():
        record = QgsFeature()
        record.setAttributes([prefix + ' ' + id, geom[1]])
        #create 'null' geometry
        if geom[0] is None:
            pass
        #create empty geometry
        elif len(geom[0]) == 0:
            record.setGeometry(QgsGeometry(QgsPoint()))
        #create geometry with verticies
        else:
            record.setGeometry(QgsGeometry(QgsPoint(geom[0][0][0], geom[0][0][1])))

        pr.addFeature(record)

    layer.updateExtents()
    return layer

def ModelMultiPoints(lay_name='Multi-Points'):

    """Creates a model single line dataset that also contains empty lines and null lines.  Constructed by function as
     it does not require methods not provided by QGSVectorLayer"""

    """The constructor is one of: 'Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString',
     or 'MultiPolygon'."""
    layer=QgsVectorLayer('MultiPoint?crs=epsg:4326&field=id:string&field=type:string', lay_name, "memory")

    pr=layer.dataProvider()
    prefix = 'MultiPoint'

    # create dictionary of lines
    geometries = {}
    geometries['1'] = [[(1,1), (1,3)], 'point{(1 3), (1 1)}']
    geometries['2'] = [[(2,2),(2,1), (2,3), (2,4)], 'point{(2 2), (2 1), (2 3), (2 4)}']
    geometries['3'] = [[(5,1)], 'point{(5 1)}']
    geometries['4'] = [[], 'empty']
    geometries['5'] = [None, 'null']

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
            points = []
            for point in geom[0]:
                points.append(QgsPointXY(point[0],point[1]))

            record.setGeometry(QgsGeometry.fromMultiPointXY(points))

        pr.addFeature(record)

    layer.updateExtents()
    return layer

def createMultiLines(layerName='Multi-part Lines'):
    """
    A geometery collection of multi-part lines and lines (single part constrained).  The collection includes the
    features with the following geometries: 2 part multi-line; 3 part multi-line, 1 part- multi-line, line,
    Empty multi-line, and, NullCreates a model single line dataset that also contains empty lines and null lines.
    """

    #The constructor is one of: 'Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', or 'MultiPolygon'."""
    layer=QgsVectorLayer('MultiLineString?crs=epsg:4326&field=id:string&field=type:string', layerName, "memory")

    pr=layer.dataProvider()
    prefix = 'MultiLine'

    # create dictionary of lines
    geometries = {}
    geometries['1'] = ['MULTILINESTRING ((1 1), (1 3)),((3 1), (3 3))', '2 part Multi-line']
    geometries['2'] = ['MULTILINESTRING (((2 1),(2 2)),((2 3), (2 4)),((4 2),(4 1)))', '3 part Multi-line']
    geometries['3'] = ['MULTILINESTRING (((5 1),(5 5)))', '1 part Multi-line']
    geometries['4'] = ['linestring(1 3, 1 1)', 'Single line']
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
            #unable to instantiate QVector class object as it is not wrapped in Python bindings
            # can't construct a geometry from a list of lines as a QVector container of lines is needed, not a list.
            record.setGeometry(QgsGeometry.fromWkt(geom[0]))

        pr.addFeature(record)

    layer.updateExtents()
    return layer



def loadInQgis():
    QgsProject.instance().addMapLayers([ModelLines(),ModelPoints(),ModelMultiPoints(),ModelMultiLines()])


def run_script(name):
    """Runs the script by ScriptRunner"""
    name = "Model Lines"
    QgsProject.instance().addMapLayer(ModelLines(name))
    print("Printing name")
    line_load.print_name()
    line_load.create_lines()


if __name__ == '__main__':
    """For running from PyCharm"""
    name = "Model Lines"
    line_load = ModelLines(name)
    print("Printing name")
    print(line_load.sourceName())