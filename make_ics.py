import pandas as pd
import logging
from ics import Calendar, Event
from dateutil import tz
import re

logger = logging.getLogger(__name__)
timezone = tz.gettz('Europe/Paris')

def isBlank(s):
    return s == 'nan' or len(s.strip()) == 0


def make_ics(raw_xls, ue=None):
    slots = [8, 9, 10, 11, 12, 14, 16, 17, 18]
    excludeList = ["Réservé aux langues"]
    if ue:
        excludeList.append(ue)
    events = []

    logger.debug('Parsing XLS')
    # Read the file and only keep the schedule and the location
    xls = pd.read_excel(raw_xls, usecols="B:R", nrows=127)

    for day in range(len(xls)):
        for slot in range(1, 8):

            # on parcourt le dataframe en excluant les valeurs nulles ou les espaces simples
            if isinstance(xls.iloc[day][slot], str) and len(xls.iloc[day][slot]) > 1:

                # Create an event and give it a name
                event = Event()
                event.name = xls.iloc[day][slot]

                # If this ue is blacklisted, ignore it and go to next event
                skip=False
                for exclude in excludeList:
                    if exclude and re.search(exclude, event.name, re.IGNORECASE):
                        logger.debug(f"skip : {exclude} on {day} at {slot}")
                        skip=True
                        break
                if(skip):
                    continue

                # If the slot is on the morning, find the location on cell 15
                location = None
                sujet = None
                intervenant = None
                entreprise = None
                if slot <= 5:
                    location = str(xls.iloc[day][15])
                    sujet = str(xls.iloc[day][9])
                    intervenant = str(xls.iloc[day][10])
                    entreprise = str(xls.iloc[day][13])
                    

                # Otherwise, find the location on cell 16
                else:
                    location = str(xls.iloc[day][16])
                    sujet = str(xls.iloc[day][11])
                    intervenant = str(xls.iloc[day][12])
                    entreprise = str(xls.iloc[day][14])

                event.description = ""
                if not isBlank(location):
                    event.location = location
                if not isBlank(sujet):
                    event.description += f"Sujet : {sujet}\n"
                if not isBlank(intervenant):
                    event.description += f"Intervenant : {intervenant}\n"
                if not isBlank(entreprise):
                    event.description += f"Entreprise : {entreprise}"


                # Set the starting and ending dates
                startingDate = xls.iloc[day][0]
                endingDate = xls.iloc[day][0]

                startingDate = startingDate.replace(hour=slots[slot - 1], tzinfo=timezone)
                endingDate = startingDate.replace(hour=slots[slot], tzinfo=timezone)

                # Assign the dates to the event
                event.begin = startingDate
                event.end = endingDate

                events.append(event)
                logger.debug(f'Create primitive event {event.name} - {event.location} [{event.begin}/{event.end}]')

    calendar = Calendar(creator="SSI - https://github.com/ThomasLachaux/ssi-scraper")

    try:
        i = 0
        while i < len(events):
            beginEvent = events[i]
            j = i

            while beginEvent.end == events[j + 1].begin and beginEvent.name == events[j + 1].name:
                j += 1

            beginEvent.end = events[j].end
            beginEvent.uid = f'{beginEvent.name}{str(beginEvent.begin)}{str(beginEvent.end)}'
            calendar.events.add(beginEvent)
            logger.debug(f'Create event {event.name} - {event.location} [{event.begin}/{event.end}]')

            i = j + 1
    except IndexError:
        pass

    return str(calendar)


if __name__ == '__main__':
    make_ics('new-edt.xlsx')
