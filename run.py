from app import create_app, db

app = create_app()
port = 5433

if __name__ == '__main__':
    print('Starting server...')
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(debug=True, port=port)
