import requests
import click
import itertools
import csv
import logging
import os
from bs4 import BeautifulSoup

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

def get_sentences(quote):
    quote = quote.replace("\r\n", "\n")
    lines = quote.split("\n")

    ret = []
    for line in lines:
        line = line.strip()
        line = line.replace("\t", "")
        # TODO: more cleaning / breaking it up on punctuation
        if line:
            ret.append(line)
    return ret

def process_page(page):
    try:
        res = requests.get(f"https://forum.sodika.org/index.php?pageNo={page}")
        soup = BeautifulSoup(res.text, 'html.parser')
        # we are looking for the retard answering troll's questions
        divs = soup.findAll("div", {"class": "comment"})
        for div in divs:
            is_it_the_recskas = div.findAll("strong", {"class": "verified recskaboy"})
            if not is_it_the_recskas:
                continue

            reaction = div.find("div", {"class": "quote"})
            if not reaction:
                continue
            
            # we need the author
            reaction_author = reaction.find("div", {"class": "author"}).text
            # we need to remove the author from the div so we can get the full text
            reaction.find("div", {"class": "author"}).decompose()
            reaction_sentences = get_sentences(reaction.text)
            # break down the comment into "sentences"
            reply = div.find("div", {"class": "innerDiv"})
            reply.find("div", {"class": "quote"}).decompose()

            reply_sentences = get_sentences(reply.text)
            
            return reaction_sentences, reply_sentences
        return None, None    

    except Exception as e:
        return None, None

@click.command()
@click.option('--max-page-number', required=False, type=int, default=0)
@click.option('--min-page-number', required=False, type=int, default=0)
def main(min_page_number, max_page_number):
    min_page_number = min_page_number or 1
    max_page_number = max_page_number or 999999999
    with open("training.tsv", "w+") as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t")
        for page in range(min_page_number, max_page_number + 1):
            logger.info(f"processing page: {page}")
            reaction_sentences, reply_sentences = process_page(page)
            if not reaction_sentences or not reply_sentences:
                logger.info("no autism found")
                continue

            combos = itertools.product(reaction_sentences, reply_sentences)
            for (question, answer) in combos:
                logger.info(f"{question} -> {answer}")
                writer.writerow([question, answer])


        

if __name__ == '__main__':
    main()