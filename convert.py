with open("C-Show - Invitation from Mr.C (_FrEsH_ChICkEn_) [ADVANCED].osu") as file:
    data = file.readlines()
    newArr = []
    for line in data[64:]:
        info = line.split(",")
        newLine = ""
        time = "#"+info[2]+":"
        lane = info[0]
        if lane == "64": lane = "0:"
        elif  lane == "192": lane = "1:"
        elif  lane == "320": lane = "2:"
        elif  lane == "448": lane = "3:"
        newLine += time+lane+"0:0\n"
        newArr.append(newLine)
    with open("new.mgame", "w") as newFile:
        newFile.writelines(newArr)