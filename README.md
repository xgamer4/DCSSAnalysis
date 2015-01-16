# DCSSAnalysis
Repository for code to parse and analyse DCSS morgues

PURPOSE:
    Parse and store Dungeon Crawl Stone Soup morgue files in a mysql database
    Use stored results in database for analysis
    
MEANS:
    Parse morgues: Python
    Analysis: R, and whatever else I find and want to use/learn

parseMorgues.py - a Python script designed to read and parse morgue files downloaded from the online servers

dbSchema.txt - A planning doc for the DB schema for morgue data storage (outdated)

Crawl.sql - A sql script to create the Crawl database (up-to-date; structure only)

TODOS:
    - Better layout for parseMorgues.py
        - Move many of the commonly-used chunks to functions for better maintenance
        - Better formatting
        - Better/more comments
