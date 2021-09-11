# SSI Scraper

[![Build Status](https://github.com/ThomasLachaux/ssi-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/ungdev/ThomasLachaux/ssi-scraper/actions)

Scraper and parser for a school schedule

## Installation

```
pip3 install pipenv
pipenv install
docker-compose up -d
cp .env.example .env # Fill with your ent credentials
pipenv run python main.py
```

## Add to Google Calendar

Go to https://calendar.google.com/calendar/u/0/r/settings/addbyurl and add either

- https://raw.githubusercontent.com/ThomasLachaux/ssi-scraper/master/calendars/ssi-all.ics
- https://raw.githubusercontent.com/ThomasLachaux/ssi-scraper/master/calendars/ssi-except-gs15.ics
- https://raw.githubusercontent.com/ThomasLachaux/ssi-scraper/master/calendars/ssi-except-gs16.ics
- https://raw.githubusercontent.com/ThomasLachaux/ssi-scraper/master/calendars/ssi-except-gs21.ics
