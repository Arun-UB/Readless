from . import app, db
from flask.ext.mongoengine import DoesNotExist, ValidationError
from flask import Response, request, render_template, redirect, url_for, flash, jsonify
from flask.ext.login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Article, Reader, Feed, Subscription, NotAFeed

@app.route('/show_db_name')
def test_config():
    '''just a test, to be removed later'''
    return Response(app.config['MONGODB_DB'], mimetype='text/plain')

@app.route('/signin', methods=['GET', 'POST'])
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

@app.route("/signout")
@login_required
def signout():
    '''all logic to correctly logout a user'''
    logout_user()
    flash('logged out')
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
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
    return render_template('signup.html', error=error)

@app.route('/index')
def index():
    '''a simple index page'''
    return render_template('index.html')

@app.route('/markRead/<article_id>')
@login_required
def MarkRead(article_id):
    '''Logic to atomically mark an article as being read by the logged in user'''
    #TODO: test it
    #atomically remove current user from readers of given article
    Article.objects.filter(id = article_id).update_one(pull__readers__id = current_user.id)
    return jsonify(dict(status = 'Success'))

@app.route('/markUnread/<article_id>')
@login_required
def MarkUnread(article_id):
    '''Logic to atomically mark an article as being unread by the logged in user'''
    #TODO: test it
    new_reader = Reader(user = current_user)
    #atomically add current user to readers of given article
    Article.objects.filter(id = article_id).update_one(add_to_set__readers = new_reader)
    return jsonify(dict(status = 'Success'))

@app.route('/subscribe/<path:rss_url>')
@login_required
def Subscribe(rss_url):
    '''Logic to add a given rss feed to the db, if required, and subscribe the current user to this feed'''
    try:
        feed = Feed.get_or_construct(rss_url)
    except NotAFeed:
        return jsonify(dict(status = 'Error', message='The given url is not an rss feed url'))
    new_subscription = Subscription(feed_id = feed.id)
    #atomically add new feed subscription to current user
    User.objects.filter(id = current_user.id).update_one(add_to_set__subscriptions = new_subscription)
    return jsonify(dict(status = 'Success'))

@app.route('/unsubscribe/<path:rss_id>')
@login_required
def Unsubscribe(rss_id):
    '''Logic to unsubscribe a user from an rss feed, and all articles from that feed'''
    try:
        feed_to_be_removed = Feed.objects.get(id = rss_id)
        #atomically remove feed subscription from current user
        User.objects.filter(id = current_user.id).update_one(pull__subscriptions__feed_id = feed_to_be_removed.id)
        #atomically remove articles from unsubscribed feed for current user
        Article. objects.filter(feed_id = feed_to_be_removed.id).update(pull__readers__user_id = current_user.id)
        return jsonify(dict(status = 'Success'))
    except DoesNotExist:
        return jsonify(dict(status = 'Error', message = 'Given feed does not exist'))

@app.route('/getUserInfo')
@login_required
def GetUserInfo():
    '''Logic to get all feeds that a user has been subscribed to'''
    items = []
    for subscription in current_user.subscriptions:
        feed = Feed.objects.get(id = subscription.feed_id)
        UnreadArticleCount = Article.objects(feed_id = subscription.feed_id).count()
        item = dict(\
                    #feed_id is encoded as string to allow it to be sent as JSON
                    feed_id = str( subscription.feed_id )\
                    , feed_name = feed.name\
                    , UnreadCount = UnreadArticleCount\
                    )
        items.append(item)
    return jsonify(dict(\
            name = current_user.name\
            , email = current_user.email\
            , subscriptions = items\
            ))
