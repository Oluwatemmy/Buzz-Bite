from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from buzz_bite import db
from buzz_bite.models import Post, Comments, Likes
from buzz_bite.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been Created Successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments =Comments.query.order_by(Comments.id.desc()).all()
    image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
    post.views += 1
    db.session.commit()
    # image = current_user.image_file
    return render_template('post.html', title=post.title, comments=comments, post=post, image_file=image_file)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been Updated Successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been Deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    name = request.form.get('name')
    email = request.form.get('email')

    if not text:
        flash('Comment section cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comments = Comments(text=text, author=current_user.id, name=name, email=email, post_id=post_id)
            db.session.add(comments)
            db.session.commit()
            flash('Your comment was posted successfully.', category='success')
        else:
            flash('Post does not exists', category='error')

    return redirect(url_for('posts.post', post_id=post_id))


@posts.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Likes.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post does not exists.", category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Likes(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('posts.post', post_id=post_id))


# @posts.route("/view-post/<post_id>", methods=['GET'])
# @login_required
# def view(post_id):
#     post = Post.query.filter_by(id=post_id)
#     views = Views.query.filter_by(author=current_user.id, post_id=post_id).first()

#     if not post:
#         flash("Post does not exists.", category='error')

#     for view in views:
#         post