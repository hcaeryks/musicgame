import json, globalVar

def read_settings():
    file = open("config/controls.json", "r")
    controls = json.load(file)
    file.close()
    for control in controls:
        key = controls[control]
        if control.startswith("Note"):
            if not control.endswith("Speed"):
                note_number = control.split()
                note_number = int(note_number[1])-1
                globalVar.NOTES[note_number] = key
            else:
                globalVar.NOTE_SPEED = float(key)