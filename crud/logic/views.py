from django.shortcuts import render, redirect, get_object_or_404
from logic.forms import UserForm
from logic.models import Person

# Create your views here.
def index(request):
    user_form=UserForm()
    people=Person.objects.all()
    return render(request,'crud/index.html',{'people':people,'form':user_form})


def create(request):
    if request.method=='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
        return redirect('crud:index')

def edit(request,person_id):
    person=get_object_or_404(Person,id=person_id)
    if request.method=='POST':
        user_form=UserForm(request.POST,instance=person)
        if user_form.is_valid():
            user_form.save()
        return redirect('crud:index')
    user_form=UserForm(instance=person)
    return render(request,'crud/edit.html',{'form':user_form})

def delete(request,person_id):
    person=get_object_or_404(Person,id=person_id)
    person.delete()
    return redirect('crud:index')

