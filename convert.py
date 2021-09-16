with open("filename.osu") as file:
    data = file.readlines()
    newArr = []
    for line in data[64:]:
        info = line.split(",")
        newLine = ""
        time = "#"+info[2]+":"
        lane = info[0]
        if lane == "42": lane = "0:"
        elif  lane == "128": lane = "1:"
        elif  lane == "213": lane = "2:"
        elif  lane == "298": lane = "3:"
        elif  lane == "384": lane = "4:"
        elif  lane == "469": lane = "5:"
        info = info[-1].split(":")[0]
        type = 0
        end = 0
        if info != 0:
            type = str(1) + ":"
            end = str(info)
        newLine += time+lane+type+end+"\n"
        newArr.append(newLine)
    with open("new.sc", "w") as newFile:
        newFile.writelines(newArr)