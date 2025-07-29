from django.contrib import admin
from django.urls import path, include
from events import views  # Добавьте этот импорт

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/<int:event_id>/', views.event, name='event'),
    path('notes/', views.notes_list, name='notes_list'),
    path('note/new/', views.note_detail, name='note_new'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('note/<int:note_id>/delete/', views.note_delete, name='note_delete'),
]