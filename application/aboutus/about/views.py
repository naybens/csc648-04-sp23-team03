from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Member
from django.urls import reverse_lazy


class MemberListView(generic.ListView):
    model = Member
    success_url = reverse_lazy("index")
    context_object_name = 'member_list'
    template_name = 'about/index.html'

    def get_queryset(self):
        return Member.objects.all()

    
def detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'about/detail.html')

class MemberDetailView(generic.DetailView):
    model = Member
    template_name = 'about/detail.html'