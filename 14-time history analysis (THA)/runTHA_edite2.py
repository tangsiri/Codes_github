# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 12:09:00 2024

@author: pc22
"""

import os
from openseespy.opensees import *
from ReadRecord import ReadRecord
from analyzeAndAnimate import analyzeAndAnimateTHA
import vfo.vfo as vfo
import opsvis as opsv
from doDynamicAnalysis import doDynamicAnalysis

firstRec = 1
lastRec = 3000
scaleFac = 10 * 9.81
TFree = 0

GMFolder = "GMFiles"
dataDir1 = "outputs/THA"
showAnimationDeform = 0 

# لیست برای ذخیره ایندکس‌های ورودی‌های ناموفق
failed_records = []

for iRec in range(firstRec, lastRec + 1):
    try:
        exec(open("model.py").read())
        exec(open("defineDamping.py").read())

        dataDir = f'{dataDir1}/{iRec}'
        
        # بررسی اینکه آیا پوشه وجود دارد یا نه
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)

        exec(open("defineRecorders.py").read())

        if not os.path.exists(f"{GMFolder}/transformed"):
            os.makedirs(f"{GMFolder}/transformed")

        inFileName = f"{GMFolder}/{iRec}.AT2"
        GMPath = f"{GMFolder}/transformed/{iRec}.txt"
        dtInput, numPoints = ReadRecord(inFileName, GMPath)
        seriesTag = 2
        timeSeries('Path', seriesTag, '-dt', dtInput, '-filePath', GMPath, '-factor', scaleFac)
        GMDir = 1
        pattern('UniformExcitation', 2, GMDir, '-accel', seriesTag)
        
        exec(open("defineRecordersAccel.py").read())

        Tmax = numPoints * dtInput + TFree
        dtAnalysis = dtInput
        nSteps = int(Tmax / dtAnalysis)

        if showAnimationDeform:
            modelName = "steelModel"
            loadCaseName = f"THA/{iRec}"
            Nmodes = 2
            vfo.createODB(model=modelName, loadcase=loadCaseName, Nmodes=Nmodes)

        print(f'iRec = {iRec} در حال اجرا است ...')

        doDynamicAnalysis(Tmax, dtInput)
        
        wipe()

        if showAnimationDeform:
            vfo.plot_deformedshape(model=modelName, loadcase=loadCaseName, scale=10)
            vfo.animate_deformedshape(model=modelName, loadcase=loadCaseName, scale=10, speedup=50, gifname="THAAnimation")

    except Exception as e:
        print(f'برای iRec = {iRec} خطایی رخ داده است: {e}')
        failed_records.append(iRec)  # ثبت ورودی ناموفق

# نوشتن نام ورودی‌های ناموفق در یک فایل متنی
with open("failed_records.txt", "w") as f:
    for rec in failed_records:
        f.write(f"{rec}.AT2\n")  # نوشتن نام فایل ورودی ناموفق
