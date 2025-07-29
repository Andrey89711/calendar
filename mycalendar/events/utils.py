import calendar
from django.utils.html import conditional_escape as esc
from .models import Event


class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li class="calendar-event"> {event.get_html_url} </li>'

        if day != 0:
            return f"""
            <td class="calendar-day">
                <div class="day-number">{day}</div>
                <ul class="event-list"> {d} </ul>
            </td>
            """
        return '<td class="calendar-day empty"></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year,
            start_time__month=self.month
        )

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal