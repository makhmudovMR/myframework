import pytest 
from api import Api


@pytest.fixture
def api():
    return Api()

def test_basic_route(api):
    @api.route('/home')
    def home(req, resp):
        resp.text = 'YOLO'

