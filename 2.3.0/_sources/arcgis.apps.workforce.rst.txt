arcgis.apps.workforce module
============================

.. automodule:: arcgis.apps.workforce


The :class:`~arcgis.apps.workforce.Project` is the main entry point into the Workforce module.
It can be used as shown in the following code example.


.. code-block:: python

    # Get a Project and search the assignments and workers, create new Workforce project

    import arcgis
    gis = arcgis.gis.GIS("https://arcgis.com", "<username>", "<password>")
    item = gis.content.get("<item-id>")
    project = arcgis.apps.workforce.Project(item)
    assignments = project.assignments.search()
    workers = project.workers.search()
    project2 = arcgis.apps.workforce.create_project('new_project', summary='This project was created by Python')

Assignment
----------
.. autoclass:: arcgis.apps.workforce.Assignment
    :members:
    :undoc-members:
    :inherited-members:

AssignmentType
--------------
.. autoclass:: arcgis.apps.workforce.AssignmentType
    :members: id, code, name, coded_value
    :undoc-members:
    :inherited-members:

Attachment
----------
.. autoclass:: arcgis.apps.workforce.Attachment
    :members:
    :undoc-members:

Dispatcher
----------
.. autoclass:: arcgis.apps.workforce.Dispatcher
    :members: name, contact_number, user_id
    :inherited-members:

Integration
----------
.. autoclass:: arcgis.apps.workforce.Integration
    :members: integration_id, prompt, url_template, assignment_type
    :inherited-members:

Project
-------
.. autoclass:: arcgis.apps.workforce.Project
    :members:
    :undoc-members:

Track
-----
.. autoclass:: arcgis.apps.workforce.Track
    :members:
    :undoc-members:
    :inherited-members:

Worker
------
.. autoclass:: arcgis.apps.workforce.Worker
    :members:
    :undoc-members:
    :inherited-members:

Submodules
----------
.. toctree::
   :maxdepth: 3

   arcgis.apps.workforce.managers




