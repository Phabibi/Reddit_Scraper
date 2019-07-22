import praw as pr
import pandas as pd
from datetime import datetime, timedelta

#Airflow
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator




reddit = pr.Reddit(client_id='vptn_Gf-ohjL7Q', client_secret='Dvkk7N2RvZ9GN-i18kUEEDDaIDc', user_agent='Simple Data Scraper')

def Reddit_scrape(name, **kwargs):
    posts =[]
    sub = reddit.subreddit(name).hot(limit=100)
    for post in sub:
        posts.append([post.title.encode("utf-8"), post.score, post.id, 
        post.subreddit, post.url.encode("utf-8"), post.num_comments, 
        post.selftext.encode("utf-8"), post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    posts.to_csv('./Subs'+name+'.csv')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 7, 18),
    'depends_on_past': False,
    'email': ['phabibi@sfu.ca'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Homework2',
    default_args=default_args,
    description='Homework2',
    schedule_interval=timedelta(minutes=1),
)

# task1 = BashOperator(
#     task_id="echo1",
#     bash_command="echo Start scraping reddit.",
#     dag=dag,
# )

task1 = PythonOperator(
    task_id="scraper",
    python_callable=Reddit_scrape,
    op_kwargs={'name': 'MachineLearning'},
    provide_context=True,
    dag=dag
)
