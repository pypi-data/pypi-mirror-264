import requests

class Layang:
    APIBase = "https://apiconfig.mailtarget.co"

    def __init__(self, api_key):
        self.api_key = api_key
        

    def send(self, message):
        # Melakukan POST request
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = message.to_json() 

        try:
            response = requests.post(self.APIBase + '/v1/layang/transmissions', headers=headers, data=data)
            # response.raise_for_status()  # Ini akan melemparkan error untuk respon 4xx atau 5xx
            return response.json()  # Mengembalikan respons dalam bentuk JSON
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6+
        except Exception as err:
            print(f'An error occurred: {err}')  # Python 3.6+
        return None