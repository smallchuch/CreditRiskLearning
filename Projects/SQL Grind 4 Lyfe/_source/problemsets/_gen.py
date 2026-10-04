from . import P
PURPOSES = ['Purchase - Owner Occupied','Purchase - Investment','Refinance','Equity Release / Top-up','Construction','Internal Refinance']
EXT_PURPOSES = PURPOSES[:5]
CHANNELS = ['Broker','Branch','Digital','Mobile Lender']
STATES = ['NSW','VIC','QLD','SA','WA','TAS','NT','ACT']
YEARS = [2019,2020,2021,2022,2023,2024,2025]
LIVE = "snapshot_date = DATE '2025-12-31' AND loan_status <> 'Closed'"
def yr(col, y): return f"{col} >= DATE '{y}-01-01' AND {col} < DATE '{y+1}-01-01'"
LIVES = "s.snapshot_date = DATE '2025-12-31' AND s.loan_status <> 'Closed'"
