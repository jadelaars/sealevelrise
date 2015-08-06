#2015-08-05
# Code for quickly getting output statistics from SLR analysis results shps




import arcpy


def list_domain(mxdPath,group_layer):
# This function builds a list of layers from our MXD, that are in the specified group layer
    mxd = arcpy.mapping.MapDocument(mxdPath)
    layers = arcpy.mapping.ListLayers(mxd)
    alayers=[]
    #print layers
    for layer in layers:
        #print layer
        if layer.isFeatureLayer:
            temp = layer.longName
            #print temp
            temp = temp.split('\\')
            if temp[0]==group_layer:
                alayers.append(layer)
    return alayers


#Set up filepaths and define variables
results_path = 'C:\\Users\\Walter\\Desktop\\Sierra\\'
counties = 'C:\\Users\\Walter\\Google Drive\\Climate Change\\GIS_files_analysis\\Jurisdictions\\CountyErase.shp'
cities = 'C:\\Users\\Walter\\Google Drive\\Climate Change\\GIS_files_analysis\\Jurisdictions\\SLRCities.shp'
cities_lyr = 'C:\\Users\\Walter\\Google Drive\\Climate Change\\GIS_files_analysis\\Jurisdictions\\SLRCities_lyr.shp'
arcpy.MakeFeatureLayer_management(cities,cities_lyr)
city_names = ['CITY OF CAPITOLA','CITY OF WATSONVILLE','CITY OF SANTA CRUZ','MARINA','MONTEREY','SAND CITY','SEASIDE']
county_names = ['Monterey','Santa Cruz']
####
mxdpath = 'C:\\Users\\Walter\\Desktop\\Sierra\\PythonResultsMap2.mxd'
sectors = list_domain(mxdpath,'RESULTS')
####
arcpy.env.workspace = mxdpath
chps = ['RT_2030_S2','RT_2060_S2','RT_2060_S3','RT_2100_S2','RT_2100_S3',
        'CF_2030_S2','CF_2060_S2','CF_2060_S3','CF_2100_S2','CF_2100_S3',
        'CN_2030_S2','CN_2060_S2','CS_2060_S3','CN_2100_S2','CS_2100_S3',
        'DN_2030_S2','DN_2060_S2','DS_2060_S3','DN_2100_S2','DS_2100_S3',
        'DN_2010','RT_2010','CF_2010','CN_2010','FEMA']


### HERE we can define if we want city or county results.
#Uncomment the one you want and comment out the one you don't. 
#FOR EACH CITY
for name in city_names:

#FOR EACH COUNTY
##for name in couty_names:

    with open(results_path+name+'.csv','a') as f:
#open file with following header
        f.write('SECTORS,RT_2030_S2,RT_2060_S2,RT_2060_S3,RT_2100_S2,'\
                'RT_2100_S3,CF_2030_S2,CF_2060_S2,CF_2060_S3,CF_2100_S2,CF_2100_S3,'\
                'CN_2030_S2,CN_2060_S2,CS_2060_S3,CN_2100_S2,CS_2100_S3,'\
                'DN_2030_S2,DN_2060_S2,DS_2060_S3,DN_2100_S2,DS_2100_S3,'\
                'DN_2010,RT_2010,CF_2010,CN_2010,FEMA')
        f.write('\n')
#Select by attribute, the city we want to get results in
        query = """ "CITY_DESC" = '"""+name+"""'"""
        print 'Select City'
        arcpy.SelectLayerByAttribute_management(cities_lyr,'NEW_SELECTION',query)



#Now iterate through the sector features
        for sector in sectors:
            s = str(sector).split('\\')[-1]
            print s
            line = s+','

#Then for each sector we want to iterate through the coastal hazard processes. This is considered a nested loop. 
            for chp in chps:
                #query2 = '"'+chp+'"= 1'
                print 'Select CHP: '+chp
                arcpy.SelectLayerByLocation_management(sector,'HAVE_THEIR_CENTER_IN',cities_lyr,selection_type='NEW_SELECTION')
                arcpy.SelectLayerByAttribute_management(sector,'SUBSET_SELECTION','"'+chp+'"= 1')

#### So beyond here we can define our output metrics, just highlight & uncomment (Alt-4) the block you want to use #####

    #### Points ####

##                count=0
##                count = arcpy.GetCount_management(sector) #use this for counting points


    #### Areas (polygons) ####            
##                count = 0  
##                field = "area_ac"
##                with arcpy.SearchCursor(sector) as cursor:
##                    for row in cursor:
##                        count = count + row.GetValue(field)

    #### Lengths (lines) ####
##                count=0
##                field = "len_ft"
##                with arcpy.SearchCursor(sector) as cursor:
##                    for row in cursor:
##                        count = count + row.GetValue(field)
                
                print chp+': '+str(count)
                line = line+str(count)+','
                arcpy.SelectLayerByAttribute_management(sector,'CLEAR_SELECTION')

                
# Finally write a line of output data for each CHP to the csv file we opened                
            f.write(line+'\n')
            print 'Line added to file'
            print line

    

           

                
                

    













