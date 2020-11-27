## SoDI bot

Experimental "AI" based on SoDI

Requires Python 3.8

Installation:
`pip install -r requirements.txt`

Usage:
- Step 1.: Gather training data 
  `python scraper.py --min-page-number=200 --max-page-number=500`

  Downloads information from SoDI Forum between {min-page-number} and {max-page-number} where SoDi is actually reacting to comments

- Step 2: Train the classifier
  `python trainer.py`

  This step creates classifier.pickle which is a surprisingly small file containing SoDi's personality

- Step 3: Ask SoDI
  `python gyagyas.py --question="hazudsz"`
