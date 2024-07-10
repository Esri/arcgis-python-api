.. arcgis documentation master file, created by
   sphinx-quickstart on Thu Oct 20 23:21:00 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

arcgis.mapping module
=================

.. automodule:: arcgis.mapping

Working with 2D Maps
--------------------
WebMap
^^^^^^
.. autoclass:: arcgis.mapping.WebMap
    :members:
    :undoc-members:
    :show-inheritance:

OfflineMapAreaManager
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.OfflineMapAreaManager
    :members:
    :undoc-members:
    :show-inheritance:

PackagingJob
^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.PackagingJob
    :members:
    :undoc-members:
    :show-inheritance:

Working with 3D Maps
--------------------
WebScene
^^^^^^^^
.. autoclass:: arcgis.mapping.WebScene
    :members:
    :undoc-members:
    :show-inheritance:

SceneLayer
^^^^^^^^^^
.. autoclass:: arcgis.mapping.SceneLayer
    :members:
    :undoc-members:
    :show-inheritance:

SceneLayerManager
^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.SceneLayerManager
    :members:
    :undoc-members:
    :show-inheritance:

EnterpriseSceneLayerManager
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.EnterpriseSceneLayerManager
    :members:
    :undoc-members:
    :show-inheritance:

BuildingLayer
^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.BuildingLayer
    :members:
    :undoc-members:
    :show-inheritance:

IntegratedMeshLayer
^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.IntegratedMeshLayer
    :members:
    :undoc-members:
    :show-inheritance:

Tiles3DLayer
^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.Tiles3DLayer
    :members:
    :undoc-members:
    :show-inheritance:

Object3DLayer
^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.Object3DLayer
    :members:
    :undoc-members:
    :show-inheritance:


Point3DLayer
^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.Point3DLayer
    :members:
    :undoc-members:
    :show-inheritance:

PointCloudLayer
^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.PointCloudLayer
    :members:
    :undoc-members:
    :show-inheritance:

VoxelLayer
^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.VoxelLayer
    :members:
    :undoc-members:
    :show-inheritance:

Working with Map Service Layers
-------------------------------
MapServiceLayer
^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.MapServiceLayer
    :members:
    :undoc-members:
    :show-inheritance:

MapFeatureLayer
^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.MapFeatureLayer
    :members:
    :undoc-members:
    :show-inheritance:

MapRasterLayer
^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.MapRasterLayer
    :members:
    :undoc-members:
    :show-inheritance:

MapImageLayer
^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.MapImageLayer
    :members:
    :undoc-members:
    :show-inheritance:

MapImageLayerManager
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.MapImageLayerManager
    :members:
    :undoc-members:
    :show-inheritance:

EnterpriseMapImageLayerManager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.EnterpriseMapImageLayerManager
    :members:
    :undoc-members:
    :show-inheritance:

MapTable
^^^^^^^^
.. autoclass:: arcgis.mapping.MapTable
    :members:
    :undoc-members:
    :show-inheritance:

VectorTileLayer
^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.VectorTileLayer
    :members:
    :undoc-members:
    :show-inheritance:
    
VectorTileLayerManager
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.VectorTileLayerManager
    :members:
    :undoc-members:
    :show-inheritance:
    
EnterpriseVectorTileLayerManager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: arcgis.mapping.EnterpriseVectorTileLayerManager
    :members:
    :undoc-members:
    :show-inheritance:

Working with OGC layers
-----------------------
arcgis.mapping.ogc
^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 3

   arcgis.mapping.ogc

Working with Map Forms
----------------------
arcgis.mapping.forms
^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 3

   arcgis.mapping.forms

Utility Functions for Mapping
-----------------------------
export_map
^^^^^^^^^^
.. autofunction:: arcgis.mapping.export_map

create_colormap
^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.create_colormap

get_layout_templates
^^^^^^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.get_layout_templates

Symbology
^^^^^^^^^
.. automodule:: arcgis.mapping.symbol
    :members:
    :undoc-members:
    :show-inheritance:

generate_simple
^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.renderer.generate_simple

generate_heatmap
^^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.renderer.generate_heatmap

generate_unique
^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.renderer.generate_unique

generate_classbreaks
^^^^^^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.renderer.generate_classbreaks

generate_renderer
^^^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.renderer.generate_renderer

visual_variables
^^^^^^^^^^^^^^^^
.. autofunction:: arcgis.mapping.renderer.visual_variables
