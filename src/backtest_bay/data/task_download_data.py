import pytask

from backtest_bay.config import BLD, END_DATES, INTERVALS, SRC, START_DATES, STOCKS
from backtest_bay.data.download_data import download_data

dependencies = [SRC / "config.py", SRC / "data" / "download_data.py"]

for index, _ in enumerate(STOCKS):
    _id = (
        STOCKS[index]
        + "_"
        + START_DATES[index]
        + "_"
        + END_DATES[index]
        + "_"
        + INTERVALS[index]
    )

    @pytask.task(id=_id)
    def task_download_data(
        symbol=STOCKS[index],
        start_date=START_DATES[index],
        end_date=END_DATES[index],
        interval=INTERVALS[index],
        depends_on=dependencies,
        produces=BLD / (_id + ".pkl"),
    ):
        data = download_data(
            symbol=symbol, start_date=start_date, end_date=end_date, interval=interval
        )
        data.to_pickle(produces)
