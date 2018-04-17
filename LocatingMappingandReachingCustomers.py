#GEO443_FinalScript_HaynesKD
#Keelin Haynes
#Geo 443
#May 3, 2017
#This script will locate kroger stores within a LBRS dataset, create a buffer
# around them, select all homes and bussinesses within that buffer,
# and create a mailing list containing thte addresses

#In order for this to be as usable as possible with as little user input as possible, this will create all items with generic terms. i.e. No county identifying information will be
#contained in it. Your outputs will by: "Kroger", "Kroger_Buffer", and "Applicable_Addresses".
#Thus, if you need to run multiple counties, you will need to go into the output folder and either rename each dataset with county identifying info (e.g. "Muskingum_Kroger")
#or you gather the mailing addresses of one county before moving on to the next


#This imports the necessary modules
import arcpy
import arcpy.da

#You will need to enter your workspace below!!
#^!
#^!
#^!

#This sets up the workspace location
arcpy.env.workspace = r"F:\1PythonFinalProject\WASHINGTONLBRS"
print "The workspace is " + arcpy.env.workspace + "\n"

#This allows outputs to be overwritten
arcpy.env.overwriteOutput = True
print "Outputs will be overwritten \n"

#This sets up a try block
try:
    #This sets up a search cursor that will list all of the Krogers in the dataset
    #SearchCursor(in_table, field_names,
    #{where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause})
    #You will need to enter the location of your data below!!
    #^!
    #^!
    #^!
    seacurin = r"F:\1PythonFinalProject\WASHINGTONLBRS\WAS_ADDS.shp"
    with arcpy.da.SearchCursor (seacurin, ("COMMENT", "LSN", "USPS_CITY", "STATE", "ZIPCODE"), '"COMMENT" = \'KROGER\'') as cursor:
        #This creates a for loop to iterate through all of the files in the LBRS data
        for row in cursor:
            
            #This tells the user the address of any Krogers in the data
            print ("Kroger Address: " + row[1]+ " "+ row[2]+ " "+ row[3]+ " "+ row[4])
            print " "
            
            #This creates a temporary feature layer of selected points in the data set
            #MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info}
            #You will need to enter the location where you either have or want your "output" folder to be located below!!
            #^!
            #^!
            #^!
            outputfeature = r"F:\1PythonFinalProject\Outputs\Kroger_location"
            arcpy.MakeFeatureLayer_management(seacurin, outputfeature, '"COMMENT" = \'KROGER\'')
            print "A feature layer was just created. \n"

            #This creates a shapefile of the above selection
            #CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})
            arcpy.CopyFeatures_management(outputfeature, r"f:\1PythonFinalProject\Outputs\Kroger.shp")
            print "A shapefile of the above feature layer was created \n"

            #This sets up variables to be used for a buffer
            #Buffer_analysis (in_features, out_feature_class, buffer_distance_or_field,
            #{line_side}, {line_end_type}, {dissolve_option}, {dissolve_field}, {method})
            buffin = r"F:\1PythonFinalProject\Outputs\Kroger.shp"
            buffout = r"F:\1PythonFinalProject\Outputs\Kroger_Buffer.shp"
            buffdist = "1 Mile"
            

            #This creates a buffer of 1 mile around the shapefiles created above
            arcpy.Buffer_analysis(buffin, buffout, buffdist)
            print "A buffer of 1 mile was created around the above shapefile (Kroger location) \n"
            
            #This will create a feature layer of the LBRS data to be used for a location query
            #MakeFeatureLayer_management (in_features, out_layer, {where_clause}, {workspace}, {field_info}
            temp_LBRS_Data_Layer = arcpy.MakeFeatureLayer_management(seacurin, r"F:\1PythonFinalProject\Outputs\LBRS_Temp_Layer.shp")
            print "A a feature layer of the LBRS data to be used for a location query was just created \n"

            #This sets up variables to be used for a select by location function
            #SelectLayerByLocation_management (in_layer, {overlap_type}, {select_features},
            #{search_distance}, {selection_type}, {invert_spatial_relationship})
            sellocin = temp_LBRS_Data_Layer
            selloctype = "Within"
            sellocselfeature = buffout

            #This performs a select by location (In this case those LBRS points within the buffer)
            selloc = arcpy.SelectLayerByLocation_management(sellocin, selloctype, sellocselfeature)
            print "A select by location (In this case those LBRS points within the buffer) was just performed \n"

            #This creates a shapefile of the above selection
            #CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})
            arcpy.CopyFeatures_management(selloc, r"F:\1PythonFinalProject\Outputs\Applicable_Addresses")
            print "A shapefile of the above selection was just created \n"

            #This adds a new field to the attribute table of the above selection
            #AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias},
            #{field_is_nullable}, {field_is_required}, {field_domain})
            arcpy.AddField_management(r"F:\1PythonFinalProject\Outputs\Applicable_Addresses.shp", "Address", "TEXT")
            print "A new field to the attribute table of the above selection was just added. \n"

            #This populates the newly created field
            #UpdateCursor (in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause}
            with arcpy.da.UpdateCursor(r"F:\1PythonFinalProject\Outputs\Applicable_Addresses.shp", ("LSN", "USPS_CITY", "STATE", "ZIPCODE", "Address")) as cursor:
                #This creates a counter
                cntr = 1
                #This creates a for loop
                for row in cursor:
                    #This creates an if statement that updates the Address field with the concatenation of the other selected fields
                    if row[4] == "":
                        row[4] = row[0] + " " + row[1] + ", " + row[2] + " " + row[3]
                    cursor.updateRow(row)
                    print ("Record number " +str(cntr) +" updated. It now says " + row[4])
                    cntr = cntr +1

            print "\n \n You now a list of addresses within 1 mile of the kroger location in your chosen county. The addresses are contained in a field that is located in the attribute table of the dataset."
            print "\n Have a great day"

except Exception as e:
    print (e.message)
