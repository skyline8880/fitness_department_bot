from enum import Enum


class Action(Enum):
    CANCEL = '✖ Отменить'
    SKIP = '➠ Пропустить'
    TOSUBDIVS = '≫ Далее'
    TOMENU = '☰ В меню'


class Menu(Enum):
    CLUB = '🏢 Выбор клубов'
    SUBDIV = '📋 Выбор подразделений'


class AdminMenuActions(Enum):
    TOMENU = '☰ В меню'
    BACK = '☚ В Начало'
    ADMINS = '◀ Назад'


class EventFreeActions(Enum):
    PAY = 'Платно'
    FREE = 'Бесплатно'


class CurrentEventActions(Enum):
    SEND = '✉️ Разослать'
    STATS = '📈 Статистика'
    DELETE = '❌ Деактивировать'
    ACTIVATE = '✔️ Активировать'


class EventsActions(Enum):
    CREATE = '📝 Создать'
    TOSENDEVENTS = '📩 К рассылке'
    COMMINGEVENTS = '📅 Предстоящие'


class AdminsActions(Enum):
    ADD = '➕ Добавить'
    REMOVE = '➖ Удалить'


class ReportsActions(Enum):
    EVENTS = '📒 Мероприятия'
    USERS = '👥 Пользователи'
    REPORT1 = 'Отчет №1'
    REPORT2 = 'Отчет №2'


class AdminMenu(Enum):
        
    
    ADMINS = '💻 Администраторы'
    EVENTS = '📑 Мероприятия'
    REPORTS = '📃 Отчёты'

    
class DateReports(Enum):
    CURRENT_DATE = 'Текущиий месяц'
    PREVIOUS_DATE = 'Предыдущий месяц'
    PERIOD = 'Выбрать период'
