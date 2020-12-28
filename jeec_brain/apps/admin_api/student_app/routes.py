from .. import bp
from flask import render_template, current_app, request, redirect, url_for, jsonify
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.levels_handler import LevelsHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.handlers.rewards_handler import RewardsHandler
from jeec_brain.handlers.events_handler import EventsHandler
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

@bp.route('/levels', methods=['GET'])
@allowed_roles(['admin'])
def levels_dashboard():
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, rewards=rewards, error='No levels found', current_user=current_user)    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.route('/create-level', methods=['POST'])
@allowed_roles(['admin'])
def create_level():
    value = request.form.get('value', None)
    points = request.form.get('points', None)
    reward_id = request.form.get('reward', None)
    if(reward_id == ""):
        reward_id = None

    if(value is None or points is None):
        return APIErrorValue('Invalid value or points').json(500)

    if(reward_id is not None):
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if(reward is None):
            return APIErrorValue('Invalid reward Id')
        
        reward_id = reward.id

    levels = LevelsFinder.get_all_levels()

    if(len(levels) > 0 and int(levels[-1].value + 1) != int(value)):
        return APIErrorValue('Invalid level value').json(500)

    level = LevelsHandler.create_level(value=value, points=points, reward_id=reward_id)
    if(level is None):
        return APIErrorValue('Error creating level').json(500)

    if(len(levels) == 0 and level.value == 0):
        students = StudentsFinder.get_from_parameters({'level_id': None})
        for student in students:
            StudentsHandler.update_student(student, level_id = level.id)

    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, rewards=rewards, error='No levels found', current_user=current_user)    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.route('/level/<string:level_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_level(level_external_id):
    level = LevelsFinder.get_level_from_external_id(level_external_id)
    if level is None:
        return APIErrorValue('Couldnt find level').json(500)

    reward_id = request.form.get('reward', None)
    if(reward_id == ""):
        reward_id = None
    if(reward_id is not None):
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if(reward is None):
            return APIErrorValue('Invalid reward Id')
        
        reward_id = reward.id

    level = LevelsHandler.update_level(level, reward_id=reward_id)
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if(level is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error='Failed to update reward', current_user=current_user)

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

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
    rewards = RewardsFinder.get_all_rewards()
    if(levels is None):
        return render_template('admin/students_app/levels/levels_dashboard.html', levels=None, rewards=rewards, error='No levels found', current_user=current_user)    

    return render_template('admin/students_app/levels/levels_dashboard.html', levels=levels, rewards=rewards, error=None, current_user=current_user)

@bp.route('/tags', methods=['GET'])
@allowed_roles(['admin'])
def tags_dashboard():
    tags = TagsFinder.get_all()
    if(tags is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=None, error='No tags found', current_user=current_user)

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None, current_user=current_user)

@bp.route('/new-tag', methods=['POST'])
@allowed_roles(['admin'])
def create_tag():
    tags = TagsFinder.get_all()
    name = request.form.get('name',None)
    if(name is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='Failed to create tag', current_user=current_user)

    tag = TagsHandler.create_tag(name=name)
    tags = TagsFinder.get_all()
    if(tag is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='Failed to create tag', current_user=current_user)

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None, current_user=current_user)

@bp.route('/tag/<string:tag_external_id>/delete', methods=['POST'])
@allowed_roles(['admin'])
def delete_tag(tag_external_id):
    tag = TagsFinder.get_from_external_id(tag_external_id)
    if tag is None:
        return APIErrorValue('Couldnt find tag').json(500)

    TagsHandler.delete_tag(tag)

    tags = TagsFinder.get_all()
    if(tags is None):
        return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error='No tags found', current_user=current_user)    

    return render_template('admin/students_app/tags/tags_dashboard.html', tags=tags, error=None, current_user=current_user)

@bp.route('/rewards', methods=['GET'])
@allowed_roles(['admin'])
def rewards_dashboard():
    search = request.args.get('search', None)

    if search is not None:
        rewards = RewardsFinder.get_rewards_from_search(search)
    else:
        search = None
        rewards = RewardsFinder.get_all_rewards()
    
    if(rewards is None or len(rewards) == 0):
        return render_template('admin/students_app/rewards/rewards_dashboard.html', search=search, error = 'No rewards found', rewards=rewards, current_user=current_user)    

    return render_template('admin/students_app/rewards/rewards_dashboard.html', search=search, error=None, rewards=rewards, current_user=current_user)

