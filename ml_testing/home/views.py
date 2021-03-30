from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
import wikipedia
from nltk import ngrams


import json

from django.conf import settings
# Create your views here.

content = ""
bigrams_list  = []
trigrams_list  = []
quadrigrams_list = []
model_ted = ''
def home(request):
    username = request.user.username






    #items = [{"id" :"1","name":"Pizza"},{"id":"2","name":"Meals"}]
    #output_customers = [{'customer':'71343247','items':['burger','pizza']},{'customer':'71343246','items':['meals<br>','pizza<br>','meals<br>','pizza','meals','pizza','meals','pizza']}]

    return render(request, 'home.html')

def fetch_corpus(request):
  #pages = ['Sachin_Tendulkar','Virat_Kohli','Sourav_Ganguly','Sunil_Gavaskar','Kapil_Dev','Anil_Kumble','Dilip_Vengsarkar','Mohammad_Azharuddin','Dhoni_','Rohit_Sharma' ]
  pages = ['Dhoni_','Sachin_Tendulkar','Virat_Kohli'  ]
  #pages = ['Dhoni_' ]
  global  content
  content = " "

  titles  = []

  for i in pages :
    page = wikipedia.page(str(i))
    # get the title of the page
    title = page.title
    titles.append(title)
    needed_data = page.content.split('== See also ==')[0]
    content = content + needed_data
  print(content.rsplit('.')[0])

  #content ="sdsdsdsMahendra Singh Dhoni (pronunciation  born 7 July 1981), is a former Indian international cricketer who captained the Indian national team in limited-overs formats from 2007 to 2017 and in Test cricket from 2008 to 2014."
  return render(request, 'corpus.html',{'content':content.rsplit('.')[0]})
def l_models(request):
  n = 2

  bigrams = ngrams(content.split(), n)
  global  bigrams_list

  for grams in bigrams:
    bigrams_list.append(grams)


  n = 3
  trigrams = ngrams(content.split(), n)

  global trigrams_list
  for grams in trigrams:
    trigrams_list.append(grams)

  n = 4
  quadrigrams  = ngrams(content.split(), n)

  global  quadrigrams_list
  for grams in quadrigrams:
    quadrigrams_list.append(grams)




  return render(request, 'l_model.html', {'content': content.rsplit('.')[0],'bigrams':bigrams_list[-10:],'trigrams':trigrams_list[-10:]})
def report(request):

  global  bigrams_list
  global trigrams_list
  global  content
  report = {
    'word_count' : len(content.split(' ')),
    'bigram_count' :len(bigrams_list),
    'trigram_count':len(trigrams_list)
      }

  return render(request, 'report.html', {'content': content.rsplit('.')[0],'bigrams':bigrams_list[-10:],'trigrams':trigrams_list[-10:],'report':report})

def grams(request):

  report = {
    'word_count' : len(content.split(' ')),
    'bigram_count' :len(bigrams_list),
    'trigram_count':len(trigrams_list)
      }
  n = request.GET['n']
  print(n)
  if  n == '2':
    return render(request, 'bigrams.html', {'content': content.rsplit('.')[0],'bigrams':bigrams_list[-10:],'trigrams':trigrams_list[-10:],'report':report,'bigram':bigrams_list})
  else :
    return render(request, 'trigrams.html', {'content': content.rsplit('.')[0],'bigrams':bigrams_list[-10:],'trigrams':trigrams_list[-10:],'report':report,'trigram':trigrams_list})

def getp(request):
  if request.method != "POST":
    report = {
      'word_count' : len(content.split(' ')),
      'bigram_count' :len(bigrams_list),
      'trigram_count':len(trigrams_list)
        }
    return render(request, 'predict.html', {'content': content.rsplit('.')[0],'report':report,'trigram':trigrams_list,'bigram':bigrams_list})
  else:
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken', None)
    print(post_data)
    if post_data['n'][0] == '3':
      inp = post_data['trigram'][0]
      inp =  tuple(eval(inp))

      count_1 = 0
      ti_list = []
      for ti in quadrigrams_list:
        # print(inp)
        # print(ti)

        if inp == ti[0:3]:
          count_1 = count_1 + 1
          ti_list.append(ti)
      from collections import Counter

      len_tri = len(ti_list)
      res = Counter(ti_list)
      out = []
      for i in res:
        r = {}
        r['item'] = i
        r['count'] = res[i]
        r['p'] = round(res[i] / len_tri, 3)
        out.append(r)
      out = sorted(out, key=lambda k: k['count'], reverse=True)
      print(out)
    else:
      inp = post_data['bigram'][0]
      inp =  tuple(eval(inp))
      count_1 = 0
      ti_list = []
      for ti in trigrams_list:
        #print(inp[0])
        #print(ti)

        if inp == ti[0:2]:
          count_1 = count_1 + 1
          ti_list.append(ti)
      from collections import Counter

      len_tri = len(ti_list)
      res = Counter(ti_list)
      out = []
      for i in res:
        r = {}
        r['item'] = i
        r['count'] = res[i]
        r['p'] = round(res[i] / len_tri, 3)
        out.append(r)
      out = sorted(out, key=lambda k: k['count'],reverse=True)
      print(out)

  return render(request, 'predict.html',
                {'content': content.rsplit('.')[0],  'trigram': trigrams_list, 'inp':inp,'bigram': bigrams_list,'out':out})


