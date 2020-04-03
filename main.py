import os

import requests
from flask import Flask, render_template, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


def query_latinizer(fact):
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    payload = f"input_text={fact}"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(url,
                             payload.encode("utf-8"),
                             headers=headers,
                             allow_redirects=False)

    return response.headers["Location"]


def get_latinized(redirect_url):
    response = requests.get(redirect_url)
    quote = ""

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        body = soup.find_all("body")
        quote = body[0].getText().strip("\nPig Latin\nEsultray\n")

    return quote.strip()


@app.route('/')
def home():
    fact = get_fact()
    redirect_url = query_latinizer(fact)
    pl_fact = get_latinized(redirect_url)

    return render_template("base.jinja2",
                           pl_fact=pl_fact,
                           redirect_url=redirect_url,
                           original_text=fact)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

