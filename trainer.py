import click
import csv
import regex
from nltk.stem.snowball import HungarianStemmer
from nltk.classify import NaiveBayesClassifier

@click.command()
@click.option('--input', required=False, default="training.tsv")
def main(input):

    stemmer = HungarianStemmer()
    tagged_features = []
    with open(input) as tsvfile:
        autireader = csv.reader(tsvfile, delimiter='\t')
        for autism in autireader:
            question = autism[0]
            answer = autism[1]

            words = question.split(" ")
            try:
                tagged_features.append([dict([(stemmer.stem(word), True) for word in words]), answer])
            except:
                pass

    classifier = NaiveBayesClassifier.train(tagged_features)

    import pickle
    f = open('classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()         


if __name__ == '__main__':
    main()