def grams(request):

  report = {
    'word_count' : len(content.split(' ')),
    'bigram_count' :len(bigrams_list),
    'trigram_count':len(trigrams_list)
      }
  n = request.GET['n']
  print(n)
  if  n == '2':
    return render(request, 'bigrams.html', {'content': content.rsplit('.')[0],'bigrams':bigrams_list[-10:],'trigrams':trigrams_list[-10:],'report':report,'bigram':bigrams_list})
  else :
    return render(request, 'trigrams.html', {'content': content.rsplit('.')[0],'bigrams':bigrams_list[-10:],'trigrams':trigrams_list[-10:],'report':report,'trigram':trigrams_list})

def custom(request):
  if request.method != "POST":
    report = {
      'word_count' : len(content.split(' ')),
      'bigram_count' :len(bigrams_list),
      'trigram_count':len(trigrams_list)
        }
    return render(request, 'custom.html', {'content': content.rsplit('.')[0],'report':report,'trigram':trigrams_list,'bigram':bigrams_list})
  else:
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken', None)
    inp = post_data['words'][0]
    out = {}
    test_list = inp.split(' ')
    if len(test_list) == 2:
      test_list = inp.split(' ')
      inp = tuple(test_list)

      count_1 = 0
      ti_list = []
      for ti in trigrams_list:
        # print(inp)
        # print(ti)

        if inp == ti[0:2]:
          count_1 = count_1 + 1
          ti_list.append(ti)
      from collections import Counter

      len_tri = len(ti_list)
      res = Counter(ti_list)
      out = []
      for i in res:
        r = {}
        r['item'] = i
        r['count'] = res[i]
        r['p'] = round(res[i] / len_tri, 3)
        out.append(r)
      out = sorted(out, key=lambda k: k['count'], reverse=True)
      print(out)
    else:
      test_list = inp.split(' ')
      inp = tuple(test_list)

      count_1 = 0
      ti_list = []
      for ti in quadrigrams_list:
        # print(inp)
        # print(ti)

        if inp == ti[0:3]:
          count_1 = count_1 + 1
          ti_list.append(ti)
      from collections import Counter

      len_tri = len(ti_list)
      res = Counter(ti_list)
      out = []
      for i in res:
        r = {}
        r['item'] = i
        r['count'] = res[i]
        r['p'] = round(res[i] / len_tri, 3)
        out.append(r)
      out = sorted(out, key=lambda k: k['count'], reverse=True)
      print(out)



  return render(request, 'custom.html',
                {'content': content.rsplit('.')[0],  'trigram': trigrams_list, 'inp':inp,'bigram': bigrams_list,'out':out[:10]})

def spell(request):
  if request.method != "POST":
    report = {
      'word_count' : len(content.split(' ')),
      'bigram_count' :len(bigrams_list),
      'trigram_count':len(trigrams_list)
        }
  else:
    post_data = dict(request.POST.lists())
    post_data.pop('csrfmiddlewaretoken', None)
    inp = post_data['word'][0]
    print(post_data)
    global model_ted
    import re
    # remove parenthesis
    input_text_noparens = re.sub(r'\([^)]*\)', '', content)
    # store as list of sentences
    sentences_strings_ted = []
    for line in input_text_noparens.split('\n'):
      m = re.match(r'^(?:(?P<precolon>[^:]{,20}):)?(?P<postcolon>.*)$', line)
      sentences_strings_ted.extend(sent for sent in m.groupdict()['postcolon'].split('.') if sent)
    # store as list of lists of words
    sentences_ted = []
    for sent_str in sentences_strings_ted:
      tokens = re.sub(r"[^a-z0-9]+", " ", sent_str.lower()).split()
      sentences_ted.append(tokens)
    import gensim
    from gensim.models import FastText
    global model_ted
    model_ted = FastText(sentences_ted, window=5, min_count=5, workers=4, sg=1)


    similar = model_ted.wv.most_similar(inp)
    semantically_similar_words = {words: [item[0] for item in model_ted.wv.most_similar([words], topn=5)]
                                  for words in ['dhoni', 'singh']}
    out = []
    for i in similar:
      s = {}
      s['item'] = i[0]
      s['p'] = i[1]
      out.append(s)
    print(similar)
    print(model_ted)
  return render(request, 'custom2.html',
                { 'bigram': bigrams_list,'similar':out,'inp':inp})


def logout(request):
    auth.logout(request)
    return redirect('/')
