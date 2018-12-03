.. _concept-page:

###########################################################
A QGIS attribute table plugin to show empty and null shapes
###########################################################

**DRAFT**

********
Preamble
********
I am in the closing stages of a MGIS at Penn State and needed a topic for capstone project.  What sort of topic?? I am gainfully employed as a GIS Officer at a local government bureau, but, my employer was not willing to offer a topic nor were they willing to offer open access to curious datasets.  I have a passion for maps, cartography and spatial analysis, but, previous attempts to combine my passion with requirements for academia often ended in a feeling of futility.  From my employment, I realised that my colleagues and I occasionally loose hours because some of our datasets were **corrupted** by *null* or empty geometries.  I also realised that I was blissfully ignorant of the concept of *null* and empty geometries as they were not included in my GIS education.  So, I wanted to learn a bit about *null* and empty geometries in the hope that I can be more capable in my employment and so that I can feed a curiosity.

The concept of a QGIS plugin that exposed *null* and empty shapes evolved quickly.  A plugin is tangible and deliverable as opposed to curiosity which is instinct and always expanding.  QGIS is the primary desktop GIS software where I work and I was keen to learn how to automate and develop QGIS for specific tasks.  In my GIS degree we had used Python to automate tasks in ArcMap, and, C# to make apps in ArcMap, but, we had not dabbled in QGIS.  So. this project was also an adventure in QGIS scripting.

What comes next?  From this project I have learnt that much of the GIS software and the GIS community is GIS centric.  After all, to create a new record in a dataset with either QGIS or ArcMap one creates the shape of a feature, and, subsequently populates the other attributes.  To work in reverse and create the shape of a feature as the last step in a workflow is not only not conventional, but, also not trivial.  But here's the point, whenever I have to create geospatial records I am always given a list of attributes and the shape is the last attribute to be created, the other attributes are already known and are re-entered.  Furthermore, most of the major desktop GIS packages report set operations between datasets differently to established database conventions.  I would like to work towards making QGIS and other software packages less GIS centric so that geospatial datasets become more ubiquitous and more open to other professional communities! To become less GIS centric you need to embrace the *null* and exploit the empty.


************
Introduction
************
A dataset is a collection of records, where each record has a defined number of elements and the data type of each
element is also defined.  The elements are commonly referred to as attributes.  For example, a dataset of street names
may consist of records have the attribute heading *“Name”* of type variable character and the character heading
*“Street Type”* of type street type.  In this example, street types may consist of the values
*(‘Lane’, ‘Road’, ‘Street’, ‘’)*.  The first three of the values *‘Lane’*, *‘Road’* and *‘Street’* are obvious – but what about
the last value of *‘’*?  **‘’ is a deliberate empty set of character values!**  In our world there are many streets that
have no type, and, indeed there are many that have no name.  Here, the use of an empty set of characters, or ‘’,
indicates that the Street Type attribute has no type, not that the type is unknown (null).

Geospatial datasets contain one or more values that refer to a location on earth.  For the majority of geospatial
datasets, the location consists of one or more points, lines and/or polygons that are referenced to a coordinate system
that is a projection of the earth’s surface.

For the purposes of this project, any dataset element type that stores the geospatial shape with respect to a referenced coordinate system is referred to as a geometry.  Any empty geometry element is simply a geometry that doesn’t have a shape.

In many enterprises geospatial datasets are contained within enterprise databases where frequently the same brand of enterprise database is used elsewhere within the same enterprise to contain non-spatial datasets.  For example, a local government office may use one or more MicroSoft SQL Server installations (MS SQL) as a dataset repository for: a content management system; a customer relationship management system; a land management system; an asset management system; and, a GIS system.

QGIS :cite:`QGIS` is a computer program that among other things is used to view, create and edit the geometry elements within geospatial datasets.  For many dataformats QGIS  QGIS does not: Pass null and empty geometry elements equivalently for different data storage formats; does not show directly show which records within a dataset have *null* or empty geometry elements; and, does not always process null and empty geometry elements as specified by standards.

This project aims to create a QGIS plugin that illuminates null and empty geometry elements in geospatial datasets.

**********
Background
**********

===================
Relational Datasets
===================
---
Set
---
A set is a collection of distinct objects.  For example, a box of apples is a set of apples, and, the set of countries in North America consists of Canada,  United States of America, and, Mexico.  By convention, sets are symbolized by enclosing within curly brackets.  Hence:

.. math::

   North\ American\ Countries = \{Canada, United\ States\ of\ America, Mexico\}

A dataset is any set where each element is restricted to one data type and where each element belongs to the same universal set.

------------------
Relational Dataset
------------------

A relational dataset is a collection of sets where:
  1. The number of objects (elements) in each set is the same.
  2. A one to one relationship exists between elements of different sets.

An example relational dataset showing the country name, country abbreviation and country population for the countries in North America is shown in :numref:`tableNA_Simple`.  This relational dataset comprises of the three sets: a set of country names; a set of abbreviations; and, a set of country populations.  A one to one relationship exists between the elements for each of these three sets.  Hence, the country with the name of *Canada* has a one to one relationship with the country abbreviation *CAN* and the country population *3563000*.

.. _tableNA_Simple:

.. table:: Example of a dataset of Countries in North America.
   :widths: auto

   +--------------------------+-----------------------+-------------+
   || Country Name            || Abbreviation         || Population |
   || (letters and spaces)    || (upper case letters) || (integer)  |
   +==========================+=======================+=============+
   | Canada                   | CAN                   |  3563000    |
   +--------------------------+-----------------------+-------------+
   | United States of America | USA                   |  32663000   |
   +--------------------------+-----------------------+-------------+
   | Mexico                   | MEX                   |  12458000   |
   +--------------------------+-----------------------+-------------+

Essential to any set is a definition or description of what type of objects can be a member.  For example, an apple which is a valid type of the set of fruit can't be a member of a set of countries.  For any dataset, both the data type and additional constraints are often used together define the universal set.  For example, the data type for *Country Name* in :numref:`tableNA_Simple` is any combination of letters and spaces, whilst the data type for *Abbreviation* is any combination of 3 upper case letters.

