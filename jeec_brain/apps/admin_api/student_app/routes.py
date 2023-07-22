from jeec_brain.finders.student_rewards_finder import StudentRewardsFinder
from jeec_brain.handlers.reward_student_handler import StudentRewardsHandler
from .. import bp
from flask import render_template, current_app, request, redirect, url_for, jsonify, make_response
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.squads_finder import SquadsFinder
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.quests_finder import QuestsFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.squads_handler import SquadsHandler
from jeec_brain.handlers.levels_handler import LevelsHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.handlers.rewards_handler import RewardsHandler
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.handlers.quests_handler import QuestsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.schemas.admin_api.student_app.schemas import *
from flask_login import current_user
from datetime import datetime
from random import choice
from config import Config
import uuid

from jeec_brain.apps.auth.wrappers import requires_client_auth

import json

# Student App routes
@bp.get("/students-app")
@allowed_roles(["admin"])
def students_app_dashboard():

    return render_template("admin/students_app/students_app_dashboard.html")


@bp.get("/students")
@allowed_roles(["admin"])
def students_dashboard():
    search = request.args.get("search")

    # handle search bar requests
    if search is not None:
        students_list = StudentsFinder.get_from_search(search)
    else:
        search = None
        students_list = StudentsFinder.get_all_simple()

    if students_list is None or len(students_list) == 0:
        error = "No students found"
        return render_template(
            "admin/students_app/students/students_dashboard.html",
            students=None,
            error=error,
            search=search,
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/students/students_dashboard.html",
        students=students_list,
        error=None,
        search=search,
        current_user=current_user,
    )


@bp.post("/student/<string:student_external_id>/ban")
@allowed_roles(["admin"])
def ban_student(path: StudentPath):
    student = StudentsFinder.get_from_external_id(path.student_external_id)
    if student is None:
        return APIErrorValue("Couldnt find student").json(404)

    if student.squad:
        SquadsHandler.delete_squad(student.squad)

    banned_student = StudentsHandler.create_banned_student(student)
    if banned_student is None:
        return APIErrorValue("Error banning student").json(500)

    UsersHandler.delete_user(Config.ROCKET_CHAT_ENABLE, student.user)

    return redirect(url_for("admin_api.students_dashboard"))


@bp.post("/student/<string:student_external_id>/add-points")
@allowed_roles(["admin"])
def add_points(path: StudentPath):
    student = StudentsFinder.get_from_external_id(path.student_external_id)
    if student is None:
        return APIErrorValue("Invalid IST ID, student not found").json(404)

    activity_id = request.form.get("activity_id")
    points = request.form.get("points")

    if activity_id:
        activity = ActivitiesFinder.get_from_id(activity_id)
        if activity is None:
            return APIErrorValue("Invalid Activity ID, activity doesn't exist").json(
                404
            )
        if activity in student.activities:
            return APIErrorValue("Student already participated in that activity").json(
                500
            )
        if not ActivitiesHandler.add_student_activity(student, activity, "admin"):
            return APIErrorValue("Failed to add activity to student").json(500)
        points = activity.points
    else:
        try:
            points = int(points)
        except ValueError:
            return APIErrorValue("Points value is not integer").json(500)

    if not StudentsHandler.add_points(student, points):
        return APIErrorValue("Failed to add points to student").json(500)

    return jsonify("Points added"), 200


@bp.get("/banned-students")
@allowed_roles(["admin"])
def banned_students_dashboard():
    banned_students = StudentsFinder.get_all_banned()

    if banned_students is None or len(banned_students) == 0:
        error = "No banned students found"
        return render_template(
            "admin/students_app/students/banned_students_dashboard.html",
            students=None,
            error=error,
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/students/banned_students_dashboard.html",
        students=banned_students,
        error=None,
        current_user=current_user,
    )


@bp.post("/student/<string:student_external_id>/unban")
@allowed_roles(["admin"])
def unban_student(path: StudentPath):
    banned_student = StudentsFinder.get_banned_student_from_external_id(
        path.student_external_id
    )
    if banned_student is None:
        return APIErrorValue("Couldnt find student").json(500)

    StudentsHandler.delete_banned_student(banned_student)

    return redirect(url_for("admin_api.banned_students_dashboard"))


@bp.get("/squads")
@allowed_roles(["admin"])
def squads_dashboard():
    search = request.args.get("search")

    # handle search bar requests
    if search is not None:
        squads = SquadsFinder.search_by_name(search)
    else:
        search = None
        squads = SquadsFinder.get_all()

    if squads is None or len(squads) == 0:
        error = "No squads found"
        return render_template(
            "admin/students_app/squads/squads_dashboard.html",
            squads=None,
            error=error,
            search=search,
            current_user=current_user,
        )

    for squad in squads:
        squad.members_id = [member.user.username for member in squad.members]
        squad.members_id.remove(squad.captain_ist_id)
        squad.members_id = " ".join(squad.members_id)

    return render_template(
        "admin/students_app/squads/squads_dashboard.html",
        squads=squads,
        error=None,
        search=search,
        current_user=current_user,
    )


@bp.post("/squad/<string:squad_external_id>/ban")
@allowed_roles(["admin"])
def ban_squad(path: SquadPath):
    squad = SquadsFinder.get_from_external_id(path.squad_external_id)
    if squad is None:
        return APIErrorValue("Couldnt find squad").json(500)

    for member in squad.members:
        StudentsHandler.leave_squad(member)

        banned_student = StudentsHandler.create_banned_student(member)
        if banned_student is None:
            return APIErrorValue("Error banning student").json(500)

        UsersHandler.delete_user(Config.ROCKET_CHAT_ENABLE, member.user)

    return redirect(url_for("admin_api.squads_dashboard"))


@bp.get("/levels")
@allowed_roles(["admin"])
def levels_dashboard():
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if levels is None:
        return render_template(
            "admin/students_app/levels/levels_dashboard.html",
            levels=None,
            rewards=rewards,
            error="No levels found",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/levels/levels_dashboard.html",
        levels=levels,
        rewards=rewards,
        error=None,
        current_user=current_user,
    )


@bp.post("/create-level")
@allowed_roles(["admin"])
def create_level():
    value = request.form.get("value", None)
    points = request.form.get("points", None)
    reward_id = request.form.get("reward", None)
    if reward_id == "":
        reward_id = None

    if value is None or points is None:
        return APIErrorValue("Invalid value or points").json(500)

    if reward_id is not None:
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue("Invalid reward Id")

        reward_id = reward.id

    levels = LevelsFinder.get_all_levels()

    if (len(levels) > 0 and int(levels[-1].value + 1) != int(value)) or (
        len(levels) == 0 and int(value) != 1
    ):
        return APIErrorValue("Invalid level value").json(500)

    level = LevelsHandler.create_level(value=value, points=points, reward_id=reward_id)
    if level is None:
        return APIErrorValue("Error creating level").json(500)

    if len(levels) == 0 and level.value == 1:
        students = StudentsFinder.get_from_parameters({"level_id": None})
        for student in students:
            StudentsHandler.update_student(student, level_id=level.id)

    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if levels is None:
        return render_template(
            "admin/students_app/levels/levels_dashboard.html",
            levels=None,
            rewards=rewards,
            error="No levels found",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/levels/levels_dashboard.html",
        levels=levels,
        rewards=rewards,
        error=None,
        current_user=current_user,
    )


