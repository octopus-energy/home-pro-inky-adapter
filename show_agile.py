import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import matplotlib.dates as mdates
import pandas as pd
import requests

from inky_drivers.inky_uc8159_mod import Inky as InkyUC8159


def pull_agile():
    url_base = "http://api.octopus.energy"

    import_endpt = (
        "/v1/products/AGILE-24-04-03/"
        "electricity-tariffs/E-1R-AGILE-24-04-03-H/standard-unit-rates/"
    )
    export_endpt = (
        "/v1/products/AGILE-OUTGOING-19-05-13/"
        "electricity-tariffs/E-1R-AGILE-OUTGOING-19-05-13-H/standard-unit-rates/"
    )
    response_import = requests.get(url_base + import_endpt).json()
    response_export = requests.get(url_base + export_endpt).json()

    dfi = pd.DataFrame(response_import["results"])

    dfe = pd.DataFrame(response_export["results"])

    df = pd.DataFrame()
    df["Import (p/kWh)"] = dfi["value_inc_vat"]
    df["Export (p/kWh)"] = dfe["value_inc_vat"]

    # time in format of day/month hour:minute
    df["time"] = dfi["valid_from"]
    df["time"] = pd.to_datetime(df["time"]).dt.tz_convert("Europe/London")
    # df["time"] = dfi["valid_from"].dt.strftime("%d/%m %H:%M")

    # sort by time
    df = df.sort_values(by="time")

    return df


df = pull_agile()
# pick out a window from df that is 12 hours ahead and 6 hours in the past
df = df[
    (df["time"] > pd.Timestamp.now(tz="Europe/London") - pd.Timedelta(hours=6))
    & (df["time"] < pd.Timestamp.now(tz="Europe/London") + pd.Timedelta(hours=12))
]


inky = InkyUC8159()
WIDTH = 600
HEIGHT = 448


saturation = 0.5


plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")  # Use a clean, readable style
ax = sns.lineplot(
    x="time",
    y="Import (p/kWh)",
    data=df,
    label="Import (p/kWh)",
    linewidth=2,
    drawstyle="steps-post",
)
sns.lineplot(
    x="time",
    y="Export (p/kWh)",
    data=df,
    label="Export (p/kWh)",
    linewidth=2,
    drawstyle="steps-post",
)

ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%H:%M", tz=pd.Timestamp.now(tz="Europe/London").tzinfo)
)
ax.grid(True, which="major", axis="both", linestyle="--", linewidth=0.5)

# Customize the plot
plt.xlabel("Time (hh:mm)", fontsize=14)
plt.ylabel("Agile price (p/kWh)", fontsize=14)
plt.legend(fontsize=12)
plt.xticks(rotation=45)


# Save the figure to a buffer
saturation = 0
dpi = 80
buf = io.BytesIO()
plt.gcf().set_size_inches(WIDTH / dpi, HEIGHT / dpi)

plt.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")

# Close the plot to free memory
plt.close()


plot_image = Image.open(buf).convert("RGB")
image = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
image.paste(plot_image, (20, 0))


image.save("graph.png")


resizedimage = image.resize(inky.resolution)

try:
    inky.set_image(resizedimage, saturation=saturation)
except TypeError:
    inky.set_image(resizedimage)

inky.show()
