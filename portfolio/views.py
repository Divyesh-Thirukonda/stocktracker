import logging
import requests
from django.shortcuts import render, redirect
from .models import Project, ArticleTitle
from portfolio.utils.fetch_data import fetch_nyt_article_title, fetch_forex, fetch_gainLose, fetch_companyOverview, fetch_companyQuote, fetch_searchResults
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import UserProfile
from django.http import JsonResponse

# Configure logging
logger = logging.getLogger(__name__)

def home(request):
    projects = Project.objects.all()
    article_title = ArticleTitle.objects.first()

    # Fetch the latest NYT article title
    try:
        nyt_article_title = fetch_nyt_article_title()
        if (nyt_article_title):
            ArticleTitle.objects.update_or_create(id=1, defaults={'title': nyt_article_title})
            article_title = ArticleTitle.objects.first()
    except Exception as e:
        logger.error(f"Error fetching NYT article title: {e}")
        nyt_article_title = None

    # Fetch forex data
    try:
        forex_data = fetch_forex()
    except Exception as e:
        logger.error(f"Error fetching forex data: {e}")
        forex_data = None

    # Fetch top gainers and losers data
    try:
        data = fetch_gainLose()
        top_gainers = data.get('top_gainers', [])[:5]
        top_losers = data.get('top_losers', [])[:5]
    except Exception as e:
        logger.error(f"Error fetching top gainers and losers data: {e}")
        top_gainers = []
        top_losers = []

    
    # Fetch user's watchlist if authenticated

    watchlist_data = []
    watchlist = []
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
        watchlist = user_profile.get_watchlist_items() # or watchlist = request.user.watchlist.all()

        for symbol in watchlist:
            print(symbol)
            stock_data = fetch_companyQuote(symbol)  #.split(':')[0]
            if stock_data:
                stock_data['symbol'] = symbol.upper()
                stock_data['is_up'] = (float(stock_data['change']) >= 0)
                watchlist_data.append(stock_data)
        
        if watchlist_data is not None:
            print(watchlist_data)
            watchlist_data.sort(key=lambda x: float(x['change_percent'].split('%')[0]), reverse=True) #.split('%')[0]

    return render(request, 'portfolio/home.html', {
        'projects': projects,
        'article_title': article_title,
        'forex_data': forex_data,
        'top_gainers': top_gainers,
        'top_losers': top_losers,
        'watchlist': watchlist_data
    })

def quote_detail(request, symbol):
    stock_data = fetch_companyQuote(symbol)  #.split(':')[0]
    if stock_data:
        stock_data['symbol'] = symbol.upper()

    income_statement_data = fetch_companyOverview(symbol)

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    watchlist_symbols = user_profile.get_watchlist_items()

    in_watchlist = symbol in watchlist_symbols

    context = {
        'stock_data': stock_data,
        "income_statement_data": income_statement_data,
        'in_watchlist': in_watchlist,
    }
    return render(request, 'portfolio/quote_detail.html', context)

@login_required
def add_to_watchlist(request, symbol):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.add_to_watchlist(symbol)
    return redirect('quote', symbol=symbol)

@login_required
def remove_from_watchlist(request, symbol):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.remove_from_watchlist(symbol)
    return redirect('home')


def search(request):
    keyword = request.GET.get('keyword', '')
    results = fetch_searchResults(keyword)
    return JsonResponse(results, safe=False)
