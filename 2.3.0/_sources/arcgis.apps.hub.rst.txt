arcgis.apps.hub module
=======================

.. automodule:: arcgis.apps.hub

The :class:`~arcgis.apps.hub.Hub` is the main entry point into the Hub module.
It can be used as shown in the following code example.

.. code-block:: python

    from arcgis.gis import GIS
    gis = GIS("https://arcgis.com", "<username>", "<password>")
    myHub = gis.hub
    a_Initiative = myHub.initiatives.get(itemId)
    a_Site = myHub.sites.get(a_Initiative.site_id)
    b_Site = myHub.sites.get(itemId)
    c_Page = myHub.pages.get(itemId)
    myEvents = myHub.events.search()

Hub
--------------------------
.. autoclass:: arcgis.apps.hub.hub.Hub
    :members:
    :undoc-members:

Initiative
--------------------------
.. autoclass:: arcgis.apps.hub.initiatives.Initiative
    :members:
    :undoc-members:

Site
--------------------------
.. autoclass:: arcgis.apps.hub.sites.Site
    :members:
    :undoc-members:

Page
--------------------------
.. autoclass:: arcgis.apps.hub.sites.Page
    :members:
    :undoc-members:

Event
--------------------------
.. autoclass:: arcgis.apps.hub.Event
    :members:
    :undoc-members:

InitiativeManager
--------------------------
.. autoclass:: arcgis.apps.hub.initiatives.InitiativeManager
    :members:
    :undoc-members:

SiteManager
--------------------------
.. autoclass:: arcgis.apps.hub.sites.SiteManager
    :members:
    :undoc-members:

PageManager
--------------------------
.. autoclass:: arcgis.apps.hub.sites.PageManager
    :members:
    :undoc-members:

EventManager
--------------------------
.. autoclass:: arcgis.apps.hub.events.EventManager
    :members:
    :undoc-members: