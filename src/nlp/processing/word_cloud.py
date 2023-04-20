import datetime
import pathlib
import numpy as np

from wordcloud import WordCloud
from loguru import logger


def build_wordcloud(
    entity: str, frequencies: dict, date: datetime.date, country: str, ent_mapper: dict
):
    logger.debug(f"Building wordcloud for {country} {entity}")

    if not frequencies:
        logger.info(f"Empty frequencies for {entity}")
        return
    x, y = np.ogrid[:500, :500]
    mask = (x - 250) ** 2 + (y - 250) ** 2 > 210**2
    mask = 255 * mask.astype(int)

    wordcloud = WordCloud(
        background_color="white",
        colormap="Set2",
        collocations=False,
        repeat=True,
        mask=mask,
        prefer_horizontal=0.9,
    )
    wordcloud.generate_from_frequencies(frequencies=frequencies)
    p = pathlib.Path(f"/media/images/{date.year}/{date.month}/{date.day}/{country}/")
    p.mkdir(parents=True, exist_ok=True)
    wordcloud.to_file(str(p.joinpath(f"{ent_mapper[entity]}.webp")))
