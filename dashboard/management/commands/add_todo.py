from dashboard.models import Todo
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_todo(self):
        get_data = requests.get('https://jsonplaceholder.typicode.com/todos')
        get_data = get_data.json()
        for data in get_data:
            Todo.objects.create(
                userId=data['userId'],
                title=data['title'], completed=data['completed'])

    def handle(self, *args, **options):
        self.add_todo()
