# Reddit_Scraper
This is a simple Reddit scraper that uses the pythons praw module inorder to access reddit and scrape subbreddits. 

1. prints "scraping reddit" onto the terminal
2. use prawn to make a REST call to the reddit endpoints and get the desired subretting
3. write my csv file into the data folder (need to configure correct premissions for airflow for this) 

### Set up
```python
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
    schedule_interval=timedelta(days=1),
)
```


### Echo to terminal 
```python
task1 = BashOperator(
    task_id="echo1",
    bash_command="echo Start scraping reddit.",
    dag=dag,
)
```
### Fetch the data
Now we just use the praw api to make a call to reddit with the desired subreddit passed in as an arguement (name) 
this will return us some texts which I then use Pandas to parse it and put into a csv file
```python
def Reddit_scrape(name, **kwargs):
    posts =[]
    #grabs the top 10 hot reddits from the subreddit
    sub = reddit.subreddit(name).hot(limit=10)
    for post in sub:
        posts.append([post.title.encode("utf-8"), post.score, post.id, 
        post.subreddit, post.url.encode("utf-8"), post.num_comments, 
        post.selftext.encode("utf-8"), post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    posts.to_csv(r'../data/data.csv')
    print(posts)

task2 = PythonOperator(
    task_id="scraper",
    python_callable=Reddit_scrape,
    op_kwargs={'name': 'Gaming'},
    provide_context=True,
    dag=dag
)
```

### Conclusion
heirarchy
```python
task1 >> task2
```

