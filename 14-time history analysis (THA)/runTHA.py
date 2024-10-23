# ################################################################
# Please keep this notification at the beginning of the file
# 
# This code is part of an OpenSees course. 
# Only the person who purchases the course is allowed to 
# use it. Any distribution of this code is forbidden.
#
# developed by:
# 				Hadi Eslamnia
# 				Amirkabir University of Technology
# 
# contact us:
# 				Website: 			eslamnia.com
# 				Instagram: 			@eslamnia.ir
#				Telegram/Eitaa :	@eslamnia
# 				WhatsApp and call: 	+989101858874
#				Email :				opensees.eslamnia@gmail.com
# ################################################################

import os
from openseespy.opensees import *
from ReadRecord import ReadRecord
from analyzeAndAnimate import analyzeAndAnimateTHA
import vfo.vfo as vfo
# import BraineryWiz as bz
import opsvis as opsv
# import matplotlib.pyplot as plt
from doDynamicAnalysis import doDynamicAnalysis

firstRec = 1
lastRec = 3000
scaleFac = 10*9.81
TFree = 0

GMFolder = "GMFiles"
dataDir1 = "outputs/THA"
showAnimationDeform = 0 

for iRec in range(firstRec,lastRec+1):

    exec(open("model.py").read())
    exec(open("defineDamping.py").read())

    dataDir = f'{dataDir1}/{iRec}'
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)
    
    exec(open("defineRecorders.py").read())


    if not os.path.exists(f"{GMFolder}/transformed"):
        os.makedirs(f"{GMFolder}/transformed")


    inFileName = f"{GMFolder}/{iRec}.AT2"
    GMPath = f"{GMFolder}/transformed/{iRec}.txt"
    dtInput, numPoints = ReadRecord (inFileName, GMPath)
    seriesTag = 2
    timeSeries('Path', seriesTag, '-dt', dtInput, '-filePath', GMPath, '-factor', scaleFac)
    GMDir = 1
    pattern('UniformExcitation', 2, GMDir, '-accel', seriesTag)
    
    exec(open("defineRecordersAccel.py").read())

    Tmax = numPoints*dtInput + TFree

    dtAnalysis = dtInput
    nSteps = int(Tmax/dtAnalysis)


    if showAnimationDeform:
        modelName = "steelModel"
        loadCaseName = f"THA/{iRec}"
        Nmodes = 2
        vfo.createODB(model= modelName, loadcase= loadCaseName, Nmodes= Nmodes)

    print(f'iRec = {iRec} is running ...')
    
    # wipeAnalysis()
    # constraints('Transformation')
    # numberer('RCM')
    # system('BandGen')
    # test('NormDispIncr', 1e-6, 100)
    # algorithm('Newton')
    # integrator('Newmark', 0.5, 0.25)
    # analysis('Transient')
    
    doDynamicAnalysis(Tmax, dtInput)
    
    
    wipe()

    if showAnimationDeform:
        vfo.plot_deformedshape(model=modelName, loadcase=loadCaseName, scale=10)
        vfo.animate_deformedshape(model=modelName, loadcase=loadCaseName, scale=10, speedup=50, gifname="THAAnimation")
