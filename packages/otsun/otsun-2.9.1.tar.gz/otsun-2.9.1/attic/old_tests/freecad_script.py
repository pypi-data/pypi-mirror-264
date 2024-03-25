import sys

FREECADPATH_1='C:\\Program Files\\FreeCAD 0.16\\bin' # adapt this path to your system

sys.path.append(FREECADPATH_1)

FREECADPATH_2 ='C:\\Program Files\FreeCAD 0.16\\Mod'

sys.path.append(FREECADPATH_2)

FREECADPATH_3 ='C:\\Program Files\FreeCAD 0.16\\Mod\\Part'

sys.path.append(FREECADPATH_3)

FREECADPATH_4 ='D:\\RAMON_2015\\RECERCA\\RETOS-2015\\Tareas\\Proves-FreeCAD-2'

sys.path.append(FREECADPATH_4)

import FreeCAD as App

#PATH = 'D:\\RAMON_2015\\RECERCA\\RETOS-2015\\Tareas\\Proves-FreeCAD-2\\FreeCADMacros\\test_PTC.FCStd'

PATH = 'D:\\RAMON_2015\\RECERCA\\RETOS-2015\\Tareas\\Proves-FreeCAD-2\\FreeCADMacros\\test_Fresnel-3.FCStd'

App.openDocument(PATH)

#execfile("D:\\Ramon_2015\\RECERCA\\RETOS-2015\\Tareas\\Proves-FreeCAD-2\\exec_test_complete_PTC.py")

#execfile("D:\\Ramon_2015\\RECERCA\\RETOS-2015\\Tareas\\Proves-FreeCAD-2\\exec_test_Fresnel.py")

execfile("D:\\Ramon_2015\\RECERCA\\RETOS-2015\\Tareas\\Proves-FreeCAD-2\\exec_test_Fresnel_Wavelength.py")
