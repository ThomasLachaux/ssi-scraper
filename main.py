import pandas as pd
from ics import Calendar, Event

slots = [8, 9, 10, 12, 14, 16, 18]

events = []


# Read the file and only keep the schedule and the location
xsl = pd.read_excel("edt.xslx", usecols="B:H,N,O")

for day in range(len(xsl)):
    for slot in range(1, 7):

        # on parcourt le dataframe en excluant les valeurs nulles ou les espaces simples
        if isinstance(xsl.iloc[day][slot], str) and len(xsl.iloc[day][slot]) > 1:

            # Create an event and give it a name
            event = Event()
            event.name = xsl.iloc[day][slot]

            # If the slot is on the morning, find the location on cell 7
            if slot < 3:
                event.location = str(xsl.iloc[day][7])

            # Otherwise, find the location on cell 8
            else:
                event.location = str(xsl.iloc[day][8])

            # Set the starting and ending dates
            startingDate = xsl.iloc[day][0]
            endingDate = xsl.iloc[day][0]

            startingDate = startingDate.replace(hour=slots[slot - 1])
            endingDate = startingDate.replace(hour=slots[slot])

            # Assign the dates to the event
            event.begin = startingDate
            event.end = endingDate

            events.append(event)

iterator = iter(events)

calendar = Calendar()

try:
    i = 0
    while i < len(events):
        beginEvent = events[i]
        j = i

        while beginEvent.end == events[j + 1].begin and beginEvent.name == events[j + 1].name:
            j += 1

        beginEvent.end = events[j].end
        calendar.events.add(beginEvent)

        i = j + 1
except IndexError:
    pass

with open('my.ics', 'w') as file:
    calendar = str(calendar)
    calendar = calendar.replace('0000Z', '0000')
    file.write(calendar)
