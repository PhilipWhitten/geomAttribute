===
Aim
===

QGIS is a capable and popular GIS desktop software that changes both *empty* and *null* geometry values, and, geometry type during both data parsing and data processing.  Some of these data changes are necessary to comply with different data source requirements.  These changes in data are likely to catch recent QGIS adopters unaware and may lead to errors and losses in productivity.

The primary aim of this project is to expose those records with *null* and *empty* geometry values.  A secondary aim of this project is to expose the geometry type per record.

If successful, this project will be a stepping stone towards:

   * increasing GIS professional awareness of *null* and *empty* geometry values;
   * illumination of QGIS data parsing errors when they occur so that developers may address them; and,
   * integrating GIS within organizational databases by embracing QGIS's open and flexible data providers.
