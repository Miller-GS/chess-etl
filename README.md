# chess-etl
Data Pipeline to extract and model chess games and player data, using Airflow and DBT.

## What is the purpose of this?

If you're an enthusiastic chess player like me, you've probably watched some high level games to understand what makes them
different to your games. What kinds of openings do they play? What are some common strategies, or even blunders? Which types of endgames happen more often?

Maybe you want to know who the top players are, or the evolution of their ratings through time. Or maybe, what's different about the
games in each rating.

Well, as a data engineer and a chess player, I couldn't help but combine the two and make a data pipeline that allows you to make
any analysis you'd like about top chess games and players. Also, I'm doing this to learn more - this is my first time using DBT, for example.

This ETL system fetches data from [The Week in Chess](https://theweekinchess.com), which has a collection of several thousands of games. It also collects player data from the International Chess Federation (FIDE). Then, all of that is processed in a way to simplify analysis.

![Overview of the data pipeline](./images/Chess%20ETL.png)

## What tools are used in the Data Pipeline?

### Apache Airflow

I've chosen Airflow as my orchestration tool. Mainly because I'm quite used to it, it's easy to setup, and simplifies the scheduling tremendously.

How it works is that there is a DAG that runs weekly, and it triggers a job to ingest data from The Week in Chess. After that, dependent
DAGs are triggered using the dataset feature. For example, one DAG will run an engine analysis, and another will ingest player data from FIDE. After all that is done, we go to the data modeling part, which is done by DBT, but triggered by Airflow.

### DBT

DBT (Data Build Tool) is great for transforming data. It doesn't directly run queries, but allows you to modularize, simplify and reuse them. It also helps with testing and documentation.

I had never used it before, so I found this to be a great opportunity to learn.

### PostgreSQL

There are several possible databases that work well with Data Pipelines. However, many of them are very closely linked with their respective cloud providers, such as Google's BigQuery and Amazon's Redshift, which comes at a cost. PostgreSQl, on the other hand, is very easy to setup and host anywhere, even locally.

# Local Execution

This project was architectured in a way so that it can be easily run in the cloud or locally. To run it locally,
you should go to orchestration/airflow-local, and copy the content from .env.example into your own .env.

Then, build the image:

```sh
docker-compose build
```

Finally, you can run the containers. Airflow will be available in port 8080.
```sh
docker-compose up
```

# License

This project is licensed under the MIT License.