@bp.route('/new-reward', methods=['GET'])
@allowed_roles(['admin'])
def add_reward_dashboard():

    return render_template('admin/students_app/rewards/add_reward.html')

@bp.route('/new-reward', methods=['POST'])
@allowed_roles(['admin'])
def create_reward():
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    link = request.form.get('link', None)
    quantity = request.form.get('quantity', None)

    reward = RewardsHandler.create_reward(name=name, description=description, link=link, quantity=quantity)
    if(reward is None):
        return render_template('admin/students_app/rewards/add_reward.html', error='Failed to create reward')

    if request.files:
        image = request.files.get('image', None)
        if image:
            result, msg = RewardsHandler.upload_reward_image(image, str(reward.external_id))
            if result == False:
                RewardsHandler.delete_reward(reward)
                return render_template('admin/students_app/rewards/add_reward.html', error=msg)

    return render_template('admin/students_app/rewards/rewards_dashboard.html', search=None, error=None, rewards=RewardsFinder.get_all_rewards(), current_user=current_user)

@bp.route('/rewards/<string:reward_external_id>', methods=['GET'])
@allowed_roles(['admin'])
def update_reward_dashboard(reward_external_id):
    reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
    if(reward is None):
        redirect(url_for('admin_api.rewards_dashboard'))

    image = RewardsHandler.find_reward_image(str(reward.external_id))

    return render_template('admin/students_app/rewards/update_reward.html', error=None, reward=reward, current_user=current_user, image=image)

