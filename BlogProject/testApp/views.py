from django.shortcuts import render,get_object_or_404
from testApp.models import Post,Comment
from testApp.forms import CommentForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
from taggit.models import Tag
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])


    paginator=Paginator(post_list,2)#paginator concept
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(page.num_pages)#paginator concept
    return render(request,'testApp/post_list.html',{'post_list':post_list,'tag':tag})


def postdetailview(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                           status="published",
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'testApp/post_detail.html',{'form':form,'post':post,'comments':comments,'csubmit':csubmit})

#Email Configuration
from django.core.mail import send_mail
from testApp.forms import EmailSendForm

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post At:\n{}\n\n{}\'Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'djangotesting1909@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'testApp/email.html',{'form':form,'post':post,'sent':sent})
