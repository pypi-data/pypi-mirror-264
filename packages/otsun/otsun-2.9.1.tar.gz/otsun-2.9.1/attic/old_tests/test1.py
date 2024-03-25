import otsun
import FreeCAD
from FreeCAD import Base

otsun.create_opaque_simple_material("Mir1", 0.885)
otsun.create_opaque_simple_material("Abs1", 1 - 0.841)
otsun.create_simple_volume_material("Glass1", 1.5)

current_doc = FreeCAD.activeDocument()
sel = current_doc.Objects
current_scene = otsun.Scene(sel)
exp = otsun.Experiment(current_scene, Base.Vector(1, 1, 1), 50, 1.0, 1.0, current_doc)
exp.run(current_doc)
