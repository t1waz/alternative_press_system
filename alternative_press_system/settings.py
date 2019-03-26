'''
How communication looks like:
        S - switchgear
        A-Z - status press 1
        Z-B - time   press 1
        B-Y - status press 2
        Y-C - time   press 2
        C-X - status press 3
        X-D - time   press 3
        D-W - status press 4
        W-E - time   press 4
        E-V - status press 5
        V-F - time   press 5
        F-U - status press 6
        U-L - time   press 6
'''
PRESSES_INFO = [['A', 'Z', 'B'],
				['B', 'Y', 'C'],
				['C', 'X', 'D'],
				['D', 'W', 'E'],
				['E', 'V', 'F'],
				['F', 'U', 'L']]

PRESS_STATE = ["READY",
			   "CLOSING",
			   "OPENING",
			   "PRESSING",
			   "OPEN"]

SWITCHGEAR_STATE = ["NONE",
					"PRESS 1",
					"PRESS 2",
					"PRESS 3",
					"PRESS 4",
					"PRESS 5",
					"PRESS 6",
					"SWITCHING"]

NUMBER_OF_PRESSES = 6

BACKEND_ACCESS_TOKEN = '123dupachujpietaszekalternativelongboardspiotrekkurwa'

BACKEND_URL = '178.183.151.29:5000'