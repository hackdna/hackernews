## Hacker News CLI app

Uses the Hacker News REST API provided by Firebase to return the top N stories currently posted to Hacker News

Requires Python 3 (tested with Python 3.7.3)

### Quick start
```bash
git clone git@github.com:hackdna/hackernews.git
cd hackernews
mkvirtualenv -a $(pwd) hackernews
pip install -r requirements.txt
python hn.py -n 3
```
