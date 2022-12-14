from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (
    Article,
    Comment,
    Notice,
    Review,
    ReviewComment,
    Faq,
    Qna,
    QnaComment,
    Product,
    WishItem,
)
from .forms import (
    ArticleForm,
    CommentForm,
    NoticeForm,
    ReviewForm,
    ReviewCommentForm,
    FaqForm,
    QnaForm,
    ProductForm,
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):

    articles = Article.objects.order_by("-pk")
    context = {
        "articles": articles,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):

    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect("articles:index")
    else:
        article_form = ArticleForm()
    context = {
        "article_form": article_form,
    }
    return render(request, "articles/create.html", context)


def detail(request, pk):

    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.order_by("-pk")

    context = {
        "article": article,
        "comment_form": comment_form,
        "comments": comments,
    }

    return render(request, "articles/detail.html", context)


def delete(request, pk):

    article = Article.objects.get(pk=pk)
    article.delete()

    return redirect("articles:index")


def update(request, pk):

    article = Article.objects.get(pk=pk)

    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect("articles:detail", pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        "article_form": article_form,
    }
    return render(request, "articles/update.html", context)


@login_required
def c_create(request, pk):

    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()

    return redirect("articles:detail", pk)


@login_required
def c_delete(request, a_pk, c_pk):

    comment = Comment.objects.get(pk=c_pk)
    comment.delete()

    return redirect("articles:detail", a_pk)


@login_required
def like(request, pk):

    article = Article.objects.get(pk=pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)

    return redirect("articles:index")


def notice(request):

    notices = Notice.objects.order_by("-pk")

    page = request.GET.get("page", "1")
    paginator = Paginator(notices, 10)
    paginated_notices = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "notices": notices,
        "paginated_notices": paginated_notices,
        "max_index": max_index,
    }

    return render(request, "articles/notice.html", context)


@login_required
def n_create(request):

    if request.user.is_staff:
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            image = request.FILES.get("image")
            user = request.user
            Notice.objects.create(
                title=title,
                content=content,
                user=user,
                image=image,
            )
            pk = Notice.objects.order_by("-pk")[0].pk
            return redirect("articles:n_detail", pk)
        return render(request, "articles/n_create.html")
    return redirect("articles:notice")


def n_detail(request, pk):

    notice = Notice.objects.get(pk=pk)

    context = {
        "notice": notice,
    }

    return render(request, "articles/n_detail.html", context)


@login_required
def n_delete(request, pk):

    if request.user.is_staff:
        notice = Notice.objects.get(pk=pk)
        notice.delete()
    return redirect("articles:notice")


@login_required
def n_update(request, pk):

    if request.user.is_staff:
        notice = Notice.objects.get(pk=pk)

        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            if request.FILES.get("image"):
                image = request.FILES.get("image")
                notice.image = image
            elif request.POST.get("check"):
                notice.image = ""
            notice.title = title
            notice.content = content
            notice.save()
            return redirect("articles:n_detail", pk)
        context = {
            "notice": notice,
        }
        return render(request, "articles/n_update.html", context)
    return redirect("articles:notice")


def reviews(request):

    reviews = Review.objects.order_by("-pk")

    page = request.GET.get("page", "1")
    paginator = Paginator(reviews, 6)
    paginated_reviews = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "reviews": reviews,
        "paginated_reviews": paginated_reviews,
        "max_index": max_index,
    }

    return render(request, "articles/reviews.html", context)


@login_required
def r_create(request):

    if request.method == "POST":
        country = request.POST.get("country")
        title = request.POST.get("title")
        content = request.POST.get("content")
        grade = request.POST.get("grade")
        user = request.user
        image = request.FILES.get("image")
        image_two = request.FILES.get("image_two")
        thumbnail = request.FILES.get("thumbnail")
        Review.objects.create(
            country=country,
            title=title,
            content=content,
            grade=grade,
            user=user,
            image=image,
            image_two=image_two,
            thumbnail=thumbnail,
        )
        pk = Review.objects.order_by("-pk")[0].pk
        return redirect("articles:r_detail", pk)

    review_form = ReviewForm()

    context = {
        "review_form": review_form,
    }
    return render(request, "articles/r_create.html", context)


@login_required
def r_detail(request, pk):

    review = Review.objects.get(pk=pk)
    review_comment_form = ReviewCommentForm()
    comments = review.reviewcomment_set.order_by("-pk")

    context = {
        "review": review,
        "review_comment_form": review_comment_form,
        "comments": comments,
    }

    return render(request, "articles/r_detail.html", context)


@login_required
def r_delete(request, pk):

    review = Review.objects.get(pk=pk)
    review.delete()

    return redirect("articles:reviews")


@login_required
def r_update(request, pk):

    review = Review.objects.get(pk=pk)

    if request.method == "POST":
        country = request.POST.get("country")
        title = request.POST.get("title")
        content = request.POST.get("content")
        grade = request.POST.get("grade")
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            review.image = image
        elif request.POST.get("check_image"):
            review.image = ""
        if request.FILES.get("image_two"):
            image_two = request.FILES.get("image_two")
            review.image_two = image_two
        elif request.POST.get("check_image_two"):
            review.image_two = ""
        if request.FILES.get("thumbnail"):
            thumbnail = request.FILES.get("thumbnail")
            review.thumbnail = thumbnail
        elif request.POST.get("check_thumbnail"):
            review.thumbnail = ""

        review.country = country
        review.title = title
        review.content = content
        review.grade = grade
        review.save()

        return redirect("articles:r_detail", pk)

    review_form = ReviewForm()

    context = {
        "review_form": review_form,
        "review": review,
    }
    return render(request, "articles/r_update.html", context)


