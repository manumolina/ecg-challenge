import os
from starlette.testclient import TestClient
from application_factory import create_api
from services.ecg.routers.default import PATH_PREFIX

"""
POST
/load
* si ecg_list no tiene el formato
- devuelve HTTP error

* si ecg_list tiene el formato
    * si tiene 

GET
/

"""
app = create_api()
client = TestClient(app)


def test_retrieve_user_ecgs():
    path = os.path.join(PATH_PREFIX)
    response = client.get(path)
    print(response.json())
    assert response.status_code == 200
    assert 1 == 2
