from typing import Union


class DealDirection:
    def __init__(self, department_id: Union[int, str]):
        self.deal_direction = {
            1: {
                'category_id': 31,
                'assigned': 45,
                'new': 'C31:NEW',
                'won': 'C31:WON',
                'cancel': 'C31:APOLOGY'},
            2: {
                'category_id': 123,
                'assigned': 85,
                'new': 'C123:NEW',
                'won': 'C123:WON',
                'cancel': 'C123:APOLOGY'},
            3: {
                'category_id': 20,
                'assigned': 44,
                'new': 'C20:NEW',
                'won': 'C20:WON',
                'cancel': 'C20:APOLOGY'},
            4: {
                'category_id': 19,
                'assigned': 59,
                'new': 'C19:NEW',
                'won': 'C19:WON',
                'cancel': 'C19:APOLOGY'}
        }
        self.direct = self.deal_direction[department_id]

    def get_direction(self):
        return self.direct
