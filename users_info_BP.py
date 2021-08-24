from flask import Blueprint, redirect, url_for
from flask_security import auth_required
from form_function import *

users_info_BP = Blueprint('users_info_BP', __name__, url_prefix='/users_info')


@users_info_BP.route("/")
@auth_required()
@admin_role_required
def sudo_view_users_info():
    admins = db_session.query(Users.id).join(RolesUsers, Users.id == RolesUsers.user_id). \
        join(Roles, Roles.id == RolesUsers.role_id).filter(Roles.name == "Admin")
    users = db_session.query(Users).filter(Users.id.not_in(admins)).all()
    return render_template("users_info.html", users=users)


@users_info_BP.route("/<user_id>/enable")
@auth_required()
@admin_role_required
def sudo_enable_enable(user_id):
    from app import user_datastore

    user = db_session.query(Users).filter(Users.id == user_id).first()
    if not user:
        return render_template("error.html", message="This user not exist")
    user_datastore.activate_user(user)
    db_session.commit()
    return redirect(url_for("users_info_BP.sudo_view_users_info"))


@users_info_BP.route("/<user_id>/disable")
@auth_required()
@admin_role_required
def sudo_enable_disable(user_id):

    user = db_session.query(Users).filter(Users.id == user_id).first()
    if not user:
        return render_template("error.html", message="This user not exist")

    from app import user_datastore
    user_datastore.deactivate_user(user)
    db_session.commit()
    return redirect(url_for("users_info_BP.sudo_view_users_info"))


@users_info_BP.route("/<user_id>/delete")
@auth_required()
@admin_role_required
def sudo_delete_user(user_id):
    user_query = db_session.query(Users).filter(Users.id == user_id)

    if not user_query.first():
        return render_template("error.html", message="This user not exist")

    for f in user_query.forms_created:
        delete_form(f.id)

    db_session.query(Answers).filter(Answers.user_id == user_id).delete()

    user_query.delete()
    db_session.commit()
    return redirect(url_for("users_info_BP.sudo_view_users_info"))


@users_info_BP.route("/form/<form_id>/delete")
@auth_required()
@admin_role_required
def sudo_delete_form(form_id):
    form = db_session.query(Forms).filter(Forms.id == form_id).first()
    if not form:
        return render_template("error.html", message="This form not exist")
    delete_form(form_id)
    return redirect(url_for("users_info_BP.sudo_view_users_info"))
