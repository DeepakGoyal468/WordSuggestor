from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv
from .models import Query
from django.conf import settings
import os
# Create your views here.


def index(request):
    file_path = os.path.join(settings.FILES_DIR, 'word_search.tsv')
    with open(file_path) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            q = Query(word_name=line[0], word_frequency=line[1], word_length=len(line[0]))
            q.save()
    return HttpResponse("Hello, This is working")


def search(request):
    word = request.GET.get('word', '')
    word_list = Query.objects.filter(word_name__contains=word).order_by('word_length').order_by('-word_frequency')
    word_list_start_with_word = word_list.filter(word_name__startswith=word)
    word_list_not_start_with_word = word_list.exclude(word_name__startswith=word)
    word_list_start_with_word_dict_list = []
    count = 1
    for v in word_list_start_with_word:
        word_list_start_with_word_dict = {"word_name":v.word_name,}
        if count <= 25:
            word_list_start_with_word_dict_list.append(word_list_start_with_word_dict)
            count += 1
        else:
            break

    for v in word_list_not_start_with_word:
        word_list_not_start_with_word_dict = {"word_name":v.word_name}
        if count <= 25:
            word_list_start_with_word_dict_list.append(word_list_not_start_with_word_dict)
            count += 1
        else:
            break

    print(word_list_start_with_word_dict_list)
    return JsonResponse({"list":word_list_start_with_word_dict_list}, safe=False)
