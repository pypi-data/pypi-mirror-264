# import pytest
# import requests_mock
# from mailtarget_sdk.layang import Layang

# def test_send():
#     with requests_mock.Mocker() as m:
#         m.post('https://apiconfig.mailtarget.co/v1/layang/transmissions', json={'success': True, 'message': 'Email sent'})
        
#         layang = Layang(api_key='fake_api_key')
#         response = layang.send({'dummy': 'data'})
        
#         assert response == {'success': True, 'message': 'Email sent'}
