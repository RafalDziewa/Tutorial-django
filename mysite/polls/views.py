from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from .forms import NameForm, LoginForm
from .models import Question, Choice, Name
from django.urls import reverse
from django.template import loader
from django.views import generic, View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        form = NameForm()
        questions = Question.objects.filter(
                    pub_date__lte=timezone.now()
                ).order_by('-pub_date')[:5]
        print(request.user)
        context = {
            'latest_question_list': questions,
            'form': form,
        }
        return render(request, 'polls/index.html', context)

    def post(self, request):

        form = NameForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(pk="+1")
            # created_name = Name.objects.create(**form.cleaned_data)
            created_name = Name.objects.create(
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                gender=form.cleaned_data['gender'],
                who_add=request.user,
                question=question,
            )
        else:
            context = {
                'message': "Your form is not valid. Sorry!",
            }
            return render(request, 'polls/index.html', context)

        form = NameForm()
        questions = Question.objects.filter(
                    pub_date__lte=timezone.now()
                )
        context = {
            'latest_question_list': questions,
            'form': form,
            'message': created_name,
        }
        return render(request, 'polls/index.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class NameEditView(View):

    def get(self, request, name_id):
        selected_name = None
        name_url = 'name_edit'
        try:
            selected_name = Name.objects.get(pk=name_id)
            form = NameForm(initial={
                'name': selected_name.name,
                'surname': selected_name.surname,
                'gender': selected_name.gender,
            })
        except ObjectDoesNotExist:
            form = NameForm()
            messages.error(request, 'Document deleted.')
            return render(request, 'polls/error_page.html')
        context = {
            'selected_name': selected_name,
            'name_id': name_id,
            'form': form,
            'name_url': name_url,
        }
        return render(request, 'polls/name_edit.html', context)

    def post(self, request, name_id):

        selected_name = Name.objects.get(pk=name_id)
        form = NameForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            selected_name.name = form.cleaned_data["name"]
            selected_name.surname = form.cleaned_data["surname"]
            selected_name.gender = form.cleaned_data["gender"]
            selected_name.save()

        return HttpResponseRedirect(reverse('polls:name_edit', args=(name_id,)))

        # try:
        #     selected_name = Name.objects.get(pk=name_id)
        #     form = NameForm(request.POST)
        #     if form.is_valid():
        #         selected_name.name = form.cleaned_data["name"]
        #         selected_name.surname = form.cleaned_data["surname"]
        #         selected_name.gender = form.cleaned_data["gender"]
        #         selected_name.save()
        #     else:
        #         return render(request, 'polls/error_page.html')
        # except ObjectDoesNotExist:
        #     messages.error(request, 'Document deleted.')
        #     return render(request, 'polls/error_page.html')
        # return HttpResponseRedirect(reverse('polls:name_edit', args=(name_id,)))


class DetailView(PermissionRequiredMixin, View):
    permission_required = 'polls.view_question'
    raise_exception = True

    def get(self, request, pk):
        questions = Question.objects.filter(pub_date__lte=timezone.now())
        question = get_object_or_404(questions, pk=pk)
        context = {
            'question': question,
        }
        return render(request, 'polls/detail.html', context)


class ResultsView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        context = {
            'question': question,
        }
        return render(request, 'polls/results.html', context)


class VoteView(View):
    def get(self, request, question_id):
        return HttpResponseRedirect(reverse('polls:index'))

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            context = {
                'question': question,
                'error_message': "You didn't select a choice.",
            }
            return render(request, 'polls/detail.html', context)
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class LoginView(View):

    def get(self, request):
        ctx = {
            'form': LoginForm,
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)
                return HttpResponseRedirect(reverse('polls:index'))
                # return HttpResponseRedirect('/polls/')

            form.add_error(field=None, error='Zły login lub hasło!')

        ctx = {
            'form': form,
        }
        return render(request, 'login.html', ctx)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         # print(Choice.objects.all().query)
#         # questions_sorted = Question.objects.filter(
#         #     pub_date__lte=timezone.now()
#         # ).order_by('-pub_date')[:5]
#         # print(questions_sorted.query)
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question,
#     }
#     return render(request, 'polls/detail.html', context)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question,
#     }
#     return render(request, 'polls/results.html', context)
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         context = {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         }
#         return render(request, 'polls/detail.html', context)
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
