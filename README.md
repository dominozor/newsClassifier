# newsClassifier
In parallel with the growth of Internet, every day news websites produce an astonishing number of articles about an astonishing number of topics. (92000 articles, 2 million blog posts) Classification of online news, has often been done manually and this requires too much time and human effort. This project automates classification of news by using Naive Bayes Classification.

### Dependencies:
```bash
$ sudo apt-get install python-tk
$ sudo apt-get install python-imaging-tk
$ pip install -U textblob nltk
```
If this is your first time installing TextBlob, you may have to download the necessary NLTK corpora. This can be done with one command:
```bash
$ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python
$ python -m textblob.download_corpora
```

### Running:
Run training.py as
```bash
$ python training.py
```
it will create a model (.pkl file) from the news files in training folder. Then run news_applet.py as
```bash
$ python news_applet.py
```
and choose .pkl file that you want to use. You can either classify a text that you write in text box or you can choose a test directory and see the accuracy result.
:)))))))))))))))))))))))))))))))))))))))