@bp.post("/level/<string:level_external_id>")
@allowed_roles(["admin"])
def update_level(path: LevelPath):
    level = LevelsFinder.get_level_from_external_id(path.level_external_id)
    if level is None:
        return APIErrorValue("Couldnt find level").json(500)

    reward_id = request.form.get("reward", None)
    if reward_id == "":
        reward_id = None
    if reward_id is not None:
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue("Invalid reward Id")

        reward_id = reward.id

    level = LevelsHandler.update_level(level, reward_id=reward_id)
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if level is None:
        return render_template(
            "admin/students_app/levels/levels_dashboard.html",
            levels=levels,
            rewards=rewards,
            error="Failed to update reward",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/levels/levels_dashboard.html",
        levels=levels,
        rewards=rewards,
        error=None,
        current_user=current_user,
    )


@bp.post("/level/<string:level_external_id>/delete")
@allowed_roles(["admin"])
def delete_level(path: LevelPath):
    level = LevelsFinder.get_level_from_external_id(path.level_external_id)
    if level is None:
        return APIErrorValue("Couldnt find level").json(500)

    levels = LevelsFinder.get_all_levels()
    if len(levels) == 0 or (len(levels) > 0 and levels[-1] == level):
        students = StudentsFinder.get_from_level_or_higher(level)
        previous_level = LevelsFinder.get_level_by_value(level.value - 1)

        if previous_level is None:
            for student in students:
                StudentsHandler.update_student(student, level_id=None, total_points=0)
        else:
            for student in students:
                StudentsHandler.update_student(
                    student,
                    level_id=previous_level.id,
                    total_points=previous_level.points,
                )

        LevelsHandler.delete_level(level)

    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    if levels is None:
        return render_template(
            "admin/students_app/levels/levels_dashboard.html",
            levels=None,
            rewards=rewards,
            error="No levels found",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/levels/levels_dashboard.html",
        levels=levels,
        rewards=rewards,
        error=None,
        current_user=current_user,
    )


@bp.get("/tags")
@allowed_roles(["admin"])
def tags_dashboard():
    tags = TagsFinder.get_all()
    if tags is None:
        return render_template(
            "admin/students_app/tags/tags_dashboard.html",
            tags=None,
            error="No tags found",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/tags/tags_dashboard.html",
        tags=tags,
        error=None,
        current_user=current_user,
    )


@bp.post("/new-tag")
@allowed_roles(["admin"])
def create_tag():
    tags = TagsFinder.get_all()
    name = request.form.get("name", None)
    if name is None:
        return render_template(
            "admin/students_app/tags/tags_dashboard.html",
            tags=tags,
            error="Failed to create tag",
            current_user=current_user,
        )

    tag = TagsHandler.create_tag(name=name)
    tags = TagsFinder.get_all()
    if tag is None:
        return render_template(
            "admin/students_app/tags/tags_dashboard.html",
            tags=tags,
            error="Failed to create tag",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/tags/tags_dashboard.html",
        tags=tags,
        error=None,
        current_user=current_user,
    )


@bp.post("/tag/<string:tag_external_id>/delete")
@allowed_roles(["admin"])
def delete_tag(path: TagPath):
    tag = TagsFinder.get_from_external_id(path.tag_external_id)
    if tag is None:
        return APIErrorValue("Couldnt find tag").json(500)

    TagsHandler.delete_tag(tag)

    tags = TagsFinder.get_all()
    if tags is None:
        return render_template(
            "admin/students_app/tags/tags_dashboard.html",
            tags=tags,
            error="No tags found",
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/tags/tags_dashboard.html",
        tags=tags,
        error=None,
        current_user=current_user,
    )


@bp.get("/rewards")
@allowed_roles(["admin"])
def rewards_dashboard():
    search = request.args.get("search", None)

    if search is not None:
        rewards = RewardsFinder.get_rewards_from_search(search)
    else:
        search = None
        rewards = RewardsFinder.get_all_rewards()

    if rewards is None or len(rewards) == 0:
        return render_template(
            "admin/students_app/rewards/rewards_dashboard.html",
            search=search,
            error="No rewards found",
            rewards=rewards,
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/rewards/rewards_dashboard.html",
        search=search,
        error=None,
        rewards=rewards,
        current_user=current_user,
    )


@bp.get("/new-reward")
@allowed_roles(["admin"])
def add_reward_dashboard():

    return render_template("admin/students_app/rewards/add_reward.html")


@bp.post("/new-reward")
@allowed_roles(["admin"])
def create_reward():
    name = request.form.get("name", None)
    description = request.form.get("description", None)
    link = request.form.get("link", None)
    quantity = request.form.get("quantity") or 0

    reward = RewardsHandler.create_reward(
        name=name, description=description, link=link, quantity=quantity
    )
    if reward is None:
        return render_template(
            "admin/students_app/rewards/add_reward.html",
            error="Failed to create reward",
        )

    if request.files:
        image = request.files.get("image", None)
        if image:
            result, msg = RewardsHandler.upload_reward_image(
                image, str(reward.external_id)
            )
            if result == False:
                RewardsHandler.delete_reward(reward)
                return render_template(
                    "admin/students_app/rewards/add_reward.html", error=msg
                )

    return render_template(
        "admin/students_app/rewards/rewards_dashboard.html",
        search=None,
        error=None,
        rewards=RewardsFinder.get_all_rewards(),
        current_user=current_user,
    )


@bp.get("/rewards/<string:reward_external_id>")
@allowed_roles(["admin"])
def update_reward_dashboard(path: RewardPath):
    reward = RewardsFinder.get_reward_from_external_id(path.reward_external_id)
    if reward is None:
        redirect(url_for("admin_api.rewards_dashboard"))

    image = RewardsHandler.find_reward_image(str(reward.external_id))

    return render_template(
        "admin/students_app/rewards/update_reward.html",
        error=None,
        reward=reward,
        current_user=current_user,
        image=image,
    )


@bp.post("/rewards/<string:reward_external_id>")
@allowed_roles(["admin"])
def update_reward(path: RewardPath):
    reward = RewardsFinder.get_reward_from_external_id(path.reward_external_id)
    if reward is None:
        redirect(url_for("admin_api.rewards_dashboard"))

    name = request.form.get("name", None)
    description = request.form.get("description", None)
    link = request.form.get("link", None)
    quantity = request.form.get("quantity", None)

    reward = RewardsHandler.update_reward(
        reward, name=name, description=description, link=link, quantity=quantity
    )
    image = RewardsHandler.find_reward_image(str(reward.external_id))
    if reward is None:
        return render_template(
            "admin/students_app/rewards/update_reward.html",
            error="Failed to update reward",
            reward=reward,
            image=image,
        )

    if request.files:
        image = request.files.get("image", None)
        if image:
            result, msg = RewardsHandler.upload_reward_image(
                image, str(reward.external_id)
            )
            if result == False:
                RewardsHandler.delete_reward(reward)
                return render_template(
                    "admin/students_app/rewards/update_reward.html",
                    error=msg,
                    reward=reward,
                    image=image,
                )

    return render_template(
        "admin/students_app/rewards/rewards_dashboard.html",
        search=None,
        error=None,
        rewards=RewardsFinder.get_all_rewards(),
        current_user=current_user,
    )


@bp.post("/reward/<string:reward_external_id>/delete")
@allowed_roles(["admin"])
def delete_reward(path: RewardPath):
    reward = RewardsFinder.get_reward_from_external_id(path.reward_external_id)
    image = RewardsHandler.find_reward_image(str(reward.external_id))

    if RewardsHandler.delete_reward(reward):
        return redirect(url_for("admin_api.rewards_dashboard"))

    else:
        return render_template(
            "admin/students_app/rewards/update_reward.html",
            reward=reward,
            image=image,
            error="Failed to delete reward!",
        )


