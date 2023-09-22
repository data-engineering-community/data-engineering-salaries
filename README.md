# Data Engineering Salaries

Each quarter we run a salary survey in our community to help increase transparency around salary and compensation for Data Engineering. This application is for exploring and analyzing the salary data.

Notes:

- This is a community project and it's early in development - contributions are welcome!
- Data from historical surveys is not yet available but we do plan to backfill it.
- [Streamlit Docs](https://docs.streamlit.io/)
- [Raw data](https://docs.google.com/spreadsheets/d/1GuEPkwjdICgJ31Ji3iUoarirZNDbPxQj_kf7fd4h4Ro/edit#gid=0)

## Requirements

- Docker

## Setup

- Download or clone the repository.
- Rename the example.secrets.toml (inside .streamlit folder) file to secrets.toml
- Open the **Raw Data** sheet, copy the full URL and paste it to the *secrets.toml* **public_gsheets_url** variable.

## Build

```bash
docker compose build
```

## Run

Run the streamlit container in detached mode
```bash
docker compose up -d
```

Start/Stop docker container
```bash
docker compose start
docker compose stop
```

In your browser, Go to `localhost:8501`
