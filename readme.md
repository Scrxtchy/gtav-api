SocialClub-example-parser
=========================

Simple example parser for Rockstar's Social Club written in Python that makes use of [gta5-map/Social-Club-API-cheat-sheet](https://github.com/gta5-map/Social-Club-API-cheat-sheet).

## Installation

    * Download file and follow configuration instructions below
    * pip install bs4 requests

## Usage

```py
from GTA import gta
sc = gta()
```

## Example Output

```json
{
    "general": {
        "rank": 98,
        "xp": "1.5M RP",
        "playTime": "Play Time: 10d 7h 36m",
        "money": {
            "cash": 88,
            "bank": 1814204
        }
    },
    "crew": {
        "name": "Facepunch",
        "tag": "FAPS",
        "emblem": "https://prod.cloud.rockstargames.com/crews/sc/0831/1270/publish/emblem/emblem_64.png",
        "colour": "e81c1c"
    },
    "freemode": {
        "races": {
            "wins": 46,
            "losses": 143,
            "time": "17h 23m 33s"
        },
        "deathmatches": {
            "wins": 28,
            "losses": 20,
            "time": "8h 8m 58s"
        },
        "parachuting": {
            "wins": 0,
            "losses": 1,
            "time": "0"
        },
        "darts": {
            "wins": 0,
            "losses": 0,
            "time": "0"
        },
        "tennis": {
            "wins": 0,
            "losses": 0,
            "time": "0"
        },
        "golf": {
            "wins": 0,
            "losses": 0,
            "time": "No"
        }
    },
    "money": {
        "total": {
            "spent": "$12M",
            "earned": "$12.7M"
        },
        "earnedby": {
            "jobs": "$10.6M",
            "shared": "$1,256",
            "betting": "$62.1K",
            "car-sales": "$2,750",
            "picked-up": "$95.2K",
            "other": "$102K"
        }
    },
    "stats": {
        "stamina": 100.0,
        "stealth": 36.0,
        "lung-capacity": 14.0,
        "flying": 68.0,
        "shooting": 100.0,
        "strength": 29.0,
        "driving": 100.0,
        "mental-state": 21.0
    },
    "criminalrecord": {
        "cops-killed": 1191,
        "wanted-stars": 2658,
        "time-wanted": "13h 20m 13s",
        "stolen-vehicles": 629,
        "cars-exported": 5,
        "store-holdups": 17
    }
}
```

## Configuration

Create a `auth.txt` file in the root directory.  
the first line is your username  
the second line is your password  

```txt
gabelogannewell
hunter2
```

Login will also fail since it's not complete, thus by default does not signin
the work around currently is to copy these from your browser (use a cookie manager)  
and them import and save them, by default these last a month

```py
from GTA import gta
sc = gta()
sc.api.cookies.set('RSAuthCookie.v2', 'AUTHCOOKIE')
sc.api.cookies.set('RockStarWebSessionId', 'WEBSESSIONID')
sc.saveCookies()
```
All future logins will use these saved cookies