from flask import Flask

app = Flask(__name__, static_folder="public", static_url_path="")
