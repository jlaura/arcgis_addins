import arcpy
import pythonaddins

class AbundanceField(object):
    """Implementation for gamma_model.abundance_combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = False
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        if selection != None:
	    self.selectedfield = selection
	    solveonce_button.enabled = True
	else:
	    self.selectedfield = None
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        #Get the selected layer from the layer combobox
	layer = input_combobox.selectedlayer
	fields = arcpy.ListFields(layer)
	self.items = [f.name for f in fields]
    def onEnter(self):
        pass
    def refresh(self):
        pass

class InputShapefile(object):
    """Implementation for gamma_model.input_combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
	self.selectedlayer = None
    def onSelChange(self, selection):
	if selection != None:
	    self.selectedlayer = selection
	    abundance_combobox.enabled = True
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        if focused:
	    self.mxd = arcpy.mapping.MapDocument("Current")
	    layers = arcpy.mapping.ListLayers(self.mxd)
	    self.items = []
	    if len(layers) != 0:
		for layer in layers:
		    if layer.isFeatureLayer:
			self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ModelIteratively(object):
    """Implementation for gamma_model.modeliter_button (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
        pass

class SolveOnce(object):
    """Implementation for gamma_model.solveonce_button (Button)"""
    def __init__(self):
        self.enabled = False
        self.checked = False
    def onClick(self):
	"""Offload all processing to an external script"""
        pass