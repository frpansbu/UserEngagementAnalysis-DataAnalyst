import numpy as np
import csv
from matplotlib import pyplot as plt
from numpy.random import randn
class User:
    def __init__(self, ID, totalProjects, totalLikes, totalComments, totalInactive, totalBugs, totalDuration):
        self.ID = ID
        self.totalProjects = totalProjects
        self.totalLikes = totalLikes
        self.totalComments = totalComments
        self.totalInactive = totalInactive
        self.totalBugs = totalBugs
        self.totalDuration = totalDuration
        
    def addToTotal(self, projects, likes, comments, inactive, bugs, duration):
        self.totalProjects += projects
        self.totalLikes += likes
        self.totalComments += comments
        self.totalInactive += inactive
        self.totalBugs += bugs
        self.totalDuration += duration

    def printUser(self):
        print("ID: " + str(self.ID) + " "
              + "Projects: " + str(self.totalProjects) + " "
              + "Likes: " + str(self.totalLikes) + " "
              + "Comments: " + str(self.totalComments) + " "
              + "Inactive: " + str(self.totalInactive) + " "
              + "Bugs: " + str(self.totalBugs) + " "
              + "Duration: " + str(self.totalDuration) + " ")

def addToUserList(row):
    if row[1] not in uniqueUsers and "" not in row:
        uniqueUsers.append(row[1])
        newUser = User(row[1], int(row[8]), int(row[9]), int(row[10]), int(row[11]), int(row[12]), int(row[13])) 
        userList.append(newUser)
    elif "" not in row and row[1] in uniqueUsers:
        index = uniqueUsers.index(row[1])
        userList[index].addToTotal(int(row[8]), int(row[9]), int(row[10]), int(row[11]), int(row[12]), int(row[13]))

# csv file name 
filename = "showwcase_sessions.csv"
  
fields = [] 
rows = []
uniqueUsers = []
userList = []
dateDict = {}

avgProjects = 0
avgLikes = 0
avgComments = 0
avgInactive = 0
avgBugs = 0
avgDuration = 0

# reading csv file 
with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile)
    
    fields = next(csvreader)
    
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 

for row in rows: 
    # parsing each column of a row
    if row[8] != '':
        avgProjects += int(row[8])
    if row[9] != '':
        avgLikes += int(row[9])
    if row[10] != '':
        avgComments += int(row[10])
    if row[11] != '':
        avgInactive += int(row[11])
    if row[12] != '':
        avgBugs += int(row[12])
    if row[13] != '':
        avgDuration += int(row[13])
        
    if row[2] not in dateDict:
        dateDict[row[2]] = 1
        addToUserList(row)
    else:
        dateDict[row[2]] += 1
        addToUserList(row)
  
#print ("\nNumber of unique users: " + str(len(uniqueUsers)))

avgProjects = avgProjects/len(uniqueUsers)
avgLikes = avgLikes/len(uniqueUsers)
avgComments = avgComments/len(uniqueUsers)
avgInactive = avgInactive/len(uniqueUsers)
avgBugs = avgBugs/len(uniqueUsers)
avgDuration = avgDuration/len(uniqueUsers)

print("Average Projects: " + str(round(avgProjects, 2)))
print("Average Likes: " + str(round(avgLikes, 2)))
print("Average Comments: " + str(round(avgComments, 2)))
print("Average Inactive Time: " + str(round(avgInactive, 2)))
print("Average Bugs: " + str(round(avgBugs, 2)))
print("Average Duration: " + str(round(avgDuration, 2)))
print()

#for user in userList:
    #user.printUser()

#print("\nNumber of users per date: ")
del dateDict[""]
#print(dateDict)

x = np.arange(1, 31) 
plt.title("Users Per Date") 
plt.xlabel("Day of Month") 
plt.ylabel("Number of Users") 
plt.plot(x,dateDict.values()) 
plt.show()

#Correlation of User Site Time to Num of Bugs Per Session

numBugs = []
timeOnSite = []
for row in rows:
    if "" not in row:
        numBugs.append(int(row[12]))
        timeOnSite.append(int(row[11]) + int(row[13]))
        
plt.title("Time Spent on Site vs Number of Bugs") 
plt.xlabel("Number of Bugs") 
plt.ylabel("Total Time on Site") 
plt.scatter(numBugs, timeOnSite)
plt.show()

pearsonCorr = np.cov(numBugs, timeOnSite)/(np.std(numBugs) * np.std(timeOnSite))
print("\nPearson Correlation (Bugs vs Time): " + str(round(pearsonCorr[0][1], 3)))

#Correlation of Active Session Duration to Projects Added

numProjects = []
sessionDuration = []
for row in rows:
    if "" not in row:
        numProjects.append(int(row[8]))
        sessionDuration.append(int(row[13]))

plt.title("Time Spent on Site vs Number of Projects Added") 
plt.xlabel("Number of Projects") 
plt.ylabel("Active Time on Site") 
plt.scatter(numProjects, sessionDuration)
plt.show()

pearsonCorr = np.cov(numProjects, sessionDuration)/(np.std(numProjects) * np.std(sessionDuration))
print("\nPearson Correlation (Projects Added vs Time): " + str(round(pearsonCorr[0][1], 3)))

#Predicted Number of Users using Simple Moving Average (n = 7)
windowNums = list(dateDict.values())[0:7]
estimates = []
#Predict next 10 days
for x in range(0, 10):
    estimate = round(sum(windowNums)/7, 2)
    estimates.append(estimate)
    windowNums.insert(0, estimate)
    windowNums.pop()

x = np.arange(1, 41) 
plt.title("Users Per Date + 10 Day Estimate") 
plt.xlabel("Day of Month") 
plt.ylabel("Number of Users") 
plt.plot(x, list(dateDict.values()) + estimates) 
plt.show()

    
    


