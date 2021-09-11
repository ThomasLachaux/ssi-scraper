import pandas as pd
import logging
from ics import Calendar, Event
from dateutil import tz
import re

logger = logging.getLogger(__name__)
timezone = tz.gettz('Europe/Paris')


def make_ics(raw_xls):
    slots = [8, 9, 10, 12, 14, 16, 18]
    events = []

    logger.debug('Parsing XLS')
    # Read the file and only keep the schedule and the location
    xls = pd.read_excel(raw_xls, usecols="B:H,N,O")

    for day in range(len(xls)):
        for slot in range(1, 7):

            # on parcourt le dataframe en excluant les valeurs nulles ou les espaces simples
            if isinstance(xls.iloc[day][slot], str) and len(xls.iloc[day][slot]) > 1:

                # Create an event and give it a name
                event = Event()
                event.name = xls.iloc[day][slot]

                # If the slot is on the morning, find the location on cell 7
                if slot < 3:
                    event.location = str(xls.iloc[day][7])

                # Otherwise, find the location on cell 8
                else:
                    event.location = str(xls.iloc[day][8])

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

    calendar = Calendar()

    try:
        i = 0
        while i < len(events):
            beginEvent = events[i]
            j = i

            while beginEvent.end == events[j + 1].begin and beginEvent.name == events[j + 1].name:
                j += 1

            beginEvent.end = events[j].end
            beginEvent.uid = f'{beginEvent.location}{str(beginEvent.begin)}'
            calendar.events.add(beginEvent)
            logger.debug(f'Create event {event.name} - {event.location} [{event.begin}/{event.end}]')

            i = j + 1
    except IndexError:
        pass

    with open('edt.ics', 'w') as file:
        calendar = str(calendar)
        calendar = re.sub(r'PRODID:.+', 'PRODID:SSI - https://github.com/ThomasLachaux/ssi-scraper', calendar)
        file.write(calendar)


if __name__ == '__main__':
    make_ics('new-edt.xlsx')
