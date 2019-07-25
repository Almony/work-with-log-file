# func calculates average hours for every employee and save it in avvHourDict dictionary
def avv_func():
    global avvHoursDict, idList

    # loop runs on every employee
    # converts presence of employee in sec
    # save value in avvHoursDict dictionary by ID of employee
    for element in idList:
        try:
            tempHourIn = int(logsDict[element]['log-in'][0:2])
            tempMinIn = int(logsDict[element]['log-in'][3:5])
            tempSecIn = int(logsDict[element]['log-in'][7:9])
            tempHourOut = int(logsDict[element]['log-out'][0:2])
            tempMinOut = int(logsDict[element]['log-out'][3:5])
            tempSecOut = int(logsDict[element]['log-in'][7:9])
        except(ValueError):
            print("non convertible value")
        # Convert work hours of employee in sec and save it in avvHoursDict
        if tempHourOut < tempHourIn:
            avvHoursDict[element] = avvHoursDict[element] + (24 - tempHourIn + tempHourOut) * 3600
            avvHoursDict[element] = avvHoursDict[element] + ((60 - tempMinIn + tempMinOut) * 60)
            avvHoursDict[element] = avvHoursDict[element] + (60 - tempSecIn + tempSecOut)
        elif tempHourOut > tempHourIn:
            avvHoursDict[element] = avvHoursDict[element] + (24 - tempHourIn) * 3600
            avvHoursDict[element] = avvHoursDict[element] + ((60 - tempMinIn + tempMinOut) * 60)
            avvHoursDict[element] = avvHoursDict[element] + (60 - tempSecIn + tempSecOut)
        elif tempHourIn == tempHourOut:
            avvHoursDict[element] = avvHoursDict[element] + tempMinOut - tempMinIn
            avvHoursDict[element] = avvHoursDict[element] + tempSecOut - tempSecIn
        else:
            print("unexpected result of convertation")


# func converts work hours in familiar format and outPuting it to consol
def op_work_hours(counter):
    global avvHoursDict
    for element in avvHoursDict:
        tempHour = round((avvHoursDict[element] / counter) / 3600)
        tempMin = round(((avvHoursDict[element] / counter) % 3600) / 60)
        tempSec = round(((avvHoursDict[element] / counter) % 3600) % 60)
        print(element, '{:02d}:{:02d}:{:02d}'.format(tempHour, tempMin, tempSec))


# connecting log file
try:
    with open("log2.log", "r") as logF:
        logLine = logF.readline()

        # dictionary of all users with log-in & log-out ID of user is a key
        # {"id1": {'log-in': 'time', 'log-out': 'time'}, "id2": {'log-in': 'time', 'log-out': 'time'}}
        logsDict = {}

        # main dictionary with employee's ID and monthly workHours in sec
        avvHoursDict = {}

        # list of employees IDs
        idList = []
        tempList = logLine.split()
        dayCounter = 0
        # main loop running on log file and getting all log-in\outs of employees
        while logLine:

            # filling dictionary of average hours by employee by IDs
            if tempList[1] not in avvHoursDict:
                avvHoursDict.update({tempList[1]: 0})

                # list of employee's IDs
                idList.insert(len(idList), tempList[1])

            # save log-in\out in logsDict
            if 'log-in' in tempList:
                tempDict = {tempList[1]: {tempList[2]: tempList[0]}}
                logsDict.update(tempDict)
            elif 'log-out' in tempList and tempList[1] in logsDict:

                tempDict = {tempList[2]: tempList[0]}
                logsDict[tempList[1]].update(tempDict)

            # if dictionary of log-in\outs is full calling the func avv_func to count average hours by employee
            # cleaning the logsDict dictionary
            if 'log-out' in logsDict[idList[len(idList) - 1]]:
                # counting days of work
                dayCounter = dayCounter + 1
                avv_func()
                logsDict[idList[len(idList) - 1]].clear()

            logLine = logF.readline()

            # splitting data to temp list in order [time , id, in\out]
            tempList = logLine.split()

        op_work_hours(dayCounter)
except(FileNotFoundError):
    print("File not found")
