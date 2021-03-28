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
def home(request):
    username = request.user.username






    #items = [{"id" :"1","name":"Pizza"},{"id":"2","name":"Meals"}]
    #output_customers = [{'customer':'71343247','items':['burger','pizza']},{'customer':'71343246','items':['meals<br>','pizza<br>','meals<br>','pizza','meals','pizza','meals','pizza']}]

    return render(request, 'home.html')

def fetch_corpus(request):
  #pages = ['Sachin_Tendulkar','Virat_Kohli','Sourav_Ganguly','Sunil_Gavaskar','Kapil_Dev','Anil_Kumble','Dilip_Vengsarkar','Mohammad_Azharuddin','Dhoni_','Rohit_Sharma' ]
  pages = ['Dhoni_']
  global  content

  titles  = []
  '''
  for i in pages :
    page = wikipedia.page(str(i))
    # get the title of the page
    title = page.title
    titles.append(title)
    needed_data = page.content.split('== See also ==')[0]
    content = content + needed_data
  print(content.rsplit('.')[0])
  '''
  content ="sdsdsdsMahendra Singh Dhoni (pronunciation  born 7 July 1981), is a former Indian international cricketer who captained the Indian national team in limited-overs formats from 2007 to 2017 and in Test cricket from 2008 to 2014."
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

def logout(request):
    auth.logout(request)
    return redirect('/')
