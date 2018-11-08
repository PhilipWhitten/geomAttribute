***
API
***

The following modules are included within this plugin.  The plugin's repository is
on `GitHub <https://github.com/PhilipWhitten/geomAttribute>`_.

.. _modelVectorLayers-API:

========================
modelVectorLayers module
========================

.. automodule:: modelVectorLayers
   :members:

.. _parseQGISGeometry-API:

========================
parseQGISGeometry module
========================

 .. automodule:: parseQGISGeometry
    :members:

    .. autofunction:: geometryField(feature, parent)

       Creates a QGIS expression called geometryField.  This expression returns a string that represents the geometry in
       the following order of decreasing precedence:

          * Null
          * Empty
          * Well known binary type string

       Returns:
          A string that represents the geometry.






