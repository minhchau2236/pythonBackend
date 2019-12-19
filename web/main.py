from app import create_app, db
from app.data import User, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post }

if __name__ == "__main__":
  app.run(debug=True,host="0.0.0.0")
