#import pandas as pd
#from .scraperfc_exceptions import InvalidLeagueException, InvalidYearException
#from utils import botasaurus_browser_get_json
#import numpy as np
#from typing import Union, Sequence
#import warnings

from botasaurus.request import request, Request
from botasaurus.browser import browser, Driver
import json

""" These are the status codes for Sofascore events. Found in event['status'] key.
{100: {'code': 100, 'description': 'Ended', 'type': 'finished'},
 120: {'code': 120, 'description': 'AP', 'type': 'finished'},
 110: {'code': 110, 'description': 'AET', 'type': 'finished'},
 70: {'code': 70, 'description': 'Canceled', 'type': 'canceled'},
 60: {'code': 60, 'description': 'Postponed', 'type': 'postponed'},
 93: {'code': 93, 'description': 'Removed', 'type': 'finished'},
 90: {'code': 90, 'description': 'Abandoned', 'type': 'canceled'},
 7: {'code': 7, 'description': '2nd half', 'type': 'inprogress'},
 6: {'code': 6, 'description': '1st half', 'type': 'inprogress'},
 0: {'code': 0, 'description': 'Not started', 'type': 'notstarted'}}
"""

API_PREFIX = 'https://api.sofascore.com/api/v1'

comps = {
    # European continental club comps
    'Champions League': 7, 'Europa League': 679, 'Europa Conference League': 17015,
    # European domestic leagues
    'EPL': 17, 'La Liga': 8, 'Bundesliga': 35, 'Serie A': 23, 'Ligue 1': 34, 'Turkish Super Lig': 52,
    # South America
    'Argentina Liga Profesional': 155, 'Argentina Copa de la Liga Profesional': 13475,
    'Liga 1 Peru': 406, "Copa Libertadores": 384,
    # USA
    'MLS': 242, 'USL Championship': 13363, 'USL1': 13362, 'USL2': 13546,
    # Middle East
    "Saudi Pro League": 955,
    # Men's international comps
    'World Cup': 16, 'Euros': 1, 'Gold Cup': 140,
    # Women's international comps
    "Women's World Cup": 290
}

# Botasaurus--------------------------------------------------------------
@request(output=None, create_error_logs=False)
def botasaurus_request_get_json(request: Request, url: str) -> dict:
    """ Use Botasaurus REQUESTS module to get JSON from page.

    Parameters
    ----------
    request : botasaurus.request.Request
        The request object provided by the botasaurus decorator
    url : str
        The URL to request

    Returns
    -------
    dict
    """
    if not isinstance(url, str):
        raise TypeError('`url` must be a string.')
    response = request.get(url)
    result = response.json()
    return result

@browser(headless=True, output=None, create_error_logs=False, block_images_and_css=True)
def botasaurus_browser_get_json(driver: Driver, url: str) -> dict:
    """ Use Botasaurus BROWSER model to get JSON from page

    Parameters
    ----------
    driver : botasaurus.browser.Driver
        Browser object. Provided by Botasaurus decorator
    url : str
        The URL to scrape

    Returns
    -------
    dict
    """
    driver.get(url)
    page_source = driver.page_text
    result = json.loads(page_source)
    return result

#--------------------------------------------------------------------------------------
class Sofascore:

    def get(self, path: str) -> dict:
        """
        It does a HTTP GET and returns JSON like dict

        Parameters
        ----------
        path: str
            Part of the URL to ask data

        Returns
        -------
        response.json() : dict
            Dict from a JSON of data
        """
        url = f"{API_PREFIX}{path}"
        return botasaurus_browser_get_json(url) # ← JSON → dict de Python
    
    def get_seasons(self, competition_id: int) -> list[dict]:
        data = self.get(f"/unique-tournament/{competition_id}/seasons/")
        # season_id = max(seasons, key=lambda s: s["year"])["id"] SEASON ACTIVA, la más nueva
        return data["seasons"]
    
    #ARREGLAR
    def get_matches(self, season_id: int) -> list[dict]:
        events = []
        page = 0

        while True:
            data = self.get(
                f"/unique-tournament/season/{season_id}/events/last/{page}"
            )
            if "events" not in data:
                break

            events.extend(data["events"])
            page += 1

        return events

    def get_match(self, match_id: int) -> dict:
        data = self.get(f"/event/{match_id}")
        return data["event"]
    
    def get_competition(self, competition_id: int) -> list[dict]:
        data = self.get(f"/unique-tournament/{competition_id}")
        return data["uniqueTournament"]
    
    def get_standings(self, competition_id: int, season_id: int) -> dict:
        data = self.get(f"/unique-tournament/{competition_id}/season/{season_id}/standings/total")
        #champion = data["standings"][0]["rows"][0]["team"] # obtiene el equipo con más puntos (campeón) (Dejarlo en el Normalize)
        return data

    #ARREGLAR
    def get_top_players(self, competition_id: int, season_id: int) -> dict: 
        data = self.get(f"/unique-tournament/{competition_id}/season/{season_id}/top-players/overall")
        #scorer = data[0]["player"] # obtiene el jugador con más goles (Dejarlo en el Normalize)
        return data["topPlayers"]