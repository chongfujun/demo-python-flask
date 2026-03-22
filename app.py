"""Flask Blog - Blueprint structure, NO AUTH"""
from flask import Flask
from models import db
from models.post import Post

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes import register_routes
    register_routes(app)

    @app.context_processor
    def inject_globals():
        from modules import system_commands
        return {'app_name': 'Flask Blog', 'version': system_commands.get_current_timestamp()}

    return app

def init_db():
    db.create_all()
    if not Post.query.first():
        post = Post(title='Welcome', content='Sample post', slug='welcome', author_id=1, published=True)
        db.session.add(post)
        db.session.commit()

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)