Although a *relational dataset* consists of multiple sets of data where the elements of each set are related, it is ubiquitously referred to as a **dataset**.

------------------
Geospatial Dataset
------------------
A geospatial dataset refers to any dataset where one or more of the composite sets refer to a location on the earth's surface.  This project is only concerned with those geospatial datasets where the location on the earth's surface is represented by one or more points, lines or polygons that are located by coordinates and stored as vectors.  These points, lines and polygons are collectively referred to as shapes or geometries [#f5]_.  Datasets that include one or more sets of geospatial vectors are referred to as *Vector Datasets* by the GIS community.

A vector geospatial dataset is a subtype of geospatial dataset where the geospatial sets can be located graphically on the earths surface by the application of coordinates.  This project is only concerned with vector geospatial datasets.

===================
Geometry data types
===================
All datasets contain some restriction on the type of data each constituent set may contain.  From a software perspective, a restriction of type is essential for minimizing both the storage size of the dataset and the response time for a dataset query.  Analagous to specific data types for storage of numbers, text or dates there is one or more data types specifically used for the storage of geospatial geometries.  Similarly, just as there are often specific data types of signed and unsigned integers, float, and, decimal numbers there are also specific data types for different types of geometries, with the type often referring to how the geometry is constructed.

For any dataset software the geometry data types that are availabe for use can be shown schematically as a hierarchy like the one shown in :numref:`figureGeomTypeI`.  Within this hierarchy, the possible data types are described by the labels in the boxes.  Essential to all such hierarchy's, a set of data of a declared type may consist of any type below it on the hierarchy.  Hence, if a set of data has a declared type of *Geometry Collection* then any data element within it may consist of *Geometry Collection*, *Multi-Point*, "Multi-Curve*, *Multi-Line*, *Multi-Surface*, and, *Multi-Polygon*.  Similarly, if a set of data has a declared type of *Point* than it may not contain a *Polygon* nor a *Line*.

The single part constrained geometry subtypes in the lower part of :numref:`figureGeomTypeI` are referred to as *Primitive Types* and must contain only one single part geometry per set element.  In contrast, the Multiple Part geometries may consist of one *or* many parts per feature.  For example, a feature of the *"Multi-Point"* geometry sub type may have one point, no points or multiple points. Another characteristic of the single part primitive types is that the *Line* and *Polygon* subtypes may only exist of straight line segments between coordinates.


.. _figureGeomTypeI:

.. figure:: _static/geomTypeSQL.png
   :scale: 80%
   :align: center

   GIS Geometry subtype hierarchy.  Adapted from :cite:`ISO19125-2`.  The more conventional term *"LineString"* that is used in the QGIS API and :cite:`ISO19125-2` is replaced here with *"Line"* for clarity.

In reality there may be many more geometry subtypes than the simplified hierarchy shown in :numref:`figureGeomTypeI`.  For example, some common additional subtypes for datasets are created for sets of geometries that incorporate elevation data, or, for lines that are constructed from curves as opposed to straight line segments.

Many GIS data format standards, and, many GIS software have a geometry subtype hierarchy that is **similar** with :numref:`figureGeomTypeI`.  Within a GIS dataset, geometry objects there are several geometry subtypes, with the main ones without elevation are shown in :numref:`figureGeomTypeI`.  Schematically, this hierarchy of geometry subtypes is replicated by the `inheritance diagram for QgsAbstractGeometry <https://qgis.org/api/classQgsAbstractGeometry.html>`_ :cite:`QGSAbstractGeometry`.

====================
Geometry data values
====================

For any data type there exists a universal set of valid values.  For example, a set of birthday dates must be restricted to valid dates.  For example, a birthday on the 30th of February is not valid as the 30th of February is not part of the universal set of dates.  Similarly, a valid geometry needs to be located within the boundaries of the coordinate system that it is referenced to.  **Empty** and **null** are two values that may be part of any set of data and could be fairly described as being:

1. Controversial
2. Miss-understood
3. Best avoided

-----
Empty
-----
A box of apples can be described as a set of apples.  A empty Apple box is an empty set of apples.  An empty geometry element is a geometry that has no coordinates.  Whether an empty element is a valid member of a set depends on the context.  For example, if a study of chickens hatching from eggs recorded the date that each chicken hatches for a set of 10 eggs than the hatch date element is of the hatch date set is empty before the chicken hatches.  It is *known* that the chicken has not hatched.

All empty sets including an empty geometry value are place holders for when it is *known* that an element does not exist :cite:`OGC2010`.  For example, consider the intersection of the Blue Crosses and the Red Circles with the two squares shown in :numref:`figureSquarePoint`.  Both of the Blue Crosses B1 and B2 intersect the Left square, and, the Blue Cross B3 intersects the Right square.  The intersections of the Squares and Blue Crosses, and the Squares with Red Circles are summarized by the datasets shown in :numref:`tableIIIA` and :numref:`tableIIIB`.  As shown in  :numref:`tableIIIA` the *Left Square* intersects with the *Blue Crosses* *B1* and *B2* which are represented as a subset *{B1, B2}*.  Similarly, it is reported in :numref:`tableIIIB` that the *Left square* intersects the subset of *Red Circles* *{R1}*.  In contrast, also in :numref:`tableIIIB` it is shown that the *Left square* does not intersect with any *Red Circles* as shown by the empty set *{ }*.  Here the empty set *{ }* shows that it is known that no intersection occurs.  The reporting of those combinations where intersections are known to not occur as shown  :numref:`tableIIIB` follows the convention used by most SQL type relational databases for all set intersections regardless of whether they are geospatial or not.  In contrast, the convention for many GIS desktop software including QGIS and ArcGIS is to only show those combinations where intersections are known to occur (are True), hence, :numref:`tableIIIB` is reported as :numref:`tableIIIC` by QGIS.


.. _figureSquarePoint:

.. figure:: _static/squaresAndPoints.png
   :scale: 50%
   :align: center

   The location of blue crosses and red circles in the “Left Square” and the “Right Square”.

.. _tableIIIA:

.. table:: The intersection of the the *Squares* and the *Blue Crosses*.
   :widths: auto

   +--------------+--------------+
   | Square       | Blue Crosses |
   +==============+==============+
   | Left square  | {B1, B2}     |
   +--------------+--------------+
   | Right square | {B3}         |
   +--------------+--------------+


.. _tableIIIB:

.. table:: The intersection of the the *Squares* and the *Red Circles*.
   :widths: auto

   +--------------+--------------+
   | Square       | Red Circles  |
   +==============+==============+
   | Left square  | {R1}         |
   +--------------+--------------+
   | Right square | {  }         |
   +--------------+--------------+

.. _tableIIIC:

.. table:: The intersection of the the *Squares* and the *Red Circles* as shown by QGIS.
   :widths: auto

   +--------------+--------------+
   | Square       | Red Circles  |
   +==============+==============+
   | Left square  | {R1}         |
   +--------------+--------------+


The real utility of empty geometry values is realised when the intersection of all the squares and both types of points (*Red Circles* and *Blue Crosses*) are collated in one dataset as shown in :numref:`tableIII` as opposed to  :numref:`tableIIID`.  By using the empty set *{ }* as a place holder for the known non-intersection of *Red Circles* with the *Right square* the sets of *Blue Crosses* and *Red Circles* are maintained as seperate columns.  Although this approach is efficient and intuitive it is not suitable when there is a large number of point types as the number of columns has a linear relationship to the numbs of points.


.. _tableIII:

.. table:: The intersection of all point types and the squares.  Note that the sets each point type are still maintained as individual columns.  This approach is not feasible for a large number of point types as there would be too many columns.
   :widths: auto

   +--------------+----------------------------+
   | Square       | Point type                 |
   +              +--------------+-------------+
   |              | Blue Crosses | Red Circles |
   +==============+==============+=============+
   | Left square  | {B1, B2}     | {R1}        |
   +--------------+--------------+-------------+
   | Right square | {B3}         | { }         |
   +--------------+--------------+-------------+


.. _tableIIID:

.. table:: The intersection of all point types and the squares.
   :widths: auto

   +--------------+--------------+----------+
   | Square       | Point type   | Geometry |
   +==============+==============+==========+
   | Left square  | Blue Crosses | {B1, B2} |
   +--------------+--------------+----------+
   | Right square | Blue Crosses | {B3}     |
   +--------------+--------------+----------+
   | Left square  | Red Circles  | {R1}     |
   +--------------+--------------+----------+

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Datasets with multiple geometry sets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Much of the GIS community work with the restriction of a single geometry set for each dataset (a single geometry column within a table).  It is difficult to have multiple geometry attributes without also allowing empty geometry attributes.  Next, I will examine the advantages and disadvantages of multiple geometry attributes.

The fundamental advantage of multiple geometry attributes is they facilitate topology. Topology refers to how the constituent parts of a system are interrelated or arranged.  The location of points within squares shown schematically in :numref:`figureSquarePoint` is an example of topology as it shows how the points are related to squares.  :numref:`tableIII` shows the topological association of point type by square type, but, uses two geometry columns to do so.  :numref:`tableV` shows the same data as :numref:`tableIII` using only one geometry column.  Examination of :numref:`tableV` reveals that the relationship between a type of point (e.g. Blue Crosses) and the Square type (e.g. Left Square or Right Square) has to be reported as two separate relationships (two separate records) and a user is left with the task of mentally connecting these two relationships.  Clearly, without using multiple geometry columns showing topological relationships is less intuitive.

.. _tableV:

.. table:: Another way to represent the data in :numref:`tableIII` that uses only one geometry column.
   :widths: auto

   +--------------+----------------------------------+
   | Square       | Point type                       |
   +==============+==================================+
   | Left square  | Blue crosses :math:`\{B1,\ B2\}` |
   +--------------+----------------------------------+
   + Left square  | Red circles :math:`\{R1\}`       |
   +--------------+----------------------------------+
   | Right square | Blue crosses :math:`\{B3\}`      |
   +--------------+----------------------------------+
   + Red circles  | red circles :math:`\{Empty\}`    |
   +--------------+----------------------------------+


The major disadvantage of multiple geometry columns is that they are not supported by many pieces of GIS software or GIS file formats.  For example, ArcGIS does not support multiple geometry columns in any capacity, QGIS treats each geometry column as an unrelated dataset, and, the ubiquitous shapefile can only contain one geometry column.  So, by adopting multiple geometry columns you are isolating yourself from a large portion of the GIS community.

----
null
----
**null** is the most common value (element) recorded many disciplines and software formats for *unknown* data values [#f6]_.  For example, if a study of chickens hatching from eggs recorded the hatch date of each chicken hatching for a set of 10 eggs than the hatch date element of the hatch date set is *null* (unknown) if the hatch date was not recorded.  Strictly speaking a *null* hatch date can be any value from the universal set of hath dates including *Empty* allowing for eggs that never hatched.

The most useful feature of *null* values is that they enable incomplete datasets.  For example, consider the Blue Crosses dataset shown in :numref:`tableIIIE` where the coordinates for B4 are unknown. Datasets like :numref:`tableIIIE` can stem from requests to georeference existing datasets where the georeferencing is incomplete.

.. _tableIIIE:

.. table:: The age, size and coordinates for the Blue Crosses.
   :widths: auto

   +------------+-------------+-------+-------------+
   | Blue Cross | Age (years) | Size  | Coordinates |
   +============+=============+=======+=============+
   | B1         | 2           | Big   | (1, 1)      |
   +------------+-------------+-------+-------------+
   | B2         | 2           | Small | (2, 2)      |
   +------------+-------------+-------+-------------+
   | B3         | 3           | Small | (4, 2)      |
   +------------+-------------+-------+-------------+
   | B4         | 8           | Big   | *null*      |
   +------------+-------------+-------+-------------+

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using joins to eliminate null
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many GIS datasets do not allow *null* geometries.  Having a dataset constraint that prevents *null* geometries does not imply that the geometries are all known, it only means that the dataset can't have a *null* geometry.  The prevention of *null* geometries without knowing all of the geometries is achieved by using multiple datasets that include a geometry only dataset that has a relationship with a non-geometry dataset as shown in :numref:`figureJoinedCrosses`.  The relationship is typically achieved by the use of a **key** that is used in all related datasets to distinguish each relationship across the datasets.  Joins refer the process of forming a new dataset from multiple datasets by the use of a relationship.  The dataset shown in :numref:`tableIIIE` can be created from the datasets shown in :numref:`figureJoinedCrosses` by application of an *outer join*.

.. _figureJoinedCrosses:

.. figure:: _static/CrossesWithoutNull.png
   :scale: 70%
   :align: center

   :numref:`tableIIIE` presented as two separate datasets where *null* *Coordinates* data values are not permitted.  The *Blue Crosses* key is used to register relationships between the two datasets that is symbolised by the grey dashed lines.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Reasons for preventing null geometries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The reasons for preventing null geometries include: it's keeps GIS feature creation simple: one can't map *null*; they permit the geometry value to be a variable; and, it keeps logic based algorithms simple.

For QGIS and many desktop GIS systems, records are created by drawing the geometry and subsequently entering the other data values.  This geospatial geometry centered approach intuitively keeps the related computer programming simple in comparison to any approach that allows a user to enter any of the data values including the geometry in the sequence that they choose.

There is no accepted universal approach to mapping a *null* geometry.  It is obvious that if a geometry is *null* then using a defined symbol at a single location is a miss-representation.  There is active research into approaches for mapping the unknown.

The use of a geometry specific dataset enables geometry to be a variable.  For example, take the Blue Cross B1.  This Blue Cross may represent a boat in a sea.  Hence, at different points in time, B1 may have different coordinates (:numref:`tableIIIF`).  Most geospatial datasets have geometries that are variable as our technology for recording and knowing location is improving.  For example, an allotment of land may be static as it is relative to reference points, but, the mapped location and hence the recorded geometry for the allotment of land will change as the location of the reference points is refined to a higher accuracy.  Whether a dataset owner should track changes to a geometry is a question that is beyond the scope of this discussion.

.. _tableIIIF:

.. table:: The coordinates of the Blue Crosses for yesterday and today.
   :widths: auto

   +------------+----------------------+
   | Blue Cross | Coordinates          |
   +            +-----------+----------+
   |            | Yesterday | Today    |
   +============+===========+==========+
   | B1         | (1, 1)    | (2, 2)   |
   +------------+-----------+----------+
   | B2         | (2, 2)    | (1, 2)   |
   +------------+-----------+----------+
   | B3         | (4, 2)    | (4, 1)   |
   +------------+-----------+----------+

Whether a dataset allows *null* values or not directly affects the type of logic applied to the dataset for set operations.  Boolean logic, also referred to as two value logic, allows only for True or False answers to set operations.  Boolean logic has can't be applied when the answer is unknown.  When *null* values are permitted, three value logic is required for set operations.  The intersection of the squares with the two subsets of blue crosses {B1, B2, B3} and {B1, B2, B3, B4} that are described in :numref:`tableIIIE` is shown in :numref:`tableIIIG`.  For {B1, B2} it is True that they intersect the Left square, whilst it is also True that {B3} does not intersect the same square, however, it is null (unknown) whether {B4} intersects the Left Square.  Compounding the implementation of Three value logic is the fact that different database platforms implement three value logic differently leading to widespread avoidance of three value logic regardless of whether the data type is geometry or something more generic like an integer.  In summary, even when *null* values are permitted in datasets, the records associated with them are typically excluded from set operations.

.. _tableIIIG:

.. table:: The intersection of the squares with the subsets {B1, B2, B3} and {B1, B2, B3, and B4} as shown in :numref:`tableIIIE`.
   :widths: auto

   +--------------+-----------------------------------+
   | Square       | Intersection with the subset      |
   +              +---------------+-------------------+
   |              | {B1, B2, B3}  | {B1, B2, B3, B4}  |
   +              +---------------+-------------------+
   |              | Boolean logic | Three value logic |
   +==============+===============+===================+
   | Left square  | {B1, B2}      | {B1, B2, null-B4} |
   +--------------+---------------+-------------------+
   | Right square | {B3}          | {B3, null-B4}     |
   +--------------+---------------+-------------------+



Although beyond the scope of this project, it is noted that although Boolean logic is applied the same in the majority of relational databases there is known diversity in the application for three value logic.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Reasons for allowing null geometries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Although the majority of GIS systems do not promote the use of null geometry data values, there are several reasons why they should be adopted: they force the adoption of geospatial datasets by enterprise databases; they illuminate the unknown; and, they facilitate a simpler dataset structure.

The forced adoption of geospatial datasets by enterprise databases is the most compelling reason to adopt null geometry values.  For example, consider a commercial database used for rates at a local government.  The current approach of most databases for rates is to mimic :numref:`figureJoinedCrosses` where the tables for the land registry are maintained within a land registry database, and, the tables for the georeferenced land allotments are in a GIS database and these databases are joined.  This approach facilitates bureaucracies where separate teams of people maintain each database, and, where the land registry database does not adopt spatial functionality as the data is located in a separate database.  Whilst using a separate GIS database allows the local government to develop a custom GIS system, it comes at a cost of minimal inbuilt spatial capability.

Allowing *null* has the potential to expose the unknown.  By exposing the unknown, it it is evident where further data capture is required, and, it is more likely that any spatial analysis will also establish the degree of dataset completeness.

A disadvantage of the lookup table approach is the requirement for the documentation of database schema for users to maintain the lookup key and to perform database queries that include spatial and non-spatial attributes.  Without lookup tables the database structure is simpler leading to fewer errors and fewer joins when constructing queries.

===================================
Parsing data by QGIS data Providers
===================================
QGIS parses data to and from many data formats without requiring importing or exporting to or from a common data format.  The intent of this data parsing is that a user may analyse data stored in different formats with a common user interface.  A key component of any GIS record is a geospatial geometry data type which could be stored in an infinite number of ways.  Fortunately, there are international standards :cite:`ISO19125-2` that describe the geospatial geometry data type and subtypes, and, there is some consistency across most data formats.


Although different GIS data formats have **similar** geometry subtype hierarchy's, they are not the same.  For example, many different SQL databases that adopt elements of ISO19125-2 :cite:`ISO19125-2` including PostGis and MS SQL by default have a *Geometry* subtype [#f4]_. Consequently, without further constraints in their native environment one can choose any subtype shown in :numref:`figureGeomTypeI` for any record.  In comparison, the *Geometry* subtype equivalent in the QGIS data type inheritance diagram :cite:`QGSAbstractGeometry` has the title *"QgsAbstractGeometry"* where the *Abstract* keyword tell us that this datatype can't be created by itself, only it's children can be created.  To emphasize, parsing data for different data formats but maintaining a uniform user interface is a Pandora's box when the data types or subtypes have different hierarchy's of data subtypes.

With the understanding that different data formats have different geometry hierarchy's it is expected that QGIS needs to make adjustments on the fly. This parsing is silent and without experience errors may be introduced into datasets.

.. _tableMultiLine:

.. table:: Feature geometry changes when exporting a QGIS Multi-Line memory layer.
   :widths: auto

   ========== ============ ============ ============ ============ ============
   Original   Geopackage   Shapefile    Spatialite   PostGis      MS SQL
   ========== ============ ============ ============ ============ ============
   Multi-Line Multi-Line   Multi-Line   Multi-Line   Multi-Line   Multi-Line
   Line       *Multi-Line* *Multi-Line* *Multi-Line* Line         Line
   Empty      Empty        *null*       Empty        Empty        *null*
   *null*     Empty        *null*       Empty        *null*       *null*
   ========== ============ ============ ============ ============ ============


For several dataproviders including QGIS memory layer, PostGIS and MicroSoft SQL Server QGIS employs a subtype hierarchy shown by :numref:`figureGeomTypeII`.  Hence for some dataproviders, by default, QGIS creates a new one part line in a dataset of the *"Multi-Line"* subtype as a Line and not a *"Multi-Line"*.  The insertion of a *"Line"* geometry subtype into a *"Multi-Line"* geometry subtype dataset is readily demonstrated by python script using the QGIS API:

.. doctest::

   >>> from qgis.core import *
   >>> layerMulti=QgsVectorLayer('MultiLineString?crs=epsg:4326&field=ID:string', 'a', "memory")
   >>> providerMulti=layerMulti.dataProvider()
   >>> recordWrite = QgsFeature()
   >>> recordWrite.setAttributes(['1'])
   >>> recordWrite.setGeometry(QgsGeometry.fromWkt('LINESTRING (1 1, 6 1)'))
   >>> providerMulti.addFeature(recordWrite)
   True
   >>> recordRead = layerMulti.getFeature(1)
   >>> print(QgsWkbTypes.displayString(recordRead.geometry().wkbType()))
   LineString
   >>> print(QgsWkbTypes.displayString(layerMulti.dataProvider().wkbType()))
   MultiLineString

More worringly, as shown in the next python script, the reverse is also possible.  One may add a feature with a *Multi-Line* geometry sub-type to a *Line* dataset.

.. doctest::

   >>> from qgis.core import *
   >>> layerSingle=QgsVectorLayer('LineString?crs=epsg:4326&field=ID:string', 'b', "memory")
   >>> providerSingle = layerSingle.dataProvider()
   >>> recordWrite = QgsFeature()
   >>> recordWrite.setAttributes(['1'])
   >>> recordWrite.setGeometry(QgsGeometry.fromWkt('MULTILINESTRING ((1 1, 6 1))'))
   >>> providerSingle.addFeature(recordWrite)
   True
   >>> recordRead = layerSingle.getFeature(1)
   >>> print(QgsWkbTypes.displayString(recordRead.geometry().wkbType()))
   MultiLineString
   >>> print(QgsWkbTypes.displayString(layerSingle.dataProvider().wkbType()))
   LineString

Fortunately with QGIS you can't insert a *Point* into a *Line* dataset, or, otherwise mix geometry sub-types of different dimensionality.

.. doctest::

   >>> from qgis.core import *
   >>> layerSingle=QgsVectorLayer('LineString?crs=epsg:4326&field=ID:string', 'b', "memory")
   >>> providerSingle = layerSingle.dataProvider()
   >>> recordWrite = QgsFeature()
   >>> recordWrite.setAttributes(['1'])
   >>> recordWrite.setGeometry(QgsGeometry.fromWkt('POINT (1 1)'))
   >>> providerSingle.addFeature(recordWrite)
   False

.. _figureGeomTypeII:

.. figure:: _static/geomTypeQGIS.png
   :scale: 80%
   :align: center

   The Geometry subtype hierarchy employed by QGIS by default for several data providers.





QGIS mixes the primitive geometry types with the modern geometry types by default.  The data providers typically handle this well, but, the pre-scripted decisions can have consequences.

For example, by default QGIS will permit a user to add a Multi-line feature to a MicroSoft SQL database that only contains Line features.


===================================
GIS Centric And the Wall of Mystery
===================================


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Records with false Boolean logic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Many GIS software packages force the user to perform a selection whenever they perform a set operation like a union, intersection or difference.  The results of an intersection without a selection of the points and squares shown in :numref:`figureSquarePoint` includes those records that don’t intersect (:numref:`tableV`).  To achieve the more common output shown in :numref:`tableVI` a selection must be performed on the data to include only those records that do intersect.  Hence, the logic performed by most GIS software packages including ArcGIS and QGIS is: 1. Select those records where intersect is True; 2. Perform intersection.

.. _tableVI:

.. table:: Another way to represent the data in 5 where records where no intersection occurs are also shown.
   :widths: auto

   +--------------+----------------------------------+
   | Square       | Point type                       |
   +==============+==================================+
   | Left square  | Blue crosses :math:`\{P1,\ P2\}` |
   +--------------+----------------------------------+
   + Left square  | Red circles :math:`\{P3\}`       |
   +--------------+----------------------------------+
   | Right square | Blue crosses :math:`\{P4\}`      |
   +--------------+----------------------------------+



Being forced to do a selection in addition to an intersection is an algorithmic solution that eliminates the need for empty geometry values.  Forcing a selection as part of a set operation introduces the assumption that records missing from the results are empty (e.g. do not intersect) and hence prohibits the ability to also record unknown (*null*) set operations.  Another problem of forced selection is that problem solving of erroneous set operations is hindered as one needs to undertake additional steps to confirm those records that were explicitly excluded by the forced selection.  For logic and critical thinking analysing the negative results can be more fruitful than analysing the positive results!

====
QGIS
====
QGIS is self-promoted as an “Open Source Geographic Information System” :cite:`QGIS`.  QGIS is used for creating, manipulating and publishing spatial data sets by many organisations.  Some organisations use QGIS to edit or create geometries for geospatial datasets within enterprise databases in their native format as no commercial software has this capability.  For example, `SMEC Pavement Management Software <http://www.smec.com/en_au/what-we-do/sectors/transport/pavement-management-systems>`_ uses a Microsoft SQL database to contain it’s pavement datasets.  QGIS can browse and edit the geometries contained within this dataset without importing or exporting any dataset.   In comparison, software like ArcMap requires a user to import, edit, then export the data to the SMEC Pavement Management Software even though both installation could have their data respective datasets within the same Microsoft SQL Server installation, and, both datasets are using the same datatype for the geometry values.
By intentional design and function, the majority of QGIS users use other software packages or software formats developed by other organisations to store geospatial datasets.  For example, the PostGIS, MS SQL and SpatiaLite databases, and, the esri shapefile format are all processed in their native format by QGIS.

------------
QGIS history
------------
QGIS was created by Gary Sherman in 2002 :cite:`QgisContributors,GarySherman2011`.  In 2007 it became a project of the Open Source Geospatial Foundation with version 1 being released in January 2009 :cite:`QgisContributors`.  The version of QGIS used in this project, Version 3, was released in February 2018 :cite:`QgisContributors`.  Version 2 of QGIS employed Python 2 for scripting and PyQT4 for the graphical user interface (GUI).  Version 3 of QGIS employs Python 3 for scripting and PyQT5 for the GUI.  QGIS version 3 is self-described as a “huge overhaul and cleanup” of QGIS version 2 :cite:`QgisChangelogV3`.  Many of the python scripts configured for version 2 no longer work with version 3 with much of the legacy sub-version support dropped.

---------------------------
Vector datasets within QGIS
---------------------------
Within QGIS, the geometries for each record are contained within instances of QgsAbstractGeometry subclasses :cite:`QGSGeometryClass`.  The manner in which QGIS stores empty geometries is not inherited from the QgsAbstractGeometry superclass, but rather is determined for each subclass separately.  Although QGIS is capable to parse empty geometries for the majority of the QgsAbstractGeometry subclass there may be some that are unable to do so.

The variations in how QgsAbstractGeometry subclasses contain empty geometries is demonstrated in the following section by example.  Using the QGIS API, empty geometries for several geometry types can be instantiated by instantiating the relevant QgsAbstractGeometry subclass without a set of vertices.  For example, to test that a ``QgsLineString()`` is empty:

.. doctest::

   >>> from qgis.core import QgsLineString
   >>> QgsLineString().isEmpty()
   True


Although empty geometries can be created for most geometry types with the QGIS API by instantiation without a set of vertices, it is not currently possible to instantiate an empty point geometry (:numref:`tableVII`). As demonstated below, the well known text representation of the call to instantiate an empty point reveals that QGIS is wrongly adding a vertex with the coordinates of :math:`(0\ 0)` :cite:`QgsPointBugReport2018` [#f1]_.


.. doctest::

   >>> from qgis.core import QgsLineString,QgsPoint
   >>> print(QgsLineString().asWkt())
   LineString ()
   >>> print(QgsPoint().asWkt())
   Point (0 0)
   >>> print(QgsPoint().createEmptyWithSameType().asWkt())
   Point (nan nan)


.. _tableVII:

.. table:: Testing whether an empty geometry has been created by the instantiation of various types of QgsAbstractGeometry subclasses using the python Console in QGIS 3.0.3.
   :widths: auto

   +---------------------------------------+-----------+
   | Input                                 | Output    |
   +=======================================+===========+
   | ``QgsPoint().isEmpty()``              | ``False`` |
   +---------------------------------------+-----------+
   | ``QgsLineString().isEmpty()``         | ``True``  |
   +---------------------------------------+-----------+
   | ``QgsPolygon().isEmpty()``            | ``True``  |
   +---------------------------------------+-----------+
   | ``QgsGeometryCollection().isEmpty()`` | ``True``  |
   +---------------------------------------+-----------+

******************
PROBLEM DEFINITION
******************
The problems that this project intends to address are:

1.	Null and empty shapes are parsed differently by different data providers in QGIS.
2.	Within QGIS, there is no published plugin or output that shows records within a dataset that have null or empty geometry values.
3.	Many GIS professionals do not anticipate or are aware of datasets that have null or empty geometries.
4.	Empty geometry values were not included in the set of valid values in the original QGIS or GDAL specifications.

=======================================================================
PARSING OF NULL AND EMPTY SHAPES TO AND FROM EXTERNAL DATABASES BY QGIS
=======================================================================
Using source specific data providers, QGIS processes data to and from third party databases without requiring constraints or additional tables in the third-party database.  Each data provider has been created independently and these do treat the same data values differently.  For example, as expected QGIS parses empty linestrings from PostGis databases as not null but it incorrectly parses empty linestrings from Microsoft SQL Server as null :cite:`ParseEmptyFromSql`.

-------------------
QGIS Data Providers
-------------------
A component of software that allows it to directly read data without conversion to a different data type, and, to write updates or new records to a dataset without exporting is called a data provider.   QGIS contains data providers for 18 different formats for which it can read from or write to in their native format :cite:`QGSProviders2018`.  Being open source, each of the data QGIS providers were created at different times for different purposes, are founded on different philosophies and have different levels of development.  Consequently, even when different database packages follow the same geospatial standards, equivalent shapes from those different database packages may be read as different shapes due to variations or errors between data providers.

Within this project it is anticipated that errors passing empty or null values from Microsoft SQL Server or PostGIS will be found.  Unfortunately, the C++ classes employed in the data type specific data providers :cite:`QGSProviders2018` are not exposed in the QGIS API which means that their function is not easily modified.

QGIS’s data providers that allow it to read or write in native format without need for additional constraints or data tables is a key feature that makes it popular in large organisations. By reading and writing in the native format, QGIS can edit or create geospatial data within an enterprise database that is configured for another piece of software and without importing and exporting.  In doing so QGIS has removed one of the barriers to integration of geospatial data within enterprise datasets.

In comparison to QGIS’s approach of editing the data in it’s native format, ESRI’s ArcMap requires a user to import into a geodatabase and undertake the editing there– even though the enterprise database and the geodatabase may be using the same database server :cite:`ArcGISTutorialForEmpty`.  ESRI’s approach often leads to a lookup table being used for geospatial data and then scripts run on those lookup tables to publish an integrated dataset.

===============================================
EXPOSURE OF NULL AND EMPTY SHAPE VALUES IN QGIS
===============================================
Within QGIS, without using custom expressions or scripts there is only limited exposure to null shapes, and, empty shapes.  Two locations within QGIS where you may find descriptive information of each record are the *“Attribute Table”* and the *“DB Manager”* plugin.

Without using expressions and creating new attributes, the “Attribute Table” does not contain any information about the record’s shapes.  The only component of the “Attribute Table” that exposes empty or null geometries is when a user selects “Zoom to Feature” for a specific record.  In QGIS version 3.x, a warning message is shown on the map canvas that the shape is empty or doesn’t exist depending on whether the shape is empty or *null* (:numref:`figureIII`).


.. _figureIII:

.. figure:: _static/FigureII.png
   :align: center

   A warning message is displayed in QGIS when a user attempts to zoom to a record with an empty geometry.

The DB Manager in QGIS 3.x is a core plugin (it can’t be uninstalled).  The DB Manager plugin provides database specific information for data from a limited number of databases that includes PostGIS, but, excludes Microsoft SQL Server.  The Table view within DB Manager shows all of the columns within the table including the geometry attribute.  For the geometry column it gives the geometry type and exposes null shapes as *“NULL”* (:numref:`figureIV`).


.. _figureIV:

.. figure:: _static/FigureIII.png
   :align: center

   The output from the DB Manager plugin in QGIS 3.x for a dataset that contains both empty geometry values and null geometry values.


==========================
GIS PROFESSIONAL AWARENESS
==========================
Many GIS professionals are educated and work within GIS dataset schema where both null and empty geometries are excluded.  It is plausible that GIS professionals that are not familiar with null and empty shapes are ignorant of them when using a GIS where they are permitted.  This is a situation that confronted the proponent of this project.  Examples of wrong understanding of null and empty geometry values are widespread on the world wide web.  For example, an article published by esri incorrectly states that an empty geometry exists for any geometry where the coordinates are unknown :cite:`ESRINullOracle`.

Micosoft SQL and PostGis both permit null and empty geometry values unless explicitly excluded by constraints or third party software.  Even when a primary dataset contains no null or empty geometry values, processing of that dataset may produce empty null or empty geometry values.  Performing set operations like intersections within the database, and, editing geometry of specific records within QGIS are two ways empty geometry values can be created.

----------------------------------------------------------------------------
Set operations in Microsoft SQL or PostGIS can produce empty geometry values
----------------------------------------------------------------------------
There are several fundamental set operations that are used to construct new sets from existing sets regardless to what it is a set of :cite:`SetTheoryOverall`.  Within a database, a set operation needs to be consistent for all data types.  As introduced in section :ref:`Records with false Boolean logic` some databases generate empty geometry values for set operations.  Microsoft SQL Server and PostGis are examples of databases that can generate empty geometry values for set operations.  Both of these databases developed from SQL conventions and their generation of empty values for geometries is consistent with set operations for other data types.

Intersection of two sets is an example of a set operation.  Intersect refers to those locations where two or more objects meet, cross or cover each other :cite:`IntersectDefinition`.  Many different fields that employ set theory, Intersect of two datasets returns all records that exist in both datasets (:numref:`figureV`).  The intersect concept can be applied to many datatypes including characters, numbers, dates, and, geometries.


.. _figureV:

.. figure:: _static/FigureIV.png
   :align: center

   The schematic intersection of Set 1 and Set 2 is purple.

Consider the intersection of the points ‘Pt1’ and ‘Pt2’ with the circle shown in :numref:`figureVI` which is an example of an intersection between two geometry datasets.  ‘Pt 1’ lies within the circle, and, hence intersects the circle.  ‘Pt2’ lies outside the circle and does not.  In both QGIS v3.x and ArcGIS desktop, the intersection of a points dataset containing ‘Pt1’ and ‘Pt2’ and a dataset containing the circle will return only those records that intersect, hence, only ‘Pt1’ is returned.  In contrast, in Microsoft SQL Server, the intersection returns both the records that do and don’t intersect with a dataset containing both ‘Pt1’ and ‘Pt2’.


.. _figureVI:

.. figure:: _static/FigureV.png
   :align: center

   A schematic of the intersection of points ‘Pt1’ and ‘Pt2’ with a circle.


There is no error with either the approach to intersection taken by QGIS 3.x and Microsoft SQL Server.  As described in the section :ref:`Records with false Boolean logic` QGIS 3.x includes an addition selection logic step that removes those records that don’t intersect.  For ‘Pt2’, Microsoft SQL server is returning an empty geometry confirming that no intersection exists, as shown by the following Transact-SQL script [#f2]_::

   DECLARE @circle geometry = 'CURVEPOLYGON (CIRCULARSTRING (0 1, 1 2, 2 1, 1 0, 0 1))';
   DECLARE @Pt2 geometry = 'POINT (3 1)';
   SELECT @Pt2.STIntersection(@circle).ToString();
   GEOMETRYCOLLECTION EMPTY

This intersection example shows the ease with which one can inadvertently generate empty geometry values in Microsoft SQL Server, and, these empty geometry values will be passed to QGIS.

---------------------------------------------------
Inadvertently Creating Empty Geometries within QGIS
---------------------------------------------------
Within QGIS, an empty geometry is created by using the “Vertex Tool” to delete all vertices of an existing shape.  A user unfamiliar with QGIS may incorrectly assume that deleting all the vertices of a shape also deletes the record.  Hence, when editing a shape, a QGIS user may unintentionally create an empty shape when they are attempting to delete the shape.

==================================================================
Retrospective incorporation of empty and null values into Software
==================================================================
The Geospatial Data Abstraction Library (GDAL) is ubiquitous within most GIS Software to translate and process geospatial data.  Handles for empty shapes were not part of the original GDAL specification, with empty shapes being treated as null.   The retrospective incorporation of empty handles into GDAL has not been picked up by many applications that employ GDAL, and, even within GDAL there are many processing tools that do not allow for empty shapes.

Many of the current GDAL set operators continue to convert empty geometry values to null geometry values even when the set being operated on has successfully implemented the empty shape handle on passing to GDAL.  For example, for the Intersection operation the output is *“a new geometry representing the intersection or NULL if there is no intersection or an error occurs”* :cite:`GDALIntersection`.  Curiously, the same GDAL geometry class has a handle to assign an empty geometry, or, to test for an empty geometry :cite:`GDALEmpty`.  On another GDAL ticket register it is stated *“GML/WFS: by default does not advertise NOT NULL fields since we treat empty strings as being null for historical reasons. By setting the open option EMPTY_AS_NULL=NO, empty strings will be reported as such and NOT NULL fields might be advertised”* :cite:`Rouault2015`, it is clear that GDAL is not originally intended to distinguish between null and empty.

The retrospective addition of handles for empty geometry values in GDAL was mimicked by QGIS.  Consequently, within QGIS there are likely to many set operators that convert empty values to null values as part of the set operation.

----------------------------------------------------------
The definition of Null and Empty Values depends on context
----------------------------------------------------------
The definition of Empty geometry values introduced in section 2.2 it was articulated that an Empty geometry is just one valid value in the set of valid values for the geometry data type.  In contrast, null indicates that the geometry value is unknown and that the value can be any value from the set of valid values. Hence, an empty geometry values is one of many possible values for a null geometry (or, empty is a subclass of null).  For example, for a point, the vertices of an empty point are :math:`\{\ \ \}` as it has no coordinates, and, the vertices of a null point are :math:`\{x,y\}` where :math:`x` and :math:`y` are both variables designating unknown coordinates. These definitions are consistent with SQL relational databases.  Unfortunately, the definition of null used by SQL relational databases is different to that used by both mathematics for set theory, and, but most computer programming languages :cite:`WhatIsNull`.

Let’s consider the definition of null for set theory and computer programming using a common example.  If one has a box of apples and a box of bananas, then the intersection of the two boxes of fruit is an empty box. For set theory, *null* – nothing is what you have when you take away the box.

Similar to set theory, for most object-oriented computer programming languages, an object that has not been instantiated is *null*.  Hence, a pointer to something that doesn’t exist is null. An empty object is an object that has been instantiated but not populated, for example, a list with no members, or, a box with no fruit.

So, from the perspective of an object-oriented computer programming language, null means no value.  Hence, a null object is an object that does not exist, or, occupies no space in a computer’s memory.  Indeed, SQL relational databases implement null as an object that doesn’t exist, so, the context difference between unknown and nothing does not have to create conflict.

The underlying conflict is based on logical deduction.  It has been proved that an empty set is a subset of any set.  It is argued that on object that doesn’t exist can’t contain anything, so, it must be empty [#f3]_.  Hence, *null* is a subclass of empty.  However, an empty set is a still a set, a container that is empty.  In contrast, null states that no container exists.  So, by arguing that a *null* object is empty you have just created an object.  A *null* object neither contains anything nor has a container.

Unfortunately, QGIS employs the logic that a null geometry is also an empty geometry :cite:`QGSGeometrySource2018`.    The QGIS test for null simply asks where there the object point points to anything :cite:`QGSGeometrySource2018`::

  144 bool QgsGeometry::isNull() const
  145 {
  146  return !d->geometry;
  147 }


Now, the QGIS test for empty performs the same test as for null, and, returns true if the test for null returns true :cite:`QGSGeometrySource2018`::

  329 bool QgsGeometry::isEmpty() const
  330 {
  331  if ( !d->geometry )
  332  {
  333  return true;
  334  }
  335
  336  return d->geometry->isEmpty();
  337 }





.. [#f1] a ``Point (nan nan)`` is also reported when an empty PostGis point is parsed by QGIS.

.. [#f2] In both Microsoft SQL and PostGis the geometry type that is empty is recorded :cite:`Loskot2010,Ramsey2010`).  Sometimes the geometry type gets changed to the generic ‘GEOMETRYCOLLECTION’ by set operations.

.. [#f3] Unable to find a high quality reference for this argument.  Several private conversations with C++ programers reveal that this logic is common and is frequently used to test for empty in C++.

.. [#f4] In many QSL databases the hierarchy separates all geometry types that employ cartesian coordinates from those that employ geographic coordinates.

.. [#f5] For SQL relational databases, the term geometry is restricted to those shapes that are located by cartesian coordinates.

.. [#f6] Python uses *None* instead of *null*, but, PyQT uses *NULL* as a QVariant, so, PyQGIS script may have a mixture of *None* and *NULL* depending on the origin of the classes in use.

******************
Future Development
******************

Some ideas for improvement:

   1. Add a summary table
   2. Add a column for number of parts
   3. Distinguish curved shapes
   4. Distinguish shapes with elevation information


************
Bibliography
************

.. bibliography:: NullFeaturesInQGIS.bib
   :style: plain


