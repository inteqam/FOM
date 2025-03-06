from django.core.management.base import BaseCommand
from aes.queryset_utils import convert_queryset_values_to_dict
from common.models import Client, BranchMaster, Department
from data_generation.feature_scripts.insert_features import insert_features
from data_generation.feature_scripts.refresh_features import refresh_features
from data_generation.feature_scripts.register_client import register_client
from data_generation.feature_scripts.subscribe_feature_for_branch_department import \
    subscribe_feature_for_branch_department
from data_generation.feature_scripts.subscribe_feature_for_client import subscribe_feature_for_client
from data_generation.feature_scripts.unsubscribe_feature import unsubscribe_feature


class Command(BaseCommand):
    """
    Command = python manage.py setup_features, or
    you can also pass an option by python manage.py setup_features --option 2

    Choose options
    [1] Register Client
    [2] Insert Features
    [3] Subscribe Feature for Client
    [4] Subscribe Feature for Branch Department
    [5] Unsubscribe a Feature

    ---- Register Client ----
        Enter Number 1
        Enter client name ginza
        ginza successfully registered.

    ---- Insert Features ----
        Enter Number 2
        Features inserted.

    ---- Subscribe Feature for Client ----
        CASE 1: SUCCESS
        Enter Number 3
        Enter client name ginza
        Enter feature name LOT_NUMBER_TRADING
        Enter feature value for ginza True
        LOT_NUMBER_TRADING subscribed for ginza with value True

        CASE 2: INCORECT FEATURE VALUE
        Enter Number 3
        Enter client name ginza
        Enter feature name DYEING_PRODUCTION_PHASE
        Enter feature value for ginza 2
        ['feature_value must be of type bool']
        Please check values passed

        CASE 3: CLIENT DOES NOT EXIST
        Enter Number 3
        Enter client name client_not_existing
        Enter feature name DYEING_PRODUCTION_PHASE
        Enter feature value for client_not_existing True
        Client matching query does not exist.
        Please check values passed

    ---- Subscribe Feature for Branch Department ----
        Enter Number: 4
        Enter Client id from {Client suggestions}: 7
        Enter Branch id {Branch suggestions}: 35
        Enter Department id {Department suggestions}: 16
        Enter feature name: FABRIC_REPACKING_THRESHOLD_PCT
        Enter feature value for 35 and 16: 10

    ---- Unsubscribe a Feature ----
        Enter Number: 5
        Enter feature name: FABRIC_REPACKING_THRESHOLD_PCT

    ---- Refresh Features ----
        Enter Number: 6
        1st: Removed Feature from DB, which are not in use.
        2nd: Refresh description of features.

    ---- ANYTHING ELSE -----
    Enter Number anything else
    anything else - Not an option


    """
    help = 'Allow to perform feature related operations.'

    def add_arguments(self, parser):
        parser.add_argument('--option', type=str)

    def handle(self, *args, **kwargs):
        user_choice = kwargs['option']

        if user_choice is None:
            self.stdout.write('Choose options')
            self.stdout.write('[1] Register Client')
            self.stdout.write('[2] Insert Features')
            self.stdout.write('[3] Subscribe Feature for Client')
            self.stdout.write('[4] Subscribe Feature for Branch Department')
            self.stdout.write('[5] Unsubscribe a Feature')
            self.stdout.write('[6] Refresh Features')

            user_choice = input("Enter Number: ")

        if not user_choice.isdigit():
            self.stdout.write(self.style.ERROR(f'{user_choice} - Not an option'))
            return

        user_choice = int(user_choice)

        match user_choice:
            case 1:
                # Register client
                client_name = input("Enter client name: ")
                register_client(client_name)
                self.stdout.write(self.style.SUCCESS(f'{client_name} successfully registered.'))

            case 2:
                # Insert and Refresh features.
                insert_features()
                refresh_features()
                self.stdout.write(self.style.SUCCESS('Features inserted and refreshed.'))

            case 3:
                # Subscribe feature for client
                client_name = input("Enter client name: ")
                feature_name = input("Enter feature name: ")
                feature_value = input(f"Enter feature value for {client_name}: ")
                subscription_result = subscribe_feature_for_client(client_name, feature_name, feature_value)
                if isinstance(subscription_result, bool) and subscription_result:
                    self.stdout.write(
                        self.style.SUCCESS(f'{feature_name} subscribed for {client_name} with value {feature_value}'))
                else:
                    self.stdout.write(self.style.ERROR(f'{subscription_result}'))
                    self.stdout.write(self.style.ERROR('Please check values passed'))

            case 4:
                # Subscribe Feature for Branch Department
                clients = convert_queryset_values_to_dict(Client.objects.values('id', 'name'), 'id')
                client_id = int(input(f"Enter Client id from {clients}"))

                branches = convert_queryset_values_to_dict(
                    BranchMaster.objects.filter(client_id=client_id).values('id', 'short_name'), 'id')

                branch_id = int(input(f"Enter Branch id {branches}"))

                departments = convert_queryset_values_to_dict(
                    Department.objects.filter(client_id=client_id).values('id', 'name'), 'id')

                department_id = int(input(f"Enter Department id {departments}"))

                feature_name = input("Enter feature name: ")
                feature_value = input(f"Enter feature value for {branch_id} and {department_id}: ")
                subscription_result = subscribe_feature_for_branch_department(client_id, branch_id, department_id,
                                                                              feature_name,
                                                                              feature_value)
                if isinstance(subscription_result, bool) and subscription_result:
                    self.stdout.write(
                        self.style.SUCCESS(f'{feature_name} subscribed for {branch_id} and {department_id}'
                                           f' with value {feature_value}'))
                else:
                    self.stdout.write(self.style.ERROR(f'{subscription_result}'))
                    self.stdout.write(self.style.ERROR('Please check values passed'))

            case 5:
                # Unsubscribe a Feature
                feature_name = input("Enter feature name: ")
                unsubscribe_feature(feature_name)
                self.stdout.write(self.style.SUCCESS(f'{feature_name} is unsubscribed now.'))

            case 6:
                refresh_features()
                self.stdout.write(self.style.SUCCESS(f'Features Refreshed.'))

            case _:
                self.stdout.write(self.style.ERROR('Not an option'))
