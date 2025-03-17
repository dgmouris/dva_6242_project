// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default async function handler(req, res) {
  try {

    const { playerId } = req.query;

    // call the api
    const response = await fetch(`https://api-web.nhle.com/v1/player/${playerId}/landing`)
    const data = await response.json()

    res.status(200).json(data);

  } catch (error) {
    console.error('Error searching for jobs:', error);
    res.status(500).json({ error: 'An internal server error occurred' });
  }
}

/*
Sample Data returned

{
  "playerId": 8478402,
  "isActive": true,
  "currentTeamId": 22,
  "currentTeamAbbrev": "EDM",
  "fullTeamName": {
    "default": "Edmonton Oilers",
    "fr": "Oilers d'Edmonton"
  },
  "teamCommonName": {
    "default": "Oilers"
  },
  "teamPlaceNameWithPreposition": {
    "default": "Edmonton",
    "fr": "d'Edmonton"
  },
  "firstName": {
    "default": "Connor"
  },
  "lastName": {
    "default": "McDavid"
  },
  "badges": [
    {
      "logoUrl": {
        "default": "https://assets.nhle.com/badges/4n_face-off.svg",
        "fr": "https://assets.nhle.com/badges/4n_face-off_fr.svg"
      },
      "title": {
        "default": "4 Nations Face-Off",
        "fr": "Confrontation Des 4 Nations"
      }
    }
  ],
  "teamLogo": "https://assets.nhle.com/logos/nhl/svg/EDM_light.svg",
  "sweaterNumber": 97,
  "position": "C",
  "headshot": "https://assets.nhle.com/mugs/nhl/20242025/EDM/8478402.png",
  "heroImage": "https://assets.nhle.com/mugs/actionshots/1296x729/8478402.jpg",
  "heightInInches": 73,
  "heightInCentimeters": 185,
  "weightInPounds": 194,
  "weightInKilograms": 88,
  "birthDate": "1997-01-13",
  "birthCity": {
    "default": "Richmond Hill"
  },
  "birthStateProvince": {
    "default": "Ontario"
  },
  "birthCountry": "CAN",
  "shootsCatches": "L",
  "draftDetails": {
    "year": 2015,
    "teamAbbrev": "EDM",
    "round": 1,
    "pickInRound": 1,
    "overallPick": 1
  },
  "playerSlug": "connor-mcdavid-8478402",
  "inTop100AllTime": 0,
  "inHHOF": 0,
  "featuredStats": {
    "season": 20242025,
    "regularSeason": {
      "subSeason": {
        "assists": 56,
        "gameWinningGoals": 3,
        "gamesPlayed": 56,
        "goals": 23,
        "otGoals": 0,
        "pim": 29,
        "plusMinus": 1,
        "points": 79,
        "powerPlayGoals": 9,
        "powerPlayPoints": 28,
        "shootingPctg": 0.132948,
        "shorthandedGoals": 0,
        "shorthandedPoints": 0,
        "shots": 173
      },
      "career": {
        "assists": 703,
        "gameWinningGoals": 72,
        "gamesPlayed": 701,
        "goals": 358,
        "otGoals": 16,
        "pim": 278,
        "plusMinus": 150,
        "points": 1061,
        "powerPlayGoals": 87,
        "powerPlayPoints": 361,
        "shootingPctg": 0.1501,
        "shorthandedGoals": 8,
        "shorthandedPoints": 17,
        "shots": 2384
      }
    }
  },
  "careerTotals": {
    "regularSeason": {
      "assists": 703,
      "avgToi": "21:44",
      "faceoffWinningPctg": 0.4778,
      "gameWinningGoals": 72,
      "gamesPlayed": 701,
      "goals": 358,
      "otGoals": 16,
      "pim": 278,
      "plusMinus": 150,
      "points": 1061,
      "powerPlayGoals": 87,
      "powerPlayPoints": 361,
      "shootingPctg": 0.1501,
      "shorthandedGoals": 8,
      "shorthandedPoints": 17,
      "shots": 2384
    },
    "playoffs": {
      "assists": 80,
      "avgToi": "23:24",
      "faceoffWinningPctg": 0.4496,
      "gameWinningGoals": 3,
      "gamesPlayed": 74,
      "goals": 37,
      "otGoals": 2,
      "pim": 24,
      "plusMinus": 28,
      "points": 117,
      "powerPlayGoals": 13,
      "powerPlayPoints": 47,
      "shootingPctg": 0.148,
      "shorthandedGoals": 2,
      "shorthandedPoints": 3,
      "shots": 250
    }
  },
  "shopLink": "#TODO",
  "twitterLink": "#TODO",
  "watchLink": "#TODO",
  "last5Games": [
    {
      "assists": 2,
      "gameDate": "2025-03-06",
      "gameId": 2024020995,
      "gameTypeId": 2,
      "goals": 0,
      "homeRoadFlag": "H",
      "opponentAbbrev": "MTL",
      "pim": 0,
      "plusMinus": 0,
      "points": 2,
      "powerPlayGoals": 0,
      "shifts": 25,
      "shorthandedGoals": 0,
      "shots": 3,
      "teamAbbrev": "EDM",
      "toi": "26:58"
    },
    {
      "assists": 1,
      "gameDate": "2025-03-04",
      "gameId": 2024020981,
      "gameTypeId": 2,
      "goals": 1,
      "homeRoadFlag": "H",
      "opponentAbbrev": "ANA",
      "pim": 0,
      "plusMinus": -2,
      "points": 2,
      "powerPlayGoals": 1,
      "shifts": 21,
      "shorthandedGoals": 0,
      "shots": 5,
      "teamAbbrev": "EDM",
      "toi": "21:59"
    },
    {
      "assists": 1,
      "gameDate": "2025-03-01",
      "gameId": 2024020955,
      "gameTypeId": 2,
      "goals": 0,
      "homeRoadFlag": "R",
      "opponentAbbrev": "CAR",
      "pim": 0,
      "plusMinus": 0,
      "points": 1,
      "powerPlayGoals": 0,
      "shifts": 23,
      "shorthandedGoals": 0,
      "shots": 4,
      "teamAbbrev": "EDM",
      "toi": "24:42"
    },
    {
      "assists": 1,
      "gameDate": "2025-02-27",
      "gameId": 2024020937,
      "gameTypeId": 2,
      "goals": 0,
      "homeRoadFlag": "R",
      "opponentAbbrev": "FLA",
      "pim": 0,
      "plusMinus": 0,
      "points": 1,
      "powerPlayGoals": 0,
      "shifts": 23,
      "shorthandedGoals": 0,
      "shots": 2,
      "teamAbbrev": "EDM",
      "toi": "22:46"
    },
    {
      "assists": 1,
      "gameDate": "2025-02-25",
      "gameId": 2024020921,
      "gameTypeId": 2,
      "goals": 0,
      "homeRoadFlag": "R",
      "opponentAbbrev": "TBL",
      "pim": 0,
      "plusMinus": -1,
      "points": 1,
      "powerPlayGoals": 0,
      "shifts": 22,
      "shorthandedGoals": 0,
      "shots": 2,
      "teamAbbrev": "EDM",
      "toi": "20:30"
    }
  ],
  "seasonTotals": [
    {
      "assists": 7,
      "gameTypeId": 2,
      "gamesPlayed": 7,
      "goals": 7,
      "leagueAbbrev": "QC Int PW",
      "pim": 0,
      "points": 14,
      "season": 20082009,
      "sequence": 315272,
      "teamName": {
        "default": "York Simcoe Peewee"
      }
    },
    {
      "assists": 50,
      "gameTypeId": 2,
      "gamesPlayed": 33,
      "goals": 27,
      "leagueAbbrev": "GTHL",
      "points": 77,
      "season": 20112012,
      "sequence": 1,
      "teamName": {
        "default": "Tor. Marlboros"
      }
    },
    {
      "assists": 65,
      "gameTypeId": 2,
      "gamesPlayed": 41,
      "goals": 41,
      "leagueAbbrev": "Other",
      "points": 106,
      "season": 20112012,
      "sequence": 2,
      "teamName": {
        "default": "Tor. Marlboros"
      }
    },
    {
      "assists": 32,
      "gameTypeId": 2,
      "gamesPlayed": 17,
      "goals": 31,
      "leagueAbbrev": "Other",
      "points": 63,
      "season": 20112012,
      "sequence": 3,
      "teamName": {
        "default": "PEAC"
      }
    },
    {
      "assists": 15,
      "gameTypeId": 3,
      "gamesPlayed": 14,
      "goals": 11,
      "leagueAbbrev": "GTHL",
      "points": 26,
      "season": 20112012,
      "sequence": 1,
      "teamName": {
        "default": "Tor. Marlboros"
      }
    },
    {
      "assists": 41,
      "gameTypeId": 2,
      "gameWinningGoals": 2,
      "gamesPlayed": 63,
      "goals": 25,
      "leagueAbbrev": "OHL",
      "pim": 36,
      "plusMinus": -24,
      "points": 66,
      "powerPlayGoals": 2,
      "season": 20122013,
      "sequence": 1,
      "shorthandedGoals": 1,
      "teamName": {
        "default": "Erie"
      }
    },
    {
      "assists": 6,
      "gameTypeId": 2,
      "gameWinningGoals": 2,
      "gamesPlayed": 7,
      "goals": 8,
      "leagueAbbrev": "WJ18-A",
      "pim": 2,
      "points": 14,
      "powerPlayGoals": 5,
      "season": 20122013,
      "sequence": 2,
      "shorthandedGoals": 0,
      "shots": 23,
      "teamCommonName": {
        "default": "Canada",
        "cs": "Kanada",
        "de": "Kanada",
        "es": "Canadá",
        "fi": "Kanada",
        "sk": "Kanada",
        "sv": "Kanada"
      },
      "teamName": {
        "default": "Canada",
        "cs": "Kanada",
        "de": "Kanada",
        "fi": "Kanada",
        "sk": "Kanada",
        "sv": "Kanada"
      },
      "teamPlaceNameWithPreposition": {
        "default": "  "
      }
    },
    {
      "assists": 71,
      "gameTypeId": 2,
      "gameWinningGoals": 4,
      "gamesPlayed": 56,
      "goals": 28,
      "leagueAbbrev": "OHL",
      "pim": 20,
      "plusMinus": 47,
      "points": 99,
      "powerPlayGoals": 7,
      "season": 20132014,
      "sequence": 1,
      "shorthandedGoals": 2,
      "teamName": {
        "default": "Erie"
      }
    },
    {
      "assists": 15,
      "gameTypeId": 3,
      "gamesPlayed": 14,
      "goals": 4,
      "leagueAbbrev": "OHL",
      "pim": 2,
      "plusMinus": -1,
      "points": 19,
      "powerPlayGoals": 0,
      "season": 20132014,
      "sequence": 1,
      "shorthandedGoals": 0,
      "teamName": {
        "default": "Erie"
      }
    },
    {
      "assists": 76,
      "gameTypeId": 2,
      "gameWinningGoals": 8,
      "gamesPlayed": 47,
      "goals": 44,
      "leagueAbbrev": "OHL",
      "pim": 48,
      "plusMinus": 60,
      "points": 120,
      "powerPlayGoals": 9,
      "season": 20142015,
      "sequence": 1,
      "shorthandedGoals": 2,
      "teamName": {
        "default": "Erie"
      }
    },
    {
      "assists": 8,
      "gameTypeId": 2,
      "gameWinningGoals": 1,
      "gamesPlayed": 7,
      "goals": 3,
      "leagueAbbrev": "WJC-A",
      "pim": 0,
      "plusMinus": 8,
      "points": 11,
      "powerPlayGoals": 1,
      "season": 20142015,
      "sequence": 2,
      "shorthandedGoals": 0,
      "shots": 21,
      "teamCommonName": {
        "default": "Canada",
        "cs": "Kanada",
        "de": "Kanada",
        "es": "Canadá",
        "fi": "Kanada",
        "sk": "Kanada",
        "sv": "Kanada"
      },
      "teamName": {
        "default": "Canada",
        "cs": "Kanada",
        "de": "Kanada",
        "fi": "Kanada",
        "sk": "Kanada",
        "sv": "Kanada"
      },
      "teamPlaceNameWithPreposition": {
        "default": "  "
      }
    },
    {
      "assists": 28,
      "gameTypeId": 3,
      "gameWinningGoals": 5,
      "gamesPlayed": 20,
      "goals": 21,
      "leagueAbbrev": "OHL",
      "pim": 12,
      "plusMinus": 12,
      "points": 49,
      "powerPlayGoals": 4,
      "season": 20142015,
      "sequence": 1,
      "shorthandedGoals": 3,
      "teamName": {
        "default": "Erie"
      }
    },
    {
      "assists": 32,
      "avgToi": "18:53",
      "faceoffWinningPctg": 0.4123,
      "gameTypeId": 2,
      "gameWinningGoals": 5,
      "gamesPlayed": 45,
      "goals": 16,
      "leagueAbbrev": "NHL",
      "otGoals": 1,
      "pim": 18,
      "plusMinus": -1,
      "points": 48,
      "powerPlayGoals": 3,
      "powerPlayPoints": 14,
      "season": 20152016,
      "sequence": 1,
      "shootingPctg": 0.1524,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 105,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 8,
      "gameTypeId": 2,
      "gameWinningGoals": 1,
      "gamesPlayed": 10,
      "goals": 1,
      "leagueAbbrev": "WC-A",
      "pim": 6,
      "plusMinus": 3,
      "points": 9,
      "powerPlayGoals": 0,
      "season": 20152016,
      "sequence": 2,
      "shorthandedGoals": 0,
      "shots": 15,
      "teamCommonName": {
        "default": "Canada",
        "cs": "Kanada",
        "de": "Kanada",
        "es": "Canadá",
        "fi": "Kanada",
        "sk": "Kanada",
        "sv": "Kanada"
      },
      "teamName": {
        "default": "Canada",
        "cs": "Kanada",
        "de": "Kanada",
        "fi": "Kanada",
        "sk": "Kanada",
        "sv": "Kanada"
      },
      "teamPlaceNameWithPreposition": {
        "default": "  "
      }
    },
    {
      "assists": 70,
      "avgToi": "21:08",
      "faceoffWinningPctg": 0.4318,
      "gameTypeId": 2,
      "gameWinningGoals": 6,
      "gamesPlayed": 82,
      "goals": 30,
      "leagueAbbrev": "NHL",
      "otGoals": 1,
      "pim": 26,
      "plusMinus": 27,
      "points": 100,
      "powerPlayGoals": 3,
      "powerPlayPoints": 27,
      "season": 20162017,
      "sequence": 1,
      "shootingPctg": 0.1195,
      "shorthandedGoals": 1,
      "shorthandedPoints": 2,
      "shots": 251,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 3,
      "gameTypeId": 2,
      "gamesPlayed": 3,
      "goals": 0,
      "leagueAbbrev": "WCup",
      "pim": 4,
      "plusMinus": 1,
      "points": 3,
      "season": 20162017,
      "sequence": 176776,
      "teamName": {
        "default": "Team North America"
      }
    },
    {
      "assists": 4,
      "avgToi": "22:25",
      "faceoffWinningPctg": 0.3578,
      "gameTypeId": 3,
      "gameWinningGoals": 0,
      "gamesPlayed": 13,
      "goals": 5,
      "leagueAbbrev": "NHL",
      "otGoals": 0,
      "pim": 2,
      "plusMinus": 3,
      "points": 9,
      "powerPlayGoals": 1,
      "powerPlayPoints": 4,
      "season": 20162017,
      "sequence": 1,
      "shootingPctg": 0.1351,
      "shorthandedGoals": 1,
      "shorthandedPoints": 1,
      "shots": 37,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 67,
      "avgToi": "21:33",
      "faceoffWinningPctg": 0.4136,
      "gameTypeId": 2,
      "gameWinningGoals": 7,
      "gamesPlayed": 82,
      "goals": 41,
      "leagueAbbrev": "NHL",
      "otGoals": 2,
      "pim": 26,
      "plusMinus": 20,
      "points": 108,
      "powerPlayGoals": 5,
      "powerPlayPoints": 20,
      "season": 20172018,
      "sequence": 1,
      "shootingPctg": 0.1496,
      "shorthandedGoals": 1,
      "shorthandedPoints": 4,
      "shots": 274,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 12,
      "gameTypeId": 2,
      "gamesPlayed": 10,
      "goals": 5,
      "leagueAbbrev": "WC",
      "pim": 10,
      "plusMinus": 6,
      "points": 17,
      "season": 20172018,
      "sequence": 17155,
      "teamName": {
        "default": "Canada"
      }
    },
    {
      "assists": 75,
      "avgToi": "22:50",
      "faceoffWinningPctg": 0.4662,
      "gameTypeId": 2,
      "gameWinningGoals": 9,
      "gamesPlayed": 78,
      "goals": 41,
      "leagueAbbrev": "NHL",
      "otGoals": 3,
      "pim": 20,
      "plusMinus": 3,
      "points": 116,
      "powerPlayGoals": 9,
      "powerPlayPoints": 33,
      "season": 20182019,
      "sequence": 1,
      "shootingPctg": 0.1708,
      "shorthandedGoals": 1,
      "shorthandedPoints": 2,
      "shots": 240,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 63,
      "avgToi": "21:52",
      "faceoffWinningPctg": 0.4776,
      "gameTypeId": 2,
      "gameWinningGoals": 6,
      "gamesPlayed": 64,
      "goals": 34,
      "leagueAbbrev": "NHL",
      "otGoals": 0,
      "pim": 28,
      "plusMinus": -6,
      "points": 97,
      "powerPlayGoals": 11,
      "powerPlayPoints": 43,
      "season": 20192020,
      "sequence": 1,
      "shootingPctg": 0.16,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 212,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 4,
      "avgToi": "22:23",
      "faceoffWinningPctg": 0.431,
      "gameTypeId": 3,
      "gameWinningGoals": 1,
      "gamesPlayed": 4,
      "goals": 5,
      "leagueAbbrev": "NHL",
      "otGoals": 0,
      "pim": 2,
      "plusMinus": 1,
      "points": 9,
      "powerPlayGoals": 3,
      "powerPlayPoints": 5,
      "season": 20192020,
      "sequence": 1,
      "shootingPctg": 0.455,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 11,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 72,
      "avgToi": "22:09",
      "faceoffWinningPctg": 0.4953,
      "gameTypeId": 2,
      "gameWinningGoals": 11,
      "gamesPlayed": 56,
      "goals": 33,
      "leagueAbbrev": "NHL",
      "otGoals": 2,
      "pim": 20,
      "plusMinus": 21,
      "points": 105,
      "powerPlayGoals": 9,
      "powerPlayPoints": 37,
      "season": 20202021,
      "sequence": 1,
      "shootingPctg": 0.165,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 200,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 3,
      "avgToi": "30:24",
      "faceoffWinningPctg": 0.4524,
      "gameTypeId": 3,
      "gameWinningGoals": 0,
      "gamesPlayed": 4,
      "goals": 1,
      "leagueAbbrev": "NHL",
      "otGoals": 0,
      "pim": 0,
      "plusMinus": -2,
      "points": 4,
      "powerPlayGoals": 0,
      "powerPlayPoints": 1,
      "season": 20202021,
      "sequence": 1,
      "shootingPctg": 0.067,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 15,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 79,
      "avgToi": "22:04",
      "faceoffWinningPctg": 0.537285,
      "gameTypeId": 2,
      "gameWinningGoals": 9,
      "gamesPlayed": 80,
      "goals": 44,
      "leagueAbbrev": "NHL",
      "otGoals": 4,
      "pim": 45,
      "plusMinus": 28,
      "points": 123,
      "powerPlayGoals": 10,
      "powerPlayPoints": 44,
      "season": 20212022,
      "sequence": 1,
      "shootingPctg": 0.14,
      "shorthandedGoals": 0,
      "shorthandedPoints": 1,
      "shots": 314,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 23,
      "avgToi": "23:02",
      "faceoffWinningPctg": 0.525714,
      "gameTypeId": 3,
      "gameWinningGoals": 1,
      "gamesPlayed": 16,
      "goals": 10,
      "leagueAbbrev": "NHL",
      "otGoals": 1,
      "pim": 10,
      "plusMinus": 15,
      "points": 33,
      "powerPlayGoals": 2,
      "powerPlayPoints": 8,
      "season": 20212022,
      "sequence": 1,
      "shootingPctg": 0.164,
      "shorthandedGoals": 0,
      "shorthandedPoints": 1,
      "shots": 61,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 89,
      "avgToi": "22:23",
      "faceoffWinningPctg": 0.519288,
      "gameTypeId": 2,
      "gameWinningGoals": 11,
      "gamesPlayed": 82,
      "goals": 64,
      "leagueAbbrev": "NHL",
      "otGoals": 2,
      "pim": 36,
      "plusMinus": 22,
      "points": 153,
      "powerPlayGoals": 21,
      "powerPlayPoints": 71,
      "season": 20222023,
      "sequence": 1,
      "shootingPctg": 0.181818,
      "shorthandedGoals": 4,
      "shorthandedPoints": 7,
      "shots": 352,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 12,
      "avgToi": "23:43",
      "faceoffWinningPctg": 0.483444,
      "gameTypeId": 3,
      "gameWinningGoals": 0,
      "gamesPlayed": 12,
      "goals": 8,
      "leagueAbbrev": "NHL",
      "otGoals": 0,
      "pim": 0,
      "plusMinus": -1,
      "points": 20,
      "powerPlayGoals": 5,
      "powerPlayPoints": 12,
      "season": 20222023,
      "sequence": 1,
      "shootingPctg": 0.156863,
      "shorthandedGoals": 1,
      "shorthandedPoints": 1,
      "shots": 51,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 100,
      "avgToi": "21:22",
      "faceoffWinningPctg": 0.510983,
      "gameTypeId": 2,
      "gameWinningGoals": 5,
      "gamesPlayed": 76,
      "goals": 32,
      "leagueAbbrev": "NHL",
      "otGoals": 1,
      "pim": 30,
      "plusMinus": 35,
      "points": 132,
      "powerPlayGoals": 7,
      "powerPlayPoints": 44,
      "season": 20232024,
      "sequence": 1,
      "shootingPctg": 0.121673,
      "shorthandedGoals": 1,
      "shorthandedPoints": 1,
      "shots": 263,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 34,
      "avgToi": "23:02",
      "faceoffWinningPctg": 0.427729,
      "gameTypeId": 3,
      "gameWinningGoals": 1,
      "gamesPlayed": 25,
      "goals": 8,
      "leagueAbbrev": "NHL",
      "otGoals": 1,
      "pim": 10,
      "plusMinus": 12,
      "points": 42,
      "powerPlayGoals": 2,
      "powerPlayPoints": 17,
      "season": 20232024,
      "sequence": 1,
      "shootingPctg": 0.106667,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 75,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 56,
      "avgToi": "22:14",
      "faceoffWinningPctg": 0.481366,
      "gameTypeId": 2,
      "gameWinningGoals": 3,
      "gamesPlayed": 56,
      "goals": 23,
      "leagueAbbrev": "NHL",
      "otGoals": 0,
      "pim": 29,
      "plusMinus": 1,
      "points": 79,
      "powerPlayGoals": 9,
      "powerPlayPoints": 28,
      "season": 20242025,
      "sequence": 1,
      "shootingPctg": 0.132948,
      "shorthandedGoals": 0,
      "shorthandedPoints": 0,
      "shots": 173,
      "teamCommonName": {
        "default": "Oilers"
      },
      "teamName": {
        "default": "Edmonton Oilers",
        "fr": "Oilers d'Edmonton"
      },
      "teamPlaceNameWithPreposition": {
        "default": "Edmonton",
        "fr": "d'Edmonton"
      }
    },
    {
      "assists": 2,
      "avgToi": "44:10",
      "faceoffWinningPctg": 0.7,
      "gameTypeId": 2,
      "gameWinningGoals": 0,
      "gamesPlayed": 4,
      "goals": 3,
      "leagueAbbrev": "4 Nations",
      "otGoals": 0,
      "pim": 0,
      "plusMinus": -1,
      "points": 5,
      "powerPlayGoals": 0,
      "season": 20242025,
      "sequence": 44,
      "shootingPctg": 0.25,
      "shorthandedGoals": 0,
      "shots": 4,
      "teamName": {
        "default": "Canada"
      }
    }
  ],
  "awards": [
    {
      "trophy": {
        "default": "Art Ross Trophy",
        "fr": "Trophée Art Ross"
      },
      "seasons": [
        {
          "assists": 89,
          "blockedShots": 40,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 64,
          "hits": 89,
          "pim": 36,
          "plusMinus": 22,
          "points": 153,
          "seasonId": 20222023
        },
        {
          "assists": 79,
          "blockedShots": 26,
          "gameTypeId": 2,
          "gamesPlayed": 80,
          "goals": 44,
          "hits": 75,
          "pim": 45,
          "plusMinus": 28,
          "points": 123,
          "seasonId": 20212022
        },
        {
          "assists": 72,
          "blockedShots": 24,
          "gameTypeId": 2,
          "gamesPlayed": 56,
          "goals": 33,
          "hits": 61,
          "pim": 20,
          "plusMinus": 21,
          "points": 105,
          "seasonId": 20202021
        },
        {
          "assists": 67,
          "blockedShots": 46,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 41,
          "hits": 28,
          "pim": 26,
          "plusMinus": 20,
          "points": 108,
          "seasonId": 20172018
        },
        {
          "assists": 70,
          "blockedShots": 29,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 30,
          "hits": 34,
          "pim": 26,
          "plusMinus": 27,
          "points": 100,
          "seasonId": 20162017
        }
      ]
    },
    {
      "trophy": {
        "default": "Conn Smythe Trophy",
        "fr": "Trophée Conn Smythe"
      },
      "seasons": [
        {
          "assists": 34,
          "blockedShots": 16,
          "gameTypeId": 3,
          "gamesPlayed": 25,
          "goals": 8,
          "hits": 43,
          "pim": 10,
          "plusMinus": 12,
          "points": 42,
          "seasonId": 20232024
        }
      ]
    },
    {
      "trophy": {
        "default": "Hart Memorial Trophy",
        "fr": "Trophée Hart"
      },
      "seasons": [
        {
          "assists": 89,
          "blockedShots": 40,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 64,
          "hits": 89,
          "pim": 36,
          "plusMinus": 22,
          "points": 153,
          "seasonId": 20222023
        },
        {
          "assists": 72,
          "blockedShots": 24,
          "gameTypeId": 2,
          "gamesPlayed": 56,
          "goals": 33,
          "hits": 61,
          "pim": 20,
          "plusMinus": 21,
          "points": 105,
          "seasonId": 20202021
        },
        {
          "assists": 70,
          "blockedShots": 29,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 30,
          "hits": 34,
          "pim": 26,
          "plusMinus": 27,
          "points": 100,
          "seasonId": 20162017
        }
      ]
    },
    {
      "trophy": {
        "default": "Maurice “Rocket” Richard Trophy"
      },
      "seasons": [
        {
          "assists": 89,
          "blockedShots": 40,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 64,
          "hits": 89,
          "pim": 36,
          "plusMinus": 22,
          "points": 153,
          "seasonId": 20222023
        }
      ]
    },
    {
      "trophy": {
        "default": "Ted Lindsay Award",
        "fr": "Trophée Ted Lindsay"
      },
      "seasons": [
        {
          "assists": 89,
          "blockedShots": 40,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 64,
          "hits": 89,
          "pim": 36,
          "plusMinus": 22,
          "points": 153,
          "seasonId": 20222023
        },
        {
          "assists": 72,
          "blockedShots": 24,
          "gameTypeId": 2,
          "gamesPlayed": 56,
          "goals": 33,
          "hits": 61,
          "pim": 20,
          "plusMinus": 21,
          "points": 105,
          "seasonId": 20202021
        },
        {
          "assists": 67,
          "blockedShots": 46,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 41,
          "hits": 28,
          "pim": 26,
          "plusMinus": 20,
          "points": 108,
          "seasonId": 20172018
        },
        {
          "assists": 70,
          "blockedShots": 29,
          "gameTypeId": 2,
          "gamesPlayed": 82,
          "goals": 30,
          "hits": 34,
          "pim": 26,
          "plusMinus": 27,
          "points": 100,
          "seasonId": 20162017
        }
      ]
    }
  ],
  "currentTeamRoster": [
    {
      "playerId": 8478042,
      "lastName": {
        "default": "Arvidsson"
      },
      "firstName": {
        "default": "Viktor"
      },
      "playerSlug": "viktor-arvidsson-8478042"
    },
    {
      "playerId": 8480803,
      "lastName": {
        "default": "Bouchard"
      },
      "firstName": {
        "default": "Evan"
      },
      "playerSlug": "evan-bouchard-8480803"
    },
    {
      "playerId": 8477015,
      "lastName": {
        "default": "Brown"
      },
      "firstName": {
        "default": "Connor"
      },
      "playerSlug": "connor-brown-8477015"
    },
    {
      "playerId": 8477934,
      "lastName": {
        "default": "Draisaitl"
      },
      "firstName": {
        "default": "Leon"
      },
      "playerSlug": "leon-draisaitl-8477934"
    },
    {
      "playerId": 8475218,
      "lastName": {
        "default": "Ekholm"
      },
      "firstName": {
        "default": "Mattias"
      },
      "playerSlug": "mattias-ekholm-8475218"
    },
    {
      "playerId": 8480834,
      "lastName": {
        "default": "Emberson"
      },
      "firstName": {
        "default": "Ty"
      },
      "playerSlug": "ty-emberson-8480834"
    },
    {
      "playerId": 8479365,
      "lastName": {
        "default": "Frederic"
      },
      "firstName": {
        "default": "Trent"
      },
      "playerSlug": "trent-frederic-8479365"
    },
    {
      "playerId": 8474641,
      "lastName": {
        "default": "Henrique"
      },
      "firstName": {
        "default": "Adam"
      },
      "playerSlug": "adam-henrique-8474641"
    },
    {
      "playerId": 8475786,
      "lastName": {
        "default": "Hyman"
      },
      "firstName": {
        "default": "Zach"
      },
      "playerSlug": "zach-hyman-8475786"
    },
    {
      "playerId": 8477406,
      "lastName": {
        "default": "Janmark"
      },
      "firstName": {
        "default": "Mattias"
      },
      "playerSlug": "mattias-janmark-8477406"
    },
    {
      "playerId": 8479368,
      "lastName": {
        "default": "Jones"
      },
      "firstName": {
        "default": "Max"
      },
      "playerSlug": "max-jones-8479368"
    },
    {
      "playerId": 8477953,
      "lastName": {
        "default": "Kapanen"
      },
      "firstName": {
        "default": "Kasperi"
      },
      "playerSlug": "kasperi-kapanen-8477953"
    },
    {
      "playerId": 8475906,
      "lastName": {
        "default": "Klingberg"
      },
      "firstName": {
        "default": "John"
      },
      "playerSlug": "john-klingberg-8475906"
    },
    {
      "playerId": 8476967,
      "lastName": {
        "default": "Kulak"
      },
      "firstName": {
        "default": "Brett"
      },
      "playerSlug": "brett-kulak-8476967"
    },
    {
      "playerId": 8478402,
      "lastName": {
        "default": "McDavid"
      },
      "firstName": {
        "default": "Connor"
      },
      "playerSlug": "connor-mcdavid-8478402"
    },
    {
      "playerId": 8476454,
      "lastName": {
        "default": "Nugent-Hopkins"
      },
      "firstName": {
        "default": "Ryan"
      },
      "playerSlug": "ryan-nugent-hopkins-8476454"
    },
    {
      "playerId": 8477498,
      "lastName": {
        "default": "Nurse"
      },
      "firstName": {
        "default": "Darnell"
      },
      "playerSlug": "darnell-nurse-8477498"
    },
    {
      "playerId": 8470621,
      "lastName": {
        "default": "Perry"
      },
      "firstName": {
        "default": "Corey"
      },
      "playerSlug": "corey-perry-8470621"
    },
    {
      "playerId": 8475717,
      "lastName": {
        "default": "Pickard"
      },
      "firstName": {
        "default": "Calvin"
      },
      "playerSlug": "calvin-pickard-8475717"
    },
    {
      "playerId": 8481617,
      "lastName": {
        "default": "Podkolzin"
      },
      "firstName": {
        "default": "Vasily",
        "cs": "Vasilij",
        "fi": "Vasili",
        "sk": "Vasilij"
      },
      "playerSlug": "vasily-podkolzin-8481617"
    },
    {
      "playerId": 8475784,
      "lastName": {
        "default": "Skinner"
      },
      "firstName": {
        "default": "Jeff"
      },
      "playerSlug": "jeff-skinner-8475784"
    },
    {
      "playerId": 8479973,
      "lastName": {
        "default": "Skinner"
      },
      "firstName": {
        "default": "Stuart"
      },
      "playerSlug": "stuart-skinner-8479973"
    },
    {
      "playerId": 8479442,
      "lastName": {
        "default": "Stecher"
      },
      "firstName": {
        "default": "Troy"
      },
      "playerSlug": "troy-stecher-8479442"
    },
    {
      "playerId": 8478013,
      "lastName": {
        "default": "Walman"
      },
      "firstName": {
        "default": "Jake"
      },
      "playerSlug": "jake-walman-8478013"
    }
  ]
}

*/
