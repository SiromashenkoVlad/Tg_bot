from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from dateutil.parser import parse

# Настройки доступа
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'


def authenticate_google_calendar():
    """Аутентификация в Google Calendar API"""
    creds = None

    # Проверяем существование файла с токеном
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Если нет валидных учетных данных, пользователь авторизуется
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохраняем учетные данные для следующего запуска
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_all_user_events(service, time_start='1970-01-01T00:00:00Z',
                        time_end=datetime.datetime.utcnow().isoformat() + 'Z'):
    # time_start и time_end указываются в формате datetime

    """Получает все события пользователя из первичного календаря"""

    # Получаем ID первичного календаря пользователя
    primary_calendar = service.calendars().get(calendarId='primary').execute()
    calendar_id = primary_calendar['id']

    all_events = []
    page_token = None

    while True:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_start,
            timeMax=time_end,
            singleEvents=True,
            orderBy='startTime',
            pageToken=page_token,
            showDeleted=False
        ).execute()

        events = events_result.get('items', [])
        all_events.extend(events)

        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    return all_events


def format_event_details(event):
    """Форматирует детали события в читаемый вид"""
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))

    # Парсим даты для красивого отображения
    try:
        start_datetime = parse(start) if start else None
        end_datetime = parse(end) if end else None
    except:
        start_datetime = end_datetime = None

    details = {
        'id': event['id'],
        'title': event.get('summary', 'Без названия'),
        'description': event.get('description', ''),
        'location': event.get('location', ''),
        'status': event.get('status', ''),
        'created': parse(event['created']).strftime('%Y-%m-%d %H:%M:%S') if 'created' in event else '',
        'updated': parse(event['updated']).strftime('%Y-%m-%d %H:%M:%S') if 'updated' in event else '',
        'start': start_datetime.strftime('%Y-%m-%d %H:%M:%S') if start_datetime else start,
        'end': end_datetime.strftime('%Y-%m-%d %H:%M:%S') if end_datetime else end,
        'is_all_day': 'date' in event['start'],
        'attendees': len(event.get('attendees', [])),
        'creator': event.get('creator', {}).get('email', ''),
        'organizer': event.get('organizer', {}).get('email', ''),
        'recurrence': bool(event.get('recurrence')),
        'recurring_event_id': event.get('recurringEventId', ''),
    }

    return details


def print_events(events):
    """Выводит информацию о событиях"""
    for i, event in enumerate(events, 1):
        details = format_event_details(event)
        print(f"\nСобытие #{i}")
        print(f"ID: {details['id']}")
        print(f"Название: {details['title']}")
        print(f"Дата создания: {details['created']}")
        print(f"Последнее обновление: {details['updated']}")
        print(f"Начало: {details['start']} {'(весь день)' if details['is_all_day'] else ''}")
        print(f"Конец: {details['end']}")
        print(f"Место: {details['location']}")
        print(f"Статус: {details['status']}")
        print(f"Участников: {details['attendees']}")
        print(f"Повторяющееся: {'Да' if details['recurrence'] else 'Нет'}")
        print(f"Описание: {details['description'][:100]}{'...' if len(details['description']) > 100 else ''}")
        print("-" * 80)


def save_to_csv(events, filename='google_calendar_events.csv'):
    """Сохраняет события в CSV файл"""
    import csv

    if not events:
        print("Нет событий для сохранения")
        return

    fieldnames = [
        'id', 'title', 'description', 'location', 'status',
        'created', 'updated', 'start', 'end', 'is_all_day',
        'attendees', 'creator', 'organizer', 'recurrence', 'recurring_event_id'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for event in events:
            writer.writerow(format_event_details(event))

    print(f"События сохранены в файл: {filename}")


if __name__ == '__main__':
    print("Аутентификация в Google Calendar...")
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    print("\nПолучение событий...")
    events = get_all_user_events(service)

    print(f"\nНайдено событий, созданных пользователем: {len(events)}")

    if events:
        print("\nПоследние 5 событий:")
        print_events(events[:5])

        save_to_csv(events)
    else:
        print("Нет событий, созданных пользователем")
