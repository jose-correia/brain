from .. import bp
from flask import render_template, current_app, request, redirect, url_for, jsonify
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.levels_handler import LevelsHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from flask_login import current_user


# Student App routes
@bp.route('/students-app', methods=['GET'])
@allowed_roles(['admin'])
def students_app_dashboard():
    
    return render_template('admin/students_app/students_app_dashboard.html')

@bp.route('/students', methods=['GET'])
@allowed_roles(['admin'])
def students_dashboard():
    search = request.args.get('search')

    # handle search bar requests
    if search is not None:
        students_list = StudentsFinder.get_from_search(search)
    
    else:
        search = None
        students_list = StudentsFinder.get_all()
    
    if students_list is None or len(students_list) == 0:
        error = 'No results found'
        return render_template('admin/students_app/students/students_dashboard.html', students=None, error=error, search=search, current_user=current_user)
    
    return render_template('admin/students_app/students/students_dashboard.html', students=students_list, error=None, search=search, current_user=current_user)

@bp.route('/student/<string:student_external_id>/ban', methods=['POST'])
@allowed_roles(['admin'])
def ban_student(student_external_id):
    student = StudentsFinder.get_from_external_id(student_external_id)
    if student is None:
        return APIErrorValue('Couldnt find student').json(500)

    banned_student = StudentsHandler.create_banned_student(student)
    if(banned_student is None):
        return APIErrorValue('Error banning student').json(500)

    UsersHandler.delete_user(student.user)
    StudentsHandler.delete_student(student)

    return redirect(url_for('admin_api.students_dashboard'))

@bp.route('/squads', methods=['GET'])
@allowed_roles(['admin'])
def squads_dashboard():
    
    return render_template('admin/students_app/students_app_dashboard.html')

@bp.route('/rewards', methods=['GET'])
@allowed_roles(['admin'])
def rewards_dashboard():
    
    return render_template('admin/students_app/students_app_dashboard.html')

@bp.route('/levels', methods=['GET'])
@allowed_roles(['admin'])
def levels_dashboard():
    levels = LevelsFinder.get_all_levels()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, error='No levels found')    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, error=None)

@bp.route('/create-level', methods=['POST'])
@allowed_roles(['admin'])
def create_level():
    value = request.form.get('value', None)
    points = request.form.get('points', None)

    if(value is None or points is None):
        return APIErrorValue('Invalid value or points').json(500)

    levels = LevelsFinder.get_all_levels()

    if(len(levels) > 0 and int(levels[-1].value + 1) != int(value)):
        return APIErrorValue('Invalid level value').json(500)

    level = LevelsHandler.create_level(value=value, points=points)
    if(level is None):
        return APIErrorValue('Error creating level').json(500)

    if(len(levels) == 0 and level.value == 0):
        students = StudentsFinder.get_from_parameters({'level_id': None})
        for student in students:
            StudentsHandler.update_student(student, level_id = level.id)

    levels = LevelsFinder.get_all_levels()

    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, error='No levels found')    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, error=None)

@bp.route('/level/<string:level_external_id>/delete', methods=['POST'])
@allowed_roles(['admin'])
def delete_level(level_external_id):
    level = LevelsFinder.get_level_from_external_id(level_external_id)
    if level is None:
        return APIErrorValue('Couldnt find level').json(500)

    levels = LevelsFinder.get_all_levels()
    if(len(levels) == 0 or (len(levels) > 0 and levels[-1] == level)):
        students = StudentsFinder.get_from_level_or_higher(level)
        previous_level = LevelsFinder.get_level_by_value(level.value - 1)
        
        if(previous_level is None):
            for student in students:
                StudentsHandler.update_student(student, level_id = None, total_points=0)
        else:
            for student in students:
                StudentsHandler.update_student(student, level_id = previous_level.id, total_points=previous_level.points)

        LevelsHandler.delete_level(level)

    levels = LevelsFinder.get_all_levels()

    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, error='No levels found')    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, error=None)

@bp.route('/tags', methods=['GET'])
@allowed_roles(['admin'])
def tags_dashboard():
    tags = TagsFinder.get_all()
    if(tags is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=None, error='No tags found')

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None)

@bp.route('/create-tag', methods=['POST'])
@allowed_roles(['admin'])
def create_tag():
    tags = TagsFinder.get_all()
    name = request.form.get('name',None)
    print(name)
    if(name is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='Failed to create tag')

    tag = TagsHandler.create_tag(name=name)
    print(tag)
    if(tag is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='Failed to create tag')

    tags = TagsFinder.get_all()

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None)

@bp.route('/tag/<string:tag_external_id>/delete', methods=['POST'])
@allowed_roles(['admin'])
def delete_tag(tag_external_id):
    tag = TagsFinder.get_from_external_id(tag_external_id)
    if tag is None:
        return APIErrorValue('Couldnt find tag').json(500)

    TagsHandler.delete_tag(tag)

    tags = TagsFinder.get_all()
    if(tags is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='No tags found')    

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None)