@bp.get("/jeecpot-rewards")
@allowed_roles(["admin"])
def jeecpot_reward_dashboard():
    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()
    rewards = RewardsFinder.get_all_rewards()

    if jeecpot_rewards is None or len(jeecpot_rewards) < 1:
        RewardsHandler.create_jeecpot_reward()
        jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()

    return render_template(
        "admin/students_app/rewards/jeecpot_rewards_dashboard.html",
        error=None,
        jeecpot_rewards=jeecpot_rewards[0],
        rewards=rewards,
        current_user=current_user,
    )


@bp.post("/jeecpot-rewards/<string:jeecpot_rewards_external_id>")
@allowed_roles(["admin"])
def update_jeecpot_reward(path: JeecpotRewardsPath):
    jeecpot_rewards = RewardsFinder.get_jeecpot_reward_from_external_id(
        path.jeecpot_rewards_external_id
    )
    if jeecpot_rewards is None:
        return APIErrorValue("JEECPOT Rewards not found").json(500)

    first_student_reward_id = request.form.get("first_student_reward", None)
    if first_student_reward_id is not None:
        if first_student_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_student_reward_id=None
            )
        else:
            first_student_reward = RewardsFinder.get_reward_from_external_id(
                first_student_reward_id
            )
            if first_student_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_student_reward_id=first_student_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    second_student_reward_id = request.form.get("second_student_reward", None)
    if second_student_reward_id is not None:
        if second_student_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_student_reward_id=None
            )
        else:
            second_student_reward = RewardsFinder.get_reward_from_external_id(
                second_student_reward_id
            )
            if second_student_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_student_reward_id=second_student_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    third_student_reward_id = request.form.get("third_student_reward", None)
    if third_student_reward_id is not None:
        if third_student_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_student_reward_id=None
            )
        else:
            third_student_reward = RewardsFinder.get_reward_from_external_id(
                third_student_reward_id
            )
            if third_student_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_student_reward_id=third_student_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    first_squad_reward_id = request.form.get("first_squad_reward", None)
    if first_squad_reward_id is not None:
        if first_squad_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_squad_reward_id=None
            )
        else:
            first_squad_reward = RewardsFinder.get_reward_from_external_id(
                first_squad_reward_id
            )
            if first_squad_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_squad_reward_id=first_squad_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    second_squad_reward_id = request.form.get("second_squad_reward", None)
    if second_squad_reward_id is not None:
        if second_squad_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_squad_reward_id=None
            )
        else:
            second_squad_reward = RewardsFinder.get_reward_from_external_id(
                second_squad_reward_id
            )
            if second_squad_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_squad_reward_id=second_squad_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    third_squad_reward_id = request.form.get("third_squad_reward", None)
    if third_squad_reward_id is not None:
        if third_squad_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_squad_reward_id=None
            )
        else:
            third_squad_reward = RewardsFinder.get_reward_from_external_id(
                third_squad_reward_id
            )
            if third_squad_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_squad_reward_id=third_squad_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_job_fair_reward_id = request.form.get("king_job_fair_reward", None)
    if king_job_fair_reward_id is not None:
        if king_job_fair_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_job_fair_reward_id=None
            )
        else:
            king_job_fair_reward = RewardsFinder.get_reward_from_external_id(
                king_job_fair_reward_id
            )
            if king_job_fair_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_job_fair_reward_id=king_job_fair_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_knowledge_reward_id = request.form.get("king_knowledge_reward", None)
    if king_knowledge_reward_id is not None:
        if king_knowledge_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_knowledge_reward_id=None
            )
        else:
            king_knowledge_reward = RewardsFinder.get_reward_from_external_id(
                king_knowledge_reward_id
            )
            if king_knowledge_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_knowledge_reward_id=king_knowledge_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_hacking_reward_id = request.form.get("king_hacking_reward", None)
    if king_hacking_reward_id is not None:
        if king_hacking_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_hacking_reward_id=None
            )
        else:
            king_hacking_reward = RewardsFinder.get_reward_from_external_id(
                king_hacking_reward_id
            )
            if king_hacking_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_hacking_reward_id=king_hacking_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_networking_reward_id = request.form.get("king_networking_reward", None)
    if king_networking_reward_id is not None:
        if king_networking_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_networking_reward_id=None
            )
        else:
            king_networking_reward = RewardsFinder.get_reward_from_external_id(
                king_networking_reward_id
            )
            if king_networking_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_networking_reward_id=king_networking_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    cv_platform_raffle_reward_id = request.form.get("cv_platform_raffle_reward", None)
    if cv_platform_raffle_reward_id is not None:
        if cv_platform_raffle_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, cv_platform_raffle_reward_id=None
            )
        else:
            cv_platform_raffle_reward = RewardsFinder.get_reward_from_external_id(
                cv_platform_raffle_reward_id
            )
            if cv_platform_raffle_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards,
                cv_platform_raffle_reward_id=cv_platform_raffle_reward.id,
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    return render_template(
        "admin/students_app/rewards/jeecpot_rewards_dashboard.html",
        error=None,
        jeecpot_rewards=jeecpot_rewards,
        rewards=RewardsFinder.get_all_rewards(),
        current_user=current_user,
    )


@bp.get("/squad-rewards")
@allowed_roles(["admin"])
def squad_rewards_dashboard():
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    rewards = RewardsFinder.get_all_rewards()
    event = EventsFinder.get_default_event()
    if event is None or event.start_date is None or event.end_date is None:
        return render_template(
            "admin/students_app/rewards/rewards_dashboard.html",
            search=None,
            error="Please select a default event and its date",
            rewards=rewards,
            current_user=current_user,
        )

    event_dates = EventsHandler.get_event_dates(event)

    for squad_reward in squad_rewards:
        if squad_reward.date not in event_dates:
            RewardsHandler.delete_squad_reward(squad_reward)

    rewards_dates = [squad_reward.date for squad_reward in squad_rewards]

    for date in event_dates:
        if not date in rewards_dates:
            RewardsHandler.create_squad_reward(reward_id=None, date=date)

    rewards = RewardsFinder.get_all_rewards()
    squad_rewards = RewardsFinder.get_all_squad_rewards()

    return render_template(
        "admin/students_app/rewards/squad_rewards_dashboard.html",
        error=None,
        squad_rewards=squad_rewards,
        rewards=rewards,
        current_user=current_user,
    )


@bp.post("/squad-rewards/<string:squad_reward_external_id>")
@allowed_roles(["admin"])
def update_squad_reward(path: SquadRewardPath):
    squad_reward = RewardsFinder.get_squad_reward_from_external_id(
        path.squad_reward_external_id
    )
    if squad_reward is None:
        return APIErrorValue("Squad Reward not found").json(404)

    reward_id = request.form.get("reward", None)
    if reward_id != "":
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue("Reward not found").json(404)

        squad_reward = RewardsHandler.update_squad_reward(
            squad_reward, reward_id=reward.id
        )
    else:
        squad_reward = RewardsHandler.update_squad_reward(squad_reward, reward_id=None)

    if squad_reward is None:
        return render_template(
            "admin/students_app/rewards/squad_rewards_dashboard.html",
            error="Failed to update reward",
            squad_rewards=None,
            rewards=None,
            current_user=current_user,
        )

    return render_template(
        "admin/students_app/rewards/squad_rewards_dashboard.html",
        error=None,
        squad_rewards=RewardsFinder.get_all_squad_rewards(),
        rewards=RewardsFinder.get_all_rewards(),
        current_user=current_user,
    )


@bp.post("/reset-daily-points")
@allowed_roles(["admin"])
def reset_daily_points():
    squads = SquadsFinder.get_all()
    for squad in squads:
        if not SquadsHandler.reset_daily_points(squad):
            return APIErrorValue("Reset failed").json(500)

    students = StudentsFinder.get_all()
    for student in students:
        if not StudentsHandler.reset_daily_points(student):
            return APIErrorValue("Reset failed").json(500)

    return jsonify("Success"), 200


