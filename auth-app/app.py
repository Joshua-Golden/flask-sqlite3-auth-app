from auth import create_app

app = create_app()
app.config['SECRET_KEY']="a407e11ecc0f751741fb542feaf26708"

if __name__ == '__main__':
    app.run(debug=True)