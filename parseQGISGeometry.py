# Update 09/11/2018

"""
The QGIS Expression and methods in this module parse a vector's geometry for a vector layer loaded into QGIS.
"""

from qgis.core import *
from qgis.utils import iface
from PyQt5.QtCore import QVariant
import PyQt5
from PyQt5 import QtWidgets


@qgsfunction(args='auto', group='Custom', usesGeometry=False)
def geometryField(feature, parent):
    """
    THIS DOCUMENTATION DOES NOT SHOW UP IN SPHINX

    Creates a QGIS expression called geometryField.  This expression returns a string that represents the geometry in
    the following order of decreasing precedence:

       * Null
       * Empty
       * Well known binary type string

    Returns:
       A string that represents the geometry.
    """
    geom = feature.geometry()
    if geom.isNull():
        return 'Null'
    elif geom.isEmpty(): #-----------------------REQUIRE TEST FOR EMPTY POINT-----------------
        return 'Empty'
    elif geom.type() ==  0 and geom.vertexAt(0) == QgsPoint():
            return 'Empty'
    else:
        return QgsWkbTypes.displayString(geom.wkbType())


def layerAddVirtualGeometryField(vectorLayer):
    """
    Uses the *geometryField* expression to provide string values that represent the feature's geometry.  These string
    values are appended to the input *vectorLayer* as a virtual field.

    Args:
        vectorLayer (QgsVectorLayer):  A QGIS vector layer.
    """

    #type can be QVariant.Sring, QVariant.int and QVariant.double
    field = QgsField( name='Geometry', type = QVariant.String, len=40)

    QgsExpression.registerFunction(geometryField)

    vectorLayer.addExpressionField('geometryField()', field)
    vectorLayer.geometryIndex = vectorLayer.fields().lookupField('Geometry')
    print(vectorLayer.geometryIndex)

def layerRemoveVirtualGeometryField(vectorLayer):
    """
    Removes the virtual field called Geometry from a vector layer if it exists.

    Args:
        vectorLayer (QgsVectorLayer):  A QGIS vector layer.
    """
    #determines the index of the field called 'Geometry'
    fieldIndex = vectorLayer.fields().indexFromName('Geometry')

    #Removes the field called 'Geometry' by reference to the field index.
    if fieldIndex == -1:
        pass
    else:
        vectorLayer.removeExpressionField(fieldIndex)

def layer_review(layer):
    """
    **IN PROGRESS**

    Reviews any vector layer for the presence of null or empty geometries.  Provides a summary of a layer by geometry
    type.

    """
    # what happens if there are no features?  Need to test for features!!

    layer.geometry_empty = 0
    layer.geometry_null = 0

    __warning_color = 'red'
    __good_color = 'green'
    __geometry_null_color = __good_color
    __geometry_empty_color = __good_color

    for feature in layer.getFeatures():
        geom = feature.geometry()
        if geom.isNull():
            layer.geometry_null += 1
        elif geom.isEmpty():
            layer.geometry_empty += 1
        else:
            pass

        if layer.geometry_null != 0:
            __geometry_null_color = __warning_color

        if layer.geometry_empty != 0:
            __geometry_empty_color = __warning_color


        #self.name = self.layer.sourceName()

    layer.attribute_no = layer.fields().count()

    layer.record_no = layer.featureCount()

    layer.provider_storage = layer.dataProvider().storageType()

    layer.provider_geometry = layer.dataProvider().wkbType()

        # self.layer_name = ...
        # self.provider = ....
        # self.shape_type = ... multi-line line ....


    layer.summary_list = [
            [f'{layer.attribute_no} columns without shape',''],
            [f'{layer.record_no} records',''],
            [f'{QgsWkbTypes.geometryDisplayString(layer.geometryType())} geometry type',''],
            [f'{QgsWkbTypes.displayString(layer.wkbType())} well known text representation',''],
            [f'The dataset is stored as {layer.provider_storage}',''],
            [f'{QgsWkbTypes.displayString(layer.provider_geometry)} provider geometry',''],
            [f'{layer.geometry_null} null geometries', __geometry_null_color],
            [f'{layer.geometry_empty} empty geometries', __geometry_empty_color]
            #,f'{self.providerType()} provider key'
        ]

    def simple_text(self):
        iter = layer.getFeatures()

        for feature in iter:
            geom = feature.geometry()
            att = feature.attributes()
            print(att, geom.asWkt())
            print(geom)
            var_has_geom = feature.hasGeometry()
            var_empty = geom.isEmpty()
            var_null = geom.isNull()
            output = 'Feature has geometry: %s | Geometry is empty: %s | Geometry is null: %s \n' % (var_has_geom, var_empty, var_null)
            print(output)


if __name__ == '__main__':
    """For running from PyCharm"""
    from model_data import ModelLines
    print('Creating model lines dataset')
    name = "Model Lines"
    test_layer = ModelLines(name)
    layer_rev = layer_review(test_layer)
    '''print(layer_rev.layer.sourceName())
    for item in layer_rev.summary_list():
        print(item[0])
        '''
