## Implementation details
The project contains the code just for demo. 

It's working as per my understanding on the requirement and made several assumptions for exception handling.

### Execution:
Command to run is `python main.py file_path date_format`
* file_name and date_format are the input parameters
* file_name should be absolute path of the data file
* date_format should be one of the item in *`DATE_FORMAT_MAPPERS`* dictionary at *`configs.py`*
  file
  
### Assumptions:
* Assumption is that data file will be provided which will contain header in the first line and data lines
  below
* Current implementation assumes that the data file is error free
* Column names are adjusted in order to have similarities in table and data files
* Country should be a mandatory column in data file as we need to insert the data into different country 
  tables
  
### Key points:
* The date formats should be maintained as mentioned above in order to parse the date from data files
* Psycopg2 package is used for interacting with the database
* Database configurations are maintained in db.ini file
* The ask was to write queries, however it's easy if we use ORM's instead of raw queries always
* Even the pandas dataframe would be easier option in order to construct intermediate tables

**One major issue to be highlighted, in the given file date format for DOB is different and for testing
 i have updated the field to correct format** 
