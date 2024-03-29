## 17 10 2022
## Tracker Checkboxes by Golan
## Inspirend and learned a lot from jazlyncartaya/J_Tracker_Checkboxes.py. Credits to her.

"""This plugin creates onUserCreate a new tab folder 'Checkboxes' on the tracker4 nodes.
This will give you the control to select multiple trackers: '1', '1-6', '1 6' or 'ALL' and set the checkboxes for all of them.
By hitting the 'execute'button. """

import nuke

"""GLOBALS"""
ALL_ROWS = 31
T_ROW = 6
R_ROW = 7
S_ROW = 8
CHECK_ROWS = [T_ROW, R_ROW, S_ROW]


def userTrackerInput(trackInput, selectedNode, booleansList, knobTracks):
    try:
        ## Checking User Input
        ## should be: "1-6", "1 6", "1" or "ALL"
        userTrackerInput.trackers = []
        # Tracker Input has a *-*
        if "-" in trackInput:
            trackInput = trackInput.split("-")
            for i in trackInput:
                i = int(i)
                userTrackerInput.trackers.append(i)
            userTrackerInput.count = userTrackerInput.trackers[0]

            # First number has to be lower
            if userTrackerInput.count > userTrackerInput.trackers[1]:
                nuke.message("Put the tracker numbers from low to high")
                pass
            else:
                loopThroughTrackers(userTrackerInput.trackers, booleansList,
                                    knobTracks)  # loopThroughTrackers --> This will loop through "1" or from low to high number "1-4"

        # Tracker Input has a space
        elif " " in trackInput:  # Seperated trackers
            trackInput = trackInput.split(" ")
            trackInput = list(filter(None, trackInput))
            for i in trackInput:
                i = int(i)
                i -= 1
                userTrackerInput.trackers.append(i)
            print(userTrackerInput.trackers)
            userTrackerInput.count = userTrackerInput.trackers[0]
            loopIndividualTracks(userTrackerInput.trackers, booleansList,
                                 knobTracks)  # --> This will only loop through the given track numbers "1 3 5" and nothing inbetween

        # Tracker Input == "ALL"
        elif "ALL" in trackInput:  # loopAll --> This will loop through all trackers.
            trackNum = selectedNode["tracks"].toScript()
            trackNum = trackNum.split("}")
            trackNum = trackNum[0]
            trackNum = int(trackNum[-3:-1])
            trackNum -= 1
            loopAll(trackNum, booleansList, knobTracks)  # loopAll --> Loops through all trackers

        else:  # loopThroughTrackers --> This will loop through "1" or from low to high number "1-4"
            userTrackerInput.trackers.append(trackInput)
            userTrackerInput.count = userTrackerInput.trackers[0]
            userTrackerInput.count = int(userTrackerInput.count)
            loopThroughTrackers(userTrackerInput.trackers, booleansList, knobTracks)

    except:  # If trackInput isn't corrected filled in.
        nuke.message('Input should be something like "1", "1-6", "1 6" or "ALL"')
        pass


def loopThroughTrackers(userTrackerInputList, booleansList,
                        knobTracks):  # --> This will loop through "1" or from low to high number "1-4"
    userTrackerInput.count -= 1
    if len(userTrackerInput.trackers) > 1:
        while userTrackerInput.count != userTrackerInput.trackers[1]:
            row = 0
            for checklist in booleansList:
                if checklist == True:
                    channel = ALL_ROWS * userTrackerInput.count + CHECK_ROWS[row]
                    knobTracks.setValue(True, channel)
                    row += 1
                else:
                    channel = ALL_ROWS * userTrackerInput.count + CHECK_ROWS[row]
                    knobTracks.setValue(False, channel)
                    row += 1
            userTrackerInput.count += 1

    else:  # trackInput == one number
        row = 0
        for checklist in booleansList:
            if checklist == True:
                channel = ALL_ROWS * userTrackerInput.count + CHECK_ROWS[row]
                knobTracks.setValue(True, channel)
                row += 1
            else:
                channel = ALL_ROWS * userTrackerInput.count + CHECK_ROWS[row]
                knobTracks.setValue(False, channel)
                row += 1


def loopIndividualTracks(userTrackerInputList, booleansList,
                         knobTracks):  # --> This will only loop through the given track numbers "1 3 5" and nothing inbetween
    for track in userTrackerInput.trackers:
        row = 0
        for checklist in booleansList:
            if checklist == True:
                channel = ALL_ROWS * track + CHECK_ROWS[row]
                knobTracks.setValue(True, channel)
                row += 1
            else:
                channel = ALL_ROWS * track + CHECK_ROWS[row]
                knobTracks.setValue(False, channel)
                row += 1


def loopAll(all, booleansList, knobTracks):  # loopAll --> Loops through all trackers
    track = 0
    while track <= all:
        row = 0
        for checklist in booleansList:
            if checklist == True:
                channel = ALL_ROWS * track + CHECK_ROWS[row]
                knobTracks.setValue(True, channel)
                row += 1
            else:
                channel = ALL_ROWS * track + CHECK_ROWS[row]
                knobTracks.setValue(False, channel)
                row += 1
        track += 1


def tracker_checkboxes():
    selectedNode = nuke.thisNode()
    knobTracks = selectedNode["tracks"]

    t_boolean = selectedNode["translate_box"].value()
    r_boolean = selectedNode["rotate_box"].value()
    s_boolean = selectedNode["scale_box"].value()

    ## 31 rows per tracker
    ## So the calculation goes as follows: 31 * trackNumber * rowNumber
    booleansList = [t_boolean, r_boolean, s_boolean]
    trackInput = selectedNode["number_of_trackers"].value()

    ## Loop Through tracks
    ## Turn the checkboxes on or off depening on _booleans values.
    ## True is on (box checked X)
    ## False is off (box unchecked)

    userTrackerInput(trackInput, selectedNode, booleansList, knobTracks)

def trackerTab():
    ## This creates the new tab folder with the needed buttons.
    ## Adds the tab folder when user creates a tracker node.
    ## In older scripts the tab won't show on already existing tracker nodes.
    ## Change below the "nuke.addOnUserCreate" to "nuke.addOnCreate" if you do want that.

    # Get node
    node = nuke.thisNode()

    # Create knobs:
    tab = nuke.Tab_Knob("Check Boxes")
    node.addKnob(tab)

    number_of_trackers = nuke.String_Knob(
        "number_of_trackers", "number of trackers:", "ALL"
    )
    nuke.knobTooltip(
        "Tracker4.number_of_trackers",
        'Input should be something like "1", "1-6", "1 6" or "ALL"',
    )

    node.addKnob(number_of_trackers)

    t_boolean_knob = nuke.Boolean_Knob("translate_box", "translate", True)
    node.addKnob(t_boolean_knob)

    r_boolean_knob = nuke.Boolean_Knob("rotate_box", "rotate", True)
    node.addKnob(r_boolean_knob)

    s_boolean_knob = nuke.Boolean_Knob("scale_box", "scale", True)
    node.addKnob(s_boolean_knob)

    pyknob = nuke.PyScript_Knob(
        "check_tracker_boxes", "execute", "nuke.thisNode() \ntracker_checkboxes()"
    )
    pyknob.setFlag(nuke.STARTLINE)
    node.addKnob(pyknob)


nuke.addOnUserCreate(lambda: trackerTab(), nodeClass="Tracker4")