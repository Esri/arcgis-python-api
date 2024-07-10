.. arcgis documentation master file, created by
   sphinx-quickstart on Thu Oct 20 23:21:00 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _gaxFeatureInput:

arcgis.geoanalytics module
==========================

.. automodule:: arcgis.geoanalytics

**Feature Input**

All GeoAnalytics Tools have input parameters that take features as their input. Features can be input as:

    * Big data file share layer. These can be obtained by using the layers property of big data file share items.
    * Item (of type Feature Layer Collection or Feature Collection) - only the first feature layer is used.
    * Instance of FeatureLayer, FeatureLayerCollection, FeatureCollection.
    * Feature Service URL as a string.
    * Python dict in the feature collection format

define_output_datastore
--------------
.. autofunction:: arcgis.geoanalytics.define_output_datastore

get_datastores
--------------
.. autofunction:: arcgis.geoanalytics.get_datastores

is_supported
--------------
.. autofunction:: arcgis.geoanalytics.is_supported

Submodules
--------------
.. toctree::
   :maxdepth: 3

   arcgis.geoanalytics.analyze_patterns
   arcgis.geoanalytics.data_enrichment
   arcgis.geoanalytics.find_locations
   arcgis.geoanalytics.manage_data
   arcgis.geoanalytics.summarize_data
   arcgis.geoanalytics.use_proximity
