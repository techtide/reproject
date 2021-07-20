To run this project, you must be running Python 3.7.10.

The dependencies for the scraping portion of this project are:
1. Scrapy
2. lxml
3. requests
4. pandas
5. scipy
6. neo4j

It is best to setup this environment through a distribution like Anaconda or in a fresh Docker box. You don't really need a configuration file because this is designed to be lightweight and fast, relying on the smallest numbner of additional dependencies possible.

If this was to be used to scrape an entire website, then it would be advisable to do this in a DigitalOcean Drop, or an AWS VPS connected to an S3 bucket. However, proper calculations should be done to see the size of the full dataset of the site. It may not be necessary to do this in a VPS with a storage bucket if the total amount of data is sufficiently small. 

Arman
