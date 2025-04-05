from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponse
from django.core.paginator import Paginator


from .models import ArticlePost, Comment, Contact, GlobalCounter
from .forms import CommentForm, ContactForm


class ArticleList(generic.ListView):
    queryset = ArticlePost.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_list'

    def get_context_data(self, **kwargs):
        counter, created = GlobalCounter.objects.get_or_create(key="blog_page_visits")

        counter.count += 1
        counter.save()
        
        return super().get_context_data(**kwargs)
    
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()

        paginator = Paginator(qs, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if request.htmx:
            return render(request, 'blog/partials/partial_blog_list.html', {'blog_list': page_obj})
        else:
            return render(request, 'blog/blog_list.html', {'blog_list': page_obj})


class ArticleDetail(generic.DetailView):
    model = ArticlePost
    template_name = 'blog/blogpost_detail.html'
    http_method_names = ['get', 'post', 'put']


    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        blog_post = get_object_or_404(ArticlePost, slug=self.kwargs['slug'])
        comments = blog_post.comments.filter(active=True)

        blog_post.views += 1
        blog_post.save()
        
        context.update({
            "blog_post": blog_post,
            "comments": comments,
            'comment_form': CommentForm(),
            # 'new_comment': None, 

        })

        return context
    
    def post(self, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = self.get_object()
            new_comment.save()
            if self.request.htmx:
                return HttpResponse('<h2 class="text-center text-2xl font-bold text-green-600">Your comment has been sent.</h2>')
        else:
            comment_form = CommentForm(self.request.POST)

        return render(self.request, self.template_name, 
            {'blog_post': self.get_object, 
             'comments': self.get_object().comments.filter(active=True), 
             'new_comment': new_comment, 
             'comment_form': comment_form
            }
        )



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return HttpResponse('<h2 class="text-center text-2xl font-bold text-green-600">Thank you! Your message has been sent.</h2>')
            return render(request, 'base/contact_success.html')
        else:
            return render(request, "base/contact_me.html", {'form': form})
    else:
        counter, created = GlobalCounter.objects.get_or_create(key="contact_page_visits")

        # Increment the count
        counter.count += 1
        counter.save()
        form = ContactForm()

    return render(request, 'base/contact_me.html', {'form': form})


class ContactView(View):
    template_name = 'base/contact_us.html'
    success_template = 'base/contact_success.html'

    def get(self, request):
        counter, created = GlobalCounter.objects.get_or_create(key="contact_page_visits")
        counter.count += 1
        counter.save()

        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.htmx:
                return HttpResponse(
                    '<h2 class="text-center text-2xl font-bold text-green-600">'
                    'Thank you! Your message has been sent.</h2>'
                )
            return render(request, self.success_template)
        return render(request, self.template_name, {'form': form})
