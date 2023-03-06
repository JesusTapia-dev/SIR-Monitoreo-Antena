from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Restart experiment every night at 05:00 am.
    Example:
        manage.py restart_experiment
    """
    def handle(self, *args, **options):
        print("Hola")

# def main():
#     print("Hola")

# if __name__=='__main__':
#     main()


