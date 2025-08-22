import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise import ag_grid

from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf


companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA"]

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
    self.selected_rows = None
    self.datetime_now = datetime.now()
    start_date = self.datetime_now - timedelta(days=180)
    
    self.data = yf.download(
            companies,
            start=start_date,
            end=self.datetime_now,
            group_by="ticker",
    )
    rows = []
    for ticker in companies:
                if isinstance(self.data.columns, pd.MultiIndex):
                    ticker_data = self.data[
                        ticker
                    ]  # Select the data for the current ticker
                else:
                    ticker_data = (
                        self.data
                    )  # If only one ticker, no multi-level index exists

                for date, row in ticker_data.iterrows():
                    rows.append(
                        {
                            "ticker": ticker,
                            "date": date.strftime("%Y-%m-%d"),
                            "open": round(row["Open"], 2),
                            "high": round(row["High"], 2),
                            "mid": round((row["High"] + row["Low"]) / 2, 2),
                            "low": round(row["Low"], 2),
                            "close": round(row["Close"], 2),
                            "volume": int(row["Volume"]),
                        }
                    )
                self.dict_data = sorted(
                    rows, key=lambda x: (x["date"], x["ticker"]), reverse=True
                )


  def handle_selection(self, selected_rows, _, __):
      self.selected_rows = selected_rows
      self.update_line_graph()

  def update_line_graph(self):
      if self.selected_rows:
          ticker = self.selected_rows[0]["ticker"]
      else:
          self.dff_ticker_hist = []
          return
      self.company = ticker

      dff_ticker_hist = self.data[ticker].reset_index()
      dff_ticker_hist["Date"] = pd.to_datetime(dff_ticker_hist["Date"]).dt.strftime(
          "%Y-%m-%d"
      )

      dff_ticker_hist["Mid"] = (
          dff_ticker_hist["Open"] + dff_ticker_hist["Close"]
      ) / 2
      dff_ticker_hist["DayDifference"] = dff_ticker_hist.apply(
          lambda row: [row["High"] - row["Mid"], row["Mid"] - row["Low"]], axis=1
      )

      self.dff_ticker_hist = dff_ticker_hist.to_dict(orient="records")                


column_defs = [
    ag_grid.column_def(
        field="ticker",
        header_name="Ticker",
        filter=ag_grid.filters.text,
        checkbox_selection=True,
    ),
    ag_grid.column_def(field="date", header_name="Date", filter=ag_grid.filters.date),
    ag_grid.column_def(field="open", header_name="Open", filter=ag_grid.filters.number),
    ag_grid.column_def(field="high", header_name="High", filter=ag_grid.filters.number),
    ag_grid.column_def(field="low", header_name="Low", filter=ag_grid.filters.number),
    ag_grid.column_def(
            ield="close", header_name="Close", filter=ag_grid.filters.number
    ),
    ag_grid.column_def(
        field="volume", header_name="Volume", filter=ag_grid.filters.number
    ),
]
    
  
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
        rx.cond(
            ChartState.dff_ticker_hist,
            rx.vstack(
                rx.heading(ChartState.company),
                rx.recharts.line_chart(
                    rx.recharts.line(
                        rx.recharts.error_bar(
                            data_key="DayDifference",
                            direction="y",
                            width=4,
                            stroke_width=2,
                            stroke="red",
                        ),
                        data_key="Mid",
                    ),
                    rx.recharts.x_axis(data_key="Date"),
                    rx.recharts.y_axis(domain=["auto", "auto"]),
                    data=ChartState.dff_ticker_hist,
                    width="100%",
                    height=300,
                ),
                align_items="center",
                width="100%",
            ),
        ),
        ag_grid(
            id="myAgGrid",
            column_defs=column_defs,
            row_data=ChartState.dict_data,
            pagination=True,
            pagination_page_size=20,
            pagination_page_size_selector=[10, 20, 50, 100],
            on_selection_changed=ChartState.handle_selection,
            theme=ChartState.grid_theme,
            width="100%",
            height="60vh",
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



