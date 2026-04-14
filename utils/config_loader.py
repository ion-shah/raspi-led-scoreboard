# this file safely loads the config.yaml file and makes sure it is valid
import yaml
import os
import pytz

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

SPORT_MAP = {
        "nba":                 ("basketball", "nba"),
        "nfl":                 ("football",   "nfl"),
        "mlb":                 ("baseball",   "mlb"),
        "nhl":                 ("hockey",     "nhl"),
        "college-football":    ("football",   "college-football"),
        "college-basketball":  ("basketball", "mens-college-basketball"),
        "college-baseball":  ("baseball",   "college-baseball"),
    }

def loadConfig(path=CONFIG_PATH):
    # Loads and validates config.yaml.
    # Returns a config dict, or raises an error with a clear message if something is wrong.
    
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    print("Config loaded successfully, validating...")
    validateConfig(config)
    print("Config loaded and validated successfully.")
    return config

def validateConfig(config):
    # Checks that required fields exist and have valid values.
    # Raises ValueError with a descriptive message if anything is wrong.

    # Check required top-level sections exist
    required_sections = ["hardware", "display", "scheduling", "sports", "priority"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"config.yaml is missing required section: '{section}'")

    # Validate hardware
    hw = config["hardware"]
    if hw.get("rows") not in [32, 64]:
        raise ValueError(f"hardware.rows must be 32 or 64, got: {hw.get('rows')}")
    if hw.get("cols") not in [32, 64, 128]:
        raise ValueError(f"hardware.cols must be 32, 64, or 128, got: {hw.get('cols')}")
    valid_mappings = ["adafruit-hat", "adafruit-hat-pwm", "regular"]
    if hw.get("gpio_mapping") not in valid_mappings:
        raise ValueError(f"hardware.gpio_mapping must be one of {valid_mappings}")

    # Validate timezone
    tz_str = config["display"].get("timezone")
    if tz_str is None:
        raise ValueError("display.timezone is required")
    try:
        pytz.timezone(tz_str)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"display.timezone '{tz_str}' is not a valid timezone. "
                         f"See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")

    # Validate scheduling
    sched = config["scheduling"]
    for key in ["pregame_lookahead_minutes", "postgame_lookback_minutes"]:
        if key not in sched:
            raise ValueError(f"scheduling.{key} is required")
        if not isinstance(sched[key], (int, float)) or sched[key] < 0:
            raise ValueError(f"scheduling.{key} must be a positive number")

    # Validate that at least one sport is enabled
    sports = config["sports"]
    enabled = [s for s, cfg in sports.items() if cfg.get("enabled", False)]
    if not enabled:
        raise ValueError("At least one sport must be enabled in config.yaml")
    
    # Abbreviation check — warns but does not crash
    print("Validating team abbreviations against ESPN API...")
    validateAbbreviations(config)
    print("Validation complete.")

    #validate logo overrides
    validateLogoOverrides(config)
    
def validateAbbreviations(config):
    # For each enabled sport, the favorites list is validating for user feedback
    
    from data.espn import getJSON, apiEndpoint

    for sport_key, (sport, league) in SPORT_MAP.items():
        sport_config = config["sports"].get(sport_key, {})
        if not sport_config.get("enabled", False):
            continue

        favorites = sport_config.get("favorites", [])
        if not favorites:
            continue

        # ESPN teams endpoint returns full team list for a league
        endpoint = apiEndpoint(sport, league, resource="teams")
        data = getJSON(endpoint)

        if data is None:
            print(f"  WARNING: Could not validate {sport_key} abbreviations (API unreachable)")
            continue

        # Build set of valid abbreviations from the response
        valid_abbrs = set()
        for team in data.get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", []):
            abbr = team.get("team", {}).get("abbreviation")
            if abbr:
                valid_abbrs.add(abbr)

        # Check each favorite against the valid set
        for abbr in favorites:
            if abbr not in valid_abbrs:
                print(f"  WARNING: '{abbr}' in {sport_key} favorites is not a valid "
                      f"ESPN abbreviation. Valid options: {sorted(valid_abbrs)}")

def validateLogoOverrides(config):
    """
    Checks that each logo override file exists at the expected exact path.
    Warns if the file is missing.
    """
    overrides = config.get("logo_overrides", {})
    if not overrides:
        return

    print("Validating logo overrides...")
    any_warnings = False

    for league, teams in overrides.items():
        if not teams:
            continue
        for abbr, override_key in teams.items():
            path = f"assets/imgs/logos/{league}/teams_alt/{abbr}_{override_key}.png"
            if not os.path.exists(path):
                print(f"  WARNING: Logo override for {league.upper()} '{abbr}' "
                      f"expected file not found at: {path}")
                any_warnings = True
            else:
                print(f"  OK: {league.upper()} '{abbr}' -> {path}")

    if not any_warnings:
        print("All logo overrides validated successfully.")

def getEnabledSports(config):
    # Returns a list of (sport, league) tuples for all enabled sports.
    # Maps config key names to ESPN API sport/league parameters.

    enabled = []
    for key, (sport, league) in SPORT_MAP.items():
        if config["sports"].get(key, {}).get("enabled", False):
            enabled.append((sport, league))
    return enabled


def getFavorites(config, sport_key):
    # Returns the favorites list for a given sport key (e.g. "nba").
    # Returns empty list if sport not configured or no favorites set.
    
    return config["sports"].get(sport_key, {}).get("favorites", [])