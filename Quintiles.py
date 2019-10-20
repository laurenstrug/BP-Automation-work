import arcpy

# Input excel file
excel = "T:/GIS_Tools/ITS/Quintile/Res_Quintile_05152019.xlsx/Sheet 1$"

# Input parcels from Enterprise
parcels = "C:/Users/laurens/AppData/Roaming/ESRI/Desktop10.6/ArcCatalog/GISENT.sde/GISENT.GIS.Parcels_All"

# Output quintiles from Enterprise
#quintiles = "C:/Users/laurens/AppData/Roaming/ESRI/Desktop10.6/ArcCatalog/GISENT.sde/GISENT.ASSESS.Quintiles"
quintiles = "T:/GIS_Tools/ITS/Quintile/ASSESS@GISENT_dc.sde/GISENT.ASSESS.Quintiles"

# Process to get Quintile Year feature 
print "Creating Features..."
arcpy.TableSelect_analysis(excel,"in_memory/QuintileTable")
arcpy.MakeTableView_management("in_memory/QuintileTable","Quintile_lyr")
arcpy.MakeFeatureLayer_management(parcels,"parcels_lyr") 
arcpy.AddJoin_management("parcels_lyr","PID_NO","Quintile_lyr","GIS_Number","KEEP_COMMON")
arcpy.Dissolve_management("parcels_lyr","in_memory/QuintileDissolve",
"QuintileTable.Quintile_Year")
arcpy.AlterField_management("in_memory/QuintileDissolve","QuintileTable_Quintile_Year","Quintile_Year","Quintile_Year")

# Store current year for updating attributes
import datetime 
now = datetime.datetime.now()
current_year = now.year

# Calculate the next review year as a new field
print "Calculating..."
arcpy.AddField_management("in_memory/QuintileDissolve","Next_Review_Year", "TEXT")
with arcpy.da.UpdateCursor("in_memory/QuintileDissolve",['Quintile_Year','Next_Review_Year']) as cursor:
    for row in cursor:
        row[1] = int(row[0][-4:])
        row[0] = row[1]
        cursor.updateRow(row)
        
        # Update review year 
        if row[1] < current_year:
            row[1] = row[1] + 5
            cursor.updateRow(row)

# Delete everything from the original Enterprise dataset and append the new
arcpy.AddField_management(quintiles,"Next_Review_Year", "TEXT")
arcpy.DeleteFeatures_management(quintiles)
arcpy.Append_management("in_memory/QuintileDissolve",quintiles,"NO_TEST")

print "Finished"