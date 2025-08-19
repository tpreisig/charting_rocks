import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise import ag_grid

from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf


companies = ["EEPL", "NFLX", "META", "EMZN", "DRVA"]

#Backend
class ChartState(rx.State):
  datetime_now: datetime = datetime.now()
  company: str
  data: pd.DataFrame

def fetch_data(self):
  self.datetime_now = datetime.now()
  
# Frontend
@rx.page("/", "Charging")
def charting_rocks() -> rx.Component:
  return vstack(
    rx.text("Why stacking vertically or horizontally not so magnificient things? 🤷")
  )


app = rxe.App()



