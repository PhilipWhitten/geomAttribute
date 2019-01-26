*********
Load Data
*********

The |model_data| *Load Data* function creates the following QGS memory vector layers and adds them to the current QGIS work space:

   * Multi-part Lines
   * Multi-part Points

Both of these layers contain records with: primitive geometries; multi-part geometries; *empty* geometry values; and, *null* geometry values.  These layers are ideal to observe the utility of the :ref:`geometryAttributeTable-page` tool.

The methods that create these layers are contained within the plugin's :ref:`modelVectorLayers-API`.

###
Use
###
Select the *Load Model Data* item from the *Geometry Attribute Table* group on the QGIS *Plugins* menu.


.. |model_data|  image:: ../../../icons/model_data.png
   :scale: 50%