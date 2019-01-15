from flask import Flask, render_template

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/monitoring', methods=['GET'])
def monitoring():
    return 'Monitoring'

@app.route('/about', methods=['GET'])
def about():
    return 'About'
