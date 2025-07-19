from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
import config


app = Flask(__name__)
app.config.from_object(config)

import config
import controllers.admin_add_lot, controllers.admin_all_users, controllers.admin_del_lot, controllers.admin_new_or_edit_parklot, controllers.admin_O_spot, controllers.admin_search, controllers.admin_summary, controllers.admin_view_spot, controllers.dashboard, controllers.edit_profile, controllers.index, controllers.login, controllers.logout, models.models, controllers.signup, controllers.user_book_spot, controllers.user_release_spot, controllers.user_search_lot, controllers.user_summary


