****************************************
QGIS Data Provider Data Parsing Problems
****************************************

The parsing of datasets by QGIS data providers is silent and can change both geometry sub-type and the geometry data values of *null* and *Empty* (:numref:`tableMultiLine`).

Changes of geometry sub-type may be required because the data source doesn't support the mixing of specific sub-types, or, because the source sub-type may not be supported at all.  For example, in :numref:`tableMultiLine`, neither Geopackage nor Spatialite permit the mixing of *Line* and *Multi-Line* subtypes, so, the data provider defaults to the *Multi-Line* subtype for the creation of a new dataset, and, all records with a *Line* subtype are changed to a *Multi-Line* subtype.  In an another example, Shapefile does not support the *Line* subtype at all, with all records with a *Line* subtype changed to a *PolyLine* [#f2]_.

For geometry data vales of *null* and *empty*, values are changed as the data source does not permit both types, or, because the data provider contains errors.  In :numref:`tableMultiLine` it is shown that with the exception of the PostGis format, either the parsing of the known geometry data value of *empty* is changed to the unknown value of *null*, or, visa versa.  The replacement of known with unknown, or unknown with known can cause erroneous analysis and interpretation.  Without experience errors may be introduced into datasets by the parsing of data by QGIS's data providers.

.. _tableMultiLine:

