# Create table query
CREATE_TABLE = """
create table if not exists Table_{country_code} (
Customer_Name varchar(255) primary key,
Customer_Id varchar(18) not null,
Open_Date Date not null,
Last_Consulted_Date Date,
Vaccination_Id char(5),
Dr_Name varchar(255),
State char(5),
Country char(5),
Post_Code integer,
DOB date,
Is_Active char(1)
);
"""

# Insert query
INSERT_ENTRY = """
insert into Table_{country_code} ({columns}) VALUES ({data_values});
"""
