

def convertPercentage(percentageString):
    for i in range(len(percentageString)):
        if percentageString[i] == '%':
            return float(percentageString[:i])
    return 0