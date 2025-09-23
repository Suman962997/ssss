

    
def risklevel_def(score):
    if score is None or score =="":
        return ""
    elif 20>=score:
        return "High"

    elif 20<50>=score:
        return "Medium"

    elif 50<100>=score:
        return "Low"
    



# def certification_find():
#     return []