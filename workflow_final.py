import sqlite3
import csv
import os
import os.path

# Start Project #
"""
@begin Data_Cleaning_Project @desc Workflow for cleaning NYPL Menus DataSet
"""



### Define the working folder
wd = ''
working_directory = os.getcwd() # wd
wd = os.path.join(working_directory, r'Data_Cleaning_Project')
if not os.path.exists(wd):
    os.makedirs(final_directory)

# Grab the raw data from four csv file


# Grobal Input
"""
@in Dish.csv @uri /wd/Dish.csv
@in MenuItem.csv @uri /wd/MenuItem.csv
@in MenuPage.csv @uri /wd/data/MenuPage.csv
@in Menu.csv @uri /wd/Dish.csv
"""

# OpenRefine clean data #
"""	    
    @begin Dish.csv_Cleaning @desc Clean Dish.csv in OpenRefine
    @in Dish.csv @uri /wd/Dish.csv
    @param DishCleaningSequence
    @out Dish_CLD.csv @uri /wd/Dish_CLD.csv
	@out Dish_CLD.json @uri /wd/Dish_CLD.json
    @end Dish.csv_Cleaning
    
    @begin MenuItem.csv_Cleaning @desc Clean MenuItem.csv in OpenRefine
    @in MenuItem.csv @uri /wd/MenuItem.csv
    @param MenuItemCleaningSequence
    @out MenuItem_CLD.csv @uri /wd/MenuItem_CLD.csv
	@out MenuItem_CLD.json @uri /wd/MenuItem_CLD.json
    @end MenuItem.csv_Cleaning
	
    @begin MenuPage.csv_Cleaning @desc Clean MenuPage.csv in OpenRefine
    @in MenuPage.csv @uri /wd/MenuPage.csv
    @param MenuPageCleaningSequence
    @out MenuPage_CLD.csv @uri /wd/MenuPage_CLD.csv
	@out MenuPage_CLD.json @uri /wd/MenuPage_CLD.json
    @end MenuPage.csv_Cleaning

    @begin Menu.csv_Cleaning @desc Use Clean Menu.csv in OpenRefine
    @in Menu.csv @uri /wd/Menu.csv
    @param MenuCleaningSequence
    @out Menu_CLD.csv @uri /wd/Menu_CLD.csv
	@out Menu_CLD.json @uri /wd/Menu_CLD.json
    @end CleanMenuWithOpenRefine
"""


# Combine the OpenRefine WorkFlow generation process #
"""
	@begin OpenRefine_clean_workflow_generateion @desc Generate workflow by YesWorkFlow (or2ywtool)
	@in Dish_CLD.json @uri /wd/Dish_CLD.json
	@in MenuItem_CLD.json @uri /wd/MenuItem_CLD.json
	@in MenuPage_CLD.json @uri /wd/MenuPage_CLD.json
	@in Menu_CLD.json @uri /wd/Menu_CLD.json
	@out Dish_CLD.pdf @uri /wd/Dish_CLD.pdf
	@out MenuItem_CLD.pdf @uri /wd/MenuItem_CLD.pdf
	@out MenuPage_CLD.pdf @uri /wd/MenuPage_CLD.pdf
	@out Menu_CLD.pdf @uri /wd/Menu_CLD.pdf
	@end OpenRefine_clean_workflow_generateion	
"""
## or2yw -i ./dish_CLD.json -o dish_CLD.pdf -ot pdf t parallel
## or2yw -i ./menuitem_CLD.json -o menuitem_CLD.pdf -ot pdf t parallel
## or2yw -i ./menupage_CLD.json -o menupage_CLD.pdf -ot pdf t parallel
## or2yw -i ./menu_CLD.json -o menu_CLD.pdf -ot pdf t parallel


# Load cleaned data separately(use this or below one) #
"""
	@begin LoadCleanedData @desc Load cleaned data into Sqlite DB with 4 tables (Dish,MenuItem,MenuPage,Menu)
	@in Dish_CLD.csv @uri /wd/Dish_CLD.csv
	@in MenuItem_CLD.csv @uri /wd/MenuItem_CLD.csv
	@in MenuPage_CLD.csv @uri /wd/MenuPage_CLD.csv
	@in Menu_CLD.csv @uri /wd/Menu_CLD.csv
	@param Database_Schema_Information 
	@out dish_in_NYPL.db @uri /wd/NYPL.db
	@out menuitem_in_NYPL.db @uri /wd/NYPL.db
	@out menupage_in_NYPL.db @uri /wd/NYPL.db
	@out menu_in_NYPL.db @uri /wd/NYPL.db
	@end LoadCleanedData
"""

