from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
import config
app = Flask(__name__)
app.config.from_object(config)

import models
import routes


