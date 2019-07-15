import mysql.connector
import time
import matplotlib.pyplot as plt
import  psutil
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="parola",
    database="webinterfacedatabase"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM energy")
myresult = mycursor.fetchall()
#myresult = mycursor.fetchall() #doar prima linie din db

ids, timestamps, sources, datas  = [], [], [], []

t = myresult[0][1]
ids.append(myresult[0][0])
timestamps.append(0)
sources.append(myresult[0][2])
datas.append(myresult[0][3])

first_source, second_source, third_source = [], [], []

first_source.append([])
first_source.append([])
second_source.append([])
second_source.append([])
third_source.append([])
third_source.append([])

if str(myresult[0][2])[-3] == '1':
    first_source[0].append(0)
    first_source[1].append(myresult[0][3])
if str(myresult[0][2])[-3] == '2':
    second_source[0].append(0)
    second_source[1].append(myresult[0][3])
if str(myresult[0][2])[-3] == '3':
    third_source[0].append(0)
    third_source[1].append(myresult[0][3])

#print(first_source)

for i in range(1,len(myresult)):
    #print(str(myresult[i][2])[-3]) # nr sursei
    if str(myresult[i][2])[-3] == '1':
        first_source[1].append(myresult[i][3])
        first_source[0].append(myresult[i][1] - myresult[i-1][1])
    if str(myresult[i][2])[-3] == '2':
        second_source[1].append(myresult[i][3])
        second_source[0].append(myresult[i][1] - myresult[i - 1][1])
    if str(myresult[i][2])[-3] == '3':
        third_source[1].append(myresult[i][3])
        third_source[0].append(myresult[i][1] - myresult[i - 1][1])


print(first_source)
print(second_source)
print(third_source)

for i in range(1,len(first_source[0])):
    first_source[0][i] += first_source[0][i-1]

for i in range(1,len(second_source[0])):
    second_source[0][i] += second_source[0][i-1]

for i in range(1,len(third_source[0])):
    third_source[0][i] += third_source[0][i-1]

print(str(len(first_source[0])) + " " + str(len(first_source[1])) + " " + str(first_source))
print(str(len(second_source[0])) + " " + str(len(second_source[1])) + " " + str(second_source))
print(str(len(third_source[0])) + " " + str(len(third_source[1])) + " " + str(third_source))


def animate(i):
    plt.cla()
    x = first_source[0]
    y = first_source[1]
    plt.plot(x, y, label="Source 1")
    #plt.plot(first_source[0], first_source[1], label="Source 1")
    #plt.plot(second_source[0], second_source[1], label="Source 2")
    #plt.plot(third_source[0], third_source[1], label="Source 3")
    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000 * 250)

#
plt.tight_layout()
plt.show()