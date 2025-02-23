"""This script deploys a task to download data."""

import pytask

from backtest_bay.config import BLD, PARAMS, SRC
from backtest_bay.data.download_data import download_data

scripts = [SRC / "config.py", SRC / "data" / "download_data.py"]

data_to_download = PARAMS.drop_duplicates(
    subset=["stock", "start_date", "end_date", "interval"]
)

for row in data_to_download.itertuples(index=False):
    id_download = f"{row.stock}_{row.start_date}_{row.end_date}_{row.interval}"

    produces = BLD / "data" / f"{id_download}.pkl"

    @pytask.task(id=id_download)
    def task_download_data(depends_on=scripts, produces=produces, param=row):
        """Task to download data and store it in the bld folder."""
        data = download_data(
            symbol=param.stock,
            start_date=param.start_date,
            end_date=param.end_date,
            interval=param.interval,
        )
        data.to_pickle(produces)