@bp.route('/rewards/<string:reward_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_reward(reward_external_id):
    reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
    if(reward is None):
        redirect(url_for('admin_api.rewards_dashboard'))

    name = request.form.get('name', None)
    description = request.form.get('description', None)
    link = request.form.get('link', None)
    quantity = request.form.get('quantity', None)
    
    reward = RewardsHandler.update_reward(reward, name=name, description=description, link=link, quantity=quantity)
    image = RewardsHandler.find_reward_image(str(reward.external_id))
    if reward is None:
        return render_template('admin/students_app/rewards/update_reward.html', error='Failed to update reward', reward=reward, image=image)

    if request.files:
        image = request.files.get('image', None) 
        if image:
            result, msg = RewardsHandler.upload_reward_image(image, str(reward.external_id))
            if result == False:
                RewardsHandler.delete_reward(reward)
                return render_template('admin/students_app/rewards/update_reward.html', error=msg, reward=reward, image=image)
    
    return render_template('admin/students_app/rewards/rewards_dashboard.html', search=None, error=None, rewards=RewardsFinder.get_all_rewards(), current_user=current_user)

@bp.route('/reward/<string:reward_external_id>/delete', methods=['POST'])
@allowed_roles(['admin'])
def delete_reward(reward_external_id):
    reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
    image = RewardsHandler.find_reward_image(str(reward.external_id))

    if RewardsHandler.delete_reward(reward):
        return redirect(url_for('admin_api.rewards_dashboard'))

    else:
        return render_template('admin/students_app/rewards/update_reward.html', reward=reward, image=image, error="Failed to delete reward!")

@bp.route('/jeecpot-rewards', methods=['GET'])
@allowed_roles(['admin'])
def jeecpot_reward_dashboard():
    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()
    rewards = RewardsFinder.get_all_rewards()

    if(jeecpot_rewards is None or len(jeecpot_rewards) < 1):
        RewardsHandler.create_jeecpot_reward(student_reward_id=None, first_squad_reward_id=None, second_squad_reward_id=None, third_squad_reward_id=None)
        jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()

    return render_template('admin/students_app/rewards/jeecpot_rewards_dashboard.html', error=None, jeecpot_rewards=jeecpot_rewards[0], rewards=rewards, current_user=current_user)

@bp.route('/jeecpot-rewards/<string:jeecpot_rewards_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_jeecpot_reward(jeecpot_rewards_external_id):
    jeecpot_rewards = RewardsFinder.get_jeecpot_reward_from_external_id(jeecpot_rewards_external_id)
    if(jeecpot_rewards is None):
        return APIErrorValue('JEECPOT Rewards not found').json(500)

    student_reward_id = request.form.get('student_reward', None)
    if(student_reward_id is not None):
        if(student_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, student_reward_id = None)
        else:
            student_reward = RewardsFinder.get_reward_from_external_id(student_reward_id)
            if(student_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, student_reward_id = student_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)
    
    first_squad_reward_id = request.form.get('first_squad_reward', None)
    if(first_squad_reward_id is not None):
        if(first_squad_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, first_squad_reward_id = None)
        else:
            first_squad_reward = RewardsFinder.get_reward_from_external_id(first_squad_reward_id)
            if(first_squad_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, first_squad_reward_id = first_squad_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    second_squad_reward_id = request.form.get('second_squad_reward', None)
    if(second_squad_reward_id is not None):
        if(second_squad_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, second_squad_reward_id = None)
        else:
            second_squad_reward = RewardsFinder.get_reward_from_external_id(second_squad_reward_id)
            if(second_squad_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, second_squad_reward_id = second_squad_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    third_squad_reward_id = request.form.get('third_squad_reward', None)
    if(third_squad_reward_id is not None):
        if(third_squad_reward_id == ""):
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, third_squad_reward_id = None)
        else:
            third_squad_reward = RewardsFinder.get_reward_from_external_id(third_squad_reward_id)
            if(third_squad_reward is None):
                return APIErrorValue('Reward not found').json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(jeecpot_rewards, third_squad_reward_id = third_squad_reward.id)
        if(jeecpot_rewards is None):
            return APIErrorValue('Failed to update reward').json(500)

    return render_template('admin/students_app/rewards/jeecpot_rewards_dashboard.html', error=None, jeecpot_rewards=jeecpot_rewards, rewards=RewardsFinder.get_all_rewards(), current_user=current_user)

@bp.route('/squad-rewards', methods=['GET'])
@allowed_roles(['admin'])
def squad_rewards_dashboard():
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    rewards = RewardsFinder.get_all_rewards()
    event = EventsFinder.get_default_event()
    if(event is None or event.start_date is None or event.end_date is None):
        return render_template('admin/students_app/rewards/rewards_dashboard.html', search=None, error='Please select a default event and its date', rewards=rewards, current_user=current_user)
    
    event_dates = EventsHandler.get_event_dates(event)

    for squad_reward in squad_rewards:
        if(squad_reward.date not in event_dates):
            RewardsHandler.delete_squad_reward(squad_reward)

    rewards_dates = [squad_reward.date for squad_reward in squad_rewards]

    for date in event_dates:
        if(not date in rewards_dates):
            RewardsHandler.create_squad_reward(reward_id=None, date=date)

    rewards = RewardsFinder.get_all_rewards()

    return render_template('admin/students_app/rewards/squad_rewards_dashboard.html', error=None, squad_rewards=squad_rewards, rewards=rewards, current_user=current_user)

@bp.route('/squad-rewards/<string:squad_reward_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_squad_reward(squad_reward_external_id):
    squad_reward = RewardsFinder.get_squad_reward_from_external_id(squad_reward_external_id)
    if squad_reward is None:
        return APIErrorValue('Squad Reward not found').json(404)

    reward_id = request.form.get('reward', None)
    if(reward_id != ""):
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue('Reward not found').json(404)

        squad_reward = RewardsHandler.update_squad_reward(squad_reward, reward_id=reward.id)
    else:
        squad_reward = RewardsHandler.update_squad_reward(squad_reward, reward_id=None)

    if squad_reward is None:
        return render_template('admin/students_app/rewards/squad_rewards_dashboard.html', error='Failed to update reward', squad_rewards=None, rewards=None, current_user=current_user)
    
    return render_template('admin/students_app/rewards/squad_rewards_dashboard.html', error=None, squad_rewards=RewardsFinder.get_all_squad_rewards(), rewards=RewardsFinder.get_all_rewards(), current_user=current_user)