from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.news_finder import NewsFinder
from jeec_brain.handlers.news_handler import NewsHandler
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from flask_login import current_user


# News routes
@bp.route('/news', methods=['GET'])
@allow_all_roles
def news_dashboard():
    search_parameters = request.args
    day = request.args.get('day')

    # handle search bar requests
    if day is not None:
        search = day
        news_list = NewsFinder.get_news_from_day(day)

    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search by day'

        news_list = NewsFinder.get_news_from_parameters(search_parameters)

    # request endpoint with no parameters should return all news
    else:
        search = None
        news_list = NewsFinder.get_all_news()

    if news_list is None or len(news_list) == 0:
        error = 'No results found'
        return render_template('admin/news/news_dashboard.html', news=None, error=error, search=search, role=current_user.role.name)

    return render_template('admin/news/news_dashboard.html', news=news_list, error=None, search=search, role=current_user.role.name)


@bp.route('/new-news', methods=['GET'])
@allowed_roles(['admin'])
def add_news_dashboard():

    return render_template('admin/news/add_news.html', error=None)


@bp.route('/new-news', methods=['POST'])
@allowed_roles(['admin'])
def create_news():

    # extract form parameters
    description = request.form.get('description')
    day = request.form.get('day')
    video_url = request.form.get('video_url')

    # create new news
    news = NewsHandler.create_news(
            description=description,
            day=day,
            video_url=video_url
        )

    if news is None:
        return render_template('admin/news/add_news.html', error="Failed to create news!")

    if request.files:
        image_file = request.files.get('news_image', None)

        if image_file:
            result, msg = NewsHandler.upload_image(image_file, str(news.external_id))

            if result == False:
                NewsHandler.delete_news(news)
                return render_template('admin/news/add_news.html', error=msg)

    return redirect(url_for('admin_api.news_dashboard'))


@bp.route('/news/<string:news_external_id>', methods=['GET'])
@allowed_roles(['admin'])
def get_news(news_external_id):
    news = NewsFinder.get_news_from_external_id(news_external_id)
    image = NewsHandler.find_image(image_name=str(news.external_id))

    return render_template('admin/news/update_news.html', news=news, image=image, error=None)

@bp.route('/news/<string:news_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_news(news_external_id):
    news = NewsFinder.get_news_from_external_id(news_external_id)

    if news is None:
        return APIErrorValue('Couldnt find news').json(500)

    # extract form parameters
    description = request.form.get('description')
    day = request.form.get('day')
    video_url = request.form.get('video_url')

    updated_news = NewsHandler.update_news(
        news=news,
        description=description,
        day=day,
        video_url=video_url
    )

    if updated_news is None:
        return render_template('admin/news/update_news.html', news=news, error="Failed to update news!")

    if request.files:
        image_file = request.files.get('news_image', None) 

        if image_file:
            result, msg = NewsHandler.upload_image(image_file, str(updated_news.external_id))
            if result == False:
                return render_template('admin/news/update_news.html', news=news, error=msg)

    return redirect(url_for('admin_api.news_dashboard'))


@bp.route('/news/<string:news_external_id>/delete', methods=['GET'])
@allowed_roles(['admin'])
def delete_news(news_external_id):
    news = NewsFinder.get_news_from_external_id(news_external_id)

    if news is None:
        return APIErrorValue('Couldnt find news').json(500)

    if NewsHandler.delete_news(news):
        return redirect(url_for('admin_api.news_dashboard'))

    else:
        return render_template('admin/news/update_news.html', news=news, error="Failed to delete news!")