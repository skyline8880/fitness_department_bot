from aiogram.filters.callback_data import CallbackData

from constants.actions import (Action, AdminMenu, AdminMenuActions,
                               AdminsActions, CurrentEventActions, DateReports,
                               EventFreeActions, EventsActions, Menu,
                               ReportsActions)


class ReferencesCD(CallbackData, prefix='ref'):
    subdiv: int
    is_checked: int


class DepartmentsCD(CallbackData, prefix='dep'):
    depart: int
    is_checked: int


class EventDepartment(CallbackData, prefix='event_depart'):
    event_depart: int


class EventSubdivision(CallbackData, prefix='event_subdiv'):
    event_subdiv: int


class EventPayment(CallbackData, prefix='event_pay'):
    isfree: int
    name: EventFreeActions


class ActionsCD(CallbackData, prefix='action'):
    action: Action


class MenuCD(CallbackData, prefix='mact'):
    menu_act: Menu


class AdminMenuCD(CallbackData, prefix='adm_menu'):
    adm_menu: AdminMenu


class AdminsActionsCD(CallbackData, prefix='adm_act'):
    adm_act: AdminsActions


class EventsActionsCD(CallbackData, prefix='event_act'):
    event_act: EventsActions


class ReportsActionsCD(CallbackData, prefix='report_act'):
    report_act: ReportsActions


class CurrenEventActionsCD(CallbackData, prefix='curev_act'):
    curev_act: CurrentEventActions


class AdminMenuActionsCD(CallbackData, prefix='admen_act'):
    admen_act: AdminMenuActions


class CustomerEventActionsCD(CallbackData, prefix='custom_act'):
    act_id: int
    custom_act: str


class DateReportsCD(CallbackData, prefix='dt_rep'):
    date_report: DateReports
    