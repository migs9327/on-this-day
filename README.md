# On This Day Events Fetcher

## Description
This Airflow DAG scrapes daily historical events from onthisday.com and stores them in a text file.

## Prerequisites
- Apache Airflow installed.
- Python with `requests` and `beautifulsoup4`.

## Installation
1. Clone this repository.
2. Place `on_this_day_dag.py` in the Airflow DAGs directory (`~/airflow/dags/`).
3. Install dependencies:
   ```shell
   pip install requests beautifulsoup4
   ```

## Usage
The DAG, `on-this-day`, appears in the Airflow web UI. It runs daily, saving events to `~/on-this-day/todays_events.txt`.

## License
[MIT License](https://choosealicense.com/licenses/mit/).
