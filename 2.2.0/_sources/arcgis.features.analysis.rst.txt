.. _FeatureInput:

arcgis.features.analysis module
=======================================
**Feature Input**

All standard spatial analysis tools accept features as input. Features can be specified in one of the following ways:

* Item (of type :class:`Feature Layer Collection<arcgis.features.FeatureLayerCollection>` or :class:`Feature Collection<arcgis.features.FeatureCollection>`) - only the first feature layer is used

* Instance of :class:`Feature Layer<arcgis.features.FeatureLayer>`, :class:`Feature Layer Collection<arcgis.features.FeatureLayerCollection>`, or :class:`Feature Collection<arcgis.features.FeatureCollection>`

* Feature Service URL as a string,

* Python dict in the format outlined in the REST API `featureCollection <https://developers.arcgis.com/rest/analysis/api-reference/feature-input.htm>`_

For point feature layers, the following inputs may additonally be used for convenience:

* (lat, long) pair for point feature layer

* dict with 'location' as key (eg result from geocoding)

.. automodule:: arcgis.features.analysis

aggregate_points
--------------
.. autofunction:: arcgis.features.analysis.aggregate_points


calculate_density
--------------
.. autofunction:: arcgis.features.analysis.calculate_density

choose_best_facilities
--------------
.. autofunction:: arcgis.features.find_locations.choose_best_facilities

connect_origins_to_destinations
--------------
.. autofunction:: arcgis.features.analysis.connect_origins_to_destinations

create_buffers
--------------
.. autofunction:: arcgis.features.analysis.create_buffers

create_drive_time_areas
--------------
.. autofunction:: arcgis.features.analysis.create_drive_time_areas

create_route_layers
--------------
.. autofunction:: arcgis.features.analysis.create_route_layers

create_viewshed
--------------
.. autofunction:: arcgis.features.analysis.create_viewshed

create_watersheds
--------------
.. autofunction:: arcgis.features.analysis.create_watersheds

derive_new_locations
--------------
.. autofunction:: arcgis.features.analysis.derive_new_locations

dissolve_boundaries
--------------
.. autofunction:: arcgis.features.analysis.dissolve_boundaries

enrich_layer
--------------
.. autofunction:: arcgis.features.analysis.enrich_layer

extract_data
--------------
.. autofunction:: arcgis.features.analysis.extract_data

find_existing_locations
--------------
.. autofunction:: arcgis.features.analysis.find_existing_locations

find_hot_spots
--------------
.. autofunction:: arcgis.features.analysis.find_hot_spots

find_nearest
--------------
.. autofunction:: arcgis.features.analysis.find_nearest

find_point_clusters
--------------
.. autofunction:: arcgis.features.analysis.find_point_clusters

find_similar_locations
--------------
.. autofunction:: arcgis.features.analysis.find_similar_locations

find_centroids
--------------
.. autofunction:: arcgis.features.analysis.find_centroids

interpolate_points
--------------
.. autofunction:: arcgis.features.analysis.interpolate_points

join_features
--------------
.. autofunction:: arcgis.features.analysis.join_features

merge_layers
--------------
.. autofunction:: arcgis.features.analysis.merge_layers

overlay_layers
--------------
.. autofunction:: arcgis.features.analysis.overlay_layers

plan_routes
--------------
.. autofunction:: arcgis.features.analysis.plan_routes

summarize_nearby
--------------
.. autofunction:: arcgis.features.analysis.summarize_nearby

summarize_center_and_dispersion
--------------
.. autofunction:: arcgis.features.analysis.summarize_center_and_dispersion

summarize_within
--------------
.. autofunction:: arcgis.features.analysis.summarize_within

trace_downstream
--------------
.. autofunction:: arcgis.features.analysis.trace_downstream
