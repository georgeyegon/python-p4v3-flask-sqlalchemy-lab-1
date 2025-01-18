import json
from app import app


class TestApp:
    def test_earthquakes_magnitude_match_response(self):
        '''displays json in earthquake/magnitude route with keys for count, quakes'''
        response = app.test_client().get('/earthquakes/magnitude/9.0')
        response_json = json.loads(response.data.decode())
        assert response.status_code == 200
        assert response_json["count"] == 1
        assert "quakes" in response_json
        assert len(response_json["quakes"]) == 1
        assert response_json["quakes"][0]["magnitude"] == 9.0

    def test_earthquakes_magnitude_no_match_response(self):
        '''displays json in earthquake/magnitude route with keys for count, quakes'''
        response = app.test_client().get('/earthquakes/magnitude/10.0')
        response_json = json.loads(response.data.decode())
        assert response.status_code == 404
        assert response_json["count"] == 0
        assert "quakes" in response_json
        assert len(response_json["quakes"]) == 0
