# Personal Wrapped

This project was born out of my dissatisfaction with the limited data provided by Spotify during Wrapped season by every year's end. Don't get me wrong, I really enjoy the data presented and the team has been clearly evolving the product year after year. But I am always left with a "I WANT MORE" urge when the experience is over :(

In order to attend to this urge, this is my attempt at tracking my musical journey during each year. My ambitions are to create several visualizations for different time periods: per day, week, month, semester and, finally, year. And also compare each time period with relevant ones, trying to answer questions like: "How was my musical consumption in every week of September 2022? How do they compare with each other? In which of those 4 Mondays have I listened to more songs?" and many, many more.

In order to do that, using Spotify's API, I decided to collect my recently played tracks daily, running a scheduled bash script that triggers a Python one (files on the data_collection folder). After calling several endpoints, the script saves the relevant non-relational data to a Mongo database hosted on the cloud. With the data collection process taken care of, I developed a Dash app (notebook in the app folder) with interactive visuals that shed some light on my historical musical consumption. For now, I'm running everything locally, but, once the project is a little more mature, I intend to migrate both stages to a cloud deployment.

The available visualizations are mostly related to the songs I listened to in the current day, comparing it to previous days. My latest addition was using MusicBrainz’ and setlist.fm’s APIs to display the setlists from an artist’s most recent shows worldwide and in Brazil whenever the user clicks on an artist's name in the “Artists played yesterday” barplot. Below are 4 screenshots of the current visuals, with a brief comment for each one:

![Yesterday-Today comparisons](https://github.com/rafael-siqueira/spotify-personal-wrapped/blob/main/images/yesterday_today.png)
<i>Previous day can be changed using the date picker component in the upper left corner</i>
<br></br>
<br></br>
![Setlists and tables](https://github.com/rafael-siqueira/spotify-personal-wrapped/blob/main/images/setlists_tables.png)
<i>Setlists displayed once I clicked in the Arctic Monkeys bar in the third barplot from left to right in the picture above this one</i>
<br></br>
<br></br>
![Matrix 1](https://github.com/rafael-siqueira/spotify-personal-wrapped/blob/main/images/matrix_1.png)
<i>Matrix for current day songs. As represented by the legend (which is also a filter), songs in major keys are colored green, whereas songs in minor keys are yellow. Also, as written in the upper right corner, ball size represents the song's valence, which is a measure of how much positivity the song conveys</i>
<br></br>
<br></br>
![Matrix 2](https://github.com/rafael-siqueira/spotify-personal-wrapped/blob/main/images/matrix_2.png)
<i>Another matrix for current day songs. Only a few keys were selected, filtering the songs displayed</i>
<br></br>
Like I mentioned, since this is a rough initial draft, a lot of things need correction or can be improved: Spotify's API calls can be optimized; callbacks' code can be refactored in several auxiliary functions to avoid repetition; and, since I'm no expert in front-end development and am learning it on the fly, CSS styling can be greatly improved, to name a few.

Hope you enjoy it and follow the repository for future improvements :)
