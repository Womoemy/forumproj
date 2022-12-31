from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Forum, Topic, Post
from .forms import NewTopicForm, PostForm
from django.views.generic import CreateView, UpdateView, ListView

# Create your views here.

class ForumListView(ListView):
    model = Forum
    context_object_name = 'forums'
    template_name = "home.html"

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        kwargs['forum'] = self.forum
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.forum = get_object_or_404(Forum, pk=self.kwargs.get('pk'))
        queryset = self.forum.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
        return queryset
    
class PostListView(ListView):
    model = Post
    template_name = "topic_posts.html"
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.topic = get_object_or_404(Topic, forum__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    
    return render(request, 'new_topic.html', {'forum': forum,'form': form})

# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_update = timezone.now()  
            topic.save()
            
            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )                         

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
# def new_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm(request.POST)
#     return render(request, 'new_post.html', {'form': form})


# class NewPostView(View):
#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#         return render(request, 'new_post', {'form': form})
    
#     def get(self, request):
#         form = PostForm()
#         return render(request, 'new_post', {'form': form})
    
class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'new_post.html'
    
 
@method_decorator(login_required, name='dispatch')   
class PostUpdateView(UpdateView):
    model = Post
    template_name = "edit_post.html"
    fields = ['message',]
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.forum.pk, topic_pk=post.topic.pk)

# experimented changing the url patterns to names of the forums
# def forum_topics(request, name):
#     forum = get_object_or_404(Forum, name=name)
#     context = {'forum': forum}
#     return render(request, 'topics.html', context)