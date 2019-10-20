import arcpy
import os
import time
import csv

"""Part One: Export the map document with the current date appended to the end of the pdf name"""
# Uses time to hold current date 
currentdate = time.strftime("%m%d%Y")

# Export FLOW_STATUS.mxd Map to PDF
                             # Update this file path with the new location of FLOW_STATUS.mxd
mxd = arcpy.mapping.MapDocument("R:/OM/Utility/Flow Status Reports/FLOW_STATUS.mxd")

print "Exporting PDF..."
                             # Update this file path with location of output pdf  
arcpy.mapping.ExportToPDF(mxd,"R:/OM/Utility/Flow Status Reports/FLOW_STATUS_"+currentdate+".pdf")

"""Part two: Output a csv where Flow_Status = 'Needs flushing' or 'Needs_jetting. This csv is connected to FLOW_STATUS.xlsx'"""
# Get 'Needs flushing' and 'Needs jetting' rows in text file
masterdata = "C:/GIS_Scheduled_Tasks/Update_Sanitary_Report/OM@GISENT.sde/GISENT.OM.SanitaryPoints"

print "Building attributes..."
# Attributes to be kept in the final spreadsheet
fields = ['ID', 'Flow_Status', 'GeneralMaintenance', 'Inspector_1', 'Inspector_2', 
'InspectionComments', 'InspectionStatus']

expression = "Flow_Status='Needs flushing' OR Flow_Status='Needs jetting'"

inputcsv = "R:/OM/Utility/Flow Status Reports/data/flowstatus.csv"

print "Writing csv..."

# Open input csv (with write access) as outputcsv
with open(inputcsv, 'w') as outputcsv:
    # Define a writer object that converts address into comma delimited strings
    writer = csv.writer(outputcsv, delimiter=',', lineterminator='\n')
    # Writes the header from the list of fields
    writer.writerow(fields) 
    # Define search cursor with data, fields, and expression
    cursor = arcpy.da.SearchCursor(masterdata,fields,expression)
    for row in cursor:
        # For each row in the cursor, write to the csv.
        writer.writerow(row)

print "Done"

