from server import app
import os

if __name__ == '__main__':
    env = os.environ.get('ENV')
    if env == 'pro':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
