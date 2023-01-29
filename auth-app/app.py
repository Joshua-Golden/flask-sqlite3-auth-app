from auth import create_app

app = create_app()
app.config['SECRET_KEY']="SECRET_KEY"

if __name__ == '__main__':
    app.run(debug=True)
