import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            gissning = int(request.form['gissning'])
            hemligt_tal = int(request.cookies.get('hemligt_tal', random.randint(1, 100)))
            gissningar_kvar = int(request.cookies.get('gissningar_kvar', 7)) - 1
            
            if gissning == hemligt_tal:
                meddelande = "Rätt gissat! Du vann!"
                resp = redirect(url_for('index'))
                resp.set_cookie('hemligt_tal', '', expires=0)  # Rensa cookies vid vinst
                resp.set_cookie('gissningar_kvar', '', expires=0)
                return resp
            elif gissningar_kvar == 0:
                meddelande = f"Du förlorade! Talet var {hemligt_tal}."
                resp = redirect(url_for('index'))
                resp.set_cookie('hemligt_tal', '', expires=0)  # Rensa cookies vid förlust
                resp.set_cookie('gissningar_kvar', '', expires=0)
                return resp
            elif gissning < hemligt_tal:
                meddelande = "För lågt!"
            else:
                meddelande = "För högt!"
                
            resp = render_template('index.html', meddelande=meddelande, gissningar_kvar=gissningar_kvar)
            resp.set_cookie('hemligt_tal', str(hemligt_tal))
            resp.set_cookie('gissningar_kvar', str(gissningar_kvar))
            return resp
        except ValueError:
            meddelande = "Ogiltig inmatning. Ange ett heltal."
            return render_template('index.html', meddelande=meddelande)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)