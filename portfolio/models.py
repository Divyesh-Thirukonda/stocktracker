from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class ArticleTitle(models.Model):
    title = models.CharField(max_length=255)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist = models.TextField(default='NVDA,HOOD')

    def get_watchlist_items(self):
        return self.watchlist.split(',')

    def add_to_watchlist(self, symbol):
        items = set(self.get_watchlist_items())
        items.add(symbol.upper())
        self.watchlist = ','.join(items)
        self.save()

    def remove_from_watchlist(self, symbol):
        items = set(self.get_watchlist_items())
        items.discard(symbol.upper())
        self.watchlist = ','.join(items)
        self.save()

    def __str__(self):
        return self.user.username + ' Profile'