import sys
#sys.path.append("D:Ramon_2015/RECERCA/RETOS-2015/Tareas/Proves-FreeCAD-2") # change for your path
import otsun
import FreeCAD
from FreeCAD import Base
import Part
import time
import numpy as np
reload(otsun)
doc = FreeCAD.ActiveDocument
otsun.create_opaque_simple_material("opa1", 0.0)
otsun.create_absorber_lambertian_layer('lamb1', 0.0)
otsun.create_two_layers_material("Abs1", "lamb1", "opa1")
otsun.create_two_layers_material("Opa1", "opa1", "opa1")
#raytrace.create_simple_volume_material("Glass1", 1.5)
file_BK7 = './BK7.txt'
otsun.create_wavelength_volume_material("Glass1", file_BK7)
#file_AR = 'D:Ramon_2015/RECERCA/RETOS-2015/Tareas/Proves-FreeCAD-2/materials-PV/AR.txt'
#raytrace.create_polarized_coating_transparent_layer("file_AR", file_AR, file_BK7)
#raytrace.create_two_layers_material("AR1","file_AR","file_AR")

sel = doc.Objects
current_scene = otsun.Scene(sel)
phi_ini = 0
phi_end = 0
phi_end = phi_end + 0.00001
phi_step = 0.1
theta_ini = 0
theta_end = 0
theta_end = theta_end + 0.00001
theta_step = 2
number_photons = 800
aperture_collector = 100. * 100.
data_file_spectrum = './ASTMG173-direct.txt'
light_spectrum = otsun.cdf_from_pdf_file(data_file_spectrum)
outfile = open('./kk.txt', 'w')
t0 = time.time()
for ph in np.arange(phi_ini, phi_end, phi_step):
    for th in np.arange(theta_ini, theta_end, theta_step):
        main_direction = otsun.polar_to_cartesian(ph, th) * -1.0 # Sun direction vector
        emitting_region = otsun.SunWindow(current_scene, main_direction)
        l_s = otsun.LightSource(current_scene, emitting_region, light_spectrum, 1.0)
        exp = otsun.Experiment(current_scene, l_s, number_photons)
        exp.run()
        efficiency = (exp.captured_energy /aperture_collector ) / (exp.number_of_rays/exp.light_source.emitting_region.aperture)
        t1 = time.time()
        print ("%s %s %s %s" % (ph, th, efficiency, t1-t0)+ '\n')
        outfile.write("%s %s %s %s" % (ph, th, efficiency, t1-t0)+ '\n')

outfile.close()