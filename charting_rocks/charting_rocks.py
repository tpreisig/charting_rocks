import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise import ag_grid

from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf


companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

#Backend
class ChartState(rx.State):
  datetime_now: datetime = datetime.now()
  selected_rows: list[dict] | None = None
  data: pd.DataFrame
  company: str
  dict_data: list[dict] = [{}]
  dff_ticker_hist: list[dict] = []
  grid_theme: str = "alpine"
  themes: list[str] = ["quartz", "balham", "alpine", "material"]

  def fetch_data(self):
    self.datetime_now = datetime.now()
  
# Frontend
@rx.page("/", "Charting")
def charting_rocks() -> rx.Component:
  return rx.vstack(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.heading("📈📈 Charting Professionally for Fun", font_size="2em"),
            min_height="5vh",
        ),
        rx.hstack(
            rx.button("Fetch latest chart data", on_click=ChartState.fetch_data, color_scheme=rx.color_mode_cond(light="blue", dark="ruby")),
            margin_bottom="1em",
        ),
        rx.badge(rx.moment(ChartState.datetime_now), size="3"),
        rx.hstack(
            rx.text("Grid Theme ➡️ ", margin_top="4px"),
            rx.select(
                ChartState.themes,
                value=ChartState.grid_theme,
                on_change=ChartState.set_grid_theme,
                size="2"
            ),
            rx.text(
                "Click on a row to see the past 6 months of data for that company",
                margin_top="4px",
                color=rx.color_mode_cond(light="rgba(0, 0, 0, 0.5)", dark="rgba(255, 255, 255, 0.8)")
            ),
        ),
        direction="column",
        padding="2rem 1rem 0",
        border=f"2px solid {rx.color_mode_cond(light="rgba(0, 0, 0, 0.2)", dark="rgba(255, 255, 255, 0.4)")}",
        border_radius="5px",
        width="100%",
        overflow="hidden",
        height="100vh",
  )


app = rxe.App()



