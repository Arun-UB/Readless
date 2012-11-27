from routes_logic import *
from . import app

app.add_url_rule('/show_db_name', view_func=test_config)
app.add_url_rule('/signin', view_func=signin)
app.add_url_rule('/signout', view_func=signout)
app.add_url_rule('/signup', view_func=signup)
app.add_url_rule('/changePassword', view_func=ChangePassword)
app.add_url_rule('/', view_func=redirect_to_index)
app.add_url_rule('/index', view_func=index)
app.add_url_rule('/markRead/<article_id>', view_func=MarkRead)
app.add_url_rule('/markUnread/<article_id>', view_func=MarkUnread)
app.add_url_rule('/subscribe/<path:rss_url>', view_func=Subscribe)
app.add_url_rule('/unsubscribe/<rss_id>', view_func=Unsubscribe)
app.add_url_rule('/getUserInfo', view_func=GetUserInfo)
app.add_url_rule('/getUnreadArticles/<feedId>', view_func=GetUnreadArticles)
