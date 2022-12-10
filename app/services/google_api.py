from typing import List
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.charity_project import CharityProjectDB
from app.services.constants import FORMAT, LOCALE


class Google:
    DRIVE_SERVICE = 'drive'
    DRIVE_SERVICE_VERSION = 'v3'
    SHEETS_SERVICE = 'sheets'
    SHEETS_SERVICE_VERSION = 'v4'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    '''Создаёт гугл-таблицу с отчётом на сервисном аккаунте.'''
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': LOCALE
        },
        'sheets': [{'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {'rowCount': 100,
                               'columnCount': 11}
        }}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id  # noqa


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    '''Выдаёт права личному аккаунту к документам созданным с сервисного аккаунта.'''
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(Google.DRIVE_SERVICE,
                                              Google.DRIVE_SERVICE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[CharityProjectDB],
    wrapper_services: Aiogoogle
):
    '''Обновляет данные в гугл-таблице.'''
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(Google.SHEETS_SERVICE, Google.SHEETS_SERVICE_VERSION)
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        sort_projects = project['close_date'] - project['create_date']
        new_row = [
            str(project['name']),
            str(sort_projects),
            str(project['description'])
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
