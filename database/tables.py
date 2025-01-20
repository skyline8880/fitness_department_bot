class Department:
    ID = 'id'
    NAME = 'name'

    def __init__(self) -> None:
        self.msk = 'Ohana-Московский'
        self.vlk = 'Ohana-Волковский'
        self.nkr = 'Ohana-Некрасовка'
        self.btv = 'Ohana-Бyнинская'

    def __str__(self) -> str:
        return 'department'


class Subdivision:
    ID = 'id'
    NAME = 'name'

    def __init__(self) -> None:
        self.pool = 'Бассейн'
        self.gp = 'Групповые программы'
        self.kids = 'Детский клуб'
        self.marts = 'Клуб единоборств'
        self.gym = 'Тренажёрный зал'

    def __str__(self) -> str:
        return 'subdivision'


class User:
    ID = 'id'
    ISADMIN = 'is_admin'
    PHONE = 'phone'
    LAST_NAME = 'last_name'
    FIRST_NAME = 'first_name'
    PATRONYMIC = 'patronymic'
    TELEGRAM_ID = 'telegram_id'
    FULLNAME = 'full_name'
    USERNAME = 'username'
    DEPARTMENT_ID = 'departments_ids'
    SUBDIV_REFERENCES = 'subdivisions_ids'

    def __str__(self) -> str:
        return 'user'


class Event:
    ID = 'id'
    CREATOR = 'telegram_id'
    DEPARTMENT_ID = 'department_id'
    SUBDIVISION_ID = 'subdivision_id'
    EVENT_DATE = 'event_date'
    NAME = 'name'
    DESCRIPTION = 'description'
    ISFREE = 'is_free'
    ISACTIVE = 'is_active'
    SENT = 'sent'
    PHOTOID = 'photo_id'

    def __str__(self) -> str:
        return 'event'


class Enroll:
    ID = 'id'
    EVENTID = 'event_id'
    CUSTOMER = 'telegram_id'
    ENROLLACTIONID = 'enroll_action_id'

    def __str__(self) -> str:
        return 'enroll'


class EnrollAction:
    ID = 'id'
    NAME = 'name'

    def __init__(self) -> None:
        self.enroll = 'Участвую'
        self.decline = 'Отказ'
        self.thinkig = 'Подумаю'

    def __str__(self) -> str:
        return 'enroll_action'


class Recievers:
    ID = 'id'
    EVENTID = 'event_id'
    CUSTOMER = 'telegram_id'

    def __str__(self) -> str:
        return 'recievers'
