import arcpy
import time 

""" New World Public Safety GIS Sync data prep"""
"""Part I: Backup the current data"""
current_date = time.strftime("%m_%Y")
# Enterprise geodatabase (bp-nwpsdb) eventually, for now, file geodatabase
arcpy.env.workspace = "T:/GIS_Tools/ITS/NWPS_Sync/NWPS1.gdb"

print "Backing up NWPS enterprise geodatabase..."
backup_gdb = arcpy.CreateFileGDB_management("T:/GIS_Tools/ITS/NWPS_Sync","NWPS_"+current_date+"_bak") 

# Import Address Points and Street Centerlines from bp-nwpsdb to the backup gdb
arcpy.FeatureClassToGeodatabase_conversion(['AddressPoints','StreetCenterlines'], backup_gdb)

"""Part II: Update the NWPS datasets"""
# Datasets from GISENT
address_data = "T:/GIS_Tools/ITS/NWPS_Sync/PLN@GISENT_dc.sde/GISENT.PLN.AddressPoints/GISENT.PLN.AddressPoints"
centerlines_data = "T:/GIS_Tools/ITS/NWPS_Sync/GIS@GISENT_dc.sde/GISENT.GIS.StreetCenterlines"

print "Deleting  AddressPoints and StreetCenterlines records in NWPS..."
arcpy.DeleteFeatures_management("T:/GIS_Tools/ITS/NWPS_Sync/NWPS1.gdb/AddressPoints")
arcpy.DeleteFeatures_management("T:/GIS_Tools/ITS/NWPS_Sync/NWPS1.gdb/StreetCenterlines")

# Append unique addresses to NWPS from GISENT 
print "Updating Address Points..."
arcpy.MakeFeatureLayer_management(address_data,"address_lyr")
arcpy.SelectLayerByAttribute_management("address_lyr", "NEW_SELECTION", " [UniqueAddress] = 'y' ")
arcpy.Append_management("address_lyr",'AddressPoints',"NO_TEST")

# Append GISENT street centerlines to NWPS. 
print "Updating Street Centerlines..."
arcpy.MakeFeatureLayer_management(centerlines_data,"centerline_lyr")


# Field mapping: 
    # - remove four ADR_ fields
    # - map four T_ADR to ADR_
    # - add mappings for CITY (to CTU) and COUNTY
