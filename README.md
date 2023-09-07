# Data Engineering Salaries

Each quarter we run a salary survey in our community to help increase transparency around salary and compensation for Data Engineering. This application is for exploring and analyzing the salary data.

Notes:

- This is a community project and it's early in development - contributions are welcome!
- Data from historical surveys is not yet available but we do plan to backfill it.

## Requirements

- Docker

## Build

```bash
docker build -t salary_transparency .
```

## Run

```bash
docker run \
-p 8501:8501 \
-it \
--mount type=bind,source="$(pwd)",target=/app \
salary_transparency
```

In your browser, Go to `localhost:8501`
