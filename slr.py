"""
This will serve as the primary analysis for CCWG SLR Project
Creator: Jason Adelaars (jadelaars@mlml.calstate.edu

Will process all infrastructure shps against all hazards


What you need to do to set this up....

1. Create an MXD with all your hazard layers in one group layer and all your sectors in another
   - I recommend separating the sector shapefiles into group layers based on their vector type (ie points, lines, polygons). Because
   - each analysis is going to be different based on their vector type.
2. Create a dump directory folder and update the 'dump_dir' path below. This folder will hold intermediate files and be deleted later
3. Also create a results directory folder and update the 'results_dir' path below. this folder will hold you final layer.
4. ..to be continued..

"""


import arcpy, gc, os

#global variable (our 20 scenarios)
scenarios = ['RT_2030_S2','RT_2060_S2','RT_2060_S3','RT_2100_S2','RT_2100_S3',
             'CF_2030_S2','CF_2060_S2','CF_2060_S3','CF_2100_S2','CF_2100_S3',
             'CN_2030_S2','CN_2060_S2','CS_2060_S3','CN_2100_S2','CS_2100_S3',
             'DN_2030_S2','DN_2060_S2','DS_2060_S3','DN_2100_S2','DS_2100_S3']

def scen():
        #return list of scenarios
        global scenarios
        return scenarios
        
       



def list_domain(mxdPath,domain):
# Build a list of layers from our MXD, that are in the 'IMPACTED LAYERS' group layer
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
                        if temp[0]==domain:
                                alayers.append(layer)

        return alayers


			
def reset(layer):
        #reset scenario attribute fields with 0
        global scenarios         
        for haz in scenarios:
                arcpy.CalculateField_management(layer,haz,"0")

#poly tool tested as of 2015-08-03
#To Do: merge all original (even those not impacted) features to resulting file
def poly(layer,scen):
        
        dump_dir = "C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis\\dump_dir"
        results_dir = "C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis\\RESULTS\\"

        
        layerS = str(layer).split('\\')[-1]
        results_shp = results_dir+layerS+'.shp'
        print results_shp
        union_list=[]
        field_list=[]
        del_list=[]
        for sce in scen:
                
                sc = str(sce).split("\\")[1]
                print 'Next Scenario: '+ sc
                outfile = dump_dir+'\\'+sc+"_clp.shp"
                outfilemp = dump_dir+'\\'+sc+"_mp.shp"
                outfilelyr = dump_dir+'\\'+sc+"_lyr.shp"
                if 'RT' in sc or 'CF' in sc:
                        print "RT or CF"
                        arcpy.SelectLayerByAttribute_management(sce,"NEW_SELECTION",""" "Connect2" = 'connected' """)
                print 'Start Clip'
                arcpy.Clip_analysis(layer,sce, outfile)
                del_list.append(outfile)
                print 'Explode'
                arcpy.MultipartToSinglepart_management(outfile,outfilemp)
                del_list.append(outfilemp)
                print 'Make Feature Layer'
                arcpy.MakeFeatureLayer_management(outfilemp,outfilelyr)
                del_list.append(outfilelyr)
                result = arcpy.GetCount_management(outfilemp)
                if result>0:
                        print 'Number of features: ',result
                        union_list.append(outfilemp)
                        print 'Add Field'
                        arcpy.AddField_management(outfilelyr,sc,'SHORT')
                        print 'Calculate Field'
                        arcpy.CalculateField_management(outfilelyr,sc,1)
                        arcpy.SelectLayerByAttribute_management(outfilelyr, "CLEAR_SELECTION")
                        arcpy.SelectLayerByAttribute_management(sce, "CLEAR_SELECTION")

                else:
                        field_list.append(sc)
                                
               
                        
        print 'UNION: saved to: '+dump_dir
        arcpy.env.extent = "MAXOF"
        arcpy.Union_analysis(union_list,dump_dir+'\\union.shp','ALL')
        print 'Deleting unnecessary fields'
        fieldList = arcpy.ListFields(dump_dir+'\\union.shp')
        for field in fieldList[2:]:
                if field.name not in scenarios:
                        arcpy.DeleteField_management(dump_dir+'\\union.shp',field.name)
        
        for i in field_list:
                arcpy.AddField_management(dump_dir+'\\union.shp',i,'SHORT')
                       
        print 'Joining Tables'
        arcpy.SpatialJoin_analysis(target_features=dump_dir+'\\union.shp',
                                   join_features=layer,
                                   out_feature_class=results_dir+'\\'+layerS+'.shp',
                                   join_operation="JOIN_ONE_TO_ONE",
                                   join_type="KEEP_ALL",
                                   match_option="HAVE_THEIR_CENTER_IN")
        print 'Delete temp files'
        for f in del_list:
                arcpy.Delete_management(f)
        arcpy.Delete_management(dump_dir+'\\union.shp')

        print 'All DONE!!!'


