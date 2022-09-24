## 2022 09 24 
## Tracker Checkboxes by Golan
## Added to menu.py


def trackerTab():
    node = nuke.thisNode()
    
    # Create knobs:
    tab = nuke.Tab_Knob('Check Boxes')
    node.addKnob(tab)
    
    number_of_trackers = nuke.String_Knob('number_of_trackers',
                                      'number of trackers:',
                                      'ALL'
                                      )
    nuke.knobTooltip('Tracker4.number_of_trackers', 'Input should be something like "1", "1-6", "1 6" or "ALL"')                                    
                                      
    node.addKnob(number_of_trackers)
    
    t_boolean_knob = nuke.Boolean_Knob('translate_box', 'translate', True)
    node.addKnob(t_boolean_knob)
    
    r_boolean_knob = nuke.Boolean_Knob('rotate_box', 'rotate', True)
    node.addKnob(r_boolean_knob)
    
    s_boolean_knob = nuke.Boolean_Knob('scale_box', 'scale', True)
    node.addKnob(s_boolean_knob)
    
    pyknob = nuke.PyScript_Knob('check_tracker_boxes',
                            'execute',
                            'tracker_checkboxes()'
                            )
    pyknob.setFlag(nuke.STARTLINE)
    node.addKnob(pyknob)
nuke.addOnUserCreate(lambda: trackerTab(), nodeClass='Tracker4')

def tracker_checkboxes():
    selectedNode = nuke.selectedNode()
    knob = selectedNode['tracks']
    
    t_boolean = selectedNode['translate_box'].value()
    r_boolean = selectedNode['rotate_box'].value()
    s_boolean = selectedNode['scale_box'].value()
    
    booleans = [t_boolean, r_boolean, s_boolean]
    allRows = 31
    trackInput = selectedNode['number_of_trackers'].value()
    t_row = 6
    r_row = 7
    s_row = 8
    checkRows = [t_row, r_row, s_row]
    
    
    ## Loop Through tracks 
    ## Set the settings as needed
    def loopThroughTrackers(): #--> This will loop through "1" or from low to high number "1-4"
        userTrackerInput.count -= 1
        if len(userTrackerInput.trackers) > 1:
            while userTrackerInput.count != userTrackerInput.trackers[1]:
                row = 0
                for checklist in booleans:
                    if checklist == True:
                        channel = allRows * userTrackerInput.count + checkRows[row]
                        knob.setValue(True, channel)
                        row += 1
                    else:
                        channel = allRows * userTrackerInput.count + checkRows[row]
                        knob.setValue(False, channel)
                        row += 1
                userTrackerInput.count += 1
                
        else:
            row = 0      
            for checklist in booleans:
                if checklist == True:
                    channel = allRows * userTrackerInput.count + checkRows[row]
                    knob.setValue(True, channel)
                    row += 1
                else:
                    channel = allRows * userTrackerInput.count + checkRows[row]
                    knob.setValue(False, channel)
                    row += 1
    
    
    def loopIndividualTracks():  #--> This will only loop through the given track numbers "1 3 5" and nothing inbetween 
        for track in userTrackerInput.trackers:
            row = 0
            for checklist in booleans:
                if checklist == True:
                    channel = allRows * track + checkRows[row]
                    knob.setValue(True, channel)
                    row += 1
                else:
                    channel = allRows * track + checkRows[row]
                    knob.setValue(False, channel)
                    row += 1
                    
                    
    def loopAll(all): #loopAll --> Loops through all trackers 
        track = 0
        while track <= all: 
            row = 0
            for checklist in booleans:
                if checklist == True:
                    channel = allRows * track + checkRows[row]
                    knob.setValue(True, channel)
                    row += 1
                else:
                    channel = allRows * track + checkRows[row]
                    knob.setValue(False, channel)
                    row += 1
            track += 1
                
                
                
    # Check user input 
    def userTrackerInput(input):
        try:
            ## Checking User Input
            ## should be: "1-6", "1 6", "1" or "ALL"
            userTrackerInput.trackers = []
            # Tracker Input has a *-*
            if "-" in input:
                input = input.split("-")
                for i in input:
                    i = int(i)
                    userTrackerInput.trackers.append(i)
                userTrackerInput.count = userTrackerInput.trackers[0]
        
                # First number has to be lower
                if userTrackerInput.count > userTrackerInput.trackers[1]: 
                    nuke.message('Put the tracker numbers from low to high')
                    pass
                else:
                    loopThroughTrackers() #loopThroughTrackers --> This will loop through "1" or from low to high number "1-4"
        
            # Tracker Input has a space
            elif " " in input: # Seperated trackers
                input = input.split(" ")
                for i in input:
                    i = int(i)
                    i -= 1
                    userTrackerInput.trackers.append(i)
                userTrackerInput.count = userTrackerInput.trackers[0]
                loopIndividualTracks() #--> This will only loop through the given track numbers "1 3 5" and nothing inbetween 
        
            # Tracker Input == "ALL"
            elif "ALL" in input: #loopAll --> This will loop through all trackers. 
                trackNum = selectedNode['tracks'].toScript()
                trackNum = trackNum.split('}')
                trackNum = trackNum[0]
                trackNum = int(trackNum[-3:-1])
                trackNum -= 1
                loopAll(trackNum) #loopAll --> Loops through all trackers 
        
            else: #loopThroughTrackers --> This will loop through "1" or from low to high number "1-4"
                userTrackerInput.trackers.append(input)
                userTrackerInput.count = userTrackerInput.trackers[0]
                userTrackerInput.count = int(userTrackerInput.count)
                loopThroughTrackers()
        
        except:
            nuke.message('Input should be something like "1", "1-6", "1 6" or "ALL"')
            pass
        
    
    userTrackerInput(trackInput)




