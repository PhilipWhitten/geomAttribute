************
Introduction
************

A dataset is a collection of records, where each record has a defined number of elements and the data type of each element is defined.  The elements are commonly referred to as attributes.  For example, the dataset of street names shown in :numref:`table_road` consists of records that have the attribute headings of *“Name”* and *"Street Type"* with the data types *letters and spaces* and *letters* respectively.  In this example, *Street Type* contains values from the set *{‘Lane’, ‘Road’, ‘Street’, ‘’}*.  The first three values *‘Lane’*, *‘Road’* and *‘Street’* are obvious – but what about the last value of *‘’*?  **‘’** *is a deliberate empty set of character values!*  In our world there are many streets that have no type, and, indeed there are many that have no name.  Here, the use of an *empty* set of characters, or *‘’*, indicates that the *Street Type* attribute has no type, not that the type is unknown (*null*).

.. _table_road:

.. table:: An example of a road name dataset.
   :widths: auto
   :align: center

   +-----------------------+--------------+
   || Name                 || Street Type |
   || (letters and spaces) || (letters)   |
   +=======================+==============+
   | Picton                | Road         |
   +-----------------------+--------------+
   | Menangle              | Street       |
   +-----------------------+--------------+
   | The Boulevard         | [#f1]_       |
   +-----------------------+--------------+

Geospatial datasets contain one or more values that refer to a location on earth.  For the majority of geospatial
datasets, the location consists of one or more points, lines, and/or polygons, that are referenced to a coordinate system that is a projection of the earth’s surface.

For this project, any dataset element type that stores the geospatial shape with respect to a referenced coordinate system is called a **geometry**.  Any *empty* geometry element is a geometry that doesn't have any of the vertices which are required to construct a shape.

In many organizations geospatial datasets are contained within enterprise databases where frequently the same brand of enterprise database is used elsewhere within the same organization to contain non-spatial datasets.  For example, a local government office may use one or more MicroSoft SQL Server installations as a dataset repository for: a content management system; a customer relationship management system; a land management system; an asset management system; and, a Geographic Information System (GIS).

QGIS :cite:`QGIS` is a computer program that among other things is used to view, create and edit the geometry values within geospatial datasets.  For many data sources QGIS does not: Parse *null* and *empty* geometry values equivalently for different data storage formats; does not directly show which records within a dataset have *null* or *empty* geometry elements; and, does not always process *null* and *empty* geometry elements as specified by international or open geospatial standards.

A conceptual description of datasets, geometry data types, and, *null* and *empty* data values are outlined in the :ref:`concept-page` section.

.. [#f1] The street name *Boulevard* is also a type of street, consequently the *Street Type* field is *empty*.



