import json 
import csv 
import os

from datetime import datetime
from .models import AuthData

import logging

logger = logging.getLogger(__name__)

logger.info("\n test test test test test \n")

logger.info("\n bla bla bla bla bla \n")

class StoreData:

    def __init__(self, payload):
        self.payload = payload

    def save_to_database(self):

        """ Save user data (ID.me payload) to the PostgreSQL database using 
        Django ORM. """

        logger.info("\n save save save save save \n")

        try:
            
            birth_date_str = self.payload.get('birth_date', None)
            if isinstance(birth_date_str, str):
                try:
                    birth_date = datetime.fromisoformat(birth_date_str)
                except ValueError:
                    print('Invalid birth_date format, setting birth_date to None')
                    birth_date = None
            else:
                birth_date = None

            auth_data = AuthData.objects.create(
                aud=self.payload.get('aud'),
                birth_date=birth_date,
                credential_option_preverified=self.payload.get('credential_option_preverified'),
                email=self.payload.get('email'),
                exp=datetime.utcfromtimestamp(self.payload.get('exp')),
                fname=self.payload.get('fname'),
                iat=datetime.utcfromtimestamp(self.payload.get('iat')),
                identifier=self.payload.get('identifier'),
                iss=self.payload.get('iss'),
                lname=self.payload.get('lname'),
                phonels=self.payload.get('phonels'),
                sub=self.payload.get('sub'),
                transaction=self.payload.get('transaction'),
                uuid=self.payload.get('uuid'),
                zip_code=self.payload.get('zip')
            )

            logger.info(f"\n Saving user data: {self.payload} \n")
            try:
                auth_data.save()
                logger.info("\n Data successfully saved to the database. \n")
            except Exception as e:
                logger.error(f"\n Error saving data: {e} \n")

        except Exception as e:
            print('ERROR: Data not saved to the database.')
            print(e)


    """  Below is sandbox test code  """

    # def __init__(self, payload):
    #     self.payload = payload
    #     self.headers = [
    #         "aud", "birth_date", "credential_option_preverified", "email", 
    #         "exp", "fname", "iat", "identifier", "iss", "lname", "phonels", "sub", "transaction", "uuid", "zip"
    #         ]

    # def check_directory(self, file_name):

    #     """Ensure the directory for the file exists."""

    #     d = os.path.dirname(file_name)
    #     if d and not os.path.exists(d):
    #         os.makedirs(d)

    # def save_json(self, file_name='data/raw_auth_data.json'):

    #     """ Save raw payload JSONs for auditing purposes. """

    #     self.check_directory(file_name)

    #     data = []
    #     if os.path.isfile(file_name):
    #         # open file in read status
    #         with open(file_name, 'r') as file:
    #             data = json.load(file)

    #     # fill any empty fields with null
    #     payload = {field: self.payload.get(field) for field in self.headers}
    #     data.append(payload) 

    #     # open file in write status
    #     with open(file_name, 'w') as file:
    #         try:
    #             json.dump(data, file, indent=5)
    #             print(f'Raw JSON saved to {file_name}.')

    #         except Exception as e:
    #             print(f'ERROR: Raw JSON not saved to {file_name}\n')
    #             print(e)

    # def save_csv(self, file_name='data/auth_data.csv'):

    #     """ Save auth data payload as a CSV file. """

    #     self.check_directory(file_name)

    #     file_exists = os.path.isfile(file_name)

    #     # open file in append status
    #     with open(file_name, 'a', newline='') as file:
    #         try:
    #             writer = csv.writer(file)

    #             if not file_exists:
    #                 writer.writerow(self.headers)
                    
    #             # check for field presence, fill with None if missing
    #             row = [self.payload.get(field) for field in self.headers]

    #             writer.writerow(row)

    #             print(f'Auth data saved to {file_name}.')
            
    #         except Exception as e:
    #             print(f'ERROR: Auth data not saved to {file_name}\n')
    #             print(e)