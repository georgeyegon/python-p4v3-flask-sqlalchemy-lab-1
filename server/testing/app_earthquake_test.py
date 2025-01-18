import json
from app import app


class TestApp:
    def test_earthquake_found_route(self):
        '''has a resource available at "/earthquakes/<id>".'''
        response = app.test_client().get('/earthquakes/1')
        assert response.status_code == 200
        response_json = json.loads(response.data.decode())
        assert "id" in response_json
        assert "magnitude" in response_json
        assert "location" in response_json
        assert "year" in response_json

    def test_earthquakes_not_found_response(self):
        '''displays appropriate message if id not found'''
        response = app.test_client().get('/earthquakes/9999')
        assert response.status_code == 404
        response_json = json.loads(response.data.decode())
        assert "error" in response_json
        assert response_json["error"] == "Earthquake not found"
