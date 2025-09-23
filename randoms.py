import random

def Industry():
    list1 = ["Automobile","Oil and Gas"]
    return random.choice(list1)


def Category():
    list1 = ["Safety Material","Adhesive","Industrial Valves","Drilling machine, Bolt cutter","Fasteners","Battery","Electrical","Drill Bit and Fasteners"]
    return random.choice(list1)


def Risk_Score():
    list1 = [76,63,89,84,91,20]
    return random.choice(list1)


def Risk_Level():
    list1 = ["Low","Medium","High"]
    return random.choice(list1)


def Compliance():
    list1 = ["Compliant","Non-Compliant"]
    return random.choice(list1)

def Status():
    list1 = [True,False]
    return random.choice(list1)

def demo_number():
    list1 = [5,7,8,3,6]
    return random.choice(list1)