@login_required
def r_c_create(request, pk):

    review = Review.objects.get(pk=pk)

    comment = request.POST.get("comment")

    if comment != "":
        user = request.user
        ReviewComment.objects.create(content=comment, user=user, review=review)

    return redirect("articles:r_detail", pk)


@login_required
def r_c_delete(request, a_pk, c_pk):

    comment = ReviewComment.objects.get(pk=c_pk)
    comment.delete()

    return redirect("articles:r_detail", a_pk)


@login_required
def r_like(request, pk):

    review = Review.objects.get(pk=pk)

    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)

    return redirect("articles:reviews")


def faq(request):

    faqs = Faq.objects.order_by("-pk")

    page = request.GET.get("page", "1")
    paginator = Paginator(faqs, 10)
    paginated_faqs = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "faqs": faqs,
        "paginated_faqs": paginated_faqs,
        "max_index": max_index,
    }

    return render(request, "articles/faq.html", context)


@login_required
def faq_create(request):

    if request.user.is_staff:
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            user = request.user
            image = request.FILES.get("image")
            Faq.objects.create(
                title=title,
                content=content,
                user=user,
                image=image,
            )
            pk = Faq.objects.order_by("-pk")[0].pk
            return redirect("articles:faq_detail", pk)

        return render(request, "articles/faq_create.html")
    redirect("articles:faq")


def faq_detail(request, pk):

    faq = Faq.objects.get(pk=pk)

    context = {
        "faq": faq,
    }

    return render(request, "articles/faq_detail.html", context)


@login_required
def faq_delete(request, pk):

    if request.user.is_staff:
        faq = Faq.objects.get(pk=pk)
        faq.delete()

    return redirect("articles:faq")


@login_required
def faq_update(request, pk):

    if request.user.is_staff:

        faq = Faq.objects.get(pk=pk)

        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            if request.FILES.get("image"):
                image = request.FILES.get("image")
                faq.image = image
            elif request.POST.get("check"):
                faq.image = ""
            faq.title = title
            faq.content = content
            faq.save()
            return redirect("articles:faq_detail", pk)
        context = {
            "faq": faq,
        }
        return render(request, "articles/faq_update.html", context)
    return redirect("articles:faq")


def qna(request):

    qnas = Qna.objects.order_by("-pk")

    page = request.GET.get("page", "1")
    paginator = Paginator(qnas, 10)
    paginated_qnas = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {
        "qnas": qnas,
        "paginated_qnas": paginated_qnas,
        "max_index": max_index,
    }

    return render(request, "articles/qna.html", context)


@login_required
def qna_create(request):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.user
        image = request.FILES.get("image")
        Qna.objects.create(
            title=title,
            content=content,
            user=user,
            image=image,
        )
        pk = Qna.objects.order_by("-pk")[0].pk
        return redirect("articles:qna_detail", pk)

    return render(request, "articles/qna_create.html")


def qna_detail(request, pk):

    qna = Qna.objects.get(pk=pk)
    comments = qna.qnacomment_set.order_by("-pk")

    context = {
        "qna": qna,
        "comments": comments,
    }

    return render(request, "articles/qna_detail.html", context)


@login_required
def qna_delete(request, pk):

    qna = Qna.objects.get(pk=pk)
    qna.delete()

    return redirect("articles:qna")


@login_required
def qna_update(request, pk):

    qna = Qna.objects.get(pk=pk)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            qna.image = image
        elif request.POST.get("check"):
            qna.image = ""
        qna.title = title
        qna.content = content
        qna.save()

        return redirect("articles:qna_detail", pk)

    context = {
        "qna": qna,
    }
    return render(request, "articles/qna_update.html", context)


@login_required
def qna_c_create(request, pk):

    if request.user.is_staff:
        qna = Qna.objects.get(pk=pk)
        comment = request.POST.get("comment")
        user = request.user
        QnaComment.objects.create(content=comment, user=user, qna=qna)
    return redirect("articles:qna_detail", pk)


@login_required
def qna_c_delete(request, a_pk, c_pk):

    if request.user.is_staff:
        comment = QnaComment.objects.get(pk=c_pk)
        comment.delete()

    return redirect("articles:qna_detail", a_pk)


def search(request):
    search = request.GET.get("search", "")

    search_list = Review.objects.filter(
        Q(title__icontains=search) | Q(content__icontains=search)  # ??????
    )

    if search:
        if search_list:
            paginator = Paginator(search_list, 6)
            page = request.GET.get("page", "")
            boards = paginator.get_page(page)
            context = {"search": search, "boards": boards, "search_list": search_list}

            return render(
                request,
                "articles/search.html",
                context,
            )
        else:
            return render(request, "articles/searchfail.html")
    else:
        return render(request, "articles/searchfail.html")


def searchfail(request):
    return render(request, "articles/searchfail.html")


def product_main(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "articles/product_main.html", context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        "product": product,
    }
    return render(request, "articles/product_detail.html", context)


def wishlist(request, pk):
    product = Product.objects.get(pk=pk)

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)
    else:
        product.wishlist.add(request.user)
        
    return redirect('articles:product_detail', pk)

def wishitem(request, pk, self):
    wishitem = WishItem.objects.get(pk=pk)
    context = {
        "wishitem": wishitem,
    }
    return redirect('articles:product_detail', context)

