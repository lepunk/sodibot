import pickle
import click
from nltk.stem.snowball import HungarianStemmer

classifier = None

@click.command()
@click.option('--question', required=True, type=str)
def main(question):
    stemmer = HungarianStemmer()
    words = question.split(" ")

    to_classify = dict([(stemmer.stem(word), True) for word in words])
    resp = classifier.classify(to_classify)
    print(resp)

if __name__ == '__main__':
    f = open('classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    main()