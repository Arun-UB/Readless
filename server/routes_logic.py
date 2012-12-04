from . import app, db
from flask.ext.mongoengine import DoesNotExist, ValidationError
from flask import Response, request, render_template, redirect, url_for, flash, jsonify
from flask.ext.login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Article, Reader, Feed, Subscription, NotAFeed
import time

def testConfig():
    '''just a test, is only accessible when in DEBUG mode'''
    return Response(app.config['MONGODB_DB'], mimetype='text/plain')

def signin():
    """all logic to check whether a user exists and log him in"""
    error = None
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.form['email'])
            if check_password_hash(user.password_hash, request.form['password']) is True:
                login_user(user)
                return redirect(url_for('index'))
            else:
                error = 'Incorrect Password'
        except DoesNotExist:
            error = 'User with this email id does not exist'
    return render_template('login.html', error=error)

@login_required
def signout():
    '''all logic to correctly logout a user'''
    logout_user()
    flash('logged out')
    return redirect(url_for('signin'))

def signup():
    '''all logic to correctly signup a user'''
    error = None
    if request.method == 'POST':
        new_user = User(\
                        email = request.form['email']\
                        , name = request.form['name']\
                        , password_hash = generate_password_hash(request.form['password'])\
                        )
        try:
            new_user.save(safe = True, force_insert=True)#waits for result and forces inserts
            flash('successfully signed up')
            return redirect(url_for('signin'))
        except db.NotUniqueError:
            error = 'User with this email id already exists'
        except ValidationError as e:
            if e.errors.get('email'):
                error = 'Invalid email'
            elif e.errors.get('name'):
                error = 'Invalid name'
            else:
                app.logger.error('An unknown validation error occured while trying to sign up a user')
                error = 'An internal server error stopped you from signing up'
    return render_template('signup.html', error=error)

@login_required
def changePassword():
    '''Logic to change the password of the logged in user'''
    error = None
    if request.method == 'POST':
        if check_password_hash(current_user.password_hash, request.form['Old_Password']) is False:
            error = 'incorrect original password'
        elif(request.form['New_Password'] != request.form['Confirm_Password']):
            error = 'New password and confirm password do not match'
        else:
            current_user.password_hash = generate_password_hash(request.form['New_Password'])
            try:
                current_user.save(safe = True)
                flash('Your password has been changed')
                return redirect(url_for('index'))
            except db.OperationError:
                error = 'Failed to save new password, try again later'
    return render_template('changePassword.html', error = error)

def redirectToIndex():
    '''a simple redirect to the index page'''
    return redirect(url_for('index'))

@login_required
def index():
    '''returns main index page containing all the files angular needs on the client side'''
    return render_template('index.html')

@login_required
def markRead(article_id, interest):
    '''Logic to atomically mark an article as being read by the logged in user'''
    #TODO: test it
    #atomically remove current user from readers of given article, add them to the interested/uninterested list
    if interest is 0:
        Article.objects(id = article_id).update_one(\
                pull__readers__user_id = current_user.id\
                , add_to_set__uninterested_users = current_user.id\
                )
    else:
        Article.objects(id = article_id).update_one(\
                pull__readers__user_id = current_user.id\
                , add_to_set__interested_users = current_user.id\
                )
    return jsonify(dict(status = 'Success'))

@login_required
def markUnread(article_id):
    '''Logic to atomically mark an article as being unread by the logged in user'''
    #TODO: test it
    new_reader = Reader(user_id = current_user.id)
    #atomically add current user to readers of given article
    number_of_items_affected = Article.objects(id = article_id).update_one(add_to_set__readers = new_reader)
    if number_of_items_affected is 1:
        return jsonify(dict(status = 'Success'))
    else:
        return jsonify(dict(\
                status = 'Error'\
                , message = 'No articles matched the given id'\
                ))

@login_required
def subscribe(rss_url):
    '''Logic to add a given rss feed to the db, if required, and subscribe the current user to this feed'''
    try:
        feed = Feed.get_or_construct(rss_url)
    except NotAFeed:
        return jsonify(dict(status = 'Error', message='The given url is not an rss feed url'))
    new_subscription = Subscription(feed_id = feed.id)
    #atomically add new feed subscription to current user
    number_of_items_affected = User.objects(id = current_user.id).update_one(add_to_set__subscriptions = new_subscription)
    new_reader = Reader(user_id = current_user.id)
    #atomically add current user to readers of all articles in subscribed feed
    Article.objects(feed_id = feed.id).update(add_to_set__readers = new_reader)
    if number_of_items_affected is 1:
        return jsonify(dict(status = 'Success'))
    else:
        return jsonify(dict(\
                status = 'Error'\
                , message = 'Unable to subscribe'\
                ))

@login_required
def unsubscribe(rss_id):
    '''Logic to unsubscribe a user from an rss feed, and all articles from that feed'''
    try:
        feed_to_be_removed = Feed.objects.get(id = rss_id)
        #atomically remove feed subscription from current user
        User.objects(id = current_user.id).update_one(pull__subscriptions__feed_id = feed_to_be_removed.id)
        #atomically remove articles from unsubscribed feed for current user
        Article.objects(feed_id = feed_to_be_removed.id).update(pull__readers__user_id = current_user.id)
        return jsonify(dict(status = 'Success'))
    except DoesNotExist:
        return jsonify(dict(status = 'Error', message = 'Given feed does not exist'))

@login_required
def getUserInfo():
    '''Logic to get all required information about a user '''
    items = []
    for subscription in current_user.subscriptions:
        feed = Feed.objects.get(id = subscription.feed_id)
        UnreadArticleCount = Article.objects(feed_id = subscription.feed_id, readers__user_id = current_user.id).count()
        item = dict(\
                    #feed_id is encoded as string to allow it to be sent as JSON
                    feed_id = str( subscription.feed_id )\
                    , feed_name = feed.name\
                    , site_url = feed.site_url\
                    , UnreadCount = UnreadArticleCount\
                    )
        items.append(item)
    return jsonify(dict(\
            name = current_user.name\
            , email = current_user.email\
            , subscriptions = items\
            ))

@login_required
def getUnreadArticles(feedId):
    '''Logic to get unread articles for a particular subscribed feed for the current user'''
    items = []
    for article in Article.objects(feed_id = feedId, readers__user_id = current_user.id):
        user_score = 0.5
        for reader in article.readers:
            if reader.user_id == current_user.id: 
                user_score = reader.score
        item = dict(\
                article_id = str( article.id )\
                , title = article.features.title\
                , content_snippet = article.features.content_snippet\
                , source_link = article.source_url\
                , time_stamp = time.mktime(article.time_stamp.timetuple())\
                , score = user_score\
                )
        items.append(item)
    return jsonify(dict(\
            articles = items\
            ))
