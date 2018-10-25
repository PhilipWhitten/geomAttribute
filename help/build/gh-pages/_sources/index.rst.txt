.. GeomAttribute documentation master file, created by
   sphinx-quickstart on Sun Oct 21 11:16:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GeomAttribute's documentation!
=========================================

|att_table| **QGIS Attribute Table with a Geometry Column**

.. |att_table|  image:: ../../icons/attribute_table.png

A QGIS 3 plugin that shows an attribute table which includes a geometry column for any vector layer.

The geometry column has icons that indicate the geometry type and may be useful in any dataset that contains
geometry collections, or, any dataset that contains empty or null geometries.  Examples of geometry collections
include a dataset that contains both multi-point and single-point geometries.

The table below shows the icons that are used for the respective geometry types:

+----------+--------------------+
| Icon     | Geometry           |
+==========+====================+
||Empty|   | Empty geometry     |
+----------+--------------------+
||Null|    | Unknown geometry   |
+----------+--------------------+
||poin_1x| | Point (single)     |
+----------+--------------------+
||poin_2x| | Multi-Part Point   |
+----------+--------------------+
||line_1x| | Line (single)      |
+----------+--------------------+
||line_2x| | Multi-part Line    |
+----------+--------------------+
||poly_1x| | Polygon (single)   |
+----------+--------------------+
||poly_2x| | Multi-Part Polygon |
+----------+--------------------+

.. |Empty|  image:: ../../icons/Empty.png
.. |Null|  image:: ../../icons/Null.png
.. |poin_1x|  image:: ../../icons/point_1x.png
.. |poin_2x|  image:: ../../icons/point_2x.png
.. |line_1x|  image:: ../../icons/line_1x.png
.. |line_2x|  image:: ../../icons/line_2x.png
.. |poly_1x| image:: ../../icons/polygon_1x.png
.. |poly_2x| image:: ../../icons/polygon_2x.png




.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
