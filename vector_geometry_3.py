"""
29/08/2018
# this script runs from the python IDE
# this script assumes that the active layer is a vector layer
# this script prints the attributes, geometries and a statement stating whether the feature
# has a geometry and whether the geometry is empty or null
"""

from qgis.core import *
from qgis.utils import iface
from PyQt5.QtCore import QVariant
import PyQt5

"""
Creates a virtual field that identifies if a column value is null, empty or it's type.
"""
@qgsfunction(args='auto', group='Custom', usesGeometry=False)
def geometryField(feature, parent):
    geom = feature.geometry()
    if geom.isNull():
        return 'Null'
    elif geom.isEmpty(): #-----------------------REQUIRE TEST FOR EMPTY POINT-----------------
        return 'Empty'
    elif geom.type() ==  0 and geom.vertexAt(0) == QgsPoint():
            return 'Empty'
    else:
        return QgsWkbTypes.displayString(geom.wkbType())


def layerAddVirtualGeometryField(layer):
    """Adds virtual field to the vector layer"""

    #type can be QVariant.Sring, QVariant.int and QVariant.double
    field = QgsField( name='Geometry', type = QVariant.String, len=40)

    QgsExpression.registerFunction(geometryField)

    layer.addExpressionField('geometryField()', field)
    layer.geometryIndex = layer.fields().lookupField('Geometry')
    print(layer.geometryIndex)



def layer_review(layer):
    """Adds attributes to a QgsVectorLayer.  The attributes are for empty or null geometries
    Takes an existing vector layer and performs methods on it.  Constructed as a function and
    not a class as it is used on layers after they have been created"""
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

"""This bit paints the virtual geometry field column"""
class geometryDelegate(PyQt5.QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(geometryDelegate, self).__init__(parent)
        self.BackgroundRole(red)




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
