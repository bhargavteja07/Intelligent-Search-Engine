# Intelligent-Search-Engine
A search engine for UIC

Instructions to execute the software:

Required Libraries:

NLTK
Regex,
Pyyaml,
json,
PyQT5 for GUI app

There are two applications in the project.
1. Crawler_App.py -  This application acts as the backend app that runs the crawler independently with the search engine. This is built using multi threading but then it takes about 15 mins to crawl 3000 urls.
The user has an option to stop the crawler at any point of time. The urls spidered until that point will be used by the search engine app.

To execute the app, Enter the command: python3 Crawler_App.py

2. The second application is the actual search engine application that enables the user to search the query.
To execute the app, enter the command: python3 Search_Engine_App.py
Note that the search engine uses an existing spider which has about 3000 URL’s which is stored under Crawler/Spider.json in the project directory.
You can directly run the search engine if you do not wish to run the crawler again.
The search engine takes time to boot the application as the web graph and tf-idf vector is constructed before loading the app. Please look at the terminal for the logs. The application boots up when it says “TF-IDF is done constructing”.

Required Source Files:

Crawler_App.py
vector_model.py
page_rank_graph.py
Search_Engine_App.py
