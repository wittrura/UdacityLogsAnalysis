#!/usr/bin/env python

import psycopg2
import datetime

DBNAME = "news"


def get_popular_articles():
    """Return top 3 articles by timestap from the database, descending."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT articles.title, count(log.time) as timestamps
                 FROM log
                 JOIN articles
                    ON log.path = concat('/article/', articles.slug)
                 GROUP BY articles.title
                 ORDER BY timestamps desc
                 LIMIT 3
                 """)
    logs = c.fetchall()
    print 'Most popular articles:'
    for log in logs:
        # log[0] = article title
        # log[1] = count of timestamps per article aka views
        print log[0] + ' - ' + str(log[1]) + ' views'

    db.close()


def get_logs_with_author():
    """Return all authors with view counts descending, based on parsing log paths"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT authors.name, count(log.time) as timestamps
                 FROM log
                 JOIN articles ON log.path = concat('/article/', articles.slug)
                 JOIN authors ON articles.author = authors.id
                 GROUP BY authors.name
                 ORDER BY timestamps desc
                 """)
    logs = c.fetchall()

    print 'Most popular authors:'
    for log in logs:
        # log[0] = authors name, log[1] = count of timestamps per article aka views
        print log[0] + ' - ' + str(log[1]) + ' views'

    db.close()
    return


def get_high_error_days():
    """Return days where over 1% of requests were errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
              SELECT ok.date, ok.count, error.count,
                ((error.count::float / (ok.count + error.count)) * 100.0) as percent
              FROM
                (SELECT date(time) as date, status, count(time) as count
                 FROM log
                 WHERE status = '200 OK'
                 GROUP BY date(time), status) ok
              JOIN
                (SELECT date(time) as date, status, count(time) as count
                 FROM log
                 WHERE status = '404 NOT FOUND'
                 GROUP BY date(time), status) error
              ON ok.date = error.date
              WHERE ((error.count::float / (ok.count + error.count)) * 100.0) > 1.0
              """)
    logs = c.fetchall()

    print 'Days with error rate greater than 1%:'
    for log in logs:
        # log[0] = date, log[3] = percentage of errors
        print log[0].strftime('%B %d, %Y') + ' - ' + str(round(log[3], 2)) + '%'

    db.close
    return

get_popular_articles()
get_logs_with_author()
get_high_error_days()