#incomplete, still working out the bugs as of 2015-07-23

def line(layer,scen):
        
        dump_dir = "C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis\\dump_dir"
        results_dir = "C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis\\RESULTS\\"

        
        layerS = str(layer).split('\\')[-1]
        results_shp = results_dir+layerS+'.shp'
        print results_shp
        union_list=[]
        field_list=[]
        for sce in scen:
                
                sc = str(sce).split("\\")[1]
                print 'Next Scenario: '+ sc
                outfile = dump_dir+'\\'+sc+"_clp.shp"
                outfilemp = dump_dir+'\\'+sc+"_mp.shp"
                outfilelyr = dump_dir+'\\'+sc+"_lyr.shp"
                if 'RT' in sc or 'CF' in sc:
                        print "RT or CF"
                        arcpy.SelectLayerByAttribute_management(sce,"NEW_SELECTION",""" "Connect2" = 'connected' """)
                print 'Start Clip'
                arcpy.Clip_analysis(layer,sce, outfile)
                print 'Explode'
                arcpy.MultipartToSinglepart_management(outfile,outfilemp)
                print 'Make Feature Layer'
                arcpy.MakeFeatureLayer_management(outfilemp,outfilelyr)
                result = arcpy.GetCount_management(outfilemp)
                if result>0:
                        print 'Number of features: ',result
                        union_list.append(outfilemp)
                        print 'Add Field'
                        arcpy.AddField_management(outfilelyr,sc,'SHORT')
                        print 'Calculate Field'
                        arcpy.CalculateField_management(outfilelyr,sc,1)
                        arcpy.SelectLayerByAttribute_management(outfilelyr, "CLEAR_SELECTION")
                        arcpy.SelectLayerByAttribute_management(sce, "CLEAR_SELECTION")
                        
                else:
                        field_list.append(sc)
                
               
                        
        print 'UNION: saved to: '+dump_dir
        arcpy.env.extent = "MAXOF"
        arcpy.Merge_management(union_list,dump_dir+'\\merge.shp','ALL')

        for i in field_list:
                arcpy.AddField_management(dump_dir+'\\merge.shp',i,'TEXT')

        print 'Joining Tables'
        arcpy.SpatialJoin_analysis(dump_dir+'\\merge.shp',layer,results_shp,"JOIN_ONE_TO_ONE","KEEP_ALL","SHARE_A_LINE_SEGMENT_WITH")                
        print 'Delete dump folder'
        arcpy.Delete_management(dump_dir)
        print 'Create new dump folder'
        arcpy.CreateFolder_management("C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis",'dump_dir')
        print 'All DONE!!!'

#point tool tested and complete as of 2015-08-03     
def point(layer,scen):
        
        dump_dir = "C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis\\dump_dir"
        results_dir = "C:\\Users\\jadelaars\\Desktop\\SLR\\Analysis\\RESULTS\\"
        
        layerS = str(layer).split('\\')[-1]
        results_shp = results_dir+layerS+'.shp'
        lyr = results_dir+layerS+'_lyr.shp'
        print 'Copy Feature: '+layerS
        arcpy.CopyFeatures_management(layer,results_shp)
        arcpy.MakeFeatureLayer_management(results_shp,lyr)
        
        for sce in scen:
                sc = str(sce).split("\\")[1]
                print sc
                print sce
                
                
                print 'Add Field'
                arcpy.AddField_management(lyr,sc,'SHORT')
                if 'RT' in sc or 'CF' in sc:
                        print "RT or CF"
                        arcpy.SelectLayerByAttribute_management(sce,"NEW_SELECTION",""" "Connect2" = 'connected' """)
                        print 'Calculating: ',val
                arcpy.SelectLayerByLocation_management(lyr,'INTERSECT',sce)
                print 'Calculate Field'
                val = arcpy.GetCount_management(lyr)
                print 'Calculating: ',val
                arcpy.CalculateField_management(lyr,sc,1)
                arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")
                arcpy.SelectLayerByAttribute_management(sce, "CLEAR_SELECTION")


        

        



