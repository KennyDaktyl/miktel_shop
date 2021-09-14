from django.views import View
from django.shortcuts import render, redirect

class First_Page(View):
    def get(self, request):
        return render(request, "front_page/first_page.html")


first_page = First_Page.as_view()