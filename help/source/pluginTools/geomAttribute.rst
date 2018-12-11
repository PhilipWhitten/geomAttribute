.. _geometryAttributeTable-page:

************************
Geometry Attribute Table
************************
|att_table|

Description
###########
An attribute table window which includes a geometry column for any vector layer.

The geometry column uses the icons shown in the table below to indicate the feature's geometry type in descending
precedence: unknown (null); empty; point; multi-part point; line; multi-part line; polygon; and, multi-part polygon.

.. _geometryIcon-table:

.. list-table:: Icons used to represent various geometries.
   :widths: 15 35
   :header-rows: 1

   * - Icon
     - Geometry
   * - |Empty|
     - Empty geometry
   * - |Null|
     - Unknown geometry
   * - |poin_1x|
     - Point
   * - |poin_2x|
     - Multi-Part Point
   * - |line_1x|
     - Line
   * - |line_2x|
     - Multi-Part Line
   * - |poly_1x|
     - Polygon
   * - |poly_2x|
     - Multi-Part Polygon

.. |Empty|  image:: ../../../icons/Empty.png
.. |Null|  image:: ../../../icons/Null.png
.. |poin_1x|  image:: ../../../icons/point_1x.png
.. |poin_2x|  image:: ../../../icons/point_2x.png
.. |line_1x|  image:: ../../../icons/line_1x.png
.. |line_2x|  image:: ../../../icons/line_2x.png
.. |poly_1x| image:: ../../../icons/polygon_1x.png
.. |poly_2x| image:: ../../../icons/polygon_2x.png

Use
###
This tool works on the current active layer within QGIS.  The current layer needs to be a vector layer.  This tool will
not work on a raster layer.

Click on the vector layer in the *Layers Panel* then click on the *Geometry Attribute Table* icon |att_table| or select
*Geometry Attribute Table* from the *Plugins* menu.


.. |att_table|  image:: ../../../icons/attribute_table.png
