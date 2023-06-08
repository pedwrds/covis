import geopandas as gpd
import pandas as pd
import plotly.express as px

from covis.utils import get_project_root


def plot_choro(save_html=True):
    geo = gpd.read_parquet(
        get_project_root() / "output/EWgeo.pkl",
    )

    geo = geo[["EER13NM", "geometry"]]
    geo.set_index("EER13NM", inplace=True)
    geo = geo.set_crs("EPSG:27700")

    weekly_reg_long = pd.read_csv(
        get_project_root() / "output/long_form_regional_weekly_deaths.csv", index_col=0
    )

    # weekly_reg_long["Week ended"] = pd.to_datetime(weekly_reg_long["Week ended"])

    weekly_reg_long = weekly_reg_long.loc[
        weekly_reg_long["Week ended"].between(
            "2020-02-28 00:00:00", "2021-07-01 23:59:59"
        )
    ]

    fig = px.choropleth(
        weekly_reg_long,
        geojson=geo["geometry"],
        locations=weekly_reg_long["region"],
        color=weekly_reg_long["pc deaths due to covid19"],
        animation_frame="Week ended",
        color_continuous_scale="reds",
        range_color=(
            weekly_reg_long["pc deaths due to covid19"].min(),
            weekly_reg_long["pc deaths due to covid19"].max(),
        ),
        hover_name="region",
        hover_data=["pc deaths due to covid19", "covid19 deaths", "total deaths"],
    )

    fig.update_geos(fitbounds="geojson", visible=False)

    if save_html is True:
        fig.write_html(get_project_root() / "output/choro_slider.html")

        fig.write_html(get_project_root() / "lfs/choro_slider.html")

        # fig.write_image(
        #     get_project_root() / "output/choro_slider.png"
        # )


if __name__ == "__main__":
    plot_choro()
