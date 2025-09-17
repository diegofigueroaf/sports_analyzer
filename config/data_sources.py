"""
Data Sources Configuration
Centralized configuration for all data collection sources
"""

# ESPN API Configuration
ESPN_CONFIG = {
    'base_url': 'http://site.api.espn.com/apis/site/v2/sports/football/nfl',
    'endpoints': {
        'scoreboard': '/scoreboard',
        'teams': '/teams',
        'team_detail': '/teams/{team_id}',
        'standings': '/standings',
        'games': '/scoreboard?dates={date}',
    },
    'rate_limit': {
        'requests_per_minute': 60,
        'requests_per_hour': 3600
    }
}

# Weather API Configuration (OpenWeatherMap)
WEATHER_CONFIG = {
    'base_url': 'http://api.openweathermap.org/data/2.5',
    'endpoints': {
        'current': '/weather',
        'forecast': '/forecast'
    },
    'rate_limit': {
        'requests_per_minute': 60,
        'requests_per_day': 1000  # Free tier limit
    }
}

# Sports Betting APIs (Future implementation)
BETTING_APIS = {
    'the_odds_api': {
        'base_url': 'https://api.the-odds-api.com/v4',
        'endpoints': {
            'sports': '/sports',
            'odds': '/sports/{sport}/odds',
            'scores': '/sports/{sport}/scores'
        },
        'rate_limit': {
            'requests_per_month': 500  # Free tier
        }
    }
}

# NFL Team Information
NFL_TEAMS = {
    'AFC_EAST': {
        'bills': {'id': '2', 'city': 'Buffalo', 'name': 'Bills'},
        'dolphins': {'id': '15', 'city': 'Miami', 'name': 'Dolphins'},
        'patriots': {'id': '17', 'city': 'New England', 'name': 'Patriots'},
        'jets': {'id': '20', 'city': 'New York', 'name': 'Jets'}
    },
    'AFC_NORTH': {
        'ravens': {'id': '33', 'city': 'Baltimore', 'name': 'Ravens'},
        'bengals': {'id': '4', 'city': 'Cincinnati', 'name': 'Bengals'},
        'browns': {'id': '5', 'city': 'Cleveland', 'name': 'Browns'},
        'steelers': {'id': '23', 'city': 'Pittsburgh', 'name': 'Steelers'}
    },
    'AFC_SOUTH': {
        'texans': {'id': '34', 'city': 'Houston', 'name': 'Texans'},
        'colts': {'id': '11', 'city': 'Indianapolis', 'name': 'Colts'},
        'jaguars': {'id': '30', 'city': 'Jacksonville', 'name': 'Jaguars'},
        'titans': {'id': '10', 'city': 'Tennessee', 'name': 'Titans'}
    },
    'AFC_WEST': {
        'broncos': {'id': '7', 'city': 'Denver', 'name': 'Broncos'},
        'chiefs': {'id': '12', 'city': 'Kansas City', 'name': 'Chiefs'},
        'raiders': {'id': '13', 'city': 'Las Vegas', 'name': 'Raiders'},
        'chargers': {'id': '24', 'city': 'Los Angeles', 'name': 'Chargers'}
    },
    'NFC_EAST': {
        'cowboys': {'id': '6', 'city': 'Dallas', 'name': 'Cowboys'},
        'giants': {'id': '19', 'city': 'New York', 'name': 'Giants'},
        'eagles': {'id': '21', 'city': 'Philadelphia', 'name': 'Eagles'},
        'commanders': {'id': '28', 'city': 'Washington', 'name': 'Commanders'}
    },
    'NFC_NORTH': {
        'bears': {'id': '3', 'city': 'Chicago', 'name': 'Bears'},
        'lions': {'id': '8', 'city': 'Detroit', 'name': 'Lions'},
        'packers': {'id': '9', 'city': 'Green Bay', 'name': 'Packers'},
        'vikings': {'id': '16', 'city': 'Minnesota', 'name': 'Vikings'}
    },
    'NFC_SOUTH': {
        'falcons': {'id': '1', 'city': 'Atlanta', 'name': 'Falcons'},
        'panthers': {'id': '29', 'city': 'Carolina', 'name': 'Panthers'},
        'saints': {'id': '18', 'city': 'New Orleans', 'name': 'Saints'},
        'buccaneers': {'id': '27', 'city': 'Tampa Bay', 'name': 'Buccaneers'}
    },
    'NFC_WEST': {
        'cardinals': {'id': '22', 'city': 'Arizona', 'name': 'Cardinals'},
        'rams': {'id': '14', 'city': 'Los Angeles', 'name': 'Rams'},
        '49ers': {'id': '25', 'city': 'San Francisco', 'name': '49ers'},
        'seahawks': {'id': '26', 'city': 'Seattle', 'name': 'Seahawks'}
    }
}

# Stadium Information (for weather data)
NFL_STADIUMS = {
    '1': {'city': 'Atlanta', 'state': 'GA', 'dome': True},
    '2': {'city': 'Buffalo', 'state': 'NY', 'dome': False},
    '3': {'city': 'Chicago', 'state': 'IL', 'dome': False},
    '4': {'city': 'Cincinnati', 'state': 'OH', 'dome': False},
    '5': {'city': 'Cleveland', 'state': 'OH', 'dome': False},
    '6': {'city': 'Arlington', 'state': 'TX', 'dome': True},
    '7': {'city': 'Denver', 'state': 'CO', 'dome': False},
    '8': {'city': 'Detroit', 'state': 'MI', 'dome': True},
    '9': {'city': 'Green Bay', 'state': 'WI', 'dome': False},
    '10': {'city': 'Nashville', 'state': 'TN', 'dome': False},
    '11': {'city': 'Indianapolis', 'state': 'IN', 'dome': True},
    '12': {'city': 'Kansas City', 'state': 'MO', 'dome': False},
    '13': {'city': 'Las Vegas', 'state': 'NV', 'dome': True},
    '14': {'city': 'Los Angeles', 'state': 'CA', 'dome': False},
    '15': {'city': 'Miami Gardens', 'state': 'FL', 'dome': False},
    '16': {'city': 'Minneapolis', 'state': 'MN', 'dome': True},
    '17': {'city': 'Foxborough', 'state': 'MA', 'dome': False},
    '18': {'city': 'New Orleans', 'state': 'LA', 'dome': True},
    '19': {'city': 'East Rutherford', 'state': 'NJ', 'dome': False},
    '20': {'city': 'East Rutherford', 'state': 'NJ', 'dome': False},
    '21': {'city': 'Philadelphia', 'state': 'PA', 'dome': False},
    '22': {'city': 'Glendale', 'state': 'AZ', 'dome': True},
    '23': {'city': 'Pittsburgh', 'state': 'PA', 'dome': False},
    '24': {'city': 'Los Angeles', 'state': 'CA', 'dome': False},
    '25': {'city': 'Santa Clara', 'state': 'CA', 'dome': False},
    '26': {'city': 'Seattle', 'state': 'WA', 'dome': False},
    '27': {'city': 'Tampa', 'state': 'FL', 'dome': False},
    '28': {'city': 'Landover', 'state': 'MD', 'dome': False},
    '29': {'city': 'Charlotte', 'state': 'NC', 'dome': False},
    '30': {'city': 'Jacksonville', 'state': 'FL', 'dome': False},
    '33': {'city': 'Baltimore', 'state': 'MD', 'dome': False},
    '34': {'city': 'Houston', 'state': 'TX', 'dome': True}
}