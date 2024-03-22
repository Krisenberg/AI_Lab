from datetime import datetime, timedelta

MAX_DATE = datetime.strptime('02.03.2023 23:59:59','%d.%m.%Y %H:%M:%S')
MAX_CHANGES = 1000
TIME_CRITERIA = 't'
LINE_CHANGE_CRITERIA = 'p'
TIME_FOR_CHANGE = timedelta(minutes=1)
#0.2 safe option
TIME_HEURISTIC_AVG_FACTOR = 0.5
STEP_LIMIT = 30
OP_LIMIT = 10

# FILENAME = 'con_graph.csv'
FILENAME = 'connection_graph.csv'

# TEST NA factor:
# 1.03.2023, KRZYKI -> Swojczyce, godz. 7:24. Najpierw np factor = 0.7, potem factor = 5