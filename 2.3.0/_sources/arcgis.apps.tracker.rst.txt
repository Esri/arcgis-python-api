arcgis.apps.tracker module
============================

.. automodule:: arcgis.apps.tracker


The :class:`~arcgis.apps.tracker.LocationTrackingManager` is the main entry point into the Tracker module.
It can be used as shown in the following code example.


.. code-block:: python

    # Access the location tracking manager and check the status

    import arcgis
    gis = arcgis.gis.GIS("https://arcgis.com", "<username>", "<password>")
    print(gis.admin.location_tracking.status)

LocationTrackingManager
-----------------------
.. autoclass:: arcgis.apps.tracker.LocationTrackingManager
    :members:
    :undoc-members:
    :inherited-members:

TrackView
--------------
.. autoclass:: arcgis.apps.tracker.TrackView
    :members:
    :undoc-members:
    :inherited-members:

TrackViewerManager
------------------
.. autoclass:: arcgis.apps.tracker.TrackViewerManager
    :members:
    :undoc-members:
    :inherited-members:

MobileUserManager
-----------------
.. autoclass:: arcgis.apps.tracker.MobileUserManager
    :members:
    :inherited-members:
