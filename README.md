# Data Engineering Salaries

Each quarter we run a salary survey in our community to help increase transparency around salary and compensation for Data Engineering. This application is for exploring and analyzing the salary data.

Notes:

- This is a community project and it's early in development - contributions are welcome!
- Data from historical surveys is not yet available but we do plan to backfill it.
- [Streamlit Docs](https://docs.streamlit.io/)
- [Raw data](https://docs.google.com/spreadsheets/d/1GuEPkwjdICgJ31Ji3iUoarirZNDbPxQj_kf7fd4h4Ro/edit#gid=0)

## Requirements

- Docker

## Build

```bash
docker build -t data_engineering_salaries .
```

## Run

```bash
docker run \
-p 8501:8501 \
-it \
--mount type=bind,source="$(pwd)",target=/app \
data_engineering_salaries
```

In your browser, Go to `localhost:8501`
