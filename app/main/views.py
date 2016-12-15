from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User 

@main.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
       old_name = session.get('name')
       if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
       session['name'] = form.name.data
       return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known',False),
                           current_time=datetime.utcnow())
                           
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.decs()).all()
    return render_template('user.html', user=user, posts=posts)
      
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit()：
       current_user.name = form.name.data
       current_user.location = form.location.data
       current_user.about_me = form.about_me.data
       db.session.add(current_user)
       flash('Your profile has been updated.')
       return redirect(url_for('.user', username=current_user.username))
    form.name.data  = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, user=user)
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data =post.body
    return render_template('edit_post.html', form=form)

@mian.route('/post/<int:id>')
def post(id):
  post = Post.query.get_or_404(id)
  return render_template('post.html', posts=[post])