# A2Y EventConnect

A2Y EventConnect is a search engine for entertainment events in Ann Arbor, Ypsilanti, and the University of Michigan. The platform centralizes all the entertainment events and provides users with the ability to search events by keywords, find and register for events, manage their event schedule, and communicate with event coordinators. The search engine is designed to help students find and attend events that interest them and improve their overall student experience.

## Features

- Crawls event links from various event websites such as "smtd.umich.edu/events", "annarbor.org/event", and "ums.org/performance", among others.
- Downloads and processes detailed event information, such as the event title, time, location, and descriptions, using text processing techniques such as tokenization, removal of stop words, and stemming with PorterStemmer.
- Implements a vector space model for information retrieval to retrieve relevant events based on user-defined queries.
- Computes precision, average precision, and macro average precision of the information retrieval system to evaluate its effectiveness.

## Requirements

- Python 3.x
- NumPy
- BeautifulSoup4

## Usage

1. Install the required packages.
```
$ pip install numpy bs4
```

2. Run the crawler.py to crawl event links.
```
$ python crawler.py
```

3. Run the download.py file to download and process event information:
```
$ python download.py
```

4. Run the VectorSpace.py file to implement the vector space model for information retrieval:
```
$ python VectorSpace.py
```

5. Check the result in the `result/` folder.

- *If user wants to change query terms, please change the query terms in the `test_queries.txt` file.*


## Contributing

We welcome contributions to this project, such as adding more event websites to crawl or improving the text processing techniques.

## Contributors

- Oliver Wu
- Yuxin Lu
- Yuhui Lai
- Yongqi Wu
- Frederick Wang