@bp.post("/select-winners")
@allowed_roles(["admin"])
def select_winners():
    top_squads = SquadsFinder.get_first()
    if top_squads is None:
        return APIErrorValue("No squad found").json(404)

    winner = choice(top_squads)
    now = datetime.utcnow()
    date = now.strftime("%d %b %Y, %a")

    squad_reward = RewardsFinder.get_squad_reward_from_date(date)
    if squad_reward is None:
        return APIErrorValue("No reward found").json(404)

    squad_reward = RewardsHandler.update_squad_reward(squad_reward, winner_id=winner.id)
    if squad_reward is None:
        return APIErrorValue("Error selecting winner").json(500)

    return jsonify("Success"), 200

@bp.get("/studentss")
@requires_client_auth
def students_dashboardd():
    students_list = StudentsFinder.get_all_simple()
    responsestudents = []

    for student in students_list:
        responsestudents.append({"id": student[10], 
                                 "name": student[0],
                                 "ist_id": student[1],
                                 "email": student[2],
                                 "linkedin": student[3],
                                 "level": student[4],
                                 "daily_points": student[5],
                                 "total_points": student[6],
                                 "cv": student[7],
                                 "squad": student[8]})

    if students_list is None or len(students_list) == 0:
        response = make_response(
        jsonify({"students": None,
        "error": "No students found"
        }))
        return response

    response = make_response(
    jsonify({"students": responsestudents,
    "error": None
    }))
    return response


@bp.post("/studentban")
@requires_client_auth
def ban_studentt():
    student_id = json.loads(request.data.decode('utf-8'))['banstudent']
    student = StudentsFinder.get_from_id(student_id)
    if student is None:
        return APIErrorValue("Couldnt find student").json(404)

    if student.squad:
        SquadsHandler.delete_squad(student.squad)

    banned_student = StudentsHandler.create_banned_student(student)
    if banned_student is None:
        return APIErrorValue("Error banning student").json(500)

    UsersHandler.delete_user(Config.ROCKET_CHAT_ENABLE, student.user)

    return ('', 204)


@bp.get("/banned-studentss")
@requires_client_auth
def banned_students_dashboardd():
    banned_students = StudentsFinder.get_all_banned()
    responsebanned = []

    if banned_students is None or len(banned_students) == 0:
        response = make_response(
        jsonify({"students": None,
        "error": "No banned students found"
        }))
        return response
    
    for student in banned_students:
        responsebanned.append({"name": student.name,
                               "ist_id": student.ist_id,
                               "email": student.email,
                               "external_id": student.external_id})

    response = make_response(
    jsonify({"students": responsebanned,
    "error": None
    }))
    return response


@bp.post("/unban")
@requires_client_auth
def unban_studentt():
    external_id = json.loads(request.data.decode('utf-8'))['unbanstudent']
    banned_student = StudentsFinder.get_banned_student_from_external_id(external_id)
    if banned_student is None:
        return APIErrorValue("Couldnt find student").json(500)

    StudentsHandler.delete_banned_student(banned_student)

    return ('', 204)


@bp.get("/levelss")
@requires_client_auth
def levels_dashboardd():
    levels = LevelsFinder.get_all_levels()
    rewards = RewardsFinder.get_all_rewards()
    responselevels = []
    responserewards = []
    
    for level in levels:
        responselevels.append({"external_id": level.external_id,
                               "value": level.value,
                               "ending_points": level.points,
                               "reward": {"external_id": level.reward.external_id, "name": level.reward.name}})
    
    for reward in rewards:
        responserewards.append({"id": reward.external_id,
                                "name": reward.name,})

    if levels is None:
        response = make_response(
        jsonify({"levels": responselevels,
                 "rewards": responserewards,
                 "error": None}))
                 
        return response

    response = make_response(
        jsonify({"levels": responselevels,
                 "rewards": responserewards,
                 "error": None}))

    return response


@bp.post("/level/create")
@requires_client_auth
def create_levell():
    value = json.loads(request.data.decode('utf-8'))['level_value']
    points = json.loads(request.data.decode('utf-8'))['level_points']
    reward_id = json.loads(request.data.decode('utf-8'))['reward_id']

    print(value)
    print(points)
    print(reward_id)

    if reward_id == "":
        reward_id = None

    if value is None or points is None:
        return APIErrorValue("Invalid value or points").json(500)

    if reward_id is not None:
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue("Invalid reward Id")

        reward_id = reward.id

    levels = LevelsFinder.get_all_levels()

    if (len(levels) > 0 and int(levels[-1].value + 1) != int(value)) or (
        len(levels) == 0 and int(value) != 1
    ):
        return APIErrorValue("Invalid level value").json(500)

    level = LevelsHandler.create_level(value=value, points=points, reward_id=reward_id)
    if level is None:
        return APIErrorValue("Error creating level").json(500)

    if len(levels) == 0 and level.value == 1:
        students = StudentsFinder.get_from_parameters({"level_id": None})
        for student in students:
            StudentsHandler.update_student(student, level_id=level.id)

    return ('', 204)


@bp.post("/level/update")
@requires_client_auth
def update_levell():
    # response = json.loads(request.data.decode('utf-8'))
    # print(response)
    level_external_id = json.loads(request.data.decode('utf-8'))['level_external_id']
    reward_id = json.loads(request.data.decode('utf-8'))['change_reward_id']

    print(reward_id)

    level = LevelsFinder.get_level_from_external_id(level_external_id)

    if level is None:
        return APIErrorValue("Couldn't find level").json(500)

    if reward_id == "":
        reward_id = None
    if reward_id is not None:
        reward = RewardsFinder.get_reward_from_external_id(reward_id)
        if reward is None:
            return APIErrorValue("Invalid reward Id")

        reward_id = reward.id

    print(level)
    print(reward_id)

    level = LevelsHandler.update_level(level, reward_id=reward_id)
    if level is None:
        return APIErrorValue("Failed to update reward").json(500)

    return('', 204)


@bp.post("/level/delete")
@requires_client_auth
def delete_levell():
    level_value = json.loads(request.data.decode('utf-8'))['level_value']
    level = LevelsFinder.get_level_by_value(level_value)

    if level is None:
        print(level)
        return APIErrorValue("Couldnt find level").json(500)

    levels = LevelsFinder.get_all_levels()
    if len(levels) == 0 or (len(levels) > 0 and levels[-1] == level):
        students = StudentsFinder.get_from_level_or_higher(level)
        previous_level = LevelsFinder.get_level_by_value(level.value - 1)

        if previous_level is None:
            for student in students:
                StudentsHandler.update_student(student, level_id=None, total_points=0)
        else:
            for student in students:
                StudentsHandler.update_student(
                    student,
                    level_id=previous_level.id,
                    total_points=previous_level.points,
                )

        LevelsHandler.delete_level(level)

    return ('', 204)


@bp.get("/squadss")
@requires_client_auth
def squads_dashboardd():
    squads = SquadsFinder.get_all()
    responsesquads = []
    
    if squads is None or len(squads) == 0:
        response = make_response(
        jsonify({"squads": None,
        "error": "No squads found"
        }))

        return response

    for squad in squads:
        squad.members_id = [member.user.username for member in squad.members]
        squad.members_id.remove(squad.captain_ist_id)
        squad.members_id = " ".join(squad.members_id)

        responsesquads.append({"name": squad.name,
                               "cry": squad.cry,
                               "captain_ist_id": squad.captain_ist_id,
                               "members_id": squad.members_id,
                               "daily_points": squad.total_points})        

    response = make_response(
        jsonify({"squads": responsesquads,
        "error": None
        }))

    return response

