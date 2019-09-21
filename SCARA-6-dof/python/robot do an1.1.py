import tkinter
from tkinter import *
from tkinter import ttk, IntVar
import pickle
import serial
from serial import *
import time
import threading
import math

root = Tk()
root.wm_title("Hai robot")
root.resizable(width=True, height=True)
root.geometry('1366x986+0+0')

root.runTrue = 0

nb = tkinter.ttk.Notebook(root, width=1366, height=698)
nb.place(x=0, y=0)

tab1 = tkinter.ttk.Frame(nb)
nb.add(tab1, text=' Main Controls ')

tab2 = tkinter.ttk.Frame(nb)
nb.add(tab2, text='  DH & Calib  ')


global J1NegAngLim
global J1PosAngLim
global J1StepLim
global J1DegPerStep
global J1StepCur
global J1AngCur
global J2NegAngLim
global J2PosAngLim
global J2StepLim
global J2DegPerStep
global J2StepCur
global J2AngCur
global J2NegAngLim
global J2PosAngLim
global J2StepLim
global J2DegPerStep
global J2StepCur
global J2AngCur
global J3NegAngLim
global J3PosAngLim
global J3StepLim
global J3DegPerStep
global J3StepCur
global J3AngCur
global J4NegAngLim
global J4PosAngLim
global J4StepLim
global J4DegPerStep
global J4StepCur
global J4AngCur
global J5NegAngLim
global J5PosAngLim
global J5StepLim
global J5DegPerStep
global J5StepCur
global J5AngCur
global J6NegAngLim
global J6PosAngLim
global J6StepLim
global J6DegPerStep
global J6StepCur
global J6AngCur
global XcurPos
global YcurPos
global ZcurPos
global RxcurPos
global RycurPos
global RzcurPos



##thuan
global H4
global H5
global H6
global H7
global H8
global H9

###nghịch
global G60
global G61
global G62
global H60
global H61
global H62
global I60
global I61
global I62

global E7
global E8
global E27
global E28


global DHr1
global DHr2
global DHr3
global DHr4
global DHr5
global DHr6

global DHa1
global DHa2
global DHa3
global DHa4
global DHa5
global DHa6

global DHd1
global DHd2
global DHd3
global DHd4
global DHd5
global DHd6

global DHt1
global DHt2
global DHt3
global DHt4
global DHt5
global DHt6


global JogStepsStat
JogStepsStat = IntVar()


def setCom():
  global ser  
  port = "COM" + comPortEntryField.get()  
  baud = 9600 
  ser = serial.Serial(port, baud)

def deleteitem():
  selRow = tab1.progView.curselection()[0]
  selection = tab1.progView.curselection()  
  tab1.progView.delete(selection[0])
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
    

def executeRow():
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global calStat
  selRow = tab1.progView.curselection()[0]
  tab1.progView.see(selRow+2)
  data = list(map(int, tab1.progView.curselection()))
  command=tab1.progView.get(data[0])
  cmdType=command[:6]
  ##Call Program##
  if (cmdType == "Call P"):
    tab1.lastRow = tab1.progView.curselection()[0]
    tab1.lastProg = ProgEntryField.get()
    programIndex = command.find("Program -")
    progNum = str(command[programIndex+10:])
    ProgEntryField.delete(0, 'end')
    ProgEntryField.insert(0,progNum)
    loadProg()
    time.sleep(.4) 
    index = 0
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(index) 
  ##Return Program##
  if (cmdType == "Return"):
    lastRow = tab1.lastRow
    lastProg = tab1.lastProg
    ProgEntryField.delete(0, 'end')
    ProgEntryField.insert(0,lastProg)
    loadProg()
    time.sleep(.4) 
    index = 0
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(lastRow)  
  ##Servo Command##
  if (cmdType == "Servo "):
    servoIndex = command.find("number ")
    posIndex = command.find("position: ")
    servoNum = str(command[servoIndex+7:posIndex-4])
    servoPos = str(command[posIndex+10:])
    command = "SV"+servoNum+"P"+servoPos
    ser.write((command +"\n").encode())
    ser.flushInput()
    time.sleep(.2)
    ser.read() 
  ##Jump to Row##
  if (cmdType == "Jump T"):
    tabIndex = command.find("Tab-")
    tabNum = str(command[tabIndex+4:])
    index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(index)  

  ##Wait Time Command##
  if (cmdType == "Wait T"):
    timeIndex = command.find("Seconds-")
    timeSeconds = str(command[timeIndex+8:])
    command = "WTS"+timeSeconds
    ser.write((command +"\n").encode())
    ser.flushInput()
    time.sleep(.2)
    ser.read() 
  ##Set Register##  
  if (cmdType == "Regist"):
    regNumIndex = command.find("Register ")
    regEqIndex = command.find(" = ")
    regNumVal = str(command[regNumIndex+9:regEqIndex])
    regEntry = "R"+regNumVal+"EntryField"
    testOper = str(command[regEqIndex+3:regEqIndex+4])
    if (testOper == "+"):
      regCEqVal = str(command[regEqIndex+4:])
      curRegVal = eval(regEntry).get()
      regEqVal = str(int(regCEqVal)+int(curRegVal))      
    elif (testOper == "-"):
      regCEqVal = str(command[regEqIndex+4:])
      curRegVal = eval(regEntry).get()
      regEqVal = str(int(curRegVal)-int(regCEqVal))
    else:
      regEqVal = str(command[regEqIndex+3:])    
    eval(regEntry).delete(0, 'end')
    eval(regEntry).insert(0,regEqVal)
  ##If Register Jump to Row##
  if (cmdType == "If Reg"):
    regIndex = command.find("If Register ")
    regEqIndex = command.find(" = ")
    regJmpIndex = command.find(" Jump to Tab ")    
    regNum = str(command[regIndex+12:regEqIndex])
    regEq = str(command[regEqIndex+3:regJmpIndex])
    tabNum = str(command[regJmpIndex+13:])
    regEntry = "R"+regNum+"EntryField"
    curRegVal = eval(regEntry).get()
    if (curRegVal == regEq):
      index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(index)  
    manEntryField.delete(0, 'end')
    manEntryField.insert(0,regNum+" "+regEq+" "+tabNum) 
  if (cmdType == "Calibr"):
    calRobot()
    if (calStat == 0):
      stopProg()
      
      
  ##Move Command##  
  if (cmdType == "Move J"):  
    J1newIndex = command.find("J1) ")
    J2newIndex = command.find("J2) ")
    J3newIndex = command.find("J3) ")
    J4newIndex = command.find("J4) ")
    J5newIndex = command.find("J5) ")
    J6newIndex = command.find("J6) ")
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    J1newStep = command[J1newIndex+4:J2newIndex-1]
    J2newStep = command[J2newIndex+4:J3newIndex-1]
    J3newStep = command[J3newIndex+4:J4newIndex-1]
    J4newStep = command[J4newIndex+4:J5newIndex-1]
    J5newStep = command[J5newIndex+4:J6newIndex-1]
    J6newStep = command[J6newIndex+4:SpeedIndex-1]
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:]
    ##J1 calc##
    if (int(J1newStep) >= J1StepCur):
      J1dir = "0"
      J1steps =  int(J1newStep) - int(J1StepCur)   
      J1StepCur = J1StepCur + J1steps      
      J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1steps = str(J1steps) 
    elif (int(J1newStep) < J1StepCur):
      J1dir = "1"
      J1steps =  int(J1StepCur) - int(J1newStep)  
      J1StepCur = J1StepCur - J1steps      
      J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1steps = str(J1steps) 
    ##J2 calc##
    if (int(J2newStep) >= J2StepCur):
      J2dir = "0"
      J2steps =  int(J2newStep) - int(J2StepCur)   
      J2StepCur = J2StepCur + J2steps      
      J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2steps = str(J2steps) 
    elif (int(J2newStep) < J2StepCur):
      J2dir = "1"
      J2steps =  int(J2StepCur) - int(J2newStep)  
      J2StepCur = J2StepCur - J2steps      
      J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2steps = str(J2steps) 
    ##J3 calc##
    if (int(J3newStep) >= J3StepCur):
      J3dir = "0"
      J3steps =  int(J3newStep) - int(J3StepCur)   
      J3StepCur = J3StepCur + J3steps      
      J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3steps = str(J3steps) 
    elif (int(J3newStep) < J3StepCur):
      J3dir = "1"
      J3steps =  int(J3StepCur) - int(J3newStep)  
      J3StepCur = J3StepCur - J3steps      
      J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3steps = str(J3steps) 
    ##J4 calc##
    if (int(J4newStep) >= J4StepCur):
      J4dir = "1"
      J4steps =  int(J4newStep) - int(J4StepCur)   
      J4StepCur = J4StepCur + J4steps     
      J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4steps = str(J4steps) 
    elif (int(J4newStep) < J4StepCur):
      J4dir = "0"
      J4steps =  int(J4StepCur) - int(J4newStep)  
      J4StepCur = J4StepCur - J4steps     
      J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4steps = str(J4steps) 
    ##J5 calc##
    if (int(J5newStep) >= J5StepCur):
      J5dir = "0"
      J5steps =  int(J5newStep) - int(J5StepCur)   
      J5StepCur = J5StepCur + J5steps     
      J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5steps = str(J5steps) 
    elif (int(J5newStep) < J5StepCur):
      J5dir = "1"
      J5steps =  int(J5StepCur) - int(J5newStep)  
      J5StepCur = J5StepCur - J5steps     
      J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5steps = str(J5steps) 
    ##J6 calc##
    if (int(J6newStep) >= J6StepCur):
      J6dir = "1"
      J6steps =  int(J6newStep) - int(J6StepCur)   
      J6StepCur = J6StepCur + J6steps     
      J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6steps = str(J6steps) 
    elif (int(J6newStep) < J6StepCur):
      J6dir = "0"
      J6steps =  int(J6StepCur) - int(J6newStep)  
      J6StepCur = J6StepCur - J6steps     
      J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6steps = str(J6steps) 
    commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"S"+newSpeed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd
    ser.write((commandCalc +"\n").encode())
    ser.flushInput()
    time.sleep(.2)
    ser.read() 
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur)) 
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    CalcFwdKin()
    DisplaySteps()
    savePosData()
     

	 
	 
def exeFineCalPos():
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global calStat
  command = fineCalEntryField.get() 
  J1newIndex = command.find("J1) ")
  J2newIndex = command.find("J2) ")
  J3newIndex = command.find("J3) ")
  J4newIndex = command.find("J4) ")
  J5newIndex = command.find("J5) ")
  J6newIndex = command.find("J6) ")
  SpeedIndex = command.find("Speed-")
  ACCdurIndex = command.find("Ad")
  ACCspdIndex = command.find("As")
  DECdurIndex = command.find("Dd")
  DECspdIndex = command.find("Ds")
  J1newStep = command[J1newIndex+4:J2newIndex-1]
  J2newStep = command[J2newIndex+4:J3newIndex-1]
  J3newStep = command[J3newIndex+4:J4newIndex-1]
  J4newStep = command[J4newIndex+4:J5newIndex-1]
  J5newStep = command[J5newIndex+4:J6newIndex-1]
  J6newStep = command[J6newIndex+4:SpeedIndex-1]
  newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
  ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
  ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
  DECdur = command[DECdurIndex+3:DECspdIndex-1]
  DECspd = command[DECspdIndex+3:]
  ##J1 calc##
  if (int(J1newStep) >= J1StepCur):
    J1dir = "0"
    J1steps =  int(J1newStep) - int(J1StepCur)   
    J1StepCur = J1StepCur + J1steps      
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1steps = str(J1steps) 
  elif (int(J1newStep) < J1StepCur):
    J1dir = "1"
    J1steps =  int(J1StepCur) - int(J1newStep)  
    J1StepCur = J1StepCur - J1steps      
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1steps = str(J1steps) 
  ##J2 calc##
  if (int(J2newStep) >= J2StepCur):
    J2dir = "0"
    J2steps =  int(J2newStep) - int(J2StepCur)   
    J2StepCur = J2StepCur + J2steps      
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2steps = str(J2steps) 
  elif (int(J2newStep) < J2StepCur):
    J2dir = "1"
    J2steps =  int(J2StepCur) - int(J2newStep)  
    J2StepCur = J2StepCur - J2steps      
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2steps = str(J2steps) 
  ##J3 calc##
  if (int(J3newStep) >= J3StepCur):
    J3dir = "0"
    J3steps =  int(J3newStep) - int(J3StepCur)   
    J3StepCur = J3StepCur + J3steps      
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3steps = str(J3steps) 
  elif (int(J3newStep) < J3StepCur):
    J3dir = "1"
    J3steps =  int(J3StepCur) - int(J3newStep)  
    J3StepCur = J3StepCur - J3steps      
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3steps = str(J3steps) 
  ##J4 calc##
  if (int(J4newStep) >= J4StepCur):
    J4dir = "1"
    J4steps =  int(J4newStep) - int(J4StepCur)   
    J4StepCur = J4StepCur + J4steps     
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4steps = str(J4steps) 
  elif (int(J4newStep) < J4StepCur):
    J4dir = "0"
    J4steps =  int(J4StepCur) - int(J4newStep)  
    J4StepCur = J4StepCur - J4steps     
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4steps = str(J4steps) 
  ##J5 calc##
  if (int(J5newStep) >= J5StepCur):
    J5dir = "0"
    J5steps =  int(J5newStep) - int(J5StepCur)   
    J5StepCur = J5StepCur + J5steps     
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5steps = str(J5steps) 
  elif (int(J5newStep) < J5StepCur):
    J5dir = "1"
    J5steps =  int(J5StepCur) - int(J5newStep)  
    J5StepCur = J5StepCur - J5steps     
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5steps = str(J5steps) 
  ##J6 calc##
  if (int(J6newStep) >= J6StepCur):
    J6dir = "1"
    J6steps =  int(J6newStep) - int(J6StepCur)   
    J6StepCur = J6StepCur + J6steps     
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6steps = str(J6steps) 
  elif (int(J6newStep) < J6StepCur):
    J6dir = "0"
    J6steps =  int(J6StepCur) - int(J6newStep)  
    J6StepCur = J6StepCur - J6steps     
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6steps = str(J6steps) 
  commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"S"+newSpeed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd
  ser.write((commandCalc +"\n").encode())
  ser.flushInput()
  time.sleep(.2)
  ser.read() 
  J1curAngEntryField.delete(0, 'end')
  J1curAngEntryField.insert(0,str(J1AngCur)) 
  J2curAngEntryField.delete(0, 'end')
  J2curAngEntryField.insert(0,str(J2AngCur))
  J3curAngEntryField.delete(0, 'end')
  J3curAngEntryField.insert(0,str(J3AngCur))
  J4curAngEntryField.delete(0, 'end')
  J4curAngEntryField.insert(0,str(J4AngCur))
  J5curAngEntryField.delete(0, 'end')
  J5curAngEntryField.insert(0,str(J5AngCur))
  J6curAngEntryField.delete(0, 'end')
  J6curAngEntryField.insert(0,str(J6AngCur))
  CalcFwdKin()
  DisplaySteps()
  savePosData()
  almStatusLab.config(text="MOVED TO FINE CALIBRATION POSITION", bg = "yellow")
	
	