.. table:: Appending of non-empty single part multi-line, non-empty line, empty line and *null* geometry records by QGIS to 5 popular data sources.
   :widths: auto
   :align: center

   =========== ============== ============ ================= =============== ==============
   QGIS memory Geopackage     Shapefile    Spatialite [#f9]_ PostGis [#f5]_  MS SQL [#f5]_
   =========== ============== ============ ================= =============== ==============
   Multi-Line  Multi-Line     Polyline     Multi-Line        Multi-Line      Multi-Line
   Line        **Multi-Line** **Polyline** **Multi-Line**    Line            Line
   *Empty*     *Empty*        **null**     *Empty*           *Empty*         **null**
   *null*      **Empty**      *null*       *Empty*           *null*          *null*
   =========== ============== ============ ================= =============== ==============

===========================
Parsing Geometry Data Types
===========================

The parsing of geometry records by the QGIS data providers often requires changing the geometry sub-type.  For example, consider the parsing of geometry subtypes between ESRI's Shapefile, QGIS, and, SpatiaLite (:numref:`figureShapeToQgis`).  SpatiaLite and Shapefiles have a single geometry sub-type defined for a dataset [#f8]_ which is simpler than data sources like Microsoft SQL Server and PostGIS where the geometry sub-type can vary for each record.

The hierarchy for the ubiquitous Shapefile shown in :numref:`figureShapeHier` is vastly different to that for QGIS :cite:`QGSAbstractGeometry`.  For constructing a single part line, QGIS has the four geometry subtypes of *"Multi-Line"*, *"Circular-String"*, *"Compound-Curve"*, and, *"Line"*, whereas Shapefile only has the single subtype of *"PolyLine"* [#fi]_.  Hence, in a QGIS editing session, a user may create a line using any of QGIS's four line subtypes, but, the line will only be recorded as a *"PolyLine*" and it is the Provider's task to inform QGIS of this requirement (:numref:`figureShapeToQgis`).

In comparison to a Shapefile, SpatiaLite has the *Multi-Line* and *Line* sub-types and QGIS has to distinguish between these.  The manner in which QGIS distinguishes between a *Multi-Line* and a *Line* for parsing to SpatiaLite is primitive.  A single part QGIS *Multi-Line* can't be parsed to a SpatiaLite *Line* as the provider refers to the geometry type and not the number of parts, but, a "Line" will be converted to a *Multi-Line* by silently changing it's geometry type if it is parsed to a SpatiaLite *Mutli-Line* data source. In a similar manner, *Circular-String* and *Compound-Curve* sub-types will be converted to *Line* sub-types, and then *Multi-Line* sub-types if required.  Some of the geometry sub-type changing may confuse unwary users, for example, a SpatiaLite Line data source read by QGIS and saved as a SpatiaLite *Multi-Line* is silent and without error or warning, however, the newly created SpatiaLite *Multi-Line* can't be then saved as a SpatiaLite *Line* by QGIS without the use of a tool that changes the geometry type to *Line*, even though each *Multi-Line* only has one part.

Editing existing geometries or creating new geometries creates similar challenges for parsing geometry types.  Any geometry edit or creation has to occur on a QGIS geometry sub-type and then parsed to the data source.  In an edit process, QGIS will allow incompatible geometries to be created and it is only when the edited geometries are attempted to be committed to the data source that QGIS either throws an error or changes to a compatible geometry sub-type.

.. _figureShapeToQgis:

.. figure:: _static/SpataLiteToQgisToShapefile.png
   :scale: 70%
   :align: center

   The association of various geometry *Line* sub-types for SpatiaLite, QGIS and Shapefile: grey arrows refer to changes in geometry sub-type within QGIS prior to committing data; black arrows indicate data parsing between QGIS and the external data sources.


----------------------------------
Data Provider Geometry Type Errors
----------------------------------

There is a great diversity in both the refinement and development of each QGIS data provider.  As QGIS is opensource, the varying levels of refinement of different data providers may reflect communities of users or the commissioning of developers.  Given the complexity of the data providers task of parsing datasources to and from QGIS, it is not surprising that there are many unexpected errors originating from the data parsing process.

For example, for a *memory* data source, QGIS allows the mixing of primitive and multi-part geometries of the same dimensionality.  The insertion of a *Line* geometry subtype record into a *Multi-Line* geometry subtype for a QGIS *memory* data source is demonstrated by Python script using the QGIS API:

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

More worryingly, as shown in the next Python script, the reverse is also possible.  One may add a feature with a *Multi-Line* geometry sub-type into a *Line* QGIS memory dataset.

.. doctest::

   >>> from qgis.core import *
   >>> layerSingle=QgsVectorLayer('LineString?crs=epsg:4326&field=ID:string', 'b', "memory")
   >>> providerSingle = layerSingle.dataProvider()
   >>> recordWrite = QgsFeature()
   >>> recordWrite.setAttributes(['1'])
   >>> recordWrite.setGeometry(QgsGeometry.fromWkt('MULTILINESTRING ((1 1, 6 1), (1 2, 6 2))'))
   >>> providerSingle.addFeature(recordWrite)
   True
   >>> recordRead = layerSingle.getFeature(1)
   >>> print(QgsWkbTypes.displayString(recordRead.geometry().wkbType()))
   MultiLineString
   >>> print(QgsWkbTypes.displayString(layerSingle.dataProvider().wkbType()))
   LineString

Fortunately with a QGIS memory dataset you can't insert a *Point* into a *Line* dataset, or, otherwise mix geometry sub-types of different dimensionality.

.. doctest::

   >>> from qgis.core import *
   >>> layerSingle=QgsVectorLayer('LineString?crs=epsg:4326&field=ID:string', 'b', "memory")
   >>> providerSingle = layerSingle.dataProvider()
   >>> recordWrite = QgsFeature()
   >>> recordWrite.setAttributes(['1'])
   >>> recordWrite.setGeometry(QgsGeometry.fromWkt('POINT (1 1)'))
   >>> providerSingle.addFeature(recordWrite)
   False

===========================================
Parsing Empty and null Geometry Data Values
===========================================

The instantiation process for *empty* and *null* data values in QGIS is very different dependent on whether the value is *empty* or *null*.

----------------------------------------------
Instantiation of Empty Geometry Values by QGIS
----------------------------------------------
An *empty* geometry is a geometry value with an *empty* set of vertices.  Hence, an *empty Line* geometry value is distinct to an *empty Multi-Line* geometry value.  As the geometry sub-type is associated with an *empty* value, the method for instantiating *empty* geometries is embedded within each geometry subclass that can be instantiated.  Unfortunately, there is some variation with how QGIS instantiates *empty* geometry values across different geometry subclasses.

Using the QGIS API, *empty* geometries for several geometry types can be instantiated by instantiating the relevant QgsAbstractGeometry subclass without a set of vertices.  For example, to test that a ``QgsLineString()`` is *empty*:

.. doctest::

   >>> from qgis.core import QgsLineString
   >>> QgsLineString().isEmpty()
   True

Although *empty* geometries can be created for most geometry types with the QGIS API by instantiation without a set of vertices, it is not currently possible to instantiate an *empty* point geometry using this approach (:numref:`tableVII`). As demonstrated below, the well known text representation of the call to instantiate an *empty* point reveals that QGIS is wrongly adding a vertex with the coordinates of :math:`(0\ 0)` :cite:`QgsPointBugReport2018` [#f1]_.

.. doctest::

   >>> from qgis.core import QgsLineString,QgsPoint
   >>> print(QgsLineString().asWkt())
   LineString ()
   >>> print(QgsPoint().asWkt())
   Point (0 0)
   >>> print(QgsPoint().createEmptyWithSameType().asWkt())
   Point (nan nan)


.. _tableVII:

.. table:: Testing whether an *empty* geometry has been created by the instantiation of various types of ``QgsAbstractGeometry`` subclasses using the Python Console in QGIS 3.0.3.
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


----------------------------------------
Changing of Empty data Values by parsing
----------------------------------------

As indicated in :numref:`tableMultiLine` *empty* geometry values are changed to *null* when parsing to Microsft SQL server or Shapefile data sources.  For a Shapefile, this change in data value maybe the most pragmatic outcome as *empty* geometries are not included in it's specification.  For the Micrsoft SQL Server data source, the change from *empty* to *null* occurs when parsing to or from this data source :cite:`ParseEmptyFromSql` although both QGIS and Microsoft SQL Server specifications include *empty* geometry data values.  In contrast to Microsoft SQL Server, *empty* and *null* values are parsed to and from PostGIS without fault or change.


---------------------------------------------------
Inadvertently Creating Empty Geometries within QGIS
---------------------------------------------------
Within QGIS, an *empty* geometry is created by using the “Vertex Tool” to delete all vertices of an existing shape.  A user unfamiliar with QGIS may incorrectly assume that deleting all the vertices of a geometry also deletes the record.  This mistake of assumed record deletion when deleting vertices is most likely to occur for geometries with single part points as the geometry disappears from view when the first and only vertex is deleted.  Hence, when editing a shape, a QGIS user may unintentionally create an *empty* shape when they are attempting to delete the shape.


^^^^^^^^^^^^^^^^^^^^^^^^^^
In QGIS null Implies Empty
^^^^^^^^^^^^^^^^^^^^^^^^^^
In the definition of *empty* geometry values in section :ref:`EmptyAnchor` it is articulated that an *empty* geometry is just one valid value in the set of valid values for the geometry data type.  In contrast, *null* indicates that the geometry value is unknown and that the value can be *any* value from the set of valid values. Hence, an *empty* geometry values is one of many possible values for a *null* geometry.  For example, for a point, the vertices of an *empty* point are :math:`\{\ \ \}` as it has no coordinates, and, the vertices of a *null* point are :math:`\{x\ y\}` where :math:`x` and :math:`y` are both variables designating unknown coordinates. These definitions are consistent with SQL relational databases.  Unfortunately, the application of *null* used by SQL relational databases is different to that used by both mathematics for set theory, and, by most computer programming languages :cite:`WhatIsNull`.

Let’s consider the definition of *null* for set theory and computer programming using a common example.  If one has a box of apples and a box of bananas, then the intersection of the two boxes of fruit is an *empty* box. For set theory, *null* – nothing is what you have when you take away the box.

Similar to set theory, for most object-oriented computer programming languages, an object that has not been instantiated is *null*.  Hence, a pointer to something that doesn’t exist is *null*. In comparison, an *empty* object is an object that has been instantiated but not populated, for example, a list with no members, or, a box with no fruit.

So, from the perspective of an object-oriented computer programming language, *null* means no value and no type.  Hence, a *null* object is an object that does not exist and does not occupy space in a computer’s memory.  Indeed, SQL relational databases implement *null* as an object that doesn’t exist, so, the context difference between unknown and nothing does not have to create conflict.

The underlying conflict is based on logical deduction.  It has been proved that an *empty* set is a subset of any set.  Some argue that on object that doesn’t exist can’t contain anything, so, it must be *empty* [#f3]_.  Hence, *null* is a subclass of *empty*.  This argument is flawed as by arguing that a *null* object is *empty* you have just created an object.  A *null* object neither contains anything nor has a container.

Unfortunately, many computer programming languages and QGIS follow a convention where something must also be *empty* if it is *null*.  QGIS employs the logic that a *null* geometry is also an *empty* geometry :cite:`QGSGeometrySource2018`.    The QGIS test for *null* in it's C++ code simply asks whether the object exists (whether it points to anything) :cite:`QGSGeometrySource2018`::

  144 bool QgsGeometry::isNull() const
  145 {
  146  return !d->geometry;
  147 }


Now, the QGIS test for *empty* in it's C++ code performs the same test as for *null*, and, returns ``True`` if the test for *null* returns ``True`` :cite:`QGSGeometrySource2018`::

  329 bool QgsGeometry::isEmpty() const
  330 {
  331  if ( !d->geometry )
  332  {
  333  return true;
  334  }
  335
  336  return d->geometry->isEmpty();
  337 }


Hence, a test for an *empty* geometry in QGIS will return ``True`` for all *null* and *empty* geometry values.

.. doctest::

   >>> from qgis.core import QgsFeature
   >>> recordNull, recordEmpty = (QgsFeature() for i in range(2))
   >>> recordEmpty.setGeometry(QgsGeometry.fromWkt('LINESTRING ()'))
   >>> # Only recordNull has a null geometry
   >>> recordNull.geometry().isNull()
   True
   >>> recordEmpty.geometry().isNull()
   False
   >>> # Both recordNull and recordEmpty have empty geometries
   >>> recordNull.geometry().isEmpty()
   True
   >>> recordEmpty.geometry().isEmpty()
   True


---------------------------------------------
Instantiation of null Geometry Values by QGIS
---------------------------------------------

To claim a *null* geometry value has been instantiated in QGIS is a *faux pas*.  *null* represents the absence of a value, so, a record with a *null* geometry value is a record without a geometry value.  *null* infers that an object (in this case a geometry value) has not been instantiated.

--------------------------------------------------------------
Retrospective Incorporation of Empty and null Values Into GDAL
--------------------------------------------------------------
The Geospatial Data Abstraction Library (GDAL) is ubiquitous within most GIS Software to translate and process geospatial data.  Handles for *empty* geometries were not part of the original GDAL specification, with *empty* geometries being treated as *null*.   The retrospective incorporation of *empty* handles into GDAL has not been picked up by many applications that employ GDAL, and, even within GDAL there are many processing tools that don't maintain *empty* geometries.

Many of the current GDAL set operators continue to convert *empty* geometry values to *null* geometry values even when the set being operated on has successfully implemented the *empty* geometry handle on parsing to GDAL.  For example, for the intersection operation the output is *“a new geometry representing the intersection or NULL if there is no intersection or an error occurs”* :cite:`GDALIntersection`.  Curiously, the same GDAL geometry class has a handle to assign an *empty* geometry, or, to test for an *empty* geometry :cite:`GDALEmpty`.  On another GDAL ticket register it is stated *“GML/WFS: by default does not advertise NOT NULL fields since we treat empty strings as being null for historical reasons. By setting the open option EMPTY_AS_NULL=NO, empty strings will be reported as such and NOT NULL fields might be advertised”* :cite:`Rouault2015`. It is clear that GDAL was not originally intended to distinguish between *null* and *empty*.

The retrospective addition of handles for *empty* geometry values in GDAL was mimicked by QGIS.  Consequently, within QGIS there are many tools that convert *empty* values to *null* during their operation.


..
   footnotes

.. [#fi] The QGIS types were renamed here for clarity.  The actual QGIS types are ``QgsLineString``, ``QgsCircularString``, ``QgsCompoundCurve``, and, ``QgsMultiLineString``.

.. [#f2] A Shapefile's *PolyLine* is essentially the same as a *Multi-Line* for the scope of this report.

.. [#f1] a ``Point (nan nan)`` is also reported when an *empty* PostGis point is parsed by QGIS.

.. [#f3] Unable to find a high quality reference for this argument.  Several private conversations with C++ programmers reveal that this logic is common and is frequently used to test for *empty* in C++.

.. [#f5] The geometry type saved by PostGis and Microsoft SQL server depends on: geometry constraints within the database; the use of a *Geometry columns* lookup table; and, what geometry types already exist within the respective datasets.

.. [#f8] Technically in a Shapefile the geometry sub-type is recorded for each record, but, the technical specifications state that "All non-null shapes must be of the same shape type" :cite:`ShapefileDesc`.

.. [#f9] SpatialLite table has a *Multi-Line* geometry data type.



