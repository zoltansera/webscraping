# Scraper for checking new ads
I've wrote this script to be able to continuously check for new advertisements on a specific website.

## Usage:
main.py followed by 5 arguments:
arg[1] = the website to be scraped (jofogas, a hungarian ad site)
arg[2] = the keyword to search for
arg[3] = a notification will be sent to this email address in case of new ad (you will need your own php or other solution for this to work for you)
arg[4] = check interval in minutes
arg[5] = how many checks do you want to run

Example:
```
main.py https://www.jofogas.hu kutya sera.kontakt@gmail.com 1 15
```