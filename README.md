# chess-etl
Data Pipeline to extract and model chess games and player data, using Airflow and DBT.

## What is the purpose of this?

If you're an enthusiastic chess player like me, you've probably watched some high level games to understand what makes them
different to your games. What kinds of openings do they play? What are some common strategies, or even blunders? Which types of endgames happen more often?

Maybe you want to know who the top players are, or the evolution of their ratings through time. Or maybe, what's different about the
games in each rating.

Well, as a data engineer and a chess player, I couldn't help but combine the two and make a data pipeline that allows you to make
any analysis you'd like about top chess games and players.

This ETL system fetches data from [The Week in Chess](https://theweekinchess.com), which has a collection of several thousands of games. It also collects player data from the International Chess Federation (FIDE). Then, all of that is processed in a way to simplify analysis.

![Overview of the data pipeline](./images/Chess%20ETL.png)
