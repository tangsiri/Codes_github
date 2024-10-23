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

from drawPlot import drawPlot, drawMultiplePlot


# dataDir = "outputs/pushover"
# xFileName, yFileName = "disp.txt", "Vx.txt"
# iColX, iColY = 2, 0
# xLabel, yLabel = "disp (m)", "base shear (N)"
# title= "pushover"
# xCoeff, yCoeff = 1, -1
# drawPlot(dataDir, xFileName, yFileName, iColX, iColY, xLabel, yLabel, title, xCoeff, yCoeff)

# dataDir = "outputs/pushover"
# xFileName, yFileName = "disp.txt", "disp.txt"
# iColX, iColY = 2, 1
# xLabel, yLabel = "disp (m)", "base shear (N)"
# title= "pushover"
# xCoeff, yCoeff = 1, 1
# drawPlot(dataDir, xFileName, yFileName, iColX, iColY, xLabel, yLabel, title, xCoeff, yCoeff)



dataDir = "outputs"
xFileNameList = ["pushover-elastic/disp.txt", "pushover-rigid/disp.txt", "pushover-krawinkler/disp.txt", "pushover-scissors/disp.txt"] 
yFileNameList = ["pushover-elastic/disp.txt", "pushover-rigid/disp.txt", "pushover-krawinkler/disp.txt", "pushover-scissors/disp.txt"] 
iColX, iColY = 2, 1
xLabel, yLabel = "disp (m)", "base shear (N)"
title= "pushover"
xCoeff, yCoeff = 1, 1
legendList = ["elastic", "rigid", "krawinkler", "scissors"]
drawMultiplePlot(dataDir, xFileNameList, yFileNameList, legendList, iColX, iColY, xLabel, yLabel, title="", xCoeff=1, yCoeff=1, legendLoc="best")
