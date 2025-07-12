The territory python files utilize predefined values that can be modified by the user before running the territory\_main.py file. Please name your file as territory\_config.py and make use of the following template.



\# Defining all the globals for the territory model



\# PATHS

main\_dir = r"path\\to\\you\\working\\directory"

netlogo\_exe = r"path\\to\\you\\netlogo\\application"

model = r"path\\to\\your\\netlogo\\model\\file"



\#INPUT VALIES

input\_parameters = {

&nbsp;           "key1": \[value1, value2, value\_n],

&nbsp;           "key2": \[value1, value2, value\_n],

&nbsp;           "key\_n": \[value1, value2, value\_n],

&nbsp;       }

file\_name = "common prefix to your output files"



\# SIMULATION SET UP

parallel\_jobs = int() # to run parallel jobs at the same time

tick\_start = int() # recommended to start at 0

tick\_step = int() # how many ticks should the model skip

max\_ticks = int() # max ticks the model should for 

runs = int() # number of runs for each combination of parameters



\# GRAPHS

id\_cols = \[value1, value2, value\_n]

var\_col = "desired column name"

value\_col = "desired column name"

column\_suffix = "common suffix defined in simulation code"

X\_data = \[x for x in range (tick\_start, max\_ticks, tick\_step)]

X\_label = "desired label name"

Y\_label = "desired label name"

graph\_title = "desired graph title or heading"

