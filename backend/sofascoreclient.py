#import pandas as pd
#from .scraperfc_exceptions import InvalidLeagueException, InvalidYearException
#from utils import botasaurus_browser_get_json
#import numpy as np
#from typing import Union, Sequence
#import warnings
from pprint import pprint

from botasaurus.request import request, Request
from botasaurus.browser import browser, Driver
from datetime import datetime
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

    def __init__(self) -> None:
        self.league_stats_fields = ['goals']
        self.concatenated_fields = '%2C'.join(self.league_stats_fields)

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
        """
        Returns the valid season to a given competition.
        
        :param competition_id: Competition ID 
        :type competition_id: int
        :return: Returns a dict list where each dict is a season
        :rtype: list[dict]
        """
        data = self.get(f"/unique-tournament/{competition_id}/seasons/")
        return data["seasons"]
    
    def get_current_season(self, competition_id: int) -> int:
        """
        Returns the current season of a given competition. 
        
        :param competition_id: Competition ID
        :type competition_id: int
        :return: Returns the season ID of the last competition.
        :rtype: int
        """
        seasons = self.get_seasons(competition_id)
        season_id = seasons[0]["id"]
        return season_id
    
    def get_matches(self, competition_id: int, season_id: int) -> list[dict]:
        """
        Gets all the matches from a competition in a determined season.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :return: Returns a dict list where each dict is a match
        :rtype: list[dict]
        """
        events = []
        page = 0

        while True:
            data = self.get(
                f"/unique-tournament/{competition_id}/season/{season_id}/events/last/{page}"
            )
            if 'events' not in data:
                break

            events.extend(data['events'])
            page += 1

        return events
    
    def get_matches_by_page(self, competition_id: int, season_id: int, page: int) -> dict:
        """
        Gets all the matches from a competition in a determined season accessing with a number of page.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :param page: The page where the different matches are found
        :return: Returns a dict that corresponds to a different matches
        :rtype: dict
        """
        data = self.get(
             f"/unique-tournament/{competition_id}/season/{season_id}/events/last/{page}"
        )
        if 'events' not in data:
            return

        return data

    def get_match(self, match_id: int) -> dict:
        """
        Gets the information about a match from its ID.
        
        :param match_id: Match ID
        :type match_id: int
        :return: Returns the data dict for the given match.
        :rtype: dict
        """
        data = self.get(f"/event/{match_id}")
        return data["event"]
    
    def get_competition(self, competition_id: int) -> dict:
        """
        Gets the general information about the competition.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :return: Returns a dict with the information about the competition
        :rtype: dict
        """
        data = self.get(f"/unique-tournament/{competition_id}")
        return data["uniqueTournament"]
    
    def get_teams(self, competition_id: int, season_id: int) -> list[dict]:
        """
        Gets all the teams in a competition in a given season.
        
        :param competition_id: Competition id
        :type competition_id: int
        :param season_id: Season id
        :type season_id: int
        :return: Returns a dict list where each dict is a different team
        :rtype: int
        """
        data = self.get(f"/unique-tournament/{competition_id}/season/{season_id}/teams")
        return data["teams"]
    
    def get_team_stats(self, competition_id: int, season_id: int) -> list[dict]:
        """
        Gets all the stats about the teams from a competition in a given season.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :return: Returns a dict list where each dict corresponds to a team stats
        :rtype: list[dict]
        """
        teams = self.get(f"/unique-tournament/{competition_id}/season/{season_id}/teams")["teams"]

        team_data = []
        for team in teams:
            team_id = team["id"]
            result = self.get(f"/team/{team_id}/unique-tournament/{competition_id}/season/{season_id}/statistics/overall")

            if "statistics" in result:
                # Team has league stats, build series with them
                team_data.append(result)

        return team_data
    
    def get_team_general_stats(self, competition_id: int, season_id: int) -> dict:
        """
        Gets the general data about the different teams from a competition in a determined season.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :return: Returns a dict with the general stats
        :rtype: dict
        """
        data = self.get(f'/unique-tournament/{competition_id}/season/{season_id}/standings/total')
        return data
    
    #-------------- MEJORAR (MUY LENTO)
    #-------------- SOLO funciona para la última temporada
    def get_champion(self, competition_id: int, season_id: int) -> dict:
        """
        Gets the champion of the competition in a given season based on the positions (league) or the result of the final (cup).
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :return: Returns a dict that corresponds to the champion team
        :rtype: int
        """
        
        champion = None
        end_date = datetime.fromtimestamp(self.get_competition(competition_id)['endDateTimestamp'])
        current_date = datetime.now()
        if end_date <= current_date:

            matches = self.get_matches(competition_id,season_id)
            # Obtener el partido de la final
            i = 0
            final = None
            for match in matches:
                if matches[i].get('roundInfo', {}).get('name') == 'Final':
                    final = match
                    break
                i+=1

            if final: # Es una copa (tiene final) #=================== VER QUE PASA SI HAY PENALES
                if final["homeScore"]["current"] > final["awayScore"]["current"]:
                    champion = final["homeTeam"]
                else:
                    champion = final["awayTeam"]
            else: # Es una liga (no tiene final)
                champion = self.get_team_general_stats(competition_id,season_id)['standings'][0]['rows'][0]

        return champion

    def get_player_data(self, competition_id: int, season_id: int) -> dict:
        """
        Gets the player data from a competition with its season.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :return: Returns a dict with the information of the different players along with his own stats
        :rtype: dict
        """
        data = self.get(f"/unique-tournament/{competition_id}/season/{season_id}/statistics?accumulation=total&fields={self.concatenated_fields}")
        return data['results']
    
    # -------------------------- Arreglar 
    def get_top_scorers2(self, competition_id: int, season_id: int) -> list:
        """
        Creates a zip list with (player id, goals) and sort the list based on goals in descending order, getting the top scorers.
        
        :param competition_id: Competition ID
        :type competition_id: int
        :param season_id: Season ID
        :type season_id: int
        :return: Returns a list of the league scorers
        :rtype: list
        """
        player_goals = self.get_player_data(competition_id, season_id)
        
        ids = []
        goals = []

        for stat in player_goals:
            ids.append(stat["player"]["id"])
            goals.append(stat["goals"])

        top_scorer = list(zip(ids, goals))

        top_scorer = sorted(top_scorer, key=lambda x: x[1], reverse=True) # Lista de goleadores de más goles a menos

        return top_scorer
    
    def get_top_scorers(self, competition_id: int, season_id: int) -> list:
        player_stats = self.get_player_data(competition_id, season_id)

        scorers = []

        for stat in player_stats:
            goals = stat.get("goals")

            if goals is None:
                continue

            goals = int(goals)

            if goals > 0:
                scorers.append(
                    (stat["player"]["id"], goals)
                )

        scorers.sort(key=lambda x: x[1], reverse=True)
        return scorers
    
    def get_max_scorers(self, top_scorer:list) -> list:
        """
        Creates a zip list with (player id, goals) of the actual top scorers.
        
        :param top_scorer: a list of the top scorers
        :type top_scorer: list
        :return: Returns the max scorers
        :rtype: list
        """
        max_goals = top_scorer[0][1]
        max_scorer = [(player_id, goals) for player_id, goals in top_scorer if goals == max_goals]
        return max_scorer