from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Forum, Topic, Post
from .forms import NewTopicForm

# Create your views here.
def home(request):
    forums = Forum.objects.all()
    context = {'forums': forums}
    return render(request, 'home.html', context)

def forum_topics(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    context = {'forum': forum}
    return render(request, 'topics.html', context)

def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    user = User.objects.first()
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('forum_topics', pk=forum.pk)
    else:
        form = NewTopicForm()
    context = {
        'forum': forum,
        'form': form
    }
    return render(request, 'new_topic.html', context)

# experimented changing the url patterns to names of the forums
# def forum_topics(request, name):
#     forum = get_object_or_404(Forum, name=name)
#     context = {'forum': forum}
#     return render(request, 'topics.html', context)