def stepFwd():
    executeRow() 
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.selection_clear(0, END)
    selRow += 1
    tab1.progView.select_set(selRow)
    time.sleep(.2)
    try:
      selRow = tab1.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")
 

def stepRev():
    executeRow()  
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.itemconfig(selRow, {'fg': 'red'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'tomato2'})
    tab1.progView.selection_clear(0, END)
    selRow -= 1
    tab1.progView.select_set(selRow)
    time.sleep(.2)
    try:
      selRow = tab1.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")
 

def runProg():
  def threadProg():
    try:
      curRow = tab1.progView.curselection()[0]
      if (curRow == 0):
        curRow=1
    except:
      curRow=1
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(curRow)
    tab1.runTrue = 1
    while tab1.runTrue == 1:
      if (tab1.runTrue == 0):
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
      else:
        runStatusLab.config(text='PROGRAM RUNNING', bg = "green")
      executeRow()  
      selRow = tab1.progView.curselection()[0]
      last = tab1.progView.index('end')
      for row in range (0,selRow):
        tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
      tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
      for row in range (selRow+1,last):
        tab1.progView.itemconfig(row, {'fg': 'black'})
      tab1.progView.selection_clear(0, END)
      selRow += 1
      tab1.progView.select_set(selRow)
      curRow += 1
      time.sleep(.2)
      try:
        selRow = tab1.progView.curselection()[0]
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,selRow)
      except:
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,"---") 
        tab1.runTrue = 0
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  t = threading.Thread(target=threadProg)
  t.start()


def stopProg():
  tab1.runTrue = 0 
  if (tab1.runTrue == 0):
    runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  else:
    runStatusLab.config(text='PROGRAM RUNNING', bg = "green")




def calRobot():
  command = "LL"+"A"+str(J1StepLim)+"B"+str(J2StepLim)+"C"+str(J3StepLim)+"D"+str(J4StepLim)+"E"+str(J5StepLim)+"F"+str(J6StepLim)  
  ser.write((command +"\n").encode())
  ser.flushInput()
  calvalue = ser.readline()
  print(calvalue)
  global calStat
  if (calvalue.decode('utf-8') == "pass\n"):
    calStat = 1
    calibration.delete(0, END)
    ##J1##
    global J1StepCur
    global J1AngCur
    J1StepCur = J1StepLim
    J1AngCur = J1PosAngLim
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    ###########
    ##J2##
    global J2StepCur
    global J2AngCur
    J2StepCur = J2StepLim
    J2AngCur = J2PosAngLim
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    ###########
    ##J3##
    global J3StepCur
    global J3AngCur
    J3StepCur = J3StepLim
    J3AngCur = J3PosAngLim
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    ###########
    ##J4##
    global J4StepCur
    global J4AngCur
    J4StepCur = J4StepLim
    J4AngCur = J4PosAngLim
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    ###########
    ##J5##
    global J5StepCur
    global J5AngCur
    J5StepCur = J5StepLim
    J5AngCur = J5PosAngLim
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    ###########
    ##J6##
    global J6StepCur
    global J6AngCur
    J6StepCur = 0
    J6AngCur = J6NegAngLim
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    ###########
    value=calibration.get(0,END)
    pickle.dump(value,open("ARbot.cal","wb"))
    almStatusLab.config(text='CALIBRATION SUCCESSFUL', bg = "grey")
    DisplaySteps()
  else:
    if (calvalue.decode('utf-8') == "J1fail\n"):
      calStat = 0
      almStatusLab.config(text="CALIBRATION FAILED", bg = "red")
  savePosData()


def calRobotMid():
  calibration.delete(0, END)
  ##J1##
  global J1StepCur
  global J1AngCur
  J1StepCur = J1StepLim/2
  J1AngCur = (J1NegAngLim + J1PosAngLim)/2
  J1curAngEntryField.delete(0, 'end')
  J1curAngEntryField.insert(0,str(J1AngCur))
  ###########
  ##J2##
  global J2StepCur
  global J2AngCur
  J2StepCur = J2StepLim/2
  J2AngCur = (J2NegAngLim + J2PosAngLim)/2
  J2curAngEntryField.delete(0, 'end')
  J2curAngEntryField.insert(0,str(J2AngCur))
  ###########
  ##J3##
  global J3StepCur
  global J3AngCur
  J3StepCur = J3StepLim/2
  J3AngCur = (J3NegAngLim + J3PosAngLim)/2
  J3curAngEntryField.delete(0, 'end')
  J3curAngEntryField.insert(0,str(J3AngCur))
  ###########
  ##J4##
  global J4StepCur
  global J4AngCur
  J4StepCur = J4StepLim/2
  J4AngCur = (J4NegAngLim + J4PosAngLim)/2
  J4curAngEntryField.delete(0, 'end')
  J4curAngEntryField.insert(0,str(J4AngCur))
  ###########
  ##J5##
  global J5StepCur
  global J5AngCur
  J5StepCur = J5StepLim/2
  J5AngCur = (J5NegAngLim + J5PosAngLim)/2
  J5curAngEntryField.delete(0, 'end')
  J5curAngEntryField.insert(0,str(J5AngCur))
  ###########
  ##J6##
  global J6StepCur
  global J6AngCur
  J6StepCur = J6StepLim/2
  J6AngCur = (J6NegAngLim + J6PosAngLim)/2
  J6curAngEntryField.delete(0, 'end')
  J6curAngEntryField.insert(0,str(J6AngCur))
  ###########
  value=calibration.get(0,END)
  pickle.dump(value,open("ARbot.cal","wb"))
  almStatusLab.config(text="CALIBRATION FORCE TO MIDPOINT / DANGER", bg = "orange")
  DisplaySteps()
  savePosData()






def savePosData():
  calibration.delete(0, END)
  calibration.insert(END, J1StepCur)
  calibration.insert(END, J1AngCur)
  calibration.insert(END, J2StepCur)
  calibration.insert(END, J2AngCur)
  calibration.insert(END, J3StepCur)
  calibration.insert(END, J3AngCur)
  calibration.insert(END, J4StepCur)
  calibration.insert(END, J4AngCur)
  calibration.insert(END, J5StepCur)
  calibration.insert(END, J5AngCur)
  calibration.insert(END, J6StepCur)
  calibration.insert(END, J6AngCur)
  calibration.insert(END, comPortEntryField.get())  
  calibration.insert(END, ProgEntryField.get())
  calibration.insert(END, fineCalEntryField.get())
  calibration.insert(END, J1NegAngLimEntryField.get())
  calibration.insert(END, J1PosAngLimEntryField.get())
  calibration.insert(END, J1StepLimEntryField.get())
  calibration.insert(END, J2NegAngLimEntryField.get())
  calibration.insert(END, J2PosAngLimEntryField.get())
  calibration.insert(END, J2StepLimEntryField.get())
  calibration.insert(END, J3NegAngLimEntryField.get())
  calibration.insert(END, J3PosAngLimEntryField.get())
  calibration.insert(END, J3StepLimEntryField.get())
  calibration.insert(END, J4NegAngLimEntryField.get())
  calibration.insert(END, J4PosAngLimEntryField.get())
  calibration.insert(END, J4StepLimEntryField.get())
  calibration.insert(END, J5NegAngLimEntryField.get())
  calibration.insert(END, J5PosAngLimEntryField.get())
  calibration.insert(END, J5StepLimEntryField.get())
  calibration.insert(END, J6NegAngLimEntryField.get())
  calibration.insert(END, J6PosAngLimEntryField.get())
  calibration.insert(END, J6StepLimEntryField.get())
  calibration.insert(END, DHr1EntryField.get())
  calibration.insert(END, DHr2EntryField.get())
  calibration.insert(END, DHr3EntryField.get())
  calibration.insert(END, DHr4EntryField.get())
  calibration.insert(END, DHr5EntryField.get())
  calibration.insert(END, DHr6EntryField.get())
  calibration.insert(END, DHa1EntryField.get())
  calibration.insert(END, DHa2EntryField.get())
  calibration.insert(END, DHa3EntryField.get())
  calibration.insert(END, DHa4EntryField.get())
  calibration.insert(END, DHa5EntryField.get())
  calibration.insert(END, DHa6EntryField.get())
  calibration.insert(END, DHd1EntryField.get())
  calibration.insert(END, DHd2EntryField.get())
  calibration.insert(END, DHd3EntryField.get())
  calibration.insert(END, DHd4EntryField.get())
  calibration.insert(END, DHd5EntryField.get())
  calibration.insert(END, DHd6EntryField.get())
  calibration.insert(END, DHt1EntryField.get())
  calibration.insert(END, DHt2EntryField.get())
  calibration.insert(END, DHt3EntryField.get())
  calibration.insert(END, DHt4EntryField.get())
  calibration.insert(END, DHt5EntryField.get())
  calibration.insert(END, DHt6EntryField.get())
  ###########
  value=calibration.get(0,END)
  pickle.dump(value,open("ARbot.cal","wb"))


def SaveAndApplyCalibration():
  global J1NegAngLim
  global J1PosAngLim
  global J1StepLim
  global J1DegPerStep
  global J1StepCur
  global J1AngCur
  global J2NegAngLim
  global J2PosAngLim
  global J2StepLim
  global J2DegPerStep
  global J2StepCur
  global J2AngCur
  global J2NegAngLim
  global J2PosAngLim
  global J2StepLim
  global J2DegPerStep
  global J2StepCur
  global J2AngCur
  global J3NegAngLim
  global J3PosAngLim
  global J3StepLim
  global J3DegPerStep
  global J3StepCur
  global J3AngCur
  global J4NegAngLim
  global J4PosAngLim
  global J4StepLim
  global J4DegPerStep
  global J4StepCur
  global J4AngCur
  global J5NegAngLim
  global J5PosAngLim
  global J5StepLim
  global J5DegPerStep
  global J5StepCur
  global J5AngCur
  global J6NegAngLim
  global J6PosAngLim
  global J6StepLim
  global J6DegPerStep
  global J6StepCur
  global J6AngCur
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global DHr1
  global DHr2
  global DHr3
  global DHr4
  global DHr5
  global DHr6
  global DHa1
  global DHa2
  global DHa3
  global DHa4
  global DHa5
  global DHa6
  global DHd1
  global DHd2
  global DHd3
  global DHd4
  global DHd5
  global DHd6
  global DHt1
  global DHt2
  global DHt3
  global DHt4
  global DHt5
  global DHt6

  J1NegAngLim = int(J1NegAngLimEntryField.get())
  J1PosAngLim = int(J1PosAngLimEntryField.get())
  J1StepLim = int(J1StepLimEntryField.get())
  J1DegPerStep = float((J1PosAngLim - J1NegAngLim)/float(J1StepLim))
  J2NegAngLim = int(J2NegAngLimEntryField.get())
  J2PosAngLim = int(J2PosAngLimEntryField.get())
  J2StepLim = int(J2StepLimEntryField.get())
  J2DegPerStep = float((J2PosAngLim - J2NegAngLim)/float(J2StepLim))
  J3NegAngLim = int(J3NegAngLimEntryField.get())
  J3PosAngLim = int(J3PosAngLimEntryField.get())
  J3StepLim = int(J3StepLimEntryField.get())
  J3DegPerStep = float((J3PosAngLim - J3NegAngLim)/float(J3StepLim))
  J4NegAngLim = int(J4NegAngLimEntryField.get())
  J4PosAngLim = int(J4PosAngLimEntryField.get())
  J4StepLim = int(J4StepLimEntryField.get())
  J4DegPerStep = float((J4PosAngLim - J4NegAngLim)/float(J4StepLim))
  J5NegAngLim = int(J5NegAngLimEntryField.get())
  J5PosAngLim = int(J5PosAngLimEntryField.get())
  J5StepLim = int(J5StepLimEntryField.get())
  J5DegPerStep = float((J5PosAngLim - J5NegAngLim)/float(J5StepLim))
  J6NegAngLim = int(J6NegAngLimEntryField.get())
  J6PosAngLim = int(J6PosAngLimEntryField.get())
  J6StepLim = int(J6StepLimEntryField.get())
  J6DegPerStep = float((J6PosAngLim - J6NegAngLim)/float(J6StepLim))

  AxLimCol = "royalblue"
  J1PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J1PosAngLim)))
  J1PlimLab.place(x=685, y=10)
  J1NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J1NegAngLim)))
  J1NlimLab.place(x=635, y=10)
  J2PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J2PosAngLim)))
  J2PlimLab.place(x=780, y=10)
  J2NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J2NegAngLim)))
  J2NlimLab.place(x=725, y=10)
  J3PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J3PosAngLim)))
  J3PlimLab.place(x=868, y=10)
  J3NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J3NegAngLim)))
  J3NlimLab.place(x=815, y=10)
  J4PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J4PosAngLim)))
  J4PlimLab.place(x=960, y=10)
  J4NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J4NegAngLim)))
  J4NlimLab.place(x=905, y=10)
  J5PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J5PosAngLim)))
  J5PlimLab.place(x=1050, y=10)
  J5NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J5NegAngLim)))
  J5NlimLab.place(x=1005, y=10)
  J6PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J6PosAngLim)))
  J6PlimLab.place(x=1140, y=10)
  J6NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J6NegAngLim)))
  J6NlimLab.place(x=1085, y=10)
  DHr1 = float(DHr1EntryField.get())
  DHr2 = float(DHr2EntryField.get())
  DHr3 = float(DHr3EntryField.get())
  DHr4 = float(DHr4EntryField.get())
  DHr5 = float(DHr5EntryField.get())
  DHr6 = float(DHr6EntryField.get())
  DHa1 = float(DHa1EntryField.get())
  DHa2 = float(DHa2EntryField.get())
  DHa3 = float(DHa3EntryField.get())
  DHa4 = float(DHa4EntryField.get())
  DHa5 = float(DHa5EntryField.get())
  DHa6 = float(DHa6EntryField.get())
  DHd1 = float(DHd1EntryField.get())
  DHd2 = float(DHd2EntryField.get())
  DHd3 = float(DHd3EntryField.get())
  DHd4 = float(DHd4EntryField.get())
  DHd5 = float(DHd5EntryField.get())
  DHd6 = float(DHd6EntryField.get())
  DHt1 = float(DHt1EntryField.get())
  DHt2 = float(DHt2EntryField.get())
  DHt3 = float(DHt3EntryField.get())
  DHt4 = float(DHt4EntryField.get())
  DHt5 = float(DHt5EntryField.get())
  DHt6 = float(DHt6EntryField.get())

  savePosData()