@bp.post("/bansquad")
@requires_client_auth
def ban_squadd():
    squadname = json.loads(request.data.decode('utf-8'))['bansquad']
    squad = SquadsFinder.get_by_name(squadname)

    if squad is None:
        return APIErrorValue("Couldnt find squad").json(500)

    for member in squad.members:
        StudentsHandler.leave_squad(member)

        banned_student = StudentsHandler.create_banned_student(member)
        if banned_student is None:
            return APIErrorValue("Error banning student").json(500)

        UsersHandler.delete_user(Config.ROCKET_CHAT_ENABLE, member.user)

    return ('', 204)


@bp.get("/tagss")
@requires_client_auth
def tagss_dashboard():
    tags = TagsFinder.get_all()
    responsetags = []
    for tag in tags:
        responsetags.append(tag.name)
    if tags is None:
        response = make_response(
        jsonify({"tags": None,
        "error": "No tags found"
        }))

        return response

    response = make_response(
        jsonify({"tags": responsetags,
        "error": None
        }))

    return response

@bp.post("/new-tagg")
@requires_client_auth
def create_tagg():
    tags = TagsFinder.get_all()
    name = json.loads(request.data.decode('utf-8'))['tagname']

    tag = TagsHandler.create_tag(name=name)
    tags = TagsFinder.get_all()
    responsetags = []
    for tag in tags:
        responsetags.append(tag.name)
    if tag is None:
        response = make_response(
        jsonify({"tags": None,
        "error": "No tags found"
        }))

        return response

    response = make_response(
        jsonify({"tags": responsetags,
        "error": None
        }))

    return response

@bp.post("/tagsdelete")
@requires_client_auth
def delete_tagg():
    name = json.loads(request.data.decode('utf-8'))['tagname']
    tag = TagsFinder.get_by_name(name)

    if tag is None:
        return APIErrorValue("Couldn't find tag").json(500)

    TagsHandler.delete_tag(tag)

    tags = TagsFinder.get_all()
    responsetags = []
    for tag in tags:
        responsetags.append(tag.name)
    if tags is None:
        response = make_response(
        jsonify({"tags": None,
        "error": "No tags found"
        }))

        return response

    response = make_response(
        jsonify({"tags": responsetags,
        "error": None
        }))

    return response

@bp.get("/rewardss")
@requires_client_auth
def rewards_dashboardd():
        
    rewards = RewardsFinder.get_all_rewards()
    responserewards = []

    for reward in rewards:
        responserewards.append({"external_id": reward.external_id,
                                "name": reward.name,
                                "description": reward.description,
                                "link": reward.link,
                                "quantity": reward.quantity})
    
    if rewards is None or len(rewards) == 0:
        response = make_response(
        jsonify({"rewards": None,
        "error": "No rewards found"
        }))

        return response

    response = make_response(
        jsonify({"rewards": responserewards,
        "error": None
        }))

    return response


@bp.post("/new-rewardd")
@requires_client_auth
def create_rewardd():
    try:
        image = request.files['image']
    except:
        image = None
    name = request.form['name']
    try:
        description = request.form['description']
    except:
        description = ''
    try:
        link = request.form['link']
    except:
        link = ''
    
    try:
        quantity = request.form['quantity']
    except:
        quantity = 0


    reward = RewardsHandler.create_reward(
        name=name, description=description, link=link, quantity=quantity
    )

    if reward is None:
        response = make_response(
        jsonify({
            'error': "Failed to create reward"
        }))

        return response

    if image:
        result, msg = RewardsHandler.upload_reward_image(
            image, str(reward.external_id))
            
        if result == False:
            RewardsHandler.delete_reward(reward)
            response = make_response(
            jsonify({
                'error': msg
            }))

            return response
    
    return ("", 204)


@bp.post("/reward/update/get")
@requires_client_auth
def update_rewarddd():
    external_id = json.loads(request.data.decode('utf-8'))['external_id']
    reward = RewardsFinder.get_reward_from_external_id(external_id)

    if reward is None:
        return APIErrorValue("Couldnt find reward").json(500)

    response = make_response(
        jsonify({"name": reward.name, "description": reward.description, "link": reward.link, "quantity": reward.quantity,
        "error": "Failed to update reward"
        }))

    return response


@bp.post("/reward/update/get/image")
@requires_client_auth
def getImageReward_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    reward_external_id = response['reward_external_id']
    
    fileUp = RewardsHandler.get_image_reward(reward_external_id)

    if not fileUp:
        return Response(response="Invalid zip file", status="200")
 
    return send_file(
        fileUp
    )


@bp.post("/reward/update/create_url")
@requires_client_auth
def create_url_error_vue2():
    
    response = json.loads(request.data.decode('utf-8'))
    reward_external_id = response['reward_external_id']
    
    fileUp = RewardsHandler.get_image_reward(reward_external_id)
    
    if not fileUp:
        response = make_response(
        jsonify({
            'error': 'erro',
        })
        )
        return response
    
    response = make_response(
    jsonify({
        'error': '',
    })
    )
    return response


@bp.post("/reward/update")
@requires_client_auth
def update_rewardd():
    external_id = request.form.get("external_id", None)
    reward = RewardsFinder.get_reward_from_external_id(external_id)

    if reward is None:
        return(None, 204)

    name = request.form.get("name", None)
    description = request.form.get("description", None)
    link = request.form.get("link", None)
    quantity = request.form.get("quantity", None)

    reward = RewardsHandler.update_reward(
        reward, name=name, description=description, link=link, quantity=quantity
    )

    if reward is None:
        response = make_response(
        jsonify({
            "error": "Failed to update reward"
        }))

        return response

    if request.files:
        image = request.files.get("image", None)
        if image:
            result, msg = RewardsHandler.upload_reward_image(
                image, str(reward.external_id)
            )
            if result == False:
                RewardsHandler.delete_reward(reward)
                response = make_response(
                jsonify({
                    "error": msg
                }))

                return response

    return ('', 204)


@bp.post("/reward/delete")
@requires_client_auth
def delete_rewardd():
    reward_external_id = json.loads(request.data.decode('utf-8'))['external_id']
    reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
    image = RewardsHandler.find_reward_image(str(reward.external_id))

    if RewardsHandler.delete_reward(reward):
        return ('', 204)

    else:
        response = make_response(
            jsonify({
                "error": "Failed to delete reward!",
            }))

        return response


