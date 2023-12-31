from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from django.views.generic import ListView,DetailView
from .forms import EmailPostForm,CommentForm,PostForm,SearchForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.
class PostList(ListView):
    model=Post
    context_object_name='posts'
    template_name='blog/post/list.html'
    paginate_by=3
    
def post_list(request, tag_slug=None):
        post_list = Post.published.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_list = post_list.filter(tag__in=[tag])
        # Pagination with 3 posts per page
        paginator = Paginator(post_list, 3)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
        # If page_number is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        return render(request,
        'blog/post/list.html',
        {'posts': posts,
        'tag': tag})
def post_detail(request, slug,day,month,year):
    post = get_object_or_404(Post,slug=slug,
                             publish__year=year,
                            publish__month=month,
                            publish__day=day)
    comments = post.comments.filter(active=True)
    all_tags=post.tag.values_list('id',flat=True)
    similar_posts=Post.published.filter(tag__in=all_tags).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags','-publish')[:4]
    
    # Form for users to comment
    form = CommentForm()
    return render(request,'blog/post/detail.html',{'post': post,'comments': comments,
 'form': form,'similar_posts': similar_posts})
class PostDetail(DetailView):
    model=Post
    template_name='blog/post/detail.html'



def post_share(request,post_id):
    
    post=get_object_or_404(Post,id=post_id)
    sent = False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'mahmoudsnasr77@gmail.com',
            [cd['to_email']])
            sent = True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form,'post':post,'sent': sent})
@login_required
def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    comment=None
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
    return render(request, 'blog/post/comment.html',
    {'post': post,
    'form': form,
    'comment': comment})
@login_required
def post_publish(request):
    
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('blog:post_list')
            
    form=PostForm()

    return render(request, 'blog/post/post.html',
    {
    'form': form})
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title',weight="A")+ SearchVector('body',weight="B")
            search_query = SearchQuery(query, config='arabic')
            results = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            #results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,'blog/post/search.html',{'form': form,'query': query,'results': results})
    