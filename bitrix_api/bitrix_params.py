import base64
import sys
from typing import Dict, List, Union


def create_deal(
        title: str,
        assigned_by: Union[int, str],
        category_id: Union[int, str],
        stage_id: Union[int, str],
        contact_ids: List):
    return {
            'fields': {
                'TITLE': title,
                'ASSIGNED_BY_ID': assigned_by,
                'CATEGORY_ID': category_id,
                'STAGE_ID': stage_id,
                'CONTACT_IDS': contact_ids
            }
        }


def update_deal_stage(
        deal_id: Union[int, str],
        stage_id: Union[int, str]) -> Dict:
    return {
        'ID': deal_id,
        'fields': {
            'STAGE_ID': stage_id,
        }
    }


def create_contact(
        last_name: str,
        first_name: str,
        patronymic: str,
        phone: Union[int, str]) -> Dict:
    return {
            'fields': {
                'LAST_NAME': f'{last_name}',
                'NAME': f'{first_name}',
                'SECOND_NAME': f'{patronymic}',
                'PHONE': [
                    {
                        'VALUE': f'{phone}',
                        'VALUE_TYPE': 'WORK',
                    },
                ]
            }
        }


def merge_contacts(contact_ids: List) -> Dict:
    return {
        'params': {
            'entityTypeId': 3,
            'entityIds': contact_ids,
        }
    }


def timeline_add_on_action(deal_id, comment):
    return {
        'fields': {
            'ENTITY_ID': deal_id,
            'ENTITY_TYPE': 'deal',
            'COMMENT': comment,
        }
    }


def timeline_add_on_close_json(
        deal_id,
        photo_path,
        comment,
        user):
    separator = '/'
    if sys.platform == 'win32':
        separator = '\\'
    photo_name = photo_path.split(separator)[-1]
    photo_encode = base64.b64encode(
        open(file=photo_path, mode='rb').read()).decode('utf-8')
    return {
        'fields': {
            'ENTITY_ID': deal_id,
            'ENTITY_TYPE': 'deal',
            'COMMENT': f'{user}: {comment}',
            'FILES': {'fileData': [photo_name, photo_encode]}
        }
    }