@bp.get("/jeecpot-rewardss")
@requires_client_auth
def jeecpot_reward_dashboardd():
    responsejeecpot = {}
    responserewards = []

    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()
    rewards = RewardsFinder.get_all_rewards()

    if jeecpot_rewards is None or len(jeecpot_rewards) < 1:
        RewardsHandler.create_jeecpot_reward()
        jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()

    if jeecpot_rewards[0].first_student_reward != None:
        responsejeecpot["first_student_reward_name"] = jeecpot_rewards[0].first_student_reward.name
        responsejeecpot["first_student_reward_id"] = jeecpot_rewards[0].first_student_reward.external_id
    if jeecpot_rewards[0].second_student_reward != None:
        responsejeecpot["second_student_reward_name"] = jeecpot_rewards[0].second_student_reward.name
        responsejeecpot["second_student_reward_id"] = jeecpot_rewards[0].second_student_reward.external_id
    if jeecpot_rewards[0].third_student_reward != None:
        responsejeecpot["third_student_reward_name"] = jeecpot_rewards[0].third_student_reward.name
        responsejeecpot["third_student_reward_id"] = jeecpot_rewards[0].third_student_reward.external_id
    if jeecpot_rewards[0].first_squad_reward != None:
        responsejeecpot["first_squad_reward_name"] = jeecpot_rewards[0].first_squad_reward.name
        responsejeecpot["first_squad_reward_id"] = jeecpot_rewards[0].first_squad_reward.external_id
    if jeecpot_rewards[0].second_squad_reward != None:
        responsejeecpot["second_squad_reward_name"] = jeecpot_rewards[0].second_squad_reward.name
        responsejeecpot["second_squad_reward_id"] = jeecpot_rewards[0].second_squad_reward.external_id
    if jeecpot_rewards[0].third_squad_reward != None:
        responsejeecpot["third_squad_reward_name"] = jeecpot_rewards[0].third_squad_reward.name
        responsejeecpot["third_squad_reward_id"] = jeecpot_rewards[0].third_squad_reward.external_id
    if jeecpot_rewards[0].king_job_fair_reward != None:
        responsejeecpot["king_job_fair_reward_name"] = jeecpot_rewards[0].king_job_fair_reward.name
        responsejeecpot["king_job_fair_reward_id"] = jeecpot_rewards[0].king_job_fair_reward.external_id
    if jeecpot_rewards[0].king_knowledge_reward != None:
        responsejeecpot["king_knowledge_reward_name"] = jeecpot_rewards[0].king_knowledge_reward.name
        responsejeecpot["king_knowledge_reward_id"] = jeecpot_rewards[0].king_knowledge_reward.external_id
    if jeecpot_rewards[0].king_hacking_reward != None:
        responsejeecpot["king_hacking_reward_name"] = jeecpot_rewards[0].king_hacking_reward.name
        responsejeecpot["king_hacking_reward_id"] = jeecpot_rewards[0].king_hacking_reward.external_id
    if jeecpot_rewards[0].king_networking_reward != None:
        responsejeecpot["king_networking_reward_name"] = jeecpot_rewards[0].king_networking_reward.name
        responsejeecpot["king_networking_reward_id"] = jeecpot_rewards[0].king_networking_reward.external_id
    if jeecpot_rewards[0].cv_platform_raffle_reward != None:
        responsejeecpot["cv_platform_raffle_reward_name"] = jeecpot_rewards[0].cv_platform_raffle_reward.name
        responsejeecpot["cv_platform_raffle_reward_id"] = jeecpot_rewards[0].cv_platform_raffle_reward.external_id
    
    for reward in rewards:
        responserewards.append({"id": reward.external_id,
                                "name": reward.name})

    response = make_response(
    jsonify({'jeecpot_rewards': responsejeecpot,
        'jeecpot_external_id': jeecpot_rewards[0].external_id,
        'rewards': responserewards,
        'error': None
        }))

    return response


@bp.post("/jeecpot-rewards/update")
@requires_client_auth
def update_jeecpot_rewardd():
    jeecpot_external_id = json.loads(request.data.decode('utf-8'))['jeecpot_external_id']
    jeecpot_rewards = RewardsFinder.get_jeecpot_reward_from_external_id(jeecpot_external_id)

    if jeecpot_rewards is None:
        return APIErrorValue("JEECPOT Rewards not found").json(500)

    first_student_reward_id = json.loads(request.data.decode('utf-8'))['first_student_reward_id']
    if first_student_reward_id is not None:
        if first_student_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_student_reward_id=None
            )
        else:
            first_student_reward = RewardsFinder.get_reward_from_external_id(
                first_student_reward_id
            )
            if first_student_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_student_reward_id=first_student_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    second_student_reward_id = json.loads(request.data.decode('utf-8'))['second_student_reward_id']
    if second_student_reward_id is not None:
        if second_student_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_student_reward_id=None
            )
        else:
            second_student_reward = RewardsFinder.get_reward_from_external_id(
                second_student_reward_id
            )
            if second_student_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_student_reward_id=second_student_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    third_student_reward_id = json.loads(request.data.decode('utf-8'))['third_student_reward_id']
    if third_student_reward_id is not None:
        if third_student_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_student_reward_id=None
            )
        else:
            third_student_reward = RewardsFinder.get_reward_from_external_id(
                third_student_reward_id
            )
            if third_student_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_student_reward_id=third_student_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    first_squad_reward_id = json.loads(request.data.decode('utf-8'))['first_squad_reward_id']
    if first_squad_reward_id is not None:
        if first_squad_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_squad_reward_id=None
            )
        else:
            first_squad_reward = RewardsFinder.get_reward_from_external_id(
                first_squad_reward_id
            )
            if first_squad_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, first_squad_reward_id=first_squad_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    second_squad_reward_id = json.loads(request.data.decode('utf-8'))['second_squad_reward_id']
    if second_squad_reward_id is not None:
        if second_squad_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_squad_reward_id=None
            )
        else:
            second_squad_reward = RewardsFinder.get_reward_from_external_id(
                second_squad_reward_id
            )
            if second_squad_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, second_squad_reward_id=second_squad_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    third_squad_reward_id = json.loads(request.data.decode('utf-8'))['third_squad_reward_id']
    if third_squad_reward_id is not None:
        if third_squad_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_squad_reward_id=None
            )
        else:
            third_squad_reward = RewardsFinder.get_reward_from_external_id(
                third_squad_reward_id
            )
            if third_squad_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, third_squad_reward_id=third_squad_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_job_fair_reward_id = json.loads(request.data.decode('utf-8'))['king_job_fair_reward_id']
    if king_job_fair_reward_id is not None:
        if king_job_fair_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_job_fair_reward_id=None
            )
        else:
            king_job_fair_reward = RewardsFinder.get_reward_from_external_id(
                king_job_fair_reward_id
            )
            if king_job_fair_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_job_fair_reward_id=king_job_fair_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_knowledge_reward_id = json.loads(request.data.decode('utf-8'))['king_knowledge_reward_id']
    if king_knowledge_reward_id is not None:
        if king_knowledge_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_knowledge_reward_id=None
            )
        else:
            king_knowledge_reward = RewardsFinder.get_reward_from_external_id(
                king_knowledge_reward_id
            )
            if king_knowledge_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_knowledge_reward_id=king_knowledge_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_hacking_reward_id = json.loads(request.data.decode('utf-8'))['king_hacking_reward_id']
    if king_hacking_reward_id is not None:
        if king_hacking_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_hacking_reward_id=None
            )
        else:
            king_hacking_reward = RewardsFinder.get_reward_from_external_id(
                king_hacking_reward_id
            )
            if king_hacking_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_hacking_reward_id=king_hacking_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    king_networking_reward_id = json.loads(request.data.decode('utf-8'))['king_networking_reward_id']
    if king_networking_reward_id is not None:
        if king_networking_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_networking_reward_id=None
            )
        else:
            king_networking_reward = RewardsFinder.get_reward_from_external_id(
                king_networking_reward_id
            )
            if king_networking_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, king_networking_reward_id=king_networking_reward.id
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    cv_platform_raffle_reward_id = json.loads(request.data.decode('utf-8'))['cv_platform_raffle_reward_id']
    if cv_platform_raffle_reward_id is not None:
        if cv_platform_raffle_reward_id == "":
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards, cv_platform_raffle_reward_id=None
            )
        else:
            cv_platform_raffle_reward = RewardsFinder.get_reward_from_external_id(
                cv_platform_raffle_reward_id
            )
            if cv_platform_raffle_reward is None:
                return APIErrorValue("Reward not found").json(404)
            jeecpot_rewards = RewardsHandler.update_jeecpot_reward(
                jeecpot_rewards,
                cv_platform_raffle_reward_id=cv_platform_raffle_reward.id,
            )
        if jeecpot_rewards is None:
            return APIErrorValue("Failed to update reward").json(500)

    return ('', 204)

