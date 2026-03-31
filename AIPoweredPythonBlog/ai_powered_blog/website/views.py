from django.http import HttpResponse
from django.shortcuts import render

def welcome(request):
    return HttpResponse("Welcome to the AI Powered Python Blog!")
