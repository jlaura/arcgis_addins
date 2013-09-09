import arcpy
import pythonaddins
import os


class LayerList(object):
    """Implementation for valuebyalpha_addin.combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWW'
        self.selectedlayer = None
    def onSelChange(self, selection):
        if selection != None:
            self.selectedlayer = selection
            createvba.enabled = True
        else:
            self.selectedlayer = None
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        #Populate the items list with the available layers
        if focused:
            self.mxd = arcpy.mapping.MapDocument("Current")
            layers = arcpy.mapping.ListLayers(self.mxd)
            self.items=[]
            if len(layers) != 0:
                for layer in layers:
                    if layer.isFeatureLayer:
                        self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class DelFeature(object):
    """Implementation for valuebyalpha_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        #Clean out the in_memory workspace.
         for x in range(createvba.c):
            arcpy.Delete_management("in_memory\\" + str(x))

class VBA(object):
    """Implementation for valuebyalpha_addin.button (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "layers")[0]
        #Progress Bar - DOES NOT WORK VIA ADDIN....
        count = int(arcpy.GetCount_management(layerlist.selectedlayer).getOutput(0))
        arcpy.SetProgressor("step", "Processing {} features".format(count), 0,count,1)

        #Pull each feature into its own in memory layer and symbolize
        self.c = 1
        with arcpy.da.SearchCursor(layerlist.selectedlayer, "*" ) as cursor:
            for r in cursor:
                try:
                    arcpy.Delete_management("in_memory\\" + str(self.c))
                except:
                    pass
                out_lyr = "in_memory\\" + str(self.c)
                arcpy.MakeFeatureLayer_management(layerlist.selectedlayer, out_lyr, "OBJECTID = " + str(self.c))
                lyr = arcpy.mapping.Layer(out_lyr)
                lyr.transparency = 85
                symbology = os.path.dirname(str(os.path.realpath(__file__))) + r"\vba_symbology.lyr"
                arcpy.ApplySymbologyFromLayer_management(lyr, symbology)
                arcpy.SetProgressorPosition(self.c)
                self.c += 1