conn = sqlite3.connect('NYPL.db')
c = conn.cursor()

def sql_check(sql_input, filename, final_directory):    
	csv_file = '//' + filename + '.csv'
	conn = sqlite3.connect(final_directory + '\\' + 'NYPL.db')
	c = conn.cursor()
	conn.row_factory = sqlite3.Row
	count = 0
	try:
		cursor = conn.execute(sql_input)
		row = cursor.fetchone()
		with open(final_directory + csv_file,'w') as out:
			csv_out=csv.writer(out, delimiter=",", lineterminator="\n")
			csv_out.writerow(row.keys())
			for row in c.execute(sql_input):
				csv_out.writerow(row)
				count += 1
		print(filename + "--Table Created.")
		print(str(count) + " records returned in this query")
	except AttributeError:
		print(filename + "--Table is empty.")
		print("0 record returned in this query")
		

# Inclusion dependency check (Referential IC) #
"""       
    @begin IDCheck @desc Apply SQL in Inclusion Dependency Check
	@in dish_in_NYPL.db @uri /wd/NYPL.db
	@in menuitem_in_NYPL.db @uri /wd/NYPL.db
	@in menupage_in_NYPL.db @uri /wd/NYPL.db
	@in menu_in_NYPL.db @uri /wd/NYPL.db
    @param InclusionDependencyIC
	@out Dish_Output @uri /wd/dish_id_check.csv
	@out MenuItem_Output @uri /wd/menuitem_id_check.csv
	@out MenuPage_Output @uri /wd/menupage_id_check.csv
	@out Menu_Output @uri /wd/menu_id_check.csv
	@out ID_check_reference
    @end IDCheck
"""

print('\n')
print("Here are the ID check:")

# ID check is only applied to dataset with referential relationship

sql_check("select id from menuitem as mi where mi.menu_page_id in (select id from menupage);", 
			  'menuitem_id_check_menuitem_menu_page_id_in_menupageTB_id', wd) 
			  
sql_check("select id from menuitem as mi where mi.dish_id in (select id from dish);", 
          'menuitem_id_check_menuitem_dish_id_in_dishTB_id', wd)  
		  
sql_check("select id from menupage as mp where mp.menu_id in (select id from menu);", 
			  'menupage_id_check_menupage_menu_id_in_menuTB_id', wd)  

# Funtional dependency check #
"""       
    @begin Dish_FD/OtherICCheck @desc Apply SQL in Single Table
	@in dish_in_NYPL.db @uri /wd/NYPL.db
    @param FDAndOtherIC(Dish)
	@out Dish_FD_IC_Output @uri /wd/dish_fd_ic.csv
	@out FD_IC_Check_Reference
    @end Dish_FD/OtherICCheck
	
    @begin MenuItem_FD/OtherICCheck @desc Apply SQL in Single Table
	@in menuitem_in_NYPL.db @uri /wd/NYPL.db
    @param FDyAndOtherIC(MenuItem)
	@out MenuItem_FD_IC_Output @uri /wd/menuitem_fd_ic.csv
	@out FD_IC_Check_Reference
    @end MenuItem_FD/OtherICCheck	

    @begin MenuPage_FD/OtherICCheck @desc Apply SQL in Single Table
	@in menupage_in_NYPL.db @uri /wd/NYPL.db
    @param FDyAndOtherIC(MenuPage)
	@out MenuPage_FD_IC_Output @uri /wd/menupage_fd_ic.csv
	@out FD_IC_Check_Reference
    @end MenuPage_FD/OtherICCheck
	
    @begin Menu_FD/OtherICCheck @desc Apply SQL in Single Table
	@in menu_in_NYPL.db @uri /wd/NYPL.db
    @param FDyAndOtherIC(Menu)
	@out Menu_FD_IC_Output @uri /wd/menu_fd_ic.csv
	@out FD_IC_Check_Reference
    @end Menu_FD/OtherICCheck	
"""
			
	# Dish 

print('\n')	
print("Here are the FD_IC check:")
	
sql_check("select d.id from (select dish.id, count(id) as count from dish group by id) d where d.count > 1", 
          'dish_fd_ic_id_unique', wd) # id is unique
	
sql_check("select * from dish where date(dish.first_appeared) > date(dish.last_appeared)", 
          'dish_fd_ic_first_appeared_GT_last_appeared', wd)  # 961 records with first_appreared later than the last_appeared
		  
