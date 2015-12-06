import goldsberry
import pandas as pd

players2014 = goldsberry.PlayerList(AllTime=True)
players2014 = pd.DataFrame(players2014)
print players2014.sample(10)
