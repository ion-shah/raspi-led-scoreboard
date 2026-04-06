from scenes.base_scene import *
from scenes.basketball import BasketballScene
from scenes.clock import ClockScene

#====get the correct scene, based on the sport====
SCENE_REGISTRY = {
    'nba': BasketballScene,
    'mlb': None, #... add as functionality expands
    'clock': ClockScene
}

def getScene(game_data, timezone):
    # Returns an instantiated scene for the given league.
    # Returns None if the league is not supported.
    
    league = game_data.league
    scene_class = SCENE_REGISTRY.get(league.lower())
    if scene_class is None:
        return None
    return scene_class(game_data, timezone)