Field_Map = """ROUTE_ID \"Route ID\" true true false 16 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ROUTE_ID,-1,-1;\
UNIQUE_ID \"Feature Unique ID\" true true false 43 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,UNIQUE_ID,-1,-1;\
ROUTE_SYS \"Route System\" true true false 2 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ROUTE_SYS,-1,-1;\
ROUTE_DIR \"Route Direction\" true true false 1 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ROUTE_DIR,-1,-1;\
DIR_RTE_ID \"DirectionalRouteID\" true true false 32 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,DIR_RTE_ID,-1,-1;\
LOC_STATE \"Local State\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,LOC_STATE,-1,-1;\
PRIME_STAT \"Primary Status\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,PRIME_STAT,-1,-1;\
ST_PRE_MOD \"Street Pre Modifier\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_PRE_MOD,-1,-1;\
ST_PRE_DIR \"Street Pre Directional\" true true false 9 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_PRE_DIR,-1,-1;\
ST_PRE_TYP \"StreetPreType\" true true false 24 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_PRE_TYP,-1,-1;\
ST_NAME \"StreetName\" true true false 42 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_NAME,-1,-1;\
ST_POS_TYP \"StreetPostType\" true true false 15 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_POS_TYP,-1,-1;\
ST_POS_DIR \"StreetPostDirectional\" true true false 9 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_POS_DIR,-1,-1;\
ST_POS_MOD \"Street Post Modifier\" true true false 12 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_POS_MOD,-1,-1;\
ST_CONCAT \"Concatenated Street\" true true false 150 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_CONCAT,-1,-1;\
ST_CON_ABR \"ST_CON_ABR\" true true false 100 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_CON_ABR,-1,-1;\
ST_NAME_A1 \"AltName1\" true true false 150 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_NAME_A1,-1,-1;\
ST_NAME_A2 \"AltName2\" true true false 150 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_NAME_A2,-1,-1;\
ST_NAME_A3 \"AltName3\" true true false 150 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ST_NAME_A3,-1,-1;\
T_ADR_FR_L \"Left From Theoretical\" true true false 4 Long 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ADR_FR_L,-1,-1;\
T_ADR_TO_L \"Left To Theoretical\" true true false 4 Long 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ADR_TO_L,-1,-1;\
T_ADR_FR_R \"Right From Theoretical\" true true false 4 Long 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ADR_FR_R,-1,-1;\
T_ADR_TO_R \"Right To Theoretical\" true true false 4 Long 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ADR_TO_R,-1,-1;\
ZIP_L \"LeftZIP\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ZIP_L,-1,-1;\
ZIP_R \"RightZIP\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ZIP_R,-1,-1;\
CITYID_L \"LeftCityID\" true true false 10 Text 0 0 ,First,#;CITYID_R \"RightCityID\" true true false 10 Text 0 0 ,First,#;\
CITY_L \"LeftCity\" true true false 50 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,CTU_NAME_L,-1,-1;\
CITY_R \"RightCity\" true true false 50 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,CTU_NAME_R,-1,-1;\
COUNTY_L \"County Code Left\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,CO_NAME_L,-1,-1;\
COUNTY_R \"County Code Right\" true true false 10 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,CO_NAME_R,-1,-1;\
STATE_L \"LeftState\" true true false 2 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,STATE_L,-1,-1;\
STATE_R \"RightState\" true true false 2 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,STATE_R,-1,-1;\
PARITY_L \"LeftParity\" true true false 1 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,PARITY_L,-1,-1;\
PARITY_R \"RightParity\" true true false 1 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,PARITY_R,-1,-1;\
ELEV_FROM \"FromElevation\" true true false 2 Short 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ELEV_FROM,-1,-1;\
ELEV_TO \"ToElevation\" true true false 2 Short 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ELEV_TO,-1,-1;\
ONEWAY \"OneWay\" true true false 1 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ONEWAY,-1,-1;\
SPEED_IMP \"ImpedenceSpeed\" true true false 2 Short 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,SPEED_IMP,-1,-1;\
EMERG_ACC \"EmergencyAccessOnly\" true true false 3 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,EMERG_ACC,-1,-1;\
SPEEDLIMIT \"Speed Limit\" true true false 2 Short 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,SPEEDLIMIT,-1,-1;\
ROUTE_NAME \"RouteName\" true true false 30 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ROUTE_NAME,-1,-1;\
ROUTE_NUM \"RouteNumber\" true true false 5 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,ROUTE_NUM,-1,-1;\
ESZ_L \"Emergency Service Left\" true true false 5 Text 0 0 ,First,#;\
ESZ_R \"Emergency Service Right\" true true false 5 Text 0 0 ,First,#;\
MSAG_C_L \"MSAG Community Left\" true true false 30 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,MSAG_C_L,-1,-1;\
MSAG_C_R \"MSAG Community Right\" true true false 30 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,MSAG_C_R,-1,-1;\
PSAP_L \"PSAP Left\" true true false 25 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,PSAP_L,-1,-1;\
PSAP_R \"PSAP Right\" true true false 25 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,PSAP_R,-1,-1;\
STATUS \"Status\" true true false 15 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,STATUS,-1,-1;\
ACT_DATE \"ActiveDate\" true true false 8 Date 0 0 ,First,#;\
RET_DATE \"RetiredDate\" true true false 8 Date 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,RET_DATE,-1,-1;\
EDITED_BY \"last_edited_user\" true true false 25 Text 0 0 ,First,#;\
EDITED_DT \"last_edited_date\" true true false 8 Date 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,EDITED_DT,-1,-1;\
SOURCE \"Source Of Data\" true true false 25 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,SOURCE,-1,-1;\
FNCT_CLASS \"FunctionalClass\" true true false 4 Long 0 0 ,First,#;\
REG_CLASS \"RegionalClass\" true true false 4 Long 0 0 ,First,#;\
SURF_TYPE \"Surface Type\" true true false 32 Text 0 0 ,First,#,T:\\GIS_Tools\\ITS\\NWPS_Sync\\GIS@GISENT_dc.sde\\GISENT.GIS.StreetCenterlines,SURF_TYPE,-1,-1;\
STREET_CD \"street_cd\" true true false 4 Long 0 0 ,First,#;SHAPE_Length \"SHAPE_Length\" false true true 8 Double 0 0 ,First,#"""

arcpy.Append_management("centerline_lyr",'StreetCenterlines',"NO_TEST",Field_Map)

# Update field syntaxes
print "Updating street centerline field syntaxes..."
stpostyp_expression = '!ST_POS_TYP!.replace("Avenue","Ave").replace("Bay","Bay").replace("Boulevard","Blvd").replace("Chase","Chase").replace("Circle","Cir").replace("Court","Ct").replace("Crescent","Cres").replace("Crossing","Xing").replace("Drive","Dr").replace("Garden","Gdn").replace("Gardens","Gdns").replace("Highway","Hwy").replace("Knoll","Knl").replace("Lane","Ln").replace("Parkway","Pkwy").replace("Place","Pl").replace("Railroad","Railroad").replace("Ridge","Rdg").replace("Road","Rd").replace("Street","St").replace("Terrace","Ter").replace("Trail","Tr").replace("Way","Way")'
stposdir_expression = '!ST_POS_DIR!.replace("North","N").replace("West","W").replace("Southeast","SE")'
stpretyp_expression = '!ST_PRE_TYP!.replace("County Road","CORD").replace("Highway","HWY").replace("Interstate","I")'
arcpy.CalculateField_management('StreetCenterlines', "ST_POS_TYP", stpostyp_expression, "PYTHON_9.3")
arcpy.CalculateField_management('StreetCenterlines', "ST_POS_DIR", stposdir_expression, "PYTHON_9.3")
arcpy.CalculateField_management('StreetCenterlines', "ST_PRE_TYP", stpretyp_expression, "PYTHON_9.3")

print "Finished!"