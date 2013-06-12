import arcpy
import pythonaddins
from collections import deque

class DrawLine(object):
    """Implementation for contour_attributor.drawline (Tool)"""
    def __init__(self):
        self.enabled = False
        self.shape = "Line"
        self.intersecting_contours = deque()
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
    def onLine(self, line_geometry):
        #Reset the deque to ensure that sequential selections without a write are not pushed to the table.
        self.intersecting_contours = deque()
        intersection_order = {}
        startpt = arcpy.Geometry("point", arcpy.Point(line_geometry.firstPoint.X, line_geometry.firstPoint.Y),arcpy.Describe(select_layer.selectedlayer).spatialReference )
        with arcpy.da.SearchCursor(arcpy.SelectLayerByLocation_management(select_layer.selectedlayer, 'intersect', line_geometry), ['OID@','Shape@']) as cursor:
            for row in cursor:
                distance = startpt.distanceTo(row[1])
                intersection_order[distance] = row[0]
        for key in sorted(intersection_order.iterkeys()):
            self.intersecting_contours.append(intersection_order[key])

class PolyLineLayers(object):
    """Implementation for contour_attributor.select_layer (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.selectedlayer = None
    def onSelChange(self, selection):
        if selection != None:
            self.selectedlayer = selection
            #enable the drawline tool if we have a valid layer
            drawline.enabled = True
            select_field.enabled = True
            contour_start.enabled = True
            contour_interval.enabled = True
            write_edits.enabled = True
            pythonaddins.MessageBox('If you have not already, please start an edit session on the selected layer.', "Info", 0)
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
                    if layer.isFeatureLayer:
                        self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class PolylineFieldEditor(object):
    """Implementation for contour_attributor.select_field (select_field)"""
    def __init__(self):
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.selectedfield = None
    def onSelChange(self, selection):
        if selection != None:
            self.selectedfield = selection
        else: self.selectedfield = None
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        layer = select_layer.selectedlayer
        self.items = []
        fields = arcpy.ListFields(layer)
        for field in fields:
            self.items.append(field.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ContourStart(object):
    """Implementation for contour_attributor.contour_start (contour_start)"""
    def __init__(self):
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        contourstart = None
    def onSelChange(self, selection):
        pass
    def onEditChange(self, text):
        try:
            self.contourstart = float(text)
        except:
            pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ContourInterval(object):
    """Implementation for contour_attributor.contour_start (contour_interval)"""
    def __init__(self):
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.interval = None
    def onSelChange(self, selection):
        pass
    def onEditChange(self, text):
        try:
            self.interval = float(text)
        except:
            pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class WriteEdits(object):
    """Implementation for contour_attributor.write_edits (write_edits)"""
    def __init__(self):
        self.enabled = False
    def onClick(self):
        startval = contour_start.contourstart
        interval = contour_interval.interval
        if len(drawline.intersecting_contours) == 0:
            pythonaddins.MessageBox("Please select one or more contour lines to attribute", "Info", 0)
        #Update cursor to write the intervals
        while len(drawline.intersecting_contours) != 0:
            contour = drawline.intersecting_contours.popleft()
            try:
                with arcpy.da.UpdateCursor(select_layer.selectedlayer, ['OID@', select_field.selectedfield],""""OBJECTID" = {}""".format(contour)) as cursor:
                    for row in cursor:
                        row[1] = startval
                        cursor.updateRow(row)
                    startval += interval
            except:
                with arcpy.da.UpdateCursor(select_layer.selectedlayer, ['FID', select_field.selectedfield],""""FID" = {}""".format(contour)) as cursor:
                    for row in cursor:
                        row[1] = startval
                        cursor.updateRow(row)
                    startval += interval

