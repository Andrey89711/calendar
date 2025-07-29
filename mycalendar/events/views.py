from datetime import datetime, date, timedelta
import calendar
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .utils import Calendar
from .forms import EventForm, NoteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    model = Event
    template_name = 'events/calendar.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = self.get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = self.prev_month(d)
        context['next_month'] = self.next_month(d)
        return context

    def get_date(self, req_month):
        if req_month:
            year, month = (int(x) for x in req_month.split('-'))
            return date(year, month, day=1)
        return datetime.today()

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month


@login_required(login_url='/accounts/login/')
def event(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = None

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendar')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event.html', {'form': form})


@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'events/notes_list.html', {'notes': notes})


@login_required
def note_detail(request, note_id=None):
    if note_id:
        note = get_object_or_404(Note, pk=note_id, user=request.user)
    else:
        note = None

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'events/note_detail.html', {'form': form})


@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    note.delete()
    return redirect('notes_list')