sql_check("select dish.id from dish where dish.lowest_price > dish.highest_price;", 
          'dish_fd_ic_lowest_price_GT_highest_price', wd)   # No record is returned
		  
sql_check("select dish.id, dish.first_appeared, dish.last_appeared from dish where dish.last_appeared = 0 or dish.first_appeared = 0;", 
          'dish_fd_ic_first_appreared_last_appreared_zero', wd) # 55293 records are returned as first_appeared or last_appeared is 0
		  
	# MenuItem FD and other IC
sql_check("select mi.id from (select id, count(id) as count from menuitem group by id) mi where mi.count > 1;", 
          'menuitem_fd_ic_check_id_unique', wd) # id is unique
		  
sql_check("select * from menuitem as mi where mi.price > mi.high_price;", 
          'menuitem_fd_ic_price_GT_high_price', wd)  # 1332 record is returned with price greater than high_price
		  
sql_check("select * from menuitem as mi where mi.xpos > 1 AND mi.xpos < 0; ", 
          'menuitem_fd_ic_xpos_check', wd)  # No record with xpos out of range [0,1]
	
sql_check("select * from menuitem as mi where mi.ypos > 1 AND mi.ypos < 0; ", 
          'menuitem_fd_ic_ypos_check', wd)  # No record with ypos out of range [0,1]
	
	# MenuPage FD and other IC
	
sql_check("select mp.id from (select menupage.id, count(id) as count from menupage group by id) mp where mp.count > 1;", 
          'menupage_fd_ic_check_id_unique', wd)   # id is unique
		  
sql_check("select * from menupage where page_number < 1;", 
          'menupage_fd_ic_check_menupage_check', wd)  # There is no record with page_number less than 1

	# Menu FD and other IC
	
sql_check("select m.id from (select id, count(id) as count from menu group by id) m where m.count > 1;", 
          'menu_fd_ic_check_id_unique', wd) # id is unique	
		  
sql_check("select date(date) as Date_error from menu where date(date) < '1850-01-01' or date(date) > '2016-01-01';", 
          'menu_fd_ic_check_date_check', wd)  # The date should be within 1850-01-01 to 2016-01-01. 3 records with violated date are returned. 
		  
sql_check("select * from menu where dish_count = 0;", 
          'menu_fd_ic_check_dish_count_check', wd)  # 32 menus are with 0 dish_count	
		  
sql_check("select * from menu where page_count = 0;", 
          'menu_fd_ic_check_page_count_check', wd) # No menu is with 0 page_count
	
##

# Generate new dataset
"""	
    @begin NewDataGeneration @desc Apply FD_IC_check result and ID_check result
	@in dish_in_NYPL.db @uri /wd/NYPL.db
	@in menuitem_in_NYPL.db @uri /wd/NYPL.db
	@in menupage_in_NYPL.db @uri /wd/NYPL.db
	@in menu_in_NYPL.db @uri /wd/NYPL.db
	@param FD_IC_Check_Reference
	@param ID_check_reference
	@out Dish_New @uri /wd/dish_new.csv
	@out MenuItem_New @uri /wd/menuitem_new.csv
	@out MenuPage_New @uri /wd/menupage_new.csv
	@out Menu_New @uri /wd/menu_new.csv
    @end NewDataGeneration	
"""    



# Grobal Output #
"""
@out Dish_Output @uri /wd/dish_id_check.csv
@out MenuItem_Output @uri /wd/menuitem_id_check.csv
@out MenuPage_Output @uri /wd/menupage_id_check.csv
@out Menu_Output @uri /wd/menu_id_check.csv
@out Dish_CLD.pdf @uri /wd/Dish_CLD.pdf
@out MenuItem_CLD.pdf @uri /wd/MenuItem_CLD.pdf
@out MenuPage_CLD.pdf @uri /wd/MenuPage_CLD.pdf
@out Menu_CLD.pdf @uri /wd/Menu_CLD.pdf
@out Dish_FD_IC_Output @uri /wd/dish_fd_ic.csv
@out MenuItem_FD_IC_Output @uri /wd/menuitem_fd_ic.csv
@out MenuPage_FD_IC_Output @uri /wd/menupage_fd_ic.csv
@out Menu_FD_IC_Output @uri /wd/menu_fd_ic.csv
@out Dish_New @uri /wd/dish_new.csv
@out MenuItem_New @uri /wd/menuitem_new.csv
@out MenuPage_New @uri /wd/menupage_new.csv
@out Menu_New @uri /wd/menu_new.csv
"""

# Close Project #
"""    
@end Data_Cleaning_Project
"""

