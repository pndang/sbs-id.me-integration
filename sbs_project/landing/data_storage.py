import json 
import csv 
import os

class StoreData:
    def __init__(self, payload):
        self.payload = payload
        self.headers = [
            "aud", "birth_date", "credential_option_preverified", "email", 
            "exp", "fname", "iat", "identifier", "iss", "lname", "phonels", "sub", "transaction", "uuid", "zip"
            ]

    def check_directory(self, file_name):

        """Ensure the directory for the file exists."""

        d = os.path.dirname(file_name)
        if d and not os.path.exists(d):
            os.makedirs(d)

    def save_json(self, file_name='data/raw_auth_data.json'):

        """ Save raw payload JSONs for auditing purposes. """

        self.check_directory(file_name)

        data = []
        if os.path.isfile(file_name):
            # open file in read status
            with open(file_name, 'r') as file:
                data = json.load(file)

        # fill any empty fields with null
        payload = {field: self.payload.get(field) for field in self.headers}
        data.append(payload) 

        # open file in write status
        with open(file_name, 'w') as file:
            try:
                json.dump(data, file, indent=5)
                print(f'Raw JSON saved to {file_name}.')

            except Exception as e:
                print(f'ERROR: Raw JSON not saved to {file_name}\n')
                print(e)

    def save_csv(self, file_name='data/auth_data.csv'):

        """ Save auth data payload as a CSV file. """

        self.check_directory(file_name)

        file_exists = os.path.isfile(file_name)

        # open file in append status
        with open(file_name, 'a', newline='') as file:
            try:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow(self.headers)
                    
                # check for field presence, fill with None if missing
                row = [self.payload.get(field) for field in self.headers]

                writer.writerow(row)

                print(f'Auth data saved to {file_name}.')
            
            except Exception as e:
                print(f'ERROR: Auth data not saved to {file_name}\n')
                print(e)