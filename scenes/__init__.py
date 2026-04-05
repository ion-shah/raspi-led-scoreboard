from scenes.base_scene import BaseScene
from scenes.basketball import BasketballScene

#====get the correct scene, based on the sport====
SCENE_REGISTRY = {
    'nba': BasketballScene,
    'mlb': None #... add as functionality expands
}

def get_scene(league, matrix, game_data):
    """
    Returns an instantiated scene for the given league.
    Returns None if the league is not supported.
    """
    scene_class = SCENE_REGISTRY.get(league.lower())
    if scene_class is None:
        return None
    return scene_class(matrix, game_data)