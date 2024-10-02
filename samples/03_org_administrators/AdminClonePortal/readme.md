# Stand-alone Python script to clone portal users groups and content

This folder contains the stand-alone Python script `clone_portal.py` for the accompanying sample titled [Clone Portal users, groups and content](https://developers.arcgis.com/python-2-3/sample-notebooks/clone-portal-users-groups-and-content/)

Running the script produces and output similar to below

## Script output

```
Starting clone portal script
Enter password for source portal:
Enter password for target portal:

Getting list of users in source portal
brown.rogers	:	org_user
davis.reed	:	org_admin
johnson.stewart	:	org_user
jones.morris	:	org_user
miller.cook	:	org_publisher
moore.bell	:	org_publisher
project_archiver	:	org_user
smith.collins	:	org_admin
taylor.murphy	:	org_publisher
williams.sanchez	:	org_user
wilson.morgan	:	org_publisher

Total number of users for cloning: 11

Users in target portal:
arcgis_python_api	:	org_publisher
publisher1	:	org_publisher

Copying users from source to target
------------------------------------
Creating user: brown.rogers
Creating user: davis.reed
Creating user: johnson.stewart
Creating user: jones.morris
Creating user: miller.cook
Creating user: moore.bell
Creating user: project_archiver
Creating user: smith.collins
Creating user: taylor.murphy
Creating user: williams.sanchez
Creating user: wilson.morgan

Groups in source portal:
Central Services
Compliance
Customer Service, Finance, Billing and Accounting
Demographic Content

Groups in target portal:
Featured Maps and Apps


Copying groups from source to target
------------------------------------
Copying: Central Services
Copying: Compliance
Copying: Customer Service, Finance, Billing and Accounting
Copying: Demographic Content

Getting the list of all items in source portal
Collecting item ids for brown.rogers		Number of folders 1 # Number of items 3
Collecting item ids for davis.reed		Number of folders 1 # Number of items 3
Collecting item ids for johnson.stewart		Number of folders 1 # Number of items 3
Collecting item ids for jones.morris		Number of folders 1 # Number of items 3
Collecting item ids for miller.cook		Number of folders 1 # Number of items 3
Collecting item ids for moore.bell		Number of folders 1 # Number of items 3
Collecting item ids for project_archiver		Number of folders 7 # Number of items 18
Collecting item ids for smith.collins		Number of folders 1 # Number of items 4
Collecting item ids for taylor.murphy		Number of folders 1 # Number of items 3
Collecting item ids for williams.sanchez		Number of folders 1 # Number of items 3
Collecting item ids for wilson.morgan		Number of folders 1 # Number of items 3

Finding which items are shared to groups

set3_Streets                             #
set1_mapping_tech                        #
Moore Bell response locations            # shared # ['Compliance', 'Demographic Content']
USA_cities_Fortune_500                   #
set2_Voronoi-diagram                     #
FL                                       #
LA                                       #
AR                                       #
set1_GeoJson                             #
set2_counties                            #
set2_SD_crime                            #
set2_empty                               #
set2_Chicago                             #
Williams Sanchez response locations      # shared # ['Customer Service, Finance, Billing and Accounting']
Johnson Stewart response locations       # shared # ['Central Services']
IN                                       #
NC                                       #
NH                                       #
NV                                       #
set1_Chicago                             #
ID                                       #
Brown Rogers response locations          # shared # ['Central Services']
Smith Collins response locations         # shared # ['Central Services']
Davis Reed response locations            # shared # ['Demographic Content']
NV                                       #
set1_india                               #
set2_catalina-points                     #
FL                                       #
NH                                       #
Miller Cook response locations           # shared # ['Demographic Content']
set1_major_cities                        #
set1_fortune500                          #
LA                                       #
KS                                       #
IN                                       #
Taylor Murphy response locations         # shared # ['Central Services', 'Compliance']
NC                                       #
AZ                                       #
set1_gov_sites_registration              #
set2_USAcities                           #
AR                                       #
set1_GeoJson                             #
ID                                       #
Wilson Morgan response locations         # shared # ['Compliance', 'Demographic Content']
Smith Collins response locations         #
AZ                                       #
set2_australia                           #
Jones Morris response locations          # shared # ['Customer Service, Finance, Billing and Accounting']
KS                                       #

Copying items
--------------
Copying set3_Streets 	for	 project_archiver
Copying set1_mapping_tech 	for	 project_archiver
Copying Moore Bell response locations 	for	 moore.bell
Copying USA_cities_Fortune_500 	for	 project_archiver
Copying set2_Voronoi-diagram 	for	 project_archiver
Copying FL 	for	 davis.reed
Copying LA 	for	 taylor.murphy
Copying AR 	for	 brown.rogers
Copying set1_GeoJson 	for	 project_archiver
Copying set2_counties 	for	 project_archiver
Copying set2_SD_crime 	for	 project_archiver
Copying set2_empty 	for	 project_archiver
Copying set2_Chicago 	for	 project_archiver
Copying Williams Sanchez response locations 	for	 williams.sanchez
Copying Johnson Stewart response locations 	for	 johnson.stewart
Copying IN 	for	 williams.sanchez
Copying NC 	for	 jones.morris
Copying NH 	for	 miller.cook
Copying NV 	for	 johnson.stewart
Copying set1_Chicago 	for	 project_archiver
Copying ID 	for	 wilson.morgan
Copying Brown Rogers response locations 	for	 brown.rogers
Copying Smith Collins response locations 	for	 smith.collins
Copying Davis Reed response locations 	for	 davis.reed
Copying NV 	for	 johnson.stewart
Copying set1_india 	for	 project_archiver
Copying set2_catalina-points 	for	 project_archiver
Copying FL 	for	 davis.reed
Copying NH 	for	 miller.cook
Copying Miller Cook response locations 	for	 miller.cook
Copying set1_major_cities 	for	 project_archiver
Copying set1_fortune500 	for	 project_archiver
Copying LA 	for	 taylor.murphy
Copying KS 	for	 smith.collins
Copying IN 	for	 williams.sanchez
Copying Taylor Murphy response locations 	for	 taylor.murphy
Copying NC 	for	 jones.morris
Copying AZ 	for	 moore.bell
Copying set1_gov_sites_registration 	for	 project_archiver
Copying set2_USAcities 	for	 project_archiver
Copying AR 	for	 brown.rogers
Copying set1_GeoJson 	for	 project_archiver
Copying ID 	for	 wilson.morgan
Copying Wilson Morgan response locations 	for	 wilson.morgan
Copying Smith Collins response locations 	for	 smith.collins
Copying AZ 	for	 moore.bell
Copying set2_australia 	for	 project_archiver
Copying Jones Morris response locations 	for	 jones.morris
Copying KS 	for	 smith.collins

Establishing relationships between items in target portal
---------------------------------------------------------
set3_Streets # Map Document
set1_mapping_tech # Microsoft Powerpoint
Moore Bell response locations # Web Map
USA_cities_Fortune_500 # Map Document
set2_Voronoi-diagram # Microsoft Word
FL # Feature Service
		FL # CSV	## Service2Data
		establishing relationship in target portalTrue
LA # Feature Service
		LA # CSV	## Service2Data
		establishing relationship in target portalTrue
AR # CSV
set1_GeoJson # Microsoft Word
set2_counties # Locator Package
set2_SD_crime # Map Document
set2_empty # Map Document
set2_Chicago # CSV
Williams Sanchez response locations # Web Map
Johnson Stewart response locations # Web Map
IN # CSV
NC # CSV
NH # Feature Service
		NH # CSV	## Service2Data
		establishing relationship in target portalTrue
NV # Feature Service
		NV # CSV	## Service2Data
		establishing relationship in target portalTrue
set1_Chicago # CSV
ID # CSV
Brown Rogers response locations # Web Map
Smith Collins response locations # Web Map
Davis Reed response locations # Web Map
NV # CSV
set1_india # GeoJson
set2_catalina-points # KML
FL # CSV
NH # CSV
Miller Cook response locations # Web Map
set1_major_cities # Locator Package
set1_fortune500 # File Geodatabase
LA # CSV
KS # Feature Service
		KS # CSV	## Service2Data
		establishing relationship in target portalTrue
IN # Feature Service
		IN # CSV	## Service2Data
		establishing relationship in target portalTrue
Taylor Murphy response locations # Web Map
NC # Feature Service
		NC # CSV	## Service2Data
		establishing relationship in target portalTrue
AZ # CSV
set1_gov_sites_registration # Microsoft Excel
set2_USAcities # File Geodatabase
AR # Feature Service
		AR # CSV	## Service2Data
		establishing relationship in target portalTrue
set1_GeoJson # PDF
ID # Feature Service
		ID # CSV	## Service2Data
		establishing relationship in target portalTrue
Wilson Morgan response locations # Web Map
Smith Collins response locations # Web Map
AZ # Feature Service
		AZ # CSV	## Service2Data
		establishing relationship in target portalTrue
set2_australia # GeoJson
Jones Morris response locations # Web Map
KS # CSV
```
