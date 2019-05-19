#!/usr/bin/env python

"""Hacker News CLI app

Uses the Hacker News REST API provided by Firebase to return the top N stories
currently posted to Hacker News

Tested with Python 3.7
"""

__version__ = '0.1'

import argparse
import sys
import time

import requests

API_BASE_URL = 'https://hacker-news.firebaseio.com/v0/'


def main():
    args = get_args()
    # get a list of top story IDs
    try:
        story_ids = get_resource('topstories.json')
    except requests.exceptions.RequestException as exc:
        sys.exit(exc)

    print('Top {} stories on Hacker News\n'.format(args.n))
    stories = get_stories(story_ids)

    # print a list of N top stories by rank in descending order
    position = 0
    for rank in sorted(stories.keys(), reverse=True)[:args.n]:
        story = stories[rank]
        position += 1
        print("{}. {}".format(position, story.get('title', '')))
        print("    posted by {} ({} points) - {} comments (rank={:1.2f})"
              .format(story.get('by', ''), story.get('score', ''),
                      story.get('descendants', 0), rank))


def get_args():
    """Parse command line arguments and return an object holding attributes"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-n', required=True, type=int,
                        help='number of top stories to retrieve')
    parser.add_argument('--version', action='version', version=__version__)
    return parser.parse_args()


def get_rank(story, current_time):
    """Return rank of a given story at a point in time"""
    try:
        factor = 1.0 if story['url'] else 0.4
    except KeyError:
        factor = 0.4
    age = (current_time - story['time']) / 3600  # hours
    return factor * ((story['score'] - 1) ** 0.8) / ((age + 2) ** 1.8)


def get_resource(suffix, session=None):
    """Return a Python object for Firebase URL response"""
    url = API_BASE_URL + suffix
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_stories(story_ids):
    """Return a dictionary of ranked stories given a list of story IDs"""
    current_time = int(time.time())
    stories = {}
    session = requests.Session()
    # construct a dict of stories as values and their ranks as keys
    for story_id in story_ids:
        try:
            story = get_resource('item/{}.json'.format(story_id), session)
        except requests.exceptions.RequestException:
            continue
        # skip dead or deleted stories
        if story == {} or story.get('deleted') is True:
            continue
        stories[get_rank(story, current_time)] = story
    return stories


if __name__ == '__main__':
    main()
