from routes_logic import *
from . import app

if app.config['DEBUG'] is True:
    #routes that are created only when application is in debug mode
    app.add_url_rule('/test_config', view_func=testConfig)

#routes related to user management
app.add_url_rule('/signin', view_func=signin, methods=['GET', 'POST'])
app.add_url_rule('/signout', view_func=signout)
app.add_url_rule('/signup', view_func=signup, methods=['GET', 'POST'])
app.add_url_rule('/changePassword', view_func=changePassword, methods=['GET', 'POST'])

#routes that control access to main page
app.add_url_rule('/', view_func=redirectToIndex)
app.add_url_rule('/index', view_func=index)

#routes used by AJAX requests
app.add_url_rule('/markRead/<article_id>', view_func=markRead)
app.add_url_rule('/markUnread/<article_id>', view_func=markUnread)
app.add_url_rule('/subscribe/<path:rss_url>', view_func=subscribe)
app.add_url_rule('/unsubscribe/<rss_id>', view_func=unsubscribe)
app.add_url_rule('/getUserInfo', view_func=getUserInfo)
app.add_url_rule('/getUnreadArticles/<feedId>', view_func=getUnreadArticles)
