import arcpy
import pythonaddins
import numpy

class selectoverlap(object):
    """Implementation for gradientmatching_addin.select_overlap (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.ul, self.ur, self.ll, self.lr = (),(),(),()
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        print dir(rectangle_geometry.upperLeft)
        self.ul = (rectangle_geometry.upperLeft.X,rectangle_geometry.upperLeft.Y)
        self.ur = (rectangle_geometry.upperRight.X,rectangle_geometry.upperRight.Y)
        self.ll = (rectangle_geometry.lowerLeft.X, rectangle_geometry.lowerLeft.Y)
        self.lr = (rectangle_geometry.lowerRight.X, rectangle_geometry.lowerRight.Y)

class RasterLayer1(object):
    """Implementation for gradientmatching_addin.select_layer1 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.selectedlayer = None
    def onSelChange(self, selection):
        if selection != None:
            self.selectedlayer = selection
        else:
            self.selected_layer = None
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
                    if layer.isRasterLayer:
                        self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class RasterLayer2(object):
    """Implementation for gradientmatching_addin.select_layer2 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.selectedlayer = None
    def onSelChange(self, selection):
        if selection != None:
            if selection == select_layer1.selection:
                pythonaddins.MessageBox("Please select two different layers", "Error", 0)
            else:
                self.selectedlayer = selection
        else:
            self.selected_layer = None
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
                    if layer.isRasterLayer:
                        self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class GradientMatch(object):
    """Implementation for gradientmatching_addin.gradient_match (write_edits)"""
    def __init__(self):
        self.enabled = False
    def onClick(self):
        ll =  select_overlap.ll
        ur =  select_overlap.ur

        raster_arr1 = arcpy.NumPyArrayToRaster(arcpy.MakeRasterLayer_management(select_layer1.selection, 'in_memory\raster1', [ll[0], ll[1], ur[0], ur[1]]))
        raster_arr2 = arcpy.NumPyArrayToRaster(arcpy.MakeRasterLayer_management(select_layer2.selection, 'in_memory\raster2', [ll[0], ll[1], ur[0], ur[1]]))


def gradientDomainMatch(r1, r2):

    return r3
