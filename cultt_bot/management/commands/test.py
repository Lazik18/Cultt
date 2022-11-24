import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        headers = {
            'authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQ2YjYwNTEwZDM5NWY1MjZjMTc5MzdiYTFmOWNhOTBlMzE4MDUyOGQzODFiYWJmZjBiOTNlY2ZjMzZkYmZkMDNlYWZjYzFlMmNhNjUwNzRhIn0.eyJhdWQiOiJhNjNlZTIwYy0yMTkyLTQ1OTEtYjMyMS00ZTk3NWQyMWFhMzUiLCJqdGkiOiI0NmI2MDUxMGQzOTVmNTI2YzE3OTM3YmExZjljYTkwZTMxODA1MjhkMzgxYmFiZmYwYjkzZWNmYzM2ZGJmZDAzZWFmY2MxZTJjYTY1MDc0YSIsImlhdCI6MTY2OTI4MjMwMywibmJmIjoxNjY5MjgyMzAzLCJleHAiOjE2NjkzNjg3MDMsInN1YiI6IjYzODA1NTQiLCJhY2NvdW50X2lkIjoyOTA3MDMwNywiYmFzZV9kb21haW4iOiJhbW9jcm0ucnUiLCJzY29wZXMiOlsicHVzaF9ub3RpZmljYXRpb25zIiwiY3JtIiwibm90aWZpY2F0aW9ucyJdfQ.DfYDHykFkqS_nzSnLue57d-KAts9QFg6rmLmyJQwOp1v7fDyuCabClVisIU0YnNhVhOHolTGKFIVBDuSBgj9GmM3Ej2mZpuRm9jgyVkw_KVx7Y8VEsOfzDgwSl-h49Gd7paaYoFOthHkNur3Ly-4oEgocndOdV9VnUltbiUzsyctVG8d1GAH4BUPa5Q0dGMU90fJqT628JegL9SP7Os9lu6aYA-7xcB92rY7WzhTgXJH9wrX_Elo99R31EGdhJT5IlZaj0xq6GdGyhHXL5kHruJJx0wIyN4ly2ub7UWJaU2X4TTZSFngsoRwklChgG_0qIRFfWLxXraFtUK1Je3y1g',
            'Content-Type': 'application/json'
        }

        resp = requests.get(f'https://thecultt.amocrm.ru/api/v4/contacts?filter[custom_fields_values][67727]=test@test.com', headers)
        print(resp)
        print(resp.json())
