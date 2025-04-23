Main idea of the Project:
- Purpose of the project: Building a full application that stores catalog data fetched from Dremio and Present them to end Users
- Application is comprised of a backend built with Django, backend will define the stucture of the DataBase using Django ORM and expose an API. it will also manage the different application building blocks and allow us to have orchestrated modules.
- Database technology that will be used is Postgres version 16.
- for the frontend part, we will be using Dash framework, the data we will be presenting is mainly tables and some charts
- We will add authentication to the Application to allow distinguiching between users, in the database we will be storing a profiles table to present content to the user depending on his profile.


Application Building Blocks (can be ammended later):
- Listing the privileges of users on the datasets of Dremio (Virtual datasets and physical datasets)
- Showing the relation between the datasets (lineage data) in a graphical manner
- Listing of Available tables on a certain source (to make data consumers know what data are available and what they need to ask for)
- possibilité to see details of tables, views
- display source details.

How to proceed:
- Any piece of data that comes from the Application is fetched through different endpoints of the Dremio API.
- Data fetched from the API are stored in the Database that attaches to Django Backend.
- Storing Data in our own Postgres makes quering much more effective.
- Data need to be refreshed constantly by polling Dremio API in an efficient way.


############# Building Block 1: Lineage Data for any dataset ##########
What is needed here:
* Complete inventory of datasets in Dremio environement, this later is stored in two different Postgres tables: VirtualDataSet and PhysicalDataset
* Lineage Data that consist of parent child relationship.
How to get the needed Data:
* using the Job endpoint, submit a job to retrieve the systemtable sys.views and a job to retrieve the sys."tables" 
* those tables contain the full listing of the views and tables, get the path from the outcome (select path from sys.views or select path from sys."tables")
* from those paths, and using the catalog endpoint with the path of a dataset, retreive details about the later (dateCreated, dataLastModified, source_id....)
* get lineage for each dataset using the lineage endpoint
* flatten the response for lineage to have one dictionary transformed into relation my relation data (one line one relation)

############# Technical Implementation ################
##### first phase is to build the structure of the project ####
- Building the Django App with Django command line startproject project name is dremio_catalog
- Creating an APP for datasets named datasets and an App for lineage named lineage.
- in the settings file of the project, set the Database to Postgres (for dev environement, it is on localhost)
- in the settings file of the project, add the installed apps (datasets, lineage)
- Set the models for datasets (Virtual and Physical) in datasets App:
    * Fields for the VirtualDataset are: name, path, hash(hash of the path in MD5 that uniquely identifies the vds) and space_name.
    * Fields for the PhysicalDataset are: name, path, hash(hash of the path in MD5 that uniquely identifies the pds) and source_name.
- Set model for lineage in lineage App:
    * Fields for lineage are Parent_path, Parent_id(which is MD5 of Parent_path), Child_path, Child_id(which is MD5 hash of Child_path)
- Make the migration to map Django ORM structure on the underlying database.

########### Submitting a job to get the system tables (generic function) #######
- we are making an api.py file that contains the api functions needed to fetch data from precise endpoints
- the api file is located under the datasets app and contains functions related to datasets (PDS and VDS) only.
- the file contains the job endpoint functions, namely run_dremio_sql that consists of submit sql, polling and retrieving results once done
Ammendment: API Being very Slow at Retrieving the sys tables, lets use JDBC instead (Jaydebi module of python) to submit the sql query and fetch outcome, it uses connexion class and cursor to fetch data.
