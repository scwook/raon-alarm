def valueconversion(valueType, value):
    if valueType == "DOUBLE":
        return float(value)
    elif valueType == "INT":
        return int(value)
    else:
        return value
    
val = 12.5
a = valueconversion("INT", val)
print(type(a))
print(a)