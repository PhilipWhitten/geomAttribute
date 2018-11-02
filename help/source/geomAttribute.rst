************************
Geometry Attribute Table
************************
|att_table|

Description
###########
An attribute table window which includes a geometry column for any vector layer.


The geometry column uses the icons shown in the table below to indicate the feature's geometry type in descending
precedence: unknown (null); empty; point; multi-part point; line; multi-part line; polygon; and, multi-part polygon.

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
     - Point (single)
   * - |poin_2x|
     - Multi-Part Point
   * - |line_1x|
     - Line (single)
   * - |line_2x|
     - Multi-part Line
   * - |poly_1x|
     - Polygon (single)
   * - |poly_2x|
     - Multi-Part Polygon

.. |Empty|  image:: ../../icons/Empty.png
.. |Null|  image:: ../../icons/Null.png
.. |poin_1x|  image:: ../../icons/point_1x.png
.. |poin_2x|  image:: ../../icons/point_2x.png
.. |line_1x|  image:: ../../icons/line_1x.png
.. |line_2x|  image:: ../../icons/line_2x.png
.. |poly_1x| image:: ../../icons/polygon_1x.png
.. |poly_2x| image:: ../../icons/polygon_2x.png

Use
###
This tool works on the current active layer within QGIS.  The current layer needs to be a vector layer.  This tool will
not work on a raster layer.

Click on the vector layer in the *Layers Panel* then click on the *Geometry Attribute Table* icon |att_table| or select
*Geometry Attribute Table* from the *Plugins* menu.

Definitions
###########
Geometry
   The shape that is associated with a feature.  In many GIS systems the a feature can only have a single geometry type,
   where the type is constrained to being the same for the entire dataset.

Dataset
   A table containing features.

Empty
   It is known that a geometry does not exist within the feature's domaine.  Normally only needed for attribute tables
   with multiple geometry columns.

Null
   The geometry is unknown.  It may or may not be empty depending on the dataset.

.. |att_table|  image:: ../../icons/attribute_table.png
