'''
How communication looks like:
        S - switchgear
        A-Z - status press 1 (value beetween two charts)
        Z-B - time   press 1 (value beetween two charts)
        B-Y - status press 2 (value beetween two charts)
        Y-C - time   press 2 (value beetween two charts)
        C-X - status press 3 (value beetween two charts)
        X-D - time   press 3 (value beetween two charts)
        D-W - status press 4 (value beetween two charts)
        W-E - time   press 4 (value beetween two charts)
        E-V - status press 5 (value beetween two charts)
        V-F - time   press 5 (value beetween two charts)
        F-U - status press 6 (value beetween two charts)
        U-L - time   press 6 (value beetween two charts)
'''
PRESSES_INFO = [['A', 'Z', 'B'],
                ['B', 'Y', 'C'],
                ['C', 'X', 'D'],
                ['D', 'W', 'E'],
                ['E', 'V', 'F'],
                ['F', 'U', 'L']]

PRESS_STATE = {
    "0": "READY",
    "1": "CLOSING",
    "2": "OPENING",
    "3": "PRESSING",
    "4": "OPEN"
}

SWITCHGEAR_STATE = {
    "0": "NONE",
    "1": "PRESS 1",
    "2": "PRESS 2",
    "3": "PRESS 3",
    "4": "PRESS 4",
    "5": "PRESS 5",
    "6": "PRESS 6",
    "7": "SWITCHING"
}

NUMBER_OF_PRESSES = 6

BACKEND_ACCESS_TOKEN = '123dupachujpietaszekalternativelongboardspiotrekkurwa'

BACKEND_URL = '178.183.151.29:5000'

PRESSES = [
    {
        "name": "A",
        "mold": "Fantail",
        "press_time": 7200,
    },
    {
        "name": "B",
        "mold": "Ostrich",
        "press_time": 7200,
    },
    {
        "name": "C",
        "mold": "Karoo",
        "press_time": 7200,
    },
    {
        "name": "D",
        "mold": "Flamingo",
        "press_time": 7200,
    },
    {
        "name": "E",
        "mold": "Erget",
        "press_time": 7200,
    },
    {
        "name": "F",
        "mold": "Chauma M",
        "press_time": 7200,
    },        
]
