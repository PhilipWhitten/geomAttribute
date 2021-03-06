# Update 09/11/2018

"""
The QGIS Expression and methods in this module parse each record's vector geometry for a QGIS vector layer.
"""

from qgis.core import *
from qgis.utils import iface
from PyQt5.QtCore import QVariant
import PyQt5
from PyQt5 import QtWidgets


@qgsfunction(args='auto', group='Custom', usesGeometry=False)
def geometryField(feature, parent):
    #   THIS DOCUMENTATION IS NOT BE SHOWN BY THE SPHINX AUTODOC DIRECTIVE
    """
    Creates a QGIS expression called geometryField.  This expression
    returns a string that represents the geometry in the following
    order of decreasing precedence:

       * Null
       * Empty
       * Well known binary type string

    Returns:
       A string that represents the geometry.
    """
    geom = feature.geometry()
    #   Creates Point(0 0)
    emptyPoint1 = QgsPoint()
    #   Creates Point(nan nan)
    emptyPoint2 = emptyPoint1.createEmptyWithSameType()
    #   Null has to be tested for before empty as QGIS treats all null
    # geometries as empty
    if geom.isNull():
        return 'Null'
    elif geom.isEmpty():
        return 'Empty'
    #   Specific tests for empty points.
    elif geom.type().__eq__(0) and geom.vertexAt(0).__eq__(emptyPoint1):
        return 'Empty'
    elif geom.type().__eq__(0) and geom.vertexAt(0).__eq__(emptyPoint2):
        return 'Empty'
    else:
        return QgsWkbTypes.displayString(geom.wkbType())


def layerAddVirtualGeometryField(vectorLayer):
    """
    Appends a virtual field called *"Geometry"* to the input *vectorLayer*.  This virtual field consists of string values populated by the *"geometryField"* expression that is contained within this module.

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
    Removes the virtual field called *'Geometry'* from a vector layer if it exists.

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
    **IN DEVELOPMENT - NOT CURRENTLY USED BY PLUGIN**

    Reviews any vector layer for the presence of *Null* or *Empty* geometries.  Provides a summary of the vector geometry types that occur within a layer.

    Args:
        vectorLayer (QgsVectorLayer):  A QGIS vector layer.

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
