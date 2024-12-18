from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, ReviewForm
from app.models import User, Review
from app.auth.email import send_password_reset_email


# Helper function to validate safe URLs
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)

        # Get the 'next' parameter from the query string
        next_page = request.args.get('next')

        # Validate the 'next' parameter for safety
        if not next_page or not is_safe_url(next_page):
            next_page = url_for('main.index')  # Default to the home page if invalid

        # Perform the redirect
        return redirect(next_page)

    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


# New Routes for Posting and Viewing Reviews
@bp.route('/post_review', methods=['GET', 'POST'])
@login_required
def post_review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(body=form.review.data, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash(_('Your review has been posted!'))
        return redirect(url_for('auth.view_reviews'))
    return render_template('auth/post_review.html', title=_('Post Review'), form=form)


@bp.route('/reviews')
@login_required
def view_reviews():
    reviews = db.session.scalars(
        sa.select(Review).order_by(Review.timestamp.desc())).all()
    return render_template('auth/reviews.html', title=_('Reviews'), reviews=reviews)