def DisplaySteps():
  J1stepsLab['text'] = str(J1StepCur)
  J2stepsLab['text'] = str(J2StepCur)
  J3stepsLab['text'] = str(J3StepCur)
  J4stepsLab['text'] = str(J4StepCur)
  J5stepsLab['text'] = str(J5StepCur)
  J6stepsLab['text'] = str(J6StepCur) 




def J1jogNeg():
  global JogStepsStat
  global J1StepCur
  global J1AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1Degs = float(J1jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J1jogSteps = int(J1Degs/J1DegPerStep)
  else:
    J1jogSteps = J1Degs
    J1Degs = J1Degs*J1DegPerStep
  if (J1Degs <= -(J1NegAngLim - J1AngCur)):
    ser.write(("MJA1"+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J1StepCur = J1StepCur - int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J1 AXIS LIMIT", bg = "red")
  DisplaySteps()

  



def J1jogPos():
  global JogStepsStat
  global J1StepCur
  global J1AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1Degs = float(J1jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J1jogSteps = int(J1Degs/J1DegPerStep)
  else:
    J1jogSteps = J1Degs
    J1Degs = J1Degs*J1DegPerStep
  if (J1Degs <= (J1PosAngLim - J1AngCur)):
    ser.write(("MJA0"+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J1StepCur = J1StepCur + int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J1 AXIS LIMIT", bg = "red")
  DisplaySteps()








def J2jogNeg():
  global JogStepsStat
  global J2StepCur
  global J2AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J2Degs = float(J2jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J2jogSteps = int(J2Degs/J2DegPerStep)
  else:
    J2jogSteps = J2Degs
    J2Degs = J2Degs*J2DegPerStep
  if (J2Degs <= -(J2NegAngLim - J2AngCur)):
    ser.write(("MJB1"+str(J2jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J2StepCur = J2StepCur - int(J2jogSteps)
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
  DisplaySteps()

  



def J2jogPos():
  global JogStepsStat
  global J2StepCur
  global J2AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J2Degs = float(J2jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J2jogSteps = int(J2Degs/J2DegPerStep)
  else:
    J2jogSteps = J2Degs
    J2Degs = J2Degs*J2DegPerStep
  if (J2Degs <= (J2PosAngLim - J2AngCur)):
    ser.write(("MJB0"+str(J2jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J2StepCur = J2StepCur + int(J2jogSteps)
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
  DisplaySteps()






def J3jogNeg():
  global JogStepsStat
  global J3StepCur
  global J3AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J3Degs = float(J3jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J3jogSteps = int(J3Degs/J3DegPerStep)
  else:
    J3jogSteps = J3Degs
    J3Degs = J3Degs*J3DegPerStep
  if (J3Degs <= -(J3NegAngLim - J3AngCur)):
    ser.write(("MJC1"+str(J3jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J3StepCur = J3StepCur - int(J3jogSteps)
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
  DisplaySteps()

  



def J3jogPos():
  global JogStepsStat
  global J3StepCur
  global J3AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J3Degs = float(J3jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J3jogSteps = int(J3Degs/J3DegPerStep)
  else:
    J3jogSteps = J3Degs
    J3Degs = J3Degs*J3DegPerStep
  if (J3Degs <= (J3PosAngLim - J3AngCur)):
    ser.write(("MJC0"+str(J3jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J3StepCur = J3StepCur + int(J3jogSteps)
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
  DisplaySteps()





def J4jogNeg():
  global JogStepsStat
  global J4StepCur
  global J4AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J4Degs = float(J4jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J4jogSteps = int(J4Degs/J4DegPerStep)
  else:
    J4jogSteps = J4Degs
    J4Degs = J4Degs*J4DegPerStep
  if (J4Degs <= -(J4NegAngLim - J4AngCur)):
    ser.write(("MJD0"+str(J4jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J4StepCur = J4StepCur - int(J4jogSteps)
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
  DisplaySteps()

  



def J4jogPos():
  global JogStepsStat
  global J4StepCur
  global J4AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J4Degs = float(J4jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J4jogSteps = int(J4Degs/J4DegPerStep)
  else:

    J4jogSteps = J4Degs
    J4Degs = J4Degs*J4DegPerStep
  if (J4Degs <= (J4PosAngLim - J4AngCur)):
    ser.write(("MJD1"+str(J4jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J4StepCur = J4StepCur + int(J4jogSteps)
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
  DisplaySteps()




def J5jogNeg():
  global JogStepsStat
  global J5StepCur
  global J5AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J5Degs = float(J5jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J5jogSteps = int(J5Degs/J5DegPerStep)
  else:
    J5jogSteps = J5Degs
    J5Degs = J5Degs*J5DegPerStep
  if (J5Degs <= -(J5NegAngLim - J5AngCur)):
    ser.write(("MJE1"+str(J5jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J5StepCur = J5StepCur - int(J5jogSteps)
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
  DisplaySteps()

  



def J5jogPos():
  global JogStepsStat
  global J5StepCur
  global J5AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J5Degs = float(J5jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J5jogSteps = int(J5Degs/J5DegPerStep)
  else:
    J5jogSteps = J5Degs
    J5Degs = J5Degs*J5DegPerStep
  if (J5Degs <= (J5PosAngLim - J5AngCur)):
    ser.write(("MJE0"+str(J5jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())  
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J5StepCur = J5StepCur + int(J5jogSteps)
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
  DisplaySteps()




def J6jogNeg():
  global JogStepsStat
  global J6StepCur
  global J6AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J6Degs = float(J6jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J6jogSteps = int(J6Degs/J6DegPerStep)
  else:
    J6jogSteps = J6Degs
    J6Degs = J6Degs*J6DegPerStep
  if (J6Degs <= -(J6NegAngLim - J6AngCur)):
    ser.write(("MJF0"+str(J6jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J6StepCur = J6StepCur - int(J6jogSteps)
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
  DisplaySteps()

  



def J6jogPos():
  global JogStepsStat
  global J6StepCur
  global J6AngCur
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J6Degs = float(J6jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J6jogSteps = int(J6Degs/J6DegPerStep)
  else:
    J6jogSteps = J6Degs
    J6Degs = J6Degs*J6DegPerStep
  if (J6Degs <= (J6PosAngLim - J6AngCur)):
    ser.write(("MJF1"+str(J6jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n").encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  
    J6StepCur = J6StepCur + int(J6jogSteps)
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    savePosData()
    CalcFwdKin()
  else:
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
  DisplaySteps()




def XjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = float(XjogEntryField.get())
  CX = CX*-1
  CY = 0 
  CZ = 0
  CRx = 0
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def YjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = 0 
  CY = float(YjogEntryField.get())
  CY = CY*-1
  CZ = 0
  CRx = 0
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def ZjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = 0 
  CY = 0
  CZ = float(ZjogEntryField.get())
  CZ = CZ*-1
  CRx = 0
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)

def RxjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = 0 
  CY = 0
  CZ = 0
  CRx = float(RxjogEntryField.get())
  CRx = CRx*-1
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)

def RyjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CY = 0
  CX = 0
  CZ = 0
  CRx = 0
  CRy = float(RyjogEntryField.get())
  CRy = CRy*-1
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)

def RzjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CZ = 0
  CY = 0
  CX = 0
  CRx = 0
  CRy = 0
  CRz = float(RzjogEntryField.get())
  CRz = CRz*-1
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def XjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = float(XjogEntryField.get())
  CY = 0 
  CZ = 0
  CRx = 0
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def YjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = 0 
  CY = float(YjogEntryField.get())
  CZ = 0
  CRx = 0
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def ZjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = 0 
  CY = 0
  CZ = float(ZjogEntryField.get())
  CRx = 0
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def RxjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CX = 0 
  CY = 0
  CZ = 0
  CRx = float(RxjogEntryField.get())
  CRy = 0
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)

def RyjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CY = 0
  CX = 0
  CZ = 0
  CRx = 0
  CRy = float(RyjogEntryField.get())
  CRz = 0
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)

def RzjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "grey")
  global CX
  global CY
  global CZ
  CZ = 0
  CY = 0
  CX = 0
  CRx = 0
  CRy = 0
  CRz = float(RzjogEntryField.get())
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz)


def teachInsertBelSelected():
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1StepWrite = str(J1StepCur)
  J2StepWrite = str(J2StepCur)
  J3StepWrite = str(J3StepCur)
  J4StepWrite = str(J4StepCur)
  J5StepWrite = str(J5StepCur)
  J6StepWrite = str(J6StepCur)
  newPos = "Move J  J1) "+J1StepWrite+"  J2) "+J2StepWrite+"  J3) "+J3StepWrite+"  J4) "+J4StepWrite+"  J5) "+J5StepWrite+"  J6) "+J6StepWrite+"  Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd               
  tab1.progView.insert(selRow, newPos) 
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def teachReplaceSelected():
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  selRow = tab1.progView.curselection()[0]
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1StepWrite = str(J1StepCur)
  J2StepWrite = str(J2StepCur)
  J3StepWrite = str(J3StepCur)
  J4StepWrite = str(J4StepCur)
  J5StepWrite = str(J5StepCur)
  J6StepWrite = str(J6StepCur)
  newPos = "Move J  J1) "+J1StepWrite+"  J2) "+J2StepWrite+"  J3) "+J3StepWrite+"  J4) "+J4StepWrite+"  J5) "+J5StepWrite+"  J6) "+J6StepWrite+"  Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd               
  tab1.progView.insert(selRow, newPos)
  selection = tab1.progView.curselection()
  tab1.progView.delete(selection[0]) 
  tab1.progView.select_set(selRow)
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

  
def teachFineCal():
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1StepWrite = str(J1StepCur)
  J2StepWrite = str(J2StepCur)
  J3StepWrite = str(J3StepCur)
  J4StepWrite = str(J4StepCur)
  J5StepWrite = str(J5StepCur)
  J6StepWrite = str(J6StepCur)
  newPos = "Move J  J1) "+J1StepWrite+"  J2) "+J2StepWrite+"  J3) "+J3StepWrite+"  J4) "+J4StepWrite+"  J5) "+J5StepWrite+"  J6) "+J6StepWrite+"  Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd                
  fineCalEntryField.delete(0, 'end')   
  fineCalEntryField.insert(0,str(newPos))
  savePosData()
  almStatusLab.config(text="NEW FINE CALIBRATION POSITION TAUGHT", bg = "blue")



def manAdditem():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  tab1.progView.insert(selRow, manEntryField.get())
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def waitTime():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  seconds = waitTimeEntryField.get()
  newTime = "Wait T - wait time - Seconds-"+seconds               
  tab1.progView.insert(selRow, newTime)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def waitInputOn():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  input = waitInputEntryField.get()
  newInput = "Wait I - wait input ON - Input-"+input              
  tab1.progView.insert(selRow, newInput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def waitInputOff():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  input = waitInputOffEntryField.get()
  newInput = "Wait Off - wait input OFF - Input-"+input              
  tab1.progView.insert(selRow, newInput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOn():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  output = outputOnEntryField.get()
  newOutput = "Out On - set output ON - Output-"+output              
  tab1.progView.insert(selRow, newOutput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOff():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  output = outputOffEntryField.get()
  newOutput = "Out Off - set output OFF - Output-"+output              
  tab1.progView.insert(selRow, newOutput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def tabNumber():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  tabNum = tabNumEntryField.get()
  tabins = "Tab Number "+tabNum              
  tab1.progView.insert(selRow, tabins) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def jumpTab():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  tabNum = jumpTabEntryField.get()
  tabjmp = "Jump Tab-"+tabNum              
  tab1.progView.insert(selRow, tabjmp) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def Servo():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  servoNum = servoNumEntryField.get()
  servoPos = servoPosEntryField.get()
  servoins = "Servo number "+servoNum+" to position: "+servoPos              
  tab1.progView.insert(selRow, servoins)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def loadProg():
  progframe=Frame(tab1)
  progframe.place(x=7,y=174)
  #progframe.pack(side=RIGHT, fill=Y)
  scrollbar = Scrollbar(progframe) 
  scrollbar.pack(side=RIGHT, fill=Y)
  tab1.progView = Listbox(progframe,width=84,height=29, yscrollcommand=scrollbar.set)
  tab1.progView.bind('<<ListboxSelect>>', progViewselect)
  try:
    Prog = pickle.load(open(ProgEntryField.get(),"rb"))
  except:
    try:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open(ProgEntryField.get(),"wb"))    
    except:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open("new","wb"))
      ProgEntryField.insert(0,"new")
  time.sleep(.2)
  for item in Prog:
    tab1.progView.insert(END,item) 
  tab1.progView.pack()
  scrollbar.config(command=tab1.progView.yview)
  savePosData()

def insertCallProg():  
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  newProg = changeProgEntryField.get()
  changeProg = "Call Program - "+newProg            
  tab1.progView.insert(selRow, changeProg)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def insertReturn():  
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  value = "Return"           
  tab1.progView.insert(selRow, value)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def IfRegjumpTab():
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  regNum = regNumJmpEntryField.get()
  regEqNum = regEqJmpEntryField.get()
  tabNum = regTabJmpEntryField.get()
  tabjmp = "If Register "+regNum+" = "+regEqNum+" Jump to Tab "+ tabNum            
  tab1.progView.insert(selRow, tabjmp)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def insertRegister():  
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  regNum = regNumEntryField.get()
  regCmd = regEqEntryField.get()
  regIns = "Register "+regNum+" = "+regCmd             
  tab1.progView.insert(selRow, regIns)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def insCalibrate():  
  selRow = tab1.progView.curselection()[0]
  selRow += 1
  insCal = "Calibrate Robot"          
  tab1.progView.insert(selRow, insCal)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def progViewselect(e):
  selRow = tab1.progView.curselection()[0]
  curRowEntryField.delete(0, 'end')
  curRowEntryField.insert(0,selRow)



def CalcFwdKin(): 
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global H4
  global H5
  global H6
  global H7
  global H8
  global H9
  global G60
  global G61
  global G62
  global H60
  global H61
  global H62
  global I60
  global I61
  global I62
  global E7
  global E8
  global E27
  global E28
  global G36
  global G37
  global G38
  global G39
  global H36
  global H37
  global H38
  global H39
  global I36
  global I37
  global I38
  global I39
  global J36
  global J37
  global J38
  global J39
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  if (J1AngCur == 0):
    J1AngCur = .0001
  if (J2AngCur == 0):
    J2AngCur = .0001
  if (J3AngCur == 0):
    J3AngCur = .0001
  if (J4AngCur == 0):
    J4AngCur = .0001
  if (J5AngCur == 0):
    J5AngCur = .0001
  if (J6AngCur == 0):
    J6AngCur = .0001  
  
  C4 = math.radians((float(J1AngCur))+DHt1)
  C5 = math.radians((float(J2AngCur))+DHt2)
  C6 = math.radians((float(J3AngCur))+DHt3)
  C7 = math.radians((float(J4AngCur))+DHt4)
  C8 = math.radians((float(J5AngCur))+DHt5)
  C9 = math.radians((float(J6AngCur))+DHt6)

  C13 = C4
  C14 = C5
  C15 = C6
  C16 = C7
  C17 = C8
  C18 = C9
  D13 = math.radians(DHr1)
  D14 = math.radians(DHr2)
  D15 = math.radians(DHr3)
  D16 = math.radians(DHr4)
  D17 = math.radians(DHr5)
  D18 = math.radians(DHr6)
  E13 = DHd1
  E14 = DHd2
  E15 = DHd3
  E16 = DHd4
  E17 = DHd5
  E18 = DHd6
  F13 = DHa1
  F14 = DHa2
  F15 = DHa3
  F16 = DHa4
  F17 = DHa5
  F18 = DHa6
  
  H13 = 0
  H14 = 0
  H15 = 0
  H16 = 0 
  H17 = 0
  H18 = 0
  
  J13 = 0
  J14 = 0  
  J15 = 0
  J16 = 0
  J17 = 0
  J18 = 0

  B21 = math.cos(math.radians(H18))*math.cos(math.radians(H17))
  B22 = math.sin(math.radians(H18))*math.cos(math.radians(H17))
  B23 = -math.sin(math.radians(H18))
  B24 = 0
  C21 = -math.sin(math.radians(H18))*math.cos(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  C22 = math.cos(math.radians(H18))*math.cos(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  C23 = math.cos(math.radians(H17))*math.sin(math.radians(H16))
  C24 = 0
  D21 = math.sin(math.radians(H18))*math.sin(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  D22 = -math.cos(math.radians(H18))*math.sin(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  D23 = math.cos(math.radians(H17))*math.cos(math.radians(H16))
  D24 = 0
  E21 = H13
  E22 = H14
  E23 = H15
  E24 = 1 

  B27 = math.cos(C13)
  B28 = math.sin(C13)
  B29 = 0
  B30 = 0
  C27 = -math.sin(C13)*math.cos(D13)
  C28 = math.cos(C13)*math.cos(D13)
  C29 = math.sin(D13)
  C30 = 0  
  D27 = math.sin(C13)*math.sin(D13)
  D28 = -math.cos(C13)*math.sin(D13)
  D29 = math.cos(D13)
  D30 = 0 
  E27 = F13*math.cos(C13)
  E28 = F13*math.sin(C13)
  E29 = E13
  E30 = 1

  B33 = math.cos(C14)
  B34 = math.sin(C14)
  B35 = 0
  B36 = 0
  C33 = -math.sin(C14)*math.cos(D14)
  C34 = math.cos(C14)*math.cos(D14)
  C35 = math.sin(D14)
  C36 = 0
  D33 = math.sin(C14)*math.sin(D14)
  D34 = -math.cos(C14)*math.sin(D14)
  D35 = math.cos(D14)
  D36 = 0
  E33 = F14*math.cos(C14)
  E34 = F14*math.sin(C14)
  E35 = E14
  E36 = 1

  B39 = math.cos(C15)
  B40 = math.sin(C15)
  B41 = 0
  B42 = 0
  C39 = -math.sin(C15)*math.cos(D15)
  C40 = math.cos(C15)*math.cos(D15)
  C41 = math.sin(D15)
  C42 = 0
  D39 = math.sin(C15)*math.sin(D15)
  D40 = -math.cos(C15)*math.sin(D15)
  D41 = math.cos(D15)
  D42 = 0
  E39 = F15*math.cos(C15)
  E40 = F15*math.sin(C15)
  E41 = 0
  E42 = 1
 
  B45 = math.cos(C16)
  B46 = math.sin(C16)
  B47 = 0
  B48 = 0
  C45 = -math.sin(C16)*math.cos(D16)
  C46 = math.cos(C16)*math.cos(D16)
  C47 = math.sin(D16)
  C48 = 0
  D45 = math.sin(C16)*math.sin(D16)
  D46 = -math.cos(C16)*math.sin(D16)
  D47 = math.cos(D16)
  D48 = 0
  E45 = F16*math.cos(C16)
  E46 = F16*math.sin(C16)
  E47 = E16
  E48 = 1

  B51 = math.cos(C17)
  B52 = math.sin(C17)
  B53 = 0
  B54 = 0
  C51 = -math.sin(C17)*math.cos(D17)
  C52 = math.cos(C17)*math.cos(D17)
  C53 = math.sin(D17)
  C54 = 0 
  D51 = math.sin(C17)*math.sin(D17)
  D52 = -math.cos(C17)*math.sin(D17)
  D53 = math.cos(D17)
  D54 = 0
  E51 = F17*math.cos(C17)
  E52 = F17*math.sin(C17)
  E53 = E17
  E54 = 1

  B57 = math.cos(C18)
  B58 = math.sin(C18)
  B59 = 0
  B60 = 0
  C57 = -math.sin(C18)*math.cos(D18)
  C58 = math.cos(C18)*math.cos(D18)
  C59 = math.sin(D18)
  C60 = 0
  D57 = math.sin(C18)*math.sin(D18)
  D58 = -math.cos(C18)*math.sin(D18)
  D59 = math.cos(D18)
  D60 = 0
  E57 = F18*math.cos(C18)
  E58 = F18*math.sin(C18)
  E59 = E18
  E60 = 1

  B63 = math.cos(math.radians(J18))*math.cos(math.radians(J17))
  B64 = math.sin(math.radians(J18))*math.cos(math.radians(J17))
  B65 = -math.sin(math.radians(J18))
  B66 = 0
  C63 = -math.sin(math.radians(J18))*math.cos(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  C64 = math.cos(math.radians(J18))*math.cos(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  C65 = math.cos(math.radians(J17))*math.sin(math.radians(J16))
  C66 = 0
  D63 = math.sin(math.radians(J18))*math.sin(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  D64 = -math.cos(math.radians(J18))*math.sin(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  D65 = math.cos(math.radians(J17))*math.cos(math.radians(J16))
  D66 = 0
  E63 = J13
  E64 = J14
  E65 = J15
  E66 = 1

  G24 = (B21*B27)+(C21*B28)+(D21*B29)+(E21*B30)
  G25 = (B22*B27)+(C22*B28)+(D22*B29)+(E22*B30)
  G26 = (B23*B27)+(C23*B28)+(D23*B29)+(E23*B30)
  G27 = (B24*B27)+(C24*B28)+(D24*B29)+(E24*B30)
  H24 = (B21*C27)+(C21*C28)+(D21*C29)+(E21*C30)
  H25 = (B22*C27)+(C22*C28)+(D22*C29)+(E22*C30)
  H26 = (B23*C27)+(C23*C28)+(D23*C29)+(E23*C30)
  H27 = (B24*C27)+(C24*C28)+(D24*C29)+(E24*C30)
  I24 = (B21*D27)+(C21*D28)+(D21*D29)+(E21*D30)
  I25 = (B22*D27)+(C22*D28)+(D22*D29)+(E22*D30)
  I26 = (B23*D27)+(C23*D28)+(D23*D29)+(E23*D30)
  I27 = (B24*D27)+(C24*D28)+(D24*D29)+(E24*D30)
  J24 = (B21*E27)+(C21*E28)+(D21*E29)+(E21*E30)
  J25 = (B22*E27)+(C22*E28)+(D22*E29)+(E22*E30)
  J26 = (B23*E27)+(C23*E28)+(D23*E29)+(E23*E30)
  J27 = (B24*E27)+(C24*E28)+(D24*E29)+(E24*E30)
  G30 = (G24*B33)+(H24*B34)+(I24*B35)+(J24*B36)
  G31 = (G25*B33)+(H25*B34)+(I25*B35)+(J25*B36)
  G32 = (G26*B33)+(H26*B34)+(I26*B35)+(J26*B36)
  G33 = (G27*B33)+(H27*B34)+(I27*B35)+(J27*B36)
  H30 = (G24*C33)+(H24*C34)+(I24*C35)+(J24*C36)
  H31 = (G25*C33)+(H25*C34)+(I25*C35)+(J25*C36)
  H32 = (G26*C33)+(H26*C34)+(I26*C35)+(J26*C36)
  H33 = (G27*C33)+(H27*C34)+(I27*C35)+(J27*C36)
  I30 = (G24*D33)+(H24*D34)+(I24*D35)+(J24*D36)
  I31 = (G25*D33)+(H25*D34)+(I25*D35)+(J25*D36)
  I32 = (G26*D33)+(H26*D34)+(I26*D35)+(J26*D36)
  I33 = (G27*D33)+(H27*D34)+(I27*D35)+(J27*D36)
  J30 = (G24*E33)+(H24*E34)+(I24*E35)+(J24*E36)
  J31 = (G25*E33)+(H25*E34)+(I25*E35)+(J25*E36)
  J32 = (G26*E33)+(H26*E34)+(I26*E35)+(J26*E36)
  J33 = (G27*E33)+(H27*E34)+(I27*E35)+(J27*E36)
  G36 = (G30*B39)+(H30*B40)+(I30*B41)+(J30*B42) 
  G37 = (G31*B39)+(H31*B40)+(I31*B41)+(J31*B42)  
  G38 = (G32*B39)+(H32*B40)+(I32*B41)+(J32*B42)  
  G39 = (G33*B39)+(H33*B40)+(I33*B41)+(J33*B42)  
  H36 = (G30*C39)+(H30*C40)+(I30*C41)+(J30*C42)  
  H37 = (G31*C39)+(H31*C40)+(I31*C41)+(J31*C42)  
  H38 = (G32*C39)+(H32*C40)+(I32*C41)+(J32*C42)  
  H39 = (G33*C39)+(H33*C40)+(I33*C41)+(J33*C42)  
  I36 = (G30*D39)+(H30*D40)+(I30*D41)+(J30*D42)  
  I37 = (G31*D39)+(H31*D40)+(I31*D41)+(J31*D42)  
  I38 = (G32*D39)+(H32*D40)+(I32*D41)+(J32*D42)  
  I39 = (G33*D39)+(H33*D40)+(I33*D41)+(J33*D42)  
  J36 = (G30*E39)+(H30*E40)+(I30*E41)+(J30*E42)  
  J37 = (G31*E39)+(H31*E40)+(I31*E41)+(J31*E42)  
  J38 = (G32*E39)+(H32*E40)+(I32*E41)+(J32*E42)  
  J39 = (G33*E39)+(H33*E40)+(I33*E41)+(J33*E42)
  G42 = (G36*B45)+(H36*B46)+(I36*B47)+(J36*B48)  
  G43 = (G37*B45)+(H37*B46)+(I37*B47)+(J37*B48) 
  G44 = (G38*B45)+(H38*B46)+(I38*B47)+(J38*B48) 
  G45 = (G39*B45)+(H39*B46)+(I39*B47)+(J39*B48) 
  H42 = (G36*C45)+(H36*C46)+(I36*C47)+(J36*C48)  
  H43 = (G37*C45)+(H37*C46)+(I37*C47)+(J37*C48) 
  H44 = (G38*C45)+(H38*C46)+(I38*C47)+(J38*C48) 
  H45 = (G39*C45)+(H39*C46)+(I39*C47)+(J39*C48) 
  I42 = (G36*D45)+(H36*D46)+(I36*D47)+(J36*D48)  
  I43 = (G37*D45)+(H37*D46)+(I37*D47)+(J37*D48) 
  I44 = (G38*D45)+(H38*D46)+(I38*D47)+(J38*D48) 
  I45 = (G39*D45)+(H39*D46)+(I39*D47)+(J39*D48) 
  J42 = (G36*E45)+(H36*E46)+(I36*E47)+(J36*E48)  
  J43 = (G37*E45)+(H37*E46)+(I37*E47)+(J37*E48) 
  J44 = (G38*E45)+(H38*E46)+(I38*E47)+(J38*E48) 
  J45 = (G39*E45)+(H39*E46)+(I39*E47)+(J39*E48)
  G48 = (G42*B51)+(H42*B52)+(I42*B53)+(J42*B54)
  G49 = (G43*B51)+(H43*B52)+(I43*B53)+(J43*B54)
  G50 = (G44*B51)+(H44*B52)+(I44*B53)+(J44*B54)
  G51 = (G45*B51)+(H45*B52)+(I45*B53)+(J45*B54)
  H48 = (G42*C51)+(H42*C52)+(I42*C53)+(J42*C54)
  H49 = (G43*C51)+(H43*C52)+(I43*C53)+(J43*C54)
  H50 = (G44*C51)+(H44*C52)+(I44*C53)+(J44*C54)
  H51 = (G45*C51)+(H45*C52)+(I45*C53)+(J45*C54)
  I48 = (G42*D51)+(H42*D52)+(I42*D53)+(J42*D54)
  I49 = (G43*D51)+(H43*D52)+(I43*D53)+(J43*D54)
  I50 = (G44*D51)+(H44*D52)+(I44*D53)+(J44*D54)
  I51 = (G45*D51)+(H45*D52)+(I45*D53)+(J45*D54)
  J48 = (G42*E51)+(H42*E52)+(I42*E53)+(J42*E54)
  J49 = (G43*E51)+(H43*E52)+(I43*E53)+(J43*E54)
  J50 = (G44*E51)+(H44*E52)+(I44*E53)+(J44*E54)
  J51 = (G45*E51)+(H45*E52)+(I45*E53)+(J45*E54)
  G54 = (G48*B57)+(H48*B58)+(I48*B59)+(J48*B60)
  G55 = (G49*B57)+(H49*B58)+(I49*B59)+(J49*B60)
  G56 = (G50*B57)+(H50*B58)+(I50*B59)+(J50*B60)
  G57 = (G51*B57)+(H51*B58)+(I51*B59)+(J51*B60)
  H54 = (G48*C57)+(H48*C58)+(I48*C59)+(J48*C60)
  H55 = (G49*C57)+(H49*C58)+(I49*C59)+(J49*C60)
  H56 = (G50*C57)+(H50*C58)+(I50*C59)+(J50*C60)
  H57 = (G51*C57)+(H51*C58)+(I51*C59)+(J51*C60)
  I54 = (G48*D57)+(H48*D58)+(I48*D59)+(J48*D60)
  I55 = (G49*D57)+(H49*D58)+(I49*D59)+(J49*D60)
  I56 = (G50*D57)+(H50*D58)+(I50*D59)+(J50*D60)
  I57 = (G51*D57)+(H51*D58)+(I51*D59)+(J51*D60)
  J54 = (G48*E57)+(H48*E58)+(I48*E59)+(J48*E60)
  J55 = (G49*E57)+(H49*E58)+(I49*E59)+(J49*E60)
  J56 = (G50*E57)+(H50*E58)+(I50*E59)+(J50*E60)
  J57 = (G51*E57)+(H51*E58)+(I51*E59)+(J51*E60)
  G60 = (G54*B63)+(H54*B64)+(I54*B65)+(J54*B66)
  G61 = (G55*B63)+(H55*B64)+(I55*B65)+(J55*B66)
  G62 = (G56*B63)+(H56*B64)+(I56*B65)+(J56*B66)
  G63 = (G57*B63)+(H57*B64)+(I57*B65)+(J57*B66)
  H60 = (G54*C63)+(H54*C64)+(I54*C65)+(J54*C66)
  H61 = (G55*C63)+(H55*C64)+(I55*C65)+(J55*C66)
  H62 = (G56*C63)+(H56*C64)+(I56*C65)+(J56*C66)
  H63 = (G57*C63)+(H57*C64)+(I57*C65)+(J57*C66)
  I60 = (G54*D63)+(H54*D64)+(I54*D65)+(J54*D66)
  I61 = (G55*D63)+(H55*D64)+(I55*D65)+(J55*D66)
  I62 = (G56*D63)+(H56*D64)+(I56*D65)+(J56*D66)
  I63 = (G57*D63)+(H57*D64)+(I57*D65)+(J57*D66)
  J60 = (G54*E63)+(H54*E64)+(I54*E65)+(J54*E66)
  J61 = (G55*E63)+(H55*E64)+(I55*E65)+(J55*E66)
  J62 = (G56*E63)+(H56*E64)+(I56*E65)+(J56*E66)
  J63 = (G57*E63)+(H57*E64)+(I57*E65)+(J57*E66)

  if E28 < 0:
    if E27 < 0:
      E7 = 1
    else: E7 = 2
  else:
    if E27 < 0:
      E7 = 4
    else: E7 = 3
  ##
  if J49 < 0:
    if J48 < 0:
      E8 = 1
    else:
      E8 = 2
  else:
    if J48 < 0:
      E8 = 4
    else:
      E8 = 3
 
  I8 = math.atan2(math.sqrt((I60**2)+(I61**2)),-I62)  
  I7 = math.atan2((G62/I8),(H62/I8))  
  I9 = math.atan2((I60/I8),(I61/I8))
  H4 = J48
  H5 = J49
  H6 = J50
  H7 = math.degrees(I7)
  H8 = math.degrees(I8)
  H9 = math.degrees(I9)  
  XcurPos = J48
  YcurPos = J49
  ZcurPos = J50
  RxcurPos = H7
  RycurPos = H8
  RzcurPos = H9
  XcurEntryField.delete(0, 'end')
  XcurEntryField.insert(0,str(XcurPos))
  YcurEntryField.delete(0, 'end')
  YcurEntryField.insert(0,str(YcurPos))
  ZcurEntryField.delete(0, 'end')
  ZcurEntryField.insert(0,str(ZcurPos))
  RxcurEntryField.delete(0, 'end')
  RxcurEntryField.insert(0,str(RxcurPos))
  RycurEntryField.delete(0, 'end')
  RycurEntryField.insert(0,str(RycurPos))
  RzcurEntryField.delete(0, 'end')
  RzcurEntryField.insert(0,str(RzcurPos))
  #manEntryField.delete(0, 'end')
  #manEntryField.insert(0,str(E7)+" "+str(E8))  



def MoveXYZ(CX,CY,CZ,CRx,CRy,CRz):
  CalcRevKin(CX,CY,CZ,CRx,CRy,CRz)  
  MoveNew(J1out,J2out,J3out,J4out,J5out,J6out)
  



def CalcRevKin(CX,CY,CZ,CRx,CRy,CRz):
  CalcFwdKin()
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  N4 = CX
  N5 = CY
  N6 = CZ
  N7 = CRx
  N8 = CRy 
  N9 = CRz
  global H4
  global H5
  global H6
  global H7
  global H8
  global H9
  global G60
  global G61
  global G62
  global H60
  global H61
  global H62
  global I60
  global I61
  global I62
  global E7
  global E8
  global E27
  global E28
  global DHa1
  global DHa2
  global DHa3 
  global DHd1
  global DHd4
  global G36
  global G37
  global G38
  global G39
  global H36
  global H37
  global H38
  global H39
  global I36
  global I37
  global I38
  global I39
  global J36
  global J37
  global J38
  global J39
  global J1out
  global J2out
  global J3out
  global J4out
  global J5out
  global J6out
  P13 = math.atan((H5+CY)/(H4+CX))
  if E7 == 1:
    Q13 = (math.degrees(P13)-90)-90
  else:
    if E7 == 2:
      Q13 = math.degrees(P13)
    else:
      if E7 == 3:
        Q13 = math.degrees(P13)
      else:
        Q13 = 90+math.degrees(P13)+90
  P14 = math.sqrt(((H5+CY)**2)+((H4+CX)**2))+DHa1
  P15 = math.sqrt(((H5+CY)**2)+((H4+CX)**2))
  P16 = abs(P15-DHa1)
  Q16 = P15-DHa1
  P17 = (H6+CZ)-DHd1
  if E7 == E8:
    P19 = math.sqrt((P16**2)+(P17**2))
  else:
    P19 = math.sqrt((P14**2)+(P17**2))
  P22 = math.atan(P17/P16)
  Q22 = math.degrees(P22)
  P23 = math.atan(P16/P17)
  Q23 = math.degrees(P23)
  P24 = math.sqrt((DHa3**2)+((abs(DHd4)**2)))
  P25 = math.atan(P17/P14)
  Q25 = math.degrees(P25)
  P26 = math.acos(((DHa2**2)+(P19**2)-(P24**2))/(2*DHa2*P19))
  Q26 = math.degrees(P26)
  P27 = math.atan2(math.sqrt(1-((((DHa2**2)+(P19**2)-(P24**2))/(2*DHa2*P19)))**2),(((DHa2**2)+(P19**2)-(P24**2))/(2*DHa2*P19)))
  Q27 = math.degrees(P27)
  if Q16>0 and E7==E8:
    Q28 = -(Q22+Q26)
  else:
    if Q16>0 and E7!=E8:
      Q28 = -(180-Q25+Q26)
    else:
      if Q16<0 and E7!=E8:
        Q28 = -(180-Q25+Q26)
      else:
        Q28 = -(Q26+Q23+90)
  P30 = math.acos(((P24**2)+(abs(DHd4)**2)-(DHa3**2))/(2*P24*abs(DHd4)))
  Q30 = math.degrees(P30)
  P32 = math.acos(((P24**2)+(DHa2**2)-(P19**2))/(2*P24*DHa2))
  Q32 = 180-math.degrees(P32)+Q30
  Q4 = Q13
  Q5 = Q28
  Q6 = Q32
  P37 = math.radians(Q4)
  P38 = math.radians(Q5)
  P39 = math.radians(Q6-90)
  Q37 = math.radians(-90)
  Q38 = math.radians(0)
  Q39 = math.radians(90)
  R37 = DHd1
  R38 = DHd2
  R39 = DHd3
  S37 = DHa1
  S38 = DHa2
  S39 = DHa3
  
  H13 = 0
  H14 = 0
  H15 = 0
  H16 = 0
  H17 = 0
  H18 = f0
 
  O45 = math.cos(math.radians(H18))*math.cos(math.radians(H17))
  O46 = math.sin(math.radians(H18))*math.cos(math.radians(H17))
  O47 = -math.sin(math.radians(H18))
  O48 = 0
  P45 = -math.sin(math.radians(H18))*math.cos(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  P46 = math.cos(math.radians(H18))*math.cos(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  P47 = math.cos(math.radians(H17))*math.sin(math.radians(H16))
  P48 = 0
  Q45 = math.sin(math.radians(H18))*math.sin(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  Q46 = -math.cos(math.radians(H18))*math.sin(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  Q47 = math.cos(math.radians(H17))*math.cos(math.radians(H16))
  Q48 = 0
  R45 = H13
  R46 = H14
  R47 = H15
  R48 = 1 

  O51 = math.cos(P37)
  O52 = math.sin(P37)
  O53 = 0
  O54 = 0
  P51 = -math.sin(P37)*math.cos(Q37)
  P52 = math.cos(P37)*math.cos(Q37)
  P53 = math.sin(Q37)
  P54 = 0  
  Q51 = math.sin(P37)*math.sin(Q37)
  Q52 = -math.cos(P37)*math.sin(Q37)
  Q53 = math.cos(Q37)
  Q54 = 0 
  R51 = S37*math.cos(P37)
  R52 = S37*math.sin(P37)
  R53 = R37
  R54 = 1

  O57 = math.cos(P38)
  O58 = math.sin(P38)
  O59 = 0
  O60 = 0
  P57 = -math.sin(P38)*math.cos(Q38)
  P58 = math.cos(P38)*math.cos(Q38)
  P59 = math.sin(Q38)
  P60 = 0
  Q57 = math.sin(P38)*math.sin(Q38)
  Q58 = -math.cos(P38)*math.sin(Q38)
  Q59 = math.cos(Q38)
  Q60 = 0
  R57 = S38*math.cos(P38)
  R58 = S38*math.sin(P38)
  R59 = R38
  R60 = 1

  O63 = math.cos(P39)
  O64 = math.sin(P39)
  O65 = 0
  O66 = 0
  P63 = -math.sin(P39)*math.cos(Q39)
  P64 = math.cos(P39)*math.cos(Q39)
  P65 = math.sin(Q39)
  P66 = 0
  Q63 = math.sin(P39)*math.sin(Q39)
  Q64 = -math.cos(P39)*math.sin(Q39)
  Q65 = math.cos(Q39)
  Q66 = 0
  R63 = S39*math.cos(P39)
  R64 = S39*math.sin(P39)
  R65 = 0
  R66 = 1

  T48 = (O45*O51)+(P45*O52)+(Q45*O53)+(R45*O54)
  T49 = (O46*O51)+(P46*O52)+(Q46*O53)+(R46*O54)
  T50 = (O47*O51)+(P47*O52)+(Q47*O53)+(R47*O54)
  T51 = (O48*O51)+(P48*O52)+(Q48*O53)+(R48*O54) 
  U48 = (O45*P51)+(P45*P52)+(Q45*P53)+(R45*P54)
  U49 = (O46*P51)+(P46*P52)+(Q46*P53)+(R46*P54)
  U50 = (O47*P51)+(P47*P52)+(Q47*P53)+(R47*P54)
  U51 = (O48*P51)+(P48*P52)+(Q48*P53)+(R48*P54)
  V48 = (O45*Q51)+(P45*Q52)+(Q45*Q53)+(R45*Q54)
  V49 = (O46*Q51)+(P46*Q52)+(Q46*Q53)+(R46*Q54)
  V50 = (O47*Q51)+(P47*Q52)+(Q47*Q53)+(R47*Q54)
  V51 = (O48*Q51)+(P48*Q52)+(Q48*Q53)+(R48*Q54)
  W48 = (O45*R51)+(P45*R52)+(Q45*R53)+(R45*R54)
  W49 = (O46*R51)+(P46*R52)+(Q46*R53)+(R46*R54)
  W50 = (O47*R51)+(P47*R52)+(Q47*R53)+(R47*R54)
  W51 = (O48*R51)+(P48*R52)+(Q48*R53)+(R48*R54) 
  T54 = (T48*O57)+(U48*O58)+(V48*O59)+(W48*O60)
  T55 = (T49*O57)+(U49*O58)+(V49*O59)+(W49*O60)
  T56 = (T50*O57)+(U50*O58)+(V50*O59)+(W50*O60)
  T57 = (T51*O57)+(U51*O58)+(V51*O59)+(W51*O60)
  U54 = (T48*P57)+(U48*P58)+(V48*P59)+(W48*P60)
  U55 = (T49*P57)+(U49*P58)+(V49*P59)+(W49*P60)
  U56 = (T50*P57)+(U50*P58)+(V50*P59)+(W50*P60)
  U57 = (T51*P57)+(U51*P58)+(V51*P59)+(W51*P60)
  V54 = (T48*Q57)+(U48*Q58)+(V48*Q59)+(W48*Q60)
  V55 = (T49*Q57)+(U49*Q58)+(V49*Q59)+(W49*Q60)
  V56 = (T50*Q57)+(U50*Q58)+(V50*Q59)+(W50*Q60)
  V57 = (T51*Q57)+(U51*Q58)+(V51*Q59)+(W51*Q60)
  W54 = (T48*R57)+(U48*R58)+(V48*R59)+(W48*R60)
  W55 = (T49*R57)+(U49*R58)+(V49*R59)+(W49*R60)
  W56 = (T50*R57)+(U50*R58)+(V50*R59)+(W50*R60)
  W57 = (T51*R57)+(U51*R58)+(V51*R59)+(W51*R60) 
  T60 = (T54*O63)+(U54*O64)+(V54*O65)+(W54*O66)
  T61 = (T55*O63)+(U55*O64)+(V55*O65)+(W55*O66)
  T62 = (T56*O63)+(U56*O64)+(V56*O65)+(W56*O66)
  T63 = (T57*O63)+(U57*O64)+(V57*O65)+(W57*O66)
  U60 = (T54*P63)+(U54*P64)+(V54*P65)+(W54*P66)
  U61 = (T55*P63)+(U55*P64)+(V55*P65)+(W55*P66)
  U62 = (T56*P63)+(U56*P64)+(V56*P65)+(W56*P66)
  U63 = (T57*P63)+(U57*P64)+(V57*P65)+(W57*P66)
  V60 = (T54*Q63)+(U54*Q64)+(V54*Q65)+(W54*Q66)
  V61 = (T55*Q63)+(U55*Q64)+(V55*Q65)+(W55*Q66)
  V62 = (T56*Q63)+(U56*Q64)+(V56*Q65)+(W56*Q66)
  V63 = (T57*Q63)+(U57*Q64)+(V57*Q65)+(W57*Q66)
  W60 = (T54*R63)+(U54*R64)+(V54*R65)+(W54*R66)
  W61 = (T55*R63)+(U55*R64)+(V55*R65)+(W55*R66)
  W62 = (T56*R63)+(U56*R64)+(V56*R65)+(W56*R66)
  W63 = (T57*R63)+(U57*R64)+(V57*R65)+(W57*R66)
 
  Y48 = U61
  Y49 = U62
  Z48 = V61
  Z49 = V62
  AA48 = T61
  AA49 = T62
  AB48 = V61
  AB49 = V62
  AC48 = T61
  AC49 = T62
  AD48 = U61
  AD49 = U62
  Y50 = U60
  Y51 = U62
  Z50 = V60
  Z51 = V62
  AA50 = T60
  AA51 = T62
  AB50 = V60
  AB51 = V62
  AC50 = T60
  AC51 = T62
  AD50 = U60
  AD51 = U62
  Y52 = U60
  Y53 = U61
  Z52 = V60
  Z53 = V61
  AA52 = T60
  AA53 = T61
  AB52 = V60
  AB53 = V61
  AC52 = T60
  AC53 = T61
  AD52 = U60
  AD53 = U61
 
  Y56 = (Y48*Z49)-(Y49*Z48)
  Y57 = (Y50*Z51)-(Y51*Z50)
  Y58 = (Y52*Z53)-(Y53*Z52)
  Z56 = (AA48*AB49)-(AA49*AB48)
  Z57 = (AA50*AB51)-(AA51*AB50)
  Z58 = (AA52*AB53)-(AA53*AB52)
  AA56 = (AC48*AD49)-(AC49*AD48)
  AA57 = (AC50*AD51)-(AC51*AD50)
  AA58 = (AC52*AD53)-(AC53*AD52)

  Y61 = 1
  Y62 = -1
  Y63 = 1
  Z61 = -1
  Z62 = 1
  Z63 = -1
  AA61 = 1
  AA62 = -1
  AA63 = 1

  AC61 = Y56*Y61
  AC62 = Y57*Y62
  AC63 = Y58*Y63
  AD61 = Z56*Z61
  AD62 = Z57*Z62
  AD63 = Z58*Z63
  AE61 = AA56*AA61
  AE62 = AA57*AA62
  AE63 = AA58*AA63
  
  Y66 = AC61
  Y67 = AD61
  Y68 = AE61
  Z66 = AC62
  Z67 = AD62
  Z68 = AE62
  AA66 = AC63
  AA67 = AD63
  AA68 = AE63
  #
  Y71 = (T60*AC61)+(U60*AD61)+(V60*AE61)
 
  AA71 = 1/Y71*Y66
  AA72 = 1/Y71*Y67
  AA73 = 1/Y71*Y68
  AB71 = 1/Y71*Z66
  AB72 = 1/Y71*Z67
  AB73 = 1/Y71*Z68
  AC71 = 1/Y71*AA66
  AC72 = 1/Y71*AA67
  AC73 = 1/Y71*AA68

  O69 = math.cos(math.radians(N9))
  O70 = math.sin(math.radians(N9))
  O71 = 0
  P69 = -math.sin(math.radians(N9))
  P70 = math.cos(math.radians(N9))
  P71 = 0
  Q69 = 0
  Q70 = 0
  Q71 = 1

  O74 = math.cos(math.radians(N8))
  O75 = 0
  O76 = -math.sin(math.radians(N8))
  P74 = 0
  P75 = 1
  P76 = 0
  Q74 = math.sin(math.radians(N8))
  Q75 = 0
  Q76 = math.cos(math.radians(N8))

  O79 = 1
  O80 = 0
  O81 = 0
  P79 = 0
  P80 = math.cos(math.radians(N7))
  P81 = math.sin(math.radians(N7))
  Q79 = 0
  Q80 = -math.sin(math.radians(N7))
  Q81 = math.cos(math.radians(N7))

  O84 = G60
  O85 = G61
  O86 = G62
  P84 = H60
  P85 = H61
  P86 = H62
  Q84 = I60
  Q85 = I61
  Q86 = I62

  S72 = (O69*O74)+(P69*O75)+(Q69*O76)
  S73 = (O70*O74)+(P70*O75)+(Q70*O76)
  S74 = (O71*O74)+(P71*O75)+(Q71*O76)
  T72 = (O69*P74)+(P69*P75)+(Q69*P76)
  T73 = (O70*P74)+(P70*P75)+(Q70*P76)
  T74 = (O71*P74)+(P71*P75)+(Q71*P76)
  U72 = (O69*Q74)+(P69*Q75)+(Q69*Q76)
  U73 = (O70*Q74)+(P70*Q75)+(Q70*Q76)
  U74 = (O71*Q74)+(P71*Q75)+(Q71*Q76)

  S77 = (S72*O79)+(T72*O80)+(U72*O81)
  S78 = (S73*O79)+(T73*O80)+(U73*O81)
  S79 = (S74*O79)+(T74*O80)+(U74*O81)
  T77 = (S72*P79)+(T72*P80)+(U72*P81)
  T78 = (S73*P79)+(T73*P80)+(U73*P81)
  T79 = (S74*P79)+(T74*P80)+(U74*P81)
  U77 = (S72*Q79)+(T72*Q80)+(U72*Q81)
  U78 = (S73*Q79)+(T73*Q80)+(U73*Q81)
  U79 = (S74*Q79)+(T74*Q80)+(U74*Q81)

  S82 = (S77*O84)+(T77*O85)+(U77*O86)
  S83 = (S78*O84)+(T78*O85)+(U78*O86)
  S84 = (S79*O84)+(T79*O85)+(U79*O86)
  T82 = (S77*P84)+(T77*P85)+(U77*P86)
  T83 = (S78*P84)+(T78*P85)+(U78*P86)
  T84 = (S79*P84)+(T79*P85)+(U79*P86)
  U82 = (S77*Q84)+(T77*Q85)+(U77*Q86)
  U83 = (S78*Q84)+(T78*Q85)+(U78*Q86)
  U84 = (S79*Q84)+(T79*Q85)+(U79*Q86)

  O89 = (AA71*S82)+(AB71*S83)+(AC71*S84)
  O90 = (AA72*S82)+(AB72*S83)+(AC72*S84)
  O91 = (AA73*S82)+(AB73*S83)+(AC73*S84)
  P89 = (AA71*T82)+(AB71*T83)+(AC71*T84)
  P90 = (AA72*T82)+(AB72*T83)+(AC72*T84)
  P91 = (AA73*T82)+(AB73*T83)+(AC73*T84)
  Q89 = (AA71*U82)+(AB71*U83)+(AC71*U84)
  Q90 = (AA72*U82)+(AB72*U83)+(AC72*U84)
  Q91 = (AA73*U82)+(AB73*U83)+(AC73*U84) 

  R7 = math.degrees(math.atan2(Q90,Q89))
  R8 = math.degrees(math.atan2(+math.sqrt(1-Q91**2),Q91))
  if (P91<0):
    R9 = math.degrees(math.atan2(P91,-O91))+180
  else:
    R9 = math.degrees(math.atan2(P91,-O91))-180
  S7 = math.degrees(math.atan2(-Q90,-Q89))
  S8 = math.degrees(math.atan2(-math.sqrt(1-Q91**2),Q91))  
  if (P91<0):
    S9 = math.degrees(math.atan2(-P91,O91))-180
  else:
    S9 = math.degrees(math.atan2(-P91,O91))+180  
  if (J5AngCur>0 and R8>0):
    Q8 = R8
  else:
    Q8 = S8
  if (Q8>0):
    Q7 = R7
  else:
    Q7 = S7
  if (Q8<0):
    Q9 = S9
  else:
    Q9 = R9
  J1out = Q4
  J2out = Q5
  J3out = Q6
  J4out = Q7
  J5out = Q8
  J6out = Q9
  return (J1out,J2out,J3out,J4out,J5out,J6out)

  
  

def MoveNew(J1out,J2out,J3out,J4out,J5out,J6out):
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  J1newAng = J1out
  J2newAng = J2out
  J3newAng = J3out
  J4newAng = J4out
  J5newAng = J5out
  J6newAng = J6out
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
 
  if (J1newAng < J1NegAngLim or J1newAng > J1PosAngLim) or (J2newAng < J2NegAngLim or J2newAng > J2PosAngLim) or (J3newAng < J3NegAngLim or J3newAng > J3PosAngLim) or (J4newAng < J4NegAngLim or J4newAng > J4PosAngLim) or (J5newAng < J5NegAngLim or J5newAng > J5PosAngLim) or (J6newAng < J6NegAngLim or J6newAng > J6PosAngLim):
    almStatusLab.config(text="AXIS LIMIT", bg = "red")
  else:  
    ##J1 calc##
    if (float(J1newAng) >= float(J1AngCur)):   
      J1dir = "0"
      J1calcAng = float(J1newAng) - float(J1AngCur)
      J1steps = int(J1calcAng / J1DegPerStep)
      J1StepCur = J1StepCur + J1steps #Invert       
      J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1steps = str(J1steps) 
    elif (float(J1newAng) < float(J1AngCur)):
      J1dir = "1"
      J1calcAng = float(J1AngCur) - float(J1newAng)
      J1steps = int(J1calcAng / J1DegPerStep)
      J1StepCur = J1StepCur - J1steps #Invert       
      J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1steps = str(J1steps) 
    ##J2 calc##
    if (float(J2newAng) >= float(J2AngCur)):
      J2dir = "0"
      J2calcAng = float(J2newAng) - float(J2AngCur)
      J2steps = int(J2calcAng / J2DegPerStep)
      J2StepCur = J2StepCur + J2steps #Invert       
      J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2steps = str(J2steps) 
    elif (float(J2newAng) < float(J2AngCur)):
      J2dir = "1"
      J2calcAng = float(J2AngCur) - float(J2newAng)
      J2steps = int(J2calcAng / J2DegPerStep)
      J2StepCur = J2StepCur - J2steps #Invert       
      J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2steps = str(J2steps) 
    ##J3 calc##
    if (float(J3newAng) >= float(J3AngCur)):
      J3dir = "0"
      J3calcAng = float(J3newAng) - float(J3AngCur)
      J3steps = int(J3calcAng / J3DegPerStep)
      J3StepCur = J3StepCur + J3steps #Invert       
      J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3steps = str(J3steps) 
    elif (float(J3newAng) < float(J3AngCur)):
      J3dir = "1"
      J3calcAng = float(J3AngCur) - float(J3newAng)
      J3steps = int(J3calcAng / J3DegPerStep)
      J3StepCur = J3StepCur - J3steps #Invert       
      J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3steps = str(J3steps)  
    ##J4 calc##
    if (float(J4newAng) >= float(J4AngCur)):
      J4dir = "0"
      J4calcAng = float(J4newAng) - float(J4AngCur)
      J4steps = int(J4calcAng / J4DegPerStep)
      J4StepCur = J4StepCur - J4steps #Invert       
      J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4steps = str(J4steps) 
    elif (float(J4newAng) < float(J4AngCur)):
      J4dir = "1"
      J4calcAng = float(J4AngCur) - float(J4newAng)
      J4steps = int(J4calcAng / J4DegPerStep)
      J4StepCur = J4StepCur + J4steps #Invert       
      J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4steps = str(J4steps)     
    ##J5 calc##
    if (float(J5newAng) >= float(J5AngCur)):
      J5dir = "0"
      J5calcAng = float(J5newAng) - float(J5AngCur)
      J5steps = int(J5calcAng / J5DegPerStep)
      J5StepCur = J5StepCur + J5steps #Invert       
      J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5steps = str(J5steps) 
    elif (float(J5newAng) < float(J5AngCur)):
      J5dir = "1"
      J5calcAng = float(J5AngCur) - float(J5newAng)
      J5steps = int(J5calcAng / J5DegPerStep)
      J5StepCur = J5StepCur - J5steps #Invert       
      J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5steps = str(J5steps)  
    ##J6 calc##
    if (float(J6newAng) >= float(J6AngCur)):
      J6dir = "0"
      J6calcAng = float(J6newAng) - float(J6AngCur)
      J6steps = int(J6calcAng / J6DegPerStep)
      J6StepCur = J6StepCur - J6steps #Invert       
      J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6steps = str(J6steps) 
    elif (float(J6newAng) < float(J6AngCur)):
      J6dir = "1"
      J6calcAng = float(J6AngCur) - float(J6newAng)
      J6steps = int(J6calcAng / J6DegPerStep)
      J6StepCur = J6StepCur + J6steps #Invert       
      J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6steps = str(J6steps) 
    commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"S"+newSpeed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd
    ser.write((commandCalc +"\n").encode())
    ser.flushInput()
    time.sleep(.2)
    ser.read() 
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    CalcFwdKin()
    DisplaySteps()
    savePosData()  



  

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
#####TAB 1



curRowLab = Label(tab1, text = "Current Row  = ")
curRowLab.place(x=407, y=150)

almStatusLab = Label(tab1, text = "SYSTEM READY - NO ACTIVE ALARMS", bg = "grey")
almStatusLab.place(x=175, y=10)


runStatusLab = Label(tab1, text = "PROGRAM STOPPED", bg = "red")
runStatusLab.place(x=20, y=150)

regEqLab = Label(tab1, font=("Arial", 6), text="Register           Num (or +)")
regEqLab.place(x=857, y=447)

ifregTabJmpLab = Label(tab1, font=("Arial", 6), text="Register             Num          Jump to Tab")
ifregTabJmpLab.place(x=857, y=487)

servoLab = Label(tab1, font=("Arial", 6), text="Number        Position")
servoLab.place(x=870, y=365)


ComPortLab = Label(tab1, text = "COM PORT:")
ComPortLab.place(x=10, y=10)

ProgLab = Label(tab1, text = "Program:")
ProgLab.place(x=10, y=45)

speedLab = Label(tab1, text = "Robot Speed (%)")
speedLab.place(x=565, y=260)

ACCLab = Label(tab1, text = "ACC(time/speed %)")
ACCLab.place(x=590, y=285)

DECLab = Label(tab1, text = "DEC(time/speed %)")
DECLab.place(x=590, y=310)


J1Lab = Label(tab1, font=("Arial", 18), text = "J1")
J1Lab.place(x=660, y=5)

J2Lab = Label(tab1, font=("Arial",18), text = "J2")
J2Lab.place(x=750, y=5)

J3Lab = Label(tab1, font=("Arial", 18), text = "J3")
J3Lab.place(x=840, y=5)

J4Lab = Label(tab1, font=("Arial", 18), text = "J4")
J4Lab.place(x=930, y=5)

J5Lab = Label(tab1, font=("Arial", 18), text = "J5")
J5Lab.place(x=1020, y=5)

J6Lab = Label(tab1, font=("Arial", 18), text = "J6")
J6Lab.place(x=1110, y=5)



stepCol = "firebrick"

StepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "/step")
StepsLab.place(x=620, y=40)

J1stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J1stepsLab.place(x=695, y=40)

J2stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J2stepsLab.place(x=785, y=40)

J3stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J3stepsLab.place(x=875, y=40)

J4stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J4stepsLab.place(x=965, y=40)

J5stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J5stepsLab.place(x=1055, y=40)

J6stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J6stepsLab.place(x=1145, y=40)





XLab = Label(tab1, font=("Arial", 18), text=" X")
XLab.place(x=660, y=125)

YLab = Label(tab1, font=("Arial", 18), text=" Y")
YLab.place(x=750, y=125)

ZLab = Label(tab1, font=("Arial", 18), text=" Z")
ZLab.place(x=840, y=125)

yLab = Label(tab1, font=("Arial", 18), text="Rx")
yLab.place(x=930, y=125)

pLab = Label(tab1, font=("Arial", 18), text="Ry")
pLab.place(x=1020, y=125)

rLab = Label(tab1, font=("Arial", 18), text="Rz")
rLab.place(x=1110, y=125)

J1curAngLab = Label(tab1, text="Current Angle:")
J1curAngLab.place(x=540, y=40)

XYZcurPoLab = Label(tab1, text="Current Position:")
XYZcurPoLab.place(x=540, y=160)

J1jogDegsLab = Label(tab1, text="Degrees/Steps to Jog:")
J1jogDegsLab.place(x=540, y=65)

XYZjogMMLab = Label(tab1, text="Millimeters to Jog:")
XYZjogMMLab.place(x=540, y=185)

J1jogRobotLab = Label(tab1, text="JOG ROBOT")
J1jogRobotLab.place(x=540, y=92)

XYZjogRobotLab = Label(tab1, text="JOG ROBOT")
XYZjogRobotLab.place(x=540, y=212)

waitTequalsLab = Label(tab1, text="=")
waitTequalsLab.place(x=855, y=260)


tabequalsLab = Label(tab1, text="=")
tabequalsLab.place(x=855, y=300)

jumpequalsLab = Label(tab1, text="=")
jumpequalsLab.place(x=855, y=340)


servoequalsLab = Label(tab1, text="=")
servoequalsLab.place(x=855, y=380)

changeProgequalsLab = Label(tab1, text="=")
changeProgequalsLab.place(x=855, y=420)

regequalsLab = Label(tab1, text="=")
regequalsLab.place(x=897, y=461)

regJmpequalsLab = Label(tab1, text="=")
regJmpequalsLab.place(x=897, y=501)


Bklogo = Label(tab1, height=100, width=147)
bkPhoto = PhotoImage(file="Bk.gif")
Bklogo.config(image=bkPhoto, width="100", height="147")
Bklogo.place(x=429, y=0)





###BUTTONS################################################################
##########################################################################




teachInsBut = Button(tab1, bg="grey85", text="Teach New Position", height=1, width=20, command=teachInsertBelSelected)
teachInsBut.place(x=540, y=340)

teachReplaceBut = Button(tab1, bg="grey85", text="Modify Position", height=1, width=20, command=teachReplaceSelected)
teachReplaceBut.place(x=540, y=380)

waitTimeBut = Button(tab1, bg="grey85", text="Wait Time (seconds)", height=1, width=20, command=waitTime)
waitTimeBut.place(x=700, y=260)

tabNumBut = Button(tab1, bg="grey85", text="Create Tab Number", height=1, width=20, command=tabNumber)
tabNumBut.place(x=700, y=300)


jumpTabBut = Button(tab1, bg="grey85", text="Jump to Tab", height=1, width=20, command=jumpTab)
jumpTabBut.place(x=700, y=340)


servoBut = Button(tab1, bg="grey85", text="Servo", height=1, width=20, command=Servo)
servoBut.place(x=700, y=380)


callBut = Button(tab1, bg="grey85", text="Call Program", height=1, width=20, command=insertCallProg)
callBut.place(x=700, y=420)

returnBut = Button(tab1, bg="grey85", text="Return", height=1, width=20, command=insertReturn)
returnBut.place(x=540, y=500)

comPortBut = Button(tab1, bg="grey85", text="Set Com", height=0, width=7, command=setCom)
comPortBut.place(x=103, y=7)

ProgBut = Button(tab1, bg="grey85", text="Load Program", height=0, width=12, command=loadProg)
ProgBut.place(x=202, y=42)

deleteBut = Button(tab1, bg="grey85", text="Delete", height=1, width=20, command=deleteitem)
deleteBut.place(x=540, y=420)

runProgBut = Button(tab1, height=60, width=60, command=runProg)
playPhoto = PhotoImage(file="play.gif")
runProgBut.config(image=playPhoto, width="60", height="60")
runProgBut.place(x=20, y=80)

stopProgBut = Button(tab1, height=60, width=60, command=stopProg)
stopPhoto = PhotoImage(file="stop.gif")
stopProgBut.config(image=stopPhoto, width="60", height="60")
stopProgBut.place(x=220, y=80)

fwdBut = Button(tab1, height=50, width=50, command=stepFwd)
fwPhoto = PhotoImage(file="1.gif")
fwdBut.config(image=fwPhoto, width="50", height="50")
fwdBut.place(x=100, y=80)

revBut = Button(tab1, height=50, width=50, command=stepRev)
rePhoto = PhotoImage(file="2.gif")
revBut.config(image=rePhoto, width="50", height="50")
revBut.place(x=150, y=80)

RegNumBut = Button(tab1, bg="grey85", text="Register", height=1, width=20, command=insertRegister)
RegNumBut.place(x=700, y=460)

RegJmpBut = Button(tab1, bg="grey85", text="If Register Jump", height=1, width=20, command=IfRegjumpTab)
RegJmpBut.place(x=700, y=500)

CalibrateBut = Button(tab1, bg="grey85", text="Auto Calibrate CMD", height=1, width=20, command=insCalibrate)
CalibrateBut.place(x=540, y=460)




J1jogNegBut = Button(tab1, bg="grey85", text="-", height=1, width=3, command = J1jogNeg)
J1jogNegBut.place(x=642, y=90)

J1jogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = J1jogPos)
J1jogPosBut.place(x=680, y=90)

J2jogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = J2jogNeg)
J2jogNegBut.place(x=732, y=90)

J2jogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = J2jogPos)
J2jogPosBut.place(x=770, y=90)

J3jogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = J3jogNeg)
J3jogNegBut.place(x=822, y=90)

J3jogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = J3jogPos)
J3jogPosBut.place(x=860, y=90)

J4jogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = J4jogNeg)
J4jogNegBut.place(x=912, y=90)

J4jogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = J4jogPos)
J4jogPosBut.place(x=950, y=90)

J5jogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = J5jogNeg)
J5jogNegBut.place(x=1002, y=90)

J5jogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = J5jogPos)
J5jogPosBut.place(x=1040, y=90)

J6jogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = J6jogNeg)
J6jogNegBut.place(x=1092, y=90)

J6jogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = J6jogPos)
J6jogPosBut.place(x=1130, y=90)

XjogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = XjogNeg)
XjogNegBut.place(x=642, y=210)

XjogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = XjogPos)
XjogPosBut.place(x=680, y=210)

YjogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = YjogNeg)
YjogNegBut.place(x=732, y=210)

YjogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = YjogPos)
YjogPosBut.place(x=770, y=210)

ZjogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = ZjogNeg)
ZjogNegBut.place(x=822, y=210)

ZjogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = ZjogPos)
ZjogPosBut.place(x=860, y=210)

RxjogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = RxjogNeg)
RxjogNegBut.place(x=912, y=210)

RxjogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = RxjogPos)
RxjogPosBut.place(x=950, y=210)

RyjogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = RyjogNeg)
RyjogNegBut.place(x=1002, y=210)

RyjogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = RyjogPos)
RyjogPosBut.place(x=1040, y=210)

RzjogNegBut = Button(tab1, bg="grey85",text="-", height=1, width=3, command = RzjogNeg)
RzjogNegBut.place(x=1092, y=210)

RzjogPosBut = Button(tab1, bg="grey85",text="+", height=1, width=3, command = RzjogPos)
RzjogPosBut.place(x=1130, y=210)

JogStepsCbut = Checkbutton(tab1,fg="crimson",font=("Arial 14 bold"), text="Jog in steps",variable = JogStepsStat)
JogStepsCbut.place(x=1015, y=260)









####ENTRY FIELDS##########################################################
##########################################################################



curRowEntryField = Entry(tab1, width=5)
curRowEntryField.place(x=497, y=150)

#manEntryField = Entry(tab1, width=40)
#manEntryField.place(x=540, y=645)

ProgEntryField = Entry(tab1, width=20)
ProgEntryField.place(x=70, y=45)

comPortEntryField = Entry(tab1, width=2)
comPortEntryField.place(x=80, y=10)

speedEntryField = Entry(tab1, width=3)
speedEntryField.place(x=540, y=260)

ACCdurField = Entry(tab1, width=3)
ACCdurField.place(x=540, y=285)

DECdurField = Entry(tab1, width=3)
DECdurField.place(x=540, y=310)

ACCspeedField = Entry(tab1, width=3)
ACCspeedField.place(x=565, y=285)

DECspeedField = Entry(tab1, width=3)
DECspeedField.place(x=565, y=310)

waitTimeEntryField = Entry(tab1, width=5)
waitTimeEntryField.place(x=872, y=263)



tabNumEntryField = Entry(tab1, width=5)
tabNumEntryField.place(x=872, y=303)
#tabNumEntryField.place(x=1092, y=363)

jumpTabEntryField = Entry(tab1, width=5)
jumpTabEntryField.place(x=872, y=343)



servoNumEntryField = Entry(tab1, width=5)
servoNumEntryField.place(x=872, y=383)

servoPosEntryField = Entry(tab1, width=5)
servoPosEntryField.place(x=915, y=383)

changeProgEntryField = Entry(tab1, width=12)
changeProgEntryField.place(x=872, y=423)

regNumEntryField = Entry(tab1, width=5)
regNumEntryField.place(x=860, y=463)

regEqEntryField = Entry(tab1, width=5)
regEqEntryField.place(x=912, y=463)

regNumJmpEntryField = Entry(tab1, width=5)
regNumJmpEntryField.place(x=860, y=503)

regEqJmpEntryField = Entry(tab1, width=5)
regEqJmpEntryField.place(x=912, y=503)

regTabJmpEntryField = Entry(tab1, width=5)
regTabJmpEntryField.place(x=964, y=503)




  ### J1 ###

J1curAngEntryField = Entry(tab1,width=5)
J1curAngEntryField.place(x=660, y=40)

J1jogDegsEntryField = Entry(tab1,width=5)
J1jogDegsEntryField.place(x=660, y=65)


   ### J2 ###

J2curAngEntryField = Entry(tab1,width=5)
J2curAngEntryField.place(x=750, y=40)

J2jogDegsEntryField = Entry(tab1,width=5)
J2jogDegsEntryField.place(x=750, y=65)


   ### J3 ###

J3curAngEntryField = Entry(tab1,width=5)
J3curAngEntryField.place(x=840, y=40)

J3jogDegsEntryField = Entry(tab1,width=5)
J3jogDegsEntryField.place(x=840, y=65)


   ### J4 ###

J4curAngEntryField = Entry(tab1,width=5)
J4curAngEntryField.place(x=930, y=40)

J4jogDegsEntryField = Entry(tab1,width=5)
J4jogDegsEntryField.place(x=930, y=65)


   ### J5 ###

J5curAngEntryField = Entry(tab1,width=5)
J5curAngEntryField.place(x=1020, y=40)

J5jogDegsEntryField = Entry(tab1,width=5)
J5jogDegsEntryField.place(x=1020, y=65)


   ### J6 ###

J6curAngEntryField = Entry(tab1,width=5)
J6curAngEntryField.place(x=1110, y=40)

J6jogDegsEntryField = Entry(tab1,width=5)
J6jogDegsEntryField.place(x=1110, y=65)







  ### X ###

XcurEntryField = Entry(tab1,width=5)
XcurEntryField.place(x=660, y=160)

XjogEntryField = Entry(tab1,width=5)
XjogEntryField.place(x=660, y=185)


   ### Y ###

YcurEntryField = Entry(tab1,width=5)
YcurEntryField.place(x=750, y=160)

YjogEntryField = Entry(tab1,width=5)
YjogEntryField.place(x=750, y=185)


   ### Z ###

ZcurEntryField = Entry(tab1,width=5)
ZcurEntryField.place(x=840, y=160)

ZjogEntryField = Entry(tab1,width=5)
ZjogEntryField.place(x=840, y=185)


   ### Rx ###

RxcurEntryField = Entry(tab1,width=5)
RxcurEntryField.place(x=930, y=160)

RxjogEntryField = Entry(tab1,width=5)
RxjogEntryField.place(x=930, y=185)


   ### Ry ###

RycurEntryField = Entry(tab1,width=5)
RycurEntryField.place(x=1020, y=160)

RyjogEntryField = Entry(tab1,width=5)
RyjogEntryField.place(x=1020, y=185)


   ### Rz ###

RzcurEntryField = Entry(tab1,width=5)
RzcurEntryField.place(x=1110, y=160)

RzjogEntryField = Entry(tab1,width=5)
RzjogEntryField.place(x=1110, y=185)











####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 2




### 2 LABELS#################################################################
##########################################################################


fineCalLab = Label(tab2, fg = "orange4", text = "Fine Calibration Position:")
fineCalLab.place(x=10, y=83)


CalibrationValuesLab = Label(tab2, text = "Robot Calibration Values:")
CalibrationValuesLab.place(x=380, y=8)

DHValuesLab = Label(tab2, text = "DH Table :")
DHValuesLab.place(x=650, y=8)


J1NegAngLimLab = Label(tab2, text = "J1 Neg Ang Lim")
J1PosAngLimLab = Label(tab2, text = "J1 Pos Ang Lim")
J1StepLimLab = Label(tab2, text = "J1 Step Lim")

J2NegAngLimLab = Label(tab2, text = "J2 Neg Ang Lim")
J2PosAngLimLab = Label(tab2, text = "J2 Pos Ang Lim")
J2StepLimLab = Label(tab2, text = "J2 Step Lim")

J3NegAngLimLab = Label(tab2, text = "J3 Neg Ang Lim")
J3PosAngLimLab = Label(tab2, text = "J3 Pos Ang Lim")
J3StepLimLab = Label(tab2, text = "J3 Step Lim")

J4NegAngLimLab = Label(tab2, text = "J4 Neg Ang Lim")
J4PosAngLimLab = Label(tab2, text = "J4 Pos Ang Lim")
J4StepLimLab = Label(tab2, text = "J4 Step Lim")

J5NegAngLimLab = Label(tab2, text = "J5 Neg Ang Lim")
J5PosAngLimLab = Label(tab2, text = "J5 Pos Ang Lim")
J5StepLimLab = Label(tab2, text = "J5 Step Lim")

J6NegAngLimLab = Label(tab2, text = "J6 Neg Ang Lim")
J6PosAngLimLab = Label(tab2, text = "J6 Pos Ang Lim")
J6StepLimLab = Label(tab2, text = "J6 Step Lim")



J1NegAngLimLab.place(x=440, y=30)
J1PosAngLimLab.place(x=440, y=55)
J1StepLimLab.place(x=440, y=80)

J2NegAngLimLab.place(x=440, y=130)
J2PosAngLimLab.place(x=440, y=155)
J2StepLimLab.place(x=440, y=180)

J3NegAngLimLab.place(x=440, y=230)
J3PosAngLimLab.place(x=440, y=255)
J3StepLimLab.place(x=440, y=280)

J4NegAngLimLab.place(x=440, y=330)
J4PosAngLimLab.place(x=440, y=355)
J4StepLimLab.place(x=440, y=380)

J5NegAngLimLab.place(x=440, y=430)
J5PosAngLimLab.place(x=440, y=455)
J5StepLimLab.place(x=440, y=480)

J6NegAngLimLab.place(x=440, y=530)
J6PosAngLimLab.place(x=440, y=555)
J6StepLimLab.place(x=440, y=580)






DHr1Lab = Label(tab2, text = "DH alpha-1 (twist)")
DHr2Lab = Label(tab2, text = "DH alpha-2 ")
DHr3Lab = Label(tab2, text = "DH alpha-3 ")
DHr4Lab = Label(tab2, text = "DH alpha-4 ")
DHr5Lab = Label(tab2, text = "DH alpha-5 ")
DHr6Lab = Label(tab2, text = "DH alpha-6 ")

DHa1Lab = Label(tab2, text = "DH a-1 (length)")
DHa2Lab = Label(tab2, text = "DH a-2 ")
DHa3Lab = Label(tab2, text = "DH a-3 ")
DHa4Lab = Label(tab2, text = "DH a-4 ")
DHa5Lab = Label(tab2, text = "DH a-5 ")
DHa6Lab = Label(tab2, text = "DH a-6 ")

DHd1Lab = Label(tab2, text = "DH d-1 (offset)")
DHd2Lab = Label(tab2, text = "DH d-2 ")
DHd3Lab = Label(tab2, text = "DH d-3 ")
DHd4Lab = Label(tab2, text = "DH d-4 ")
DHd5Lab = Label(tab2, text = "DH d-5 ")
DHd6Lab = Label(tab2, text = "DH d-6 ")

DHt1Lab = Label(tab2, text = "DH theta-1 (angle)")
DHt2Lab = Label(tab2, text = "DH theta-2 ")
DHt3Lab = Label(tab2, text = "DH theta-3 ")
DHt4Lab = Label(tab2, text = "DH theta-4 ")
DHt5Lab = Label(tab2, text = "DH theta-5 ")
DHt6Lab = Label(tab2, text = "DH theta-6 ")









### 2 BUTTONS################################################################
##########################################################################


manCalBut = Button(tab2, bg="skyblue2", text="Auto Calibrate", height=1, width=20, command = calRobot)
manCalBut.place(x=10, y=10)

ForcCalBut = Button(tab2, bg="light salmon", text="Force Calibration to Mid Range", height=1, width=26, command = calRobotMid)
ForcCalBut.place(x=170, y=10)

fineCalBut = Button(tab2, bg="khaki2", text="Execute Fine Calibratation", height=1, width=20, command = exeFineCalPos)
fineCalBut.place(x=10, y=40)

teachfineCalBut = Button(tab2, bg="khaki2", text="Teach Fine Calibration Position", height=1, width=26, command = teachFineCal)
teachfineCalBut.place(x=170, y=40)

saveCalBut = Button(tab2, bg="Light green", text="SAVE CALIBRATION DATA", height=1, width=26, command = SaveAndApplyCalibration)
saveCalBut.place(x=90, y=140)



#### 2 ENTRY FIELDS##########################################################
##########################################################################

  

fineCalEntryField = Entry(tab2,fg="orange4",bg="khaki2",width=58)
fineCalEntryField.place(x=10, y=103)



J1NegAngLimEntryField = Entry(tab2,width=8)
J1PosAngLimEntryField = Entry(tab2,width=8)
J1StepLimEntryField = Entry(tab2,width=8)

J2NegAngLimEntryField = Entry(tab2,width=8)
J2PosAngLimEntryField = Entry(tab2,width=8)
J2StepLimEntryField = Entry(tab2,width=8)

J3NegAngLimEntryField = Entry(tab2,width=8)
J3PosAngLimEntryField = Entry(tab2,width=8)
J3StepLimEntryField = Entry(tab2,width=8)

J4NegAngLimEntryField = Entry(tab2,width=8)
J4PosAngLimEntryField = Entry(tab2,width=8)
J4StepLimEntryField = Entry(tab2,width=8)

J5NegAngLimEntryField = Entry(tab2,width=8)
J5PosAngLimEntryField = Entry(tab2,width=8)
J5StepLimEntryField = Entry(tab2,width=8)

J6NegAngLimEntryField = Entry(tab2,width=8)
J6PosAngLimEntryField = Entry(tab2,width=8)
J6StepLimEntryField = Entry(tab2,width=8)


J1NegAngLimEntryField.place(x=380, y=30)
J1PosAngLimEntryField.place(x=380, y=55)
J1StepLimEntryField.place(x=380, y=80)

J2NegAngLimEntryField.place(x=380, y=130)
J2PosAngLimEntryField.place(x=380, y=155)
J2StepLimEntryField.place(x=380, y=180)

J3NegAngLimEntryField.place(x=380, y=230)
J3PosAngLimEntryField.place(x=380, y=255)
J3StepLimEntryField.place(x=380, y=280)

J4NegAngLimEntryField.place(x=380, y=330)
J4PosAngLimEntryField.place(x=380, y=355)
J4StepLimEntryField.place(x=380, y=380)

J5NegAngLimEntryField.place(x=380, y=430)
J5PosAngLimEntryField.place(x=380, y=455)
J5StepLimEntryField.place(x=380, y=480)

J6NegAngLimEntryField.place(x=380, y=530)
J6PosAngLimEntryField.place(x=380, y=555)
J6StepLimEntryField.place(x=380, y=580)





DHr1EntryField = Entry(tab2,width=8)
DHr2EntryField = Entry(tab2,width=8)
DHr3EntryField = Entry(tab2,width=8)
DHr4EntryField = Entry(tab2,width=8)
DHr5EntryField = Entry(tab2,width=8)
DHr6EntryField = Entry(tab2,width=8)

DHa1EntryField = Entry(tab2,width=8)
DHa2EntryField = Entry(tab2,width=8)
DHa3EntryField = Entry(tab2,width=8)
DHa4EntryField = Entry(tab2,width=8)
DHa5EntryField = Entry(tab2,width=8)
DHa6EntryField = Entry(tab2,width=8)

DHd1EntryField = Entry(tab2,width=8)
DHd2EntryField = Entry(tab2,width=8)
DHd3EntryField = Entry(tab2,width=8)
DHd4EntryField = Entry(tab2,width=8)
DHd5EntryField = Entry(tab2,width=8)
DHd6EntryField = Entry(tab2,width=8)

DHt1EntryField = Entry(tab2,width=8)
DHt2EntryField = Entry(tab2,width=8)
DHt3EntryField = Entry(tab2,width=8)
DHt4EntryField = Entry(tab2,width=8)
DHt5EntryField = Entry(tab2,width=8)
DHt6EntryField = Entry(tab2,width=8)



DHr1EntryField.place(x=650, y=30)
DHr2EntryField.place(x=650, y=55)
DHr3EntryField.place(x=650, y=80)
DHr4EntryField.place(x=650, y=105)
DHr5EntryField.place(x=650, y=130)
DHr6EntryField.place(x=650, y=155)

DHa1EntryField.place(x=650, y=180)
DHa2EntryField.place(x=650, y=205)
DHa3EntryField.place(x=650, y=230)
DHa4EntryField.place(x=650, y=255)
DHa5EntryField.place(x=650, y=280)
DHa6EntryField.place(x=650, y=305)

DHd1EntryField.place(x=650, y=330)
DHd2EntryField.place(x=650, y=355)
DHd3EntryField.place(x=650, y=380)
DHd4EntryField.place(x=650, y=405)
DHd5EntryField.place(x=650, y=430)
DHd6EntryField.place(x=650, y=455)

DHt1EntryField.place(x=650, y=480)
DHt2EntryField.place(x=650, y=505)
DHt3EntryField.place(x=650, y=530)
DHt4EntryField.place(x=650, y=555)
DHt5EntryField.place(x=650, y=580)
DHt6EntryField.place(x=650, y=605)



DHr1Lab.place(x=710, y=30)
DHr2Lab.place(x=710, y=55)
DHr3Lab.place(x=710, y=80)
DHr4Lab.place(x=710, y=105)
DHr5Lab.place(x=710, y=130)
DHr6Lab.place(x=710, y=155)

DHa1Lab.place(x=710, y=180)
DHa2Lab.place(x=710, y=205)
DHa3Lab.place(x=710, y=230)
DHa4Lab.place(x=710, y=255)
DHa5Lab.place(x=710, y=280)
DHa6Lab.place(x=710, y=305)

DHd1Lab.place(x=710, y=330)
DHd2Lab.place(x=710, y=355)
DHd3Lab.place(x=710, y=380)
DHd4Lab.place(x=710, y=405)
DHd5Lab.place(x=710, y=430)
DHd6Lab.place(x=710, y=455)

DHt1Lab.place(x=710, y=480)
DHt2Lab.place(x=710, y=505)
DHt3Lab.place(x=710, y=530)
DHt4Lab.place(x=710, y=555)
DHt5Lab.place(x=710, y=580)
DHt6Lab.place(x=710, y=605)


###OPEN CAL FILE AND LOAD LIST###########################################
##########################################################################

calibration = Listbox(tab2,width=20,height=60)
#calibration.place(x=160,y=170)

try:
  Cal = pickle.load(open("ARbot.cal","rb"))
except:
  Cal = "0"
  pickle.dump(Cal,open("ARbot.cal","wb"))
for item in Cal:
  calibration.insert(END,item)
J1StepCur   =calibration.get("0")
J1AngCur    =calibration.get("1")
J2StepCur   =calibration.get("2")
J2AngCur    =calibration.get("3")
J3StepCur   =calibration.get("4")
J3AngCur    =calibration.get("5")
J4StepCur   =calibration.get("6")
J4AngCur    =calibration.get("7")
J5StepCur   =calibration.get("8")
J5AngCur    =calibration.get("9")
J6StepCur   =calibration.get("10")
J6AngCur    =calibration.get("11")
comPort     =calibration.get("12")
Prog        =calibration.get("13")
FineCalPos  =calibration.get("14")
J1NegAngLim =calibration.get("15")
J1PosAngLim =calibration.get("16")
J1StepLim   =calibration.get("17")
J2NegAngLim =calibration.get("18")
J2PosAngLim =calibration.get("19")
J2StepLim   =calibration.get("20")
J3NegAngLim =calibration.get("21")
J3PosAngLim =calibration.get("22")
J3StepLim   =calibration.get("23")
J4NegAngLim =calibration.get("24")
J4PosAngLim =calibration.get("25")
J4StepLim   =calibration.get("26")
J5NegAngLim =calibration.get("27")
J5PosAngLim =calibration.get("28")
J5StepLim   =calibration.get("29")
J6NegAngLim =calibration.get("30")
J6PosAngLim =calibration.get("31")
J6StepLim   =calibration.get("32")
DHr1        =calibration.get("33")
DHr2        =calibration.get("34")
DHr3        =calibration.get("35")
DHr4        =calibration.get("36")
DHr5        =calibration.get("37")
DHr6        =calibration.get("38")
DHa1        =calibration.get("39")
DHa2        =calibration.get("40")
DHa3        =calibration.get("41")
DHa4        =calibration.get("42")
DHa5        =calibration.get("43")
DHa6        =calibration.get("44")
DHd1        =calibration.get("45")
DHd2        =calibration.get("46")
DHd3        =calibration.get("47")
DHd4        =calibration.get("48")
DHd5        =calibration.get("49")
DHd6        =calibration.get("50")
DHt1        =calibration.get("51")
DHt2        =calibration.get("52")
DHt3        =calibration.get("53")
DHt4        =calibration.get("54")
DHt5        =calibration.get("55")
DHt6        =calibration.get("56")




####

J1curAngEntryField.insert(0,str(J1AngCur))
J2curAngEntryField.insert(0,str(J2AngCur))
J3curAngEntryField.insert(0,str(J3AngCur))
J4curAngEntryField.insert(0,str(J4AngCur))
J5curAngEntryField.insert(0,str(J5AngCur))
J6curAngEntryField.insert(0,str(J6AngCur))
comPortEntryField.insert(0,str(comPort))
speedEntryField.insert(0,"10")
ACCdurField.insert(0,"10")
ACCspeedField.insert(0,"25")
DECdurField.insert(0,"25")
DECspeedField.insert(0,"10")
ProgEntryField.insert(0,(Prog))
J1jogDegsEntryField.insert(0,"5")
J2jogDegsEntryField.insert(0,"5")
J3jogDegsEntryField.insert(0,"5")
J4jogDegsEntryField.insert(0,"5")
J5jogDegsEntryField.insert(0,"5")
J6jogDegsEntryField.insert(0,"5")
XjogEntryField.insert(0,"10")
YjogEntryField.insert(0,"10")
ZjogEntryField.insert(0,"10")
RxjogEntryField.insert(0,"10")
RyjogEntryField.insert(0,"10")
RzjogEntryField.insert(0,"10")
fineCalEntryField.insert(0,str(FineCalPos))
J1NegAngLimEntryField.insert(0,str(J1NegAngLim))
J1PosAngLimEntryField.insert(0,str(J1PosAngLim))
J1StepLimEntryField.insert(0,str(J1StepLim))
J2NegAngLimEntryField.insert(0,str(J2NegAngLim))
J2PosAngLimEntryField.insert(0,str(J2PosAngLim))
J2StepLimEntryField.insert(0,str(J2StepLim))
J3NegAngLimEntryField.insert(0,str(J3NegAngLim))
J3PosAngLimEntryField.insert(0,str(J3PosAngLim))
J3StepLimEntryField.insert(0,str(J3StepLim))
J4NegAngLimEntryField.insert(0,str(J4NegAngLim))
J4PosAngLimEntryField.insert(0,str(J4PosAngLim))
J4StepLimEntryField.insert(0,str(J4StepLim))
J5NegAngLimEntryField.insert(0,str(J5NegAngLim))
J5PosAngLimEntryField.insert(0,str(J5PosAngLim))
J5StepLimEntryField.insert(0,str(J5StepLim))
J6NegAngLimEntryField.insert(0,str(J6NegAngLim))
J6PosAngLimEntryField.insert(0,str(J6PosAngLim))
J6StepLimEntryField.insert(0,str(J6StepLim))
DHr1EntryField.insert(0,str(DHr1))
DHr2EntryField.insert(0,str(DHr2))
DHr3EntryField.insert(0,str(DHr3))
DHr4EntryField.insert(0,str(DHr4))
DHr5EntryField.insert(0,str(DHr5))
DHr6EntryField.insert(0,str(DHr6))
DHa1EntryField.insert(0,str(DHa1))
DHa2EntryField.insert(0,str(DHa2))
DHa3EntryField.insert(0,str(DHa3))
DHa4EntryField.insert(0,str(DHa4))
DHa5EntryField.insert(0,str(DHa5))
DHa6EntryField.insert(0,str(DHa6))
DHd1EntryField.insert(0,str(DHd1))
DHd2EntryField.insert(0,str(DHd2))
DHd3EntryField.insert(0,str(DHd3))
DHd4EntryField.insert(0,str(DHd4))
DHd5EntryField.insert(0,str(DHd5))
DHd6EntryField.insert(0,str(DHd6))
DHt1EntryField.insert(0,str(DHt1))
DHt2EntryField.insert(0,str(DHt2))
DHt3EntryField.insert(0,str(DHt3))
DHt4EntryField.insert(0,str(DHt4))
DHt5EntryField.insert(0,str(DHt5))
DHt6EntryField.insert(0,str(DHt6))


#CalcFwdKin()
SaveAndApplyCalibration()
DisplaySteps()

try:
  setCom()
except:
  print("")

loadProg()

tab1.mainloop()
