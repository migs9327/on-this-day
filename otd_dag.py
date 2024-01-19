#%%
from airflow import DAG
from datetime import timedelta
from datetime import datetime
from airflow.operators.python import PythonOperator
from bs4 import BeautifulSoup
from os.path import expanduser, join
import requests
#%%

def get_today_events_ul(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Find the header for historical events
    header = soup.find('header', class_='section__heading header-history')
    if header:
        # Find the next <ul> element after the header and the one after the 'cafemedia' div
        first_ul = header.find_next_sibling('ul')
        second_ul = first_ul.find_next_sibling('div').find_next_sibling('ul')
        return first_ul, second_ul
    return None, None

def write_file(text: str, file_dir: str):
    with open(file_dir, 'a') as f:
        f.write(text + '\n')

def clear_file(file_dir: str):
    with open(file_dir, 'w') as f:
        pass

def get_today_events(url: str, file_dir: str):
    first_ul, second_ul = get_today_events_ul(url)
    if first_ul and second_ul:
        # Combine both ul elements for iteration
        all_events = first_ul.find_all('li', class_='event') + second_ul.find_all('li', class_='event')
        for li in all_events:
            write_file(li.get_text(), file_dir)


home = expanduser("~")
save_dir = join(home, 'on-this-day/todays_events.txt')
otd_url = 'https://www.onthisday.com'
# %%
with DAG(dag_id='on-this-day',
         start_date=datetime(2024, 1, 19),
         description='A DAG to fetch events from onthisday.com',
         schedule_interval="@daily",
         catchup=False
        ) as dag:

     clear_file = PythonOperator(task_id='clear-file', python_callable=clear_file, op_args=[save_dir])     
     get_today_events = PythonOperator(task_id='get-today-events', python_callable=get_today_events, op_args=[otd_url, save_dir])

     clear_file >> get_today_events