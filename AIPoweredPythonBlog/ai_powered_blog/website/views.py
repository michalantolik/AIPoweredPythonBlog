from django.http import HttpResponse
from django.shortcuts import render

def welcome(request):
    return HttpResponse("Welcome to the AI Powered Python Blog!")

def about(request):
    return HttpResponse("I am Michal and I am developing this AI Powered Python Blog")
