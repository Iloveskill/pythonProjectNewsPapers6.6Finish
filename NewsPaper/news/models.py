from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self):
        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(Sum('rating_news')).get('rating_news__sum') * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']
        rating_of_comments_under_posts_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']

        self.rating = rating_of_comments_by_author + rating_of_posts_by_author + rating_of_comments_under_posts_of_author
        self.save()

    def __str__(self) -> str:
        return Author.objects.filter(pk=self.id).values_list('user__username')[0][0]

sport = 'SP'
policy = 'PO'
education = 'ED'
culture = 'CU'
technology = "TECH"

SUBJECTS = [
        ("policy", 'Политика'),
        ("culture", 'Культура'),
        ("education", 'Образование'),
        ("sport", 'Спорт'),
        ("technology", 'Технологии')
]

class Category(models.Model):
    subject = models.CharField(max_length=10, choices=SUBJECTS, default=sport, unique=True)

    def __str__(self) -> str:
        return self.subject

Article = "AT"
News = "NW"

POST_TYPES = [
    ('Article', 'Статья'),
    ('News', 'Новость'),
]


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    article_news = models.CharField(max_length=10, choices=POST_TYPES, default=Article, verbose_name='Вид поста')
    date_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    title = models.CharField(max_length=255, default='Defaullt title', verbose_name='Заголовок')
    content = models.CharField(max_length=2012, default='Default content', verbose_name='Контент')
    rating_news = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        return f'{self.title.title()}:{self.text.title()}:{self.date_in}'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    content =  models.CharField(max_length=512, default='Defaulet comment', verbose_name='Коментарий')
    comment_time_in = models.DateTimeField(auto_now_add=True, verbose_name='Время создания коментария')
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()