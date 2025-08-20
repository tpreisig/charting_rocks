import reflex as rx

config = rx.Config(
    app_name="charting_rocks",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)