@bp.get("/quests")
@requires_client_auth
def all_quests():
    quests = QuestsFinder.get_all()
    quests_to_send = []
    for quest in quests:
        reward = RewardsFinder.get_reward_from_id(quest.reward_id)
        quests_to_send.append({"name":quest.name, "description":quest.description, "reward":reward.name, "external_id":str(quest.external_id),"id":quest.id,"day":quest.day})
    response = make_response(jsonify({
    "quests": quests_to_send,
    }))
    return response

@bp.post("/quest/create")
@requires_client_auth
def create_quest():

    name = request.form.get("name")
    try:
        description =  request.form.get("description")
    except:
        description = ''
    
    reward = RewardsFinder.get_reward_from_external_id(uuid.UUID(request.form.get("reward"))) #get by external
    number_of_activities =  request.form.get("quantity")
    activity_type_external_id = request.form.get("activity_type")
    activity_type = ""
    activity_type_id = -1
    day = request.form.get("day")
    if activity_type_external_id != "":
        activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(activity_type_external_id)) #get by external
        activity_type_id = activity_type.id
        
    try:
        activities =  request.form.get("activities") #get by external
    except:
        activities = None

    activities_id = []
    activities = activities.split(",")
    if activities[0]!='':
        for activity in activities:
            activities_id.append(ActivitiesFinder.get_from_external_id(uuid.UUID(activity)).id) 


    created_quest = QuestsHandler.create_quest(
        name = name,
        description = description,
        activities_id = activities_id,
        reward_id = reward.id,
        number_of_activities = number_of_activities,
        activity_type_id = activity_type_id,
        day = day
    )
    response = make_response(jsonify({
    "error": ""
    }))
    return response

@bp.post("/quest/delete")
@requires_client_auth
def delete_quest():
    quest_external_id = json.loads(request.data.decode('utf-8'))['external_id']
   
    quest_to_delete = QuestsFinder.get_quest_from_external_id(uuid.UUID(quest_external_id))
    if QuestsHandler.delete_quest(quest_to_delete):
        response = make_response(jsonify({
        "error":""
        }))
        return response,204
    else:
        response = make_response(jsonify({
        "error":"Could not delete the quest"
    }))
        return response,200


@bp.get("/quest/create")
@requires_client_auth
def get_all_activities_and_activity_types():
    activities = ActivitiesFinder.get_all()
    activity_types = ActivityTypesFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()
    activities_to_send = [] 
    activity_types_to_send = []
    rewards_to_send = []

    for activity in activities:
        activities_to_send.append({"name":activity.name, "external_id": activity.external_id})
    for activity_type in activity_types:
        activity_types_to_send.append({"name":activity_type.name, "external_id": activity_type.external_id})
    for reward in rewards:
        rewards_to_send.append({"name":reward.name, "external_id": reward.external_id})

    response = make_response(jsonify({
        "activities" : activities_to_send,"activity_types":activity_types_to_send ,"rewards":rewards_to_send, "error":""
    }))
    return response


@bp.post("/quest/info")
@requires_client_auth
def info_quest():

    quest_external_id = json.loads(request.data.decode('utf-8'))['external_id']
    quest = QuestsFinder.get_quest_from_external_id(uuid.UUID(quest_external_id))
    reward = RewardsFinder.get_reward_from_id(quest.reward_id)
    reward_to_send = {"name":reward.name, "external_id": reward.external_id}
    activities_to_send = []
    if quest.activity_type_id == -1:
        for activity_id in quest.activities_id:
            activity = ActivitiesFinder.get_from_id(activity_id)
            if activity != None:
                activities_to_send.append(activity.external_id)

    activity_type_to_send= -1
    if quest.activity_type_id != -1:
        activity_type = ActivityTypesFinder.get_from_activity_type_id(quest.activity_type_id)
        activity_type_to_send = activity_type.external_id
    quest_to_send={
        'name':quest.name,
        'description':quest.description,
        "reward": reward_to_send,
        "quantity":quest.number_of_activities,
        "day": quest.day,
        "activities":activities_to_send,
        "activity_type":activity_type_to_send
    }
   
    activities = ActivitiesFinder.get_all()
    activity_types = ActivityTypesFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()
    activities_to_send = [] 
    activity_types_to_send = []
    rewards_to_send = []

    for activity in activities:
        activities_to_send.append({"name":activity.name, "external_id": activity.external_id})
    for activity_type in activity_types:
        activity_types_to_send.append({"name":activity_type.name, "external_id": activity_type.external_id})
    for reward in rewards:
        rewards_to_send.append({"name":reward.name, "external_id": reward.external_id})
   

    response = make_response(jsonify({
    "quest":quest_to_send,
    "activities":activities_to_send,
    "activity_types":activity_types_to_send,
    "rewards":rewards_to_send,
    "error": ""
    }))
    return response

@bp.post("/quest/update")
@requires_client_auth
def update_quest():

    quest_external_id = request.form.get("external_id")
    quest = QuestsFinder.get_quest_from_external_id(uuid.UUID(quest_external_id))
    name = request.form.get("name")
    try:
        description =  request.form.get("description")
    except:
        description = ''
    
    reward = RewardsFinder.get_reward_from_external_id(uuid.UUID(request.form.get("reward"))) #get by external
    number_of_activities =  request.form.get("quantity")
    activity_type_external_id = request.form.get("activity_type")
    activity_type = ""
    activity_type_id = -1
    day = request.form.get("day")
    if activity_type_external_id != "":
        activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(activity_type_external_id)) #get by external
        activity_type_id = activity_type.id
        
    try:
        activities =  request.form.get("activities") #get by external
    except:
        activities = None

    activities_id = []
    activities = activities.split(",")
    if activities[0]!='':
        for activity in activities:
            activities_id.append(ActivitiesFinder.get_from_external_id(uuid.UUID(activity)).id) 


    updated_quest = QuestsHandler.update_quest(
        quest = quest,
        name = name,
        description = description,
        activities_id = activities_id,
        reward_id = reward.id,
        number_of_activities = number_of_activities,
        activity_type_id = activity_type_id,
        day = day
    )
    response = make_response(jsonify({
    "error": ""
    }))
    return response



@bp.post("/squadrewards_vue")
@requires_client_auth
def squadreward():
    rewards = RewardsFinder.get_all_rewards()
    rewards_to_send = []

    for reward in rewards:
        rewards_to_send.append({"name":reward.name, "external_id": reward.external_id, "id": reward.id})
        
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    squad_rewards_to_send = []
    
    for squad_reward in squad_rewards:
        have_squad_reward = 1
        rewardd = RewardsFinder.get_reward_from_id(squad_reward.reward_id)
        if rewardd == None:
            response = make_response(jsonify({
                "rewards": [], "error":"", 'squad_rewards': []
            }))
            return response
        squad_rewards_to_send.append({"reward_id":squad_reward.reward_id, 
                                      "winner_id":squad_reward.winner_id, 
                                      "external_id": squad_reward.external_id, 
                                      "date": squad_reward.date,
                                      "id": squad_reward.id, 'name': rewardd.name})

    
    datess = EventsHandler.get_event_dates(EventsFinder.get_default_event())
        
    event_dates = []
    i = 0
    for date in datess:
        new_date = {
            'id': i, 'name': date[0:2] + '/' + date[3:5] # 05 03 2023, Sunday
        }
        i = i + 1
        event_dates.append(new_date)
    
    response = make_response(jsonify({
        "rewards":rewards_to_send, "error":"", 'squad_rewards': squad_rewards_to_send, 'dates': event_dates
    }))
    return response

@bp.post("/createsquadreward_vue")
@requires_client_auth
def createsquadreward():
    response = json.loads(request.data.decode('utf-8'))

    try:
        reward_id = response['reward_id']
    except:
        response = make_response(
        jsonify({
            'error': "Failed to create squad reward"
        }))

        return response    
    
    # try:
    #     winner_id = response['winner_id']
    # except:
    #     response = make_response(
    #     jsonify({
    #         'error': "Failed to create squad reward"
    #     }))

    #     return response
    

    try:
        date = response['date']
    except:
        response = make_response(
        jsonify({
            'error': "Failed to create squad reward"
        }))

        return response
    
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    for squad_reward in squad_rewards:
        if date == squad_reward.date:
            response = make_response(
            jsonify({
                'error': "Date already taken"
            }))

            return response

    if reward_id == '' or date == '':
        response = make_response(
        jsonify({
            'error': "Failed to create squad reward"
        }))

        return response
    
    reward = RewardsHandler.create_squad_reward(
        reward_id=reward_id, date=date
    )

    if reward is None:
        response = make_response(
        jsonify({
            'error': "Failed to create reward"
        }))

        return response
    
    response = make_response(
    jsonify({
        'error': ""
    }))

    return response

    
    
@bp.post("/deletesquadreward_vue")
@requires_client_auth
def deletequadreward():
    squad_reward_external_id = json.loads(request.data.decode('utf-8'))['external_id']
    sq_reward = RewardsFinder.get_squad_reward_from_external_id(squad_reward_external_id)

    if RewardsHandler.delete_squad_reward(sq_reward):
        response = make_response(
            jsonify({
                "error": "",
            }))

    else:
        response = make_response(
            jsonify({
                "error": "Failed to delete reward!",
            }))

    return response

@bp.post("/squadreward/update/get")
@requires_client_auth
def update_squad_rewarddd():
    external_id = json.loads(request.data.decode('utf-8'))['external_id']
    squad_reward = RewardsFinder.get_squad_reward_from_external_id(external_id)
    
    try:
        if squad_reward.date is None or squad_reward.reward_id is None:
            response = make_response(
                jsonify({"date": '', "reward_id": '',
                "error": "Couldnt find reward"
                }))
        else:
            response = make_response(
                jsonify({"date": squad_reward.date, "reward_id": squad_reward.reward_id,
                "error": ""
                }))

        return response
    
    except:
        response = make_response(
                jsonify({"date": '', "reward_id": '',
                "error": "Couldnt find reward"
                }))
        return response
        

@bp.post("/squadreward/update")
@requires_client_auth
def update_squad_rewardd():
    response = json.loads(request.data.decode('utf-8'))

    try:
        external_id = response['external_id']  
    except:
        response = make_response(
            jsonify({
            "error": "Couldnt find squad reward"
            }))
        return
    
    squad_reward = RewardsFinder.get_squad_reward_from_external_id(external_id)

    if squad_reward is None:
        response = make_response(
            jsonify({
            "error": "Couldnt find squad reward"
            }))
        return

    try:
        date = response['date']  
    except:
        response = make_response(
            jsonify({
            "error": "Couldnt find squad reward"
            }))
        return 

    try:
        reward_id = response['reward_id']  
    except:
        response = make_response(
            jsonify({
            "error": "Couldnt find squad reward"
            }))
        return
    
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    for squad_rewardd in squad_rewards:
        print(squad_reward.external_id, '.')
        print(squad_rewardd.external_id, '.')
        if date == squad_rewardd.date and squad_rewardd.external_id != squad_reward.external_id:
            response = make_response(
            jsonify({
                'error': "Date already taken"
            }))

            return response
    
    if date == '' or reward_id == '':
        response = make_response(
            jsonify({
            "error": "Couldnt find squad reward"
            }))
        return


    squad_reward = RewardsHandler.update_squad_reward(
        squad_reward, reward_id = reward_id, date=date
    )

    if squad_reward is None:
        response = make_response(
        jsonify({
            "error": "Failed to update squad reward"
        }))

        return response

    response = make_response(
        jsonify({
            "error": ""
        }))

    return response


@bp.post("/student_rewards")
def all_student_rewards():
    response = json.loads(request.data.decode('utf-8'))
    student = StudentsFinder.get_from_ist_id(response["search"])
    if student is None:
        response = make_response(
            jsonify({"rewards":[],
            "error":"Student does not exist"
            })
        )
        return response
    student_rewards = StudentRewardsFinder.get_by_id(student.id)
    rewards_to_send = []
    if student_rewards != []:
        for student_reward in student_rewards:
            reward = RewardsFinder.get_reward_from_id(student_reward.reward_id)
            ist_id = response["search"]
            rewards_to_send.append({"student_id":ist_id,"reward_name":reward.name,"acquired":student_reward.acquired,"ext_id":str(student_reward.external_id)})
    else:
        response = make_response(
        jsonify({"rewards":[],
                 "length":0,
        "error":"Student does have rewards"
        })
    )
    response = make_response(
        jsonify({"rewards":rewards_to_send,
                "length":len(rewards_to_send), 
        "error":""
        })
    )

    return response


@bp.post("/student_rewards/update")
def update_student_rewards():
    response = json.loads(request.data.decode('utf-8'))
    student_reward = StudentRewardsFinder.get_by_external_id(response["external_id"])
    updated = StudentRewardsHandler.update_reward_student(student_reward=student_reward[0],acquired=not student_reward[0].acquired)
    student_rewards = StudentRewardsFinder.get_by_id(student_reward[0].student_id)
    rewards_to_send = []
    if student_rewards != []:
        for student_reward in student_rewards:
            reward = RewardsFinder.get_reward_from_id(student_reward.reward_id)
            ist_id = StudentsFinder.get_from_id( student_reward.student_id).user.username
            rewards_to_send.append({"student_id":ist_id,"reward_name":reward.name,"acquired":student_reward.acquired,"ext_id":str(student_reward.external_id)})
    else:
        response = make_response(
        jsonify({"rewards":[],
                 "length":0,
        "error":"Student does have rewards"
        })
    )
    response = make_response(
        jsonify({"rewards":rewards_to_send,
                "length":len(rewards_to_send), 
        "error":""
        })
    )
    return response

@bp.get("/skywalker")
@requires_client_auth
def skywalker():
    
    banned_students = StudentsFinder.get_all_banned()

    for banned_student in banned_students:
        if banned_student is None:
            return APIErrorValue("Couldnt find student").json(500)

        StudentsHandler.delete_banned_student(banned_student)

    return ('', 204)


#ban all
@bp.get("/order66")
@requires_client_auth
def order66():

    students = StudentsFinder.get_all()
    for student in students:
        if student is None:
            return APIErrorValue("Couldnt find student").json(404)

        if student.squad:
            SquadsHandler.delete_squad(student.squad)

        banned_student = StudentsHandler.create_banned_student(student)
        if banned_student is None:
            return APIErrorValue("Error banning student").json(500)

        UsersHandler.delete_user(Config.ROCKET_CHAT_ENABLE, student.user)

    return ('', 204)

@bp.post("/remove_xp")
@requires_client_auth
def removexp():
    response = json.loads(request.data.decode('utf-8'))

    try:
        xp = response['xp']  
        xp = int(xp)
        student = StudentsFinder.get_from_id(response['student_id'])
    except:
        response = make_response(
            jsonify({
            "error": "Failed to remove xp"
            }))
        return
    
    if student is None:
        return APIErrorValue("Student not found").json(404)

    if not StudentsHandler.remove_points(student, xp):
        return APIErrorValue("Failed to add points to student").json(500)

    return '',204
    
