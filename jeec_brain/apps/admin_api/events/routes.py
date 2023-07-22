from .. import bp
from flask import render_template, current_app, request, redirect, url_for, make_response, jsonify, send_file
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.schemas.admin_api.events.schemas import *
from flask_login import current_user
from datetime import datetime
import json
from PIL import Image

from jeec_brain.apps.auth.wrappers import requires_client_auth

# Events routes
@bp.get("/events")
def events_dashboard():
    search_parameters = request.args
    name = request.args.get("name")

    # handle search bar requests
    if name is not None:
        search = name
        events_list = EventsFinder.search_by_name(name)

    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = "search name"

        events_list = EventsFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all events
    else:
        search = None
        events_list = EventsFinder.get_all()

    if events_list is None or len(events_list) == 0:
        error = "No results found"
        return render_template(
            "admin/events/events_dashboard.html",
            events=None,
            error=error,
            search=search,
            role=current_user.role,
        )

    now = datetime.utcnow()
    for event in events_list:
        if event.cvs_access_end:
            try:
                cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %b %Y, %a")
            except:
                break
            event.cvs_purgeable = now > cvs_access_end
        else:
            event.cvs_purgeable = False

    return render_template(
        "admin/events/events_dashboard.html",
        events=events_list,
        error=None,
        search=search,
        role=current_user.role,
    )


@bp.post("/events")
def search_event():
    name = request.form.get("name")
    events_list = EventsFinder.search_by_name(name)

    if len(events_list) == 0:
        error = "No results found"
        return render_template(
            "admin/events/events_dashboard.html",
            events=None,
            error=error,
            search=name,
            role=current_user.role,
        )

    return render_template(
        "admin/events/events_dashboard.html",
        events=events_list,
        error=None,
        search=name,
        role=current_user.role,
    )


@bp.get("/new-event")
def add_event_dashboard():
    return render_template("admin/events/add_event.html", error=None)


@bp.post("/new-event")
def create_event():
    name = request.form.get("name")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    cvs_submission_start = request.form.get("cvs_submission_start")
    cvs_submission_end = request.form.get("cvs_submission_end")
    cvs_access_start = request.form.get("cvs_access_start")
    cvs_access_end = request.form.get("cvs_access_end")
    end_game_day = request.form.get("end_game_day")
    end_game_time = request.form.get("end_game_time")
    email = request.form.get("email")
    location = request.form.get("location")
    default = request.form.get("default")
    facebook_event_link = request.form.get("facebook_event_link")
    facebook_link = request.form.get("facebook_link")
    youtube_link = request.form.get("youtube_link")
    instagram_link = request.form.get("instagram_link")
    show_schedule = request.form.get("show_schedule")
    show_registrations = request.form.get("show_registrations")
    show_prizes = request.form.get("show_prizes")

    if default == "True":
        default = True
    else:
        default = False

    if show_schedule == "True":
        show_schedule = True
    else:
        show_schedule = False

    if show_registrations == "True":
        show_registrations = True
    else:
        show_registrations = False

    if show_prizes == "True":
        show_prizes = True
    else:
        show_prizes = False

    event = EventsHandler.create_event(
        name=name,
        start_date=start_date,
        end_date=end_date,
        default=default,
        email=email,
        location=location,
        facebook_link=facebook_link,
        facebook_event_link=facebook_event_link,
        youtube_link=youtube_link,
        instagram_link=instagram_link,
        show_schedule=show_schedule,
        show_registrations=show_registrations,
        show_prizes=show_prizes,
        cvs_submission_start=cvs_submission_start,
        cvs_submission_end=cvs_submission_end,
        cvs_access_start=cvs_access_start,
        cvs_access_end=cvs_access_end,
        end_game_day=end_game_day,
        end_game_time=end_game_time,
    )

    if event is None:
        return render_template(
            "admin/events/add_event.html", error="Failed to create event!"
        )

    # there can only be one default
    if default:
        default_events = EventsFinder.get_from_parameters({"default": True})
        for default_event in default_events:
            if default_event is not event:
                EventsHandler.update_event(event=default_event, default=False)

    if request.files:
        image_file = request.files.get("event_image", None)
        mobile_image_file = request.files.get("event_mobile_image", None)
        blueprint_file = request.files.get("event_blueprint", None)
        schedule_file = request.files.get("event_schedule", None)

        if image_file:
            result, msg = EventsHandler.upload_image(image_file, str(event.external_id))

            if result == False:
                EventsHandler.delete_event(event)
                return render_template("admin/events/add_event.html", error=msg)

        if mobile_image_file:
            image_name = f"{event.external_id}_mobile"
            result, msg = EventsHandler.upload_image(mobile_image_file, image_name)

            if result == False:
                EventsHandler.delete_event(event)
                return render_template("admin/events/add_event.html", error=msg)

        if blueprint_file:
            image_name = f"{event.external_id}_blueprint"
            result, msg = EventsHandler.upload_image(blueprint_file, image_name)

            if result == False:
                EventsHandler.delete_event(event)
                return render_template("admin/events/add_event.html", error=msg)

        if schedule_file:
            image_name = f"{event.external_id}_schedule"
            result, msg = EventsHandler.upload_image(blueprint_file, image_name)

            if result == False:
                EventsHandler.delete_event(event)
                return render_template("admin/events/add_event.html", error=msg)

    return redirect(url_for("admin_api.events_dashboard"))


@bp.get("/events/<string:event_external_id>")
def get_event(path: EventPath):
    event = EventsFinder.get_from_external_id(path.event_external_id)

    if event is None:
        return render_template(url_for("admin_api.add_event_dashboard"))

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    mobile_image_name = f"{event.external_id}_mobile"
    logo_mobile = EventsHandler.find_image(image_name=mobile_image_name)
    schedule_name = f"{event.external_id}_schedule"
    schedule = EventsHandler.find_image(image_name=schedule_name)
    blueprint_name = f"{event.external_id}_blueprint"
    blueprint = EventsHandler.find_image(image_name=blueprint_name)

    return render_template(
        "admin/events/update_event.html",
        event=event,
        logo=logo,
        logo_mobile=logo_mobile,
        schedule=schedule,
        blueprint=blueprint,
        error=None,
    )


@bp.post("/events/<string:event_external_id>")
def update_event(path: EventPath):
    event = EventsFinder.get_from_external_id(path.event_external_id)
    if event is None:
        return APIErrorValue("Couldnt find event").json(500)

    name = request.form.get("name")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    cvs_submission_start = request.form.get("cvs_submission_start")
    cvs_submission_end = request.form.get("cvs_submission_end")
    cvs_access_start = request.form.get("cvs_access_start")
    cvs_access_end = request.form.get("cvs_access_end")
    end_game_day = request.form.get("end_game_day")
    end_game_time = request.form.get("end_game_time")
    default = request.form.get("default")
    email = request.form.get("email")
    location = request.form.get("location")
    facebook_event_link = request.form.get("facebook_event_link")
    facebook_link = request.form.get("facebook_link")
    youtube_link = request.form.get("youtube_link")
    instagram_link = request.form.get("instagram_link")
    show_schedule = request.form.get("show_schedule")
    show_registrations = request.form.get("show_registrations")
    show_prizes = request.form.get("show_prizes")

    if default == "True":
        default = True
    else:
        default = False

    if show_schedule == "True":
        show_schedule = True
    else:
        show_schedule = False

    if show_registrations == "True":
        show_registrations = True
    else:
        show_registrations = False

    if show_prizes == "True":
        show_prizes = True
    else:
        show_prizes = False

    updated_event = EventsHandler.update_event(
        event=event,
        name=name,
        start_date=start_date,
        end_date=end_date,
        default=default,
        email=email,
        location=location,
        facebook_link=facebook_link,
        facebook_event_link=facebook_event_link,
        youtube_link=youtube_link,
        instagram_link=instagram_link,
        show_schedule=show_schedule,
        show_registrations=show_registrations,
        show_prizes=show_prizes,
        cvs_submission_start=cvs_submission_start,
        cvs_submission_end=cvs_submission_end,
        cvs_access_start=cvs_access_start,
        cvs_access_end=cvs_access_end,
        end_game_day=end_game_day,
        end_game_time=end_game_time,
    )

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    mobile_image_name = f"{event.external_id}_mobile"
    logo_mobile = EventsHandler.find_image(image_name=mobile_image_name)
    schedule_name = f"{event.external_id}_schedule"
    schedule = EventsHandler.find_image(image_name=schedule_name)
    blueprint_name = f"{event.external_id}_blueprint"
    blueprint = EventsHandler.find_image(image_name=blueprint_name)

    if updated_event is None:
        return render_template(
            "admin/events/update_event.html",
            event=event,
            logo=logo,
            logo_mobile=logo_mobile,
            schedule=schedule,
            blueprint=blueprint,
            error="Failed to update event",
        )

    # there can only be one default
    if default:
        default_events = EventsFinder.get_from_parameters({"default": True})
        for default_event in default_events:
            if default_event is not updated_event:
                EventsHandler.update_event(event=default_event, default=False)

    current_app.logger.error(request.files)

    if request.files:
        image_file = request.files.get("event_image", None)
        mobile_image_file = request.files.get("event_mobile_image", None)
        blueprint_file = request.files.get("event_blueprint", None)
        schedule_file = request.files.get("event_schedule", None)

        if image_file:
            result, msg = EventsHandler.upload_image(
                image_file, str(updated_event.external_id)
            )
            if result == False:
                return render_template(
                    "admin/events/update_event.html",
                    event=event,
                    logo=logo,
                    logo_mobile=logo_mobile,
                    schedule=schedule,
                    blueprint=blueprint,
                    error=msg,
                )

        if mobile_image_file:
            image_name = f"{updated_event.external_id}_mobile"
            result, msg = EventsHandler.upload_image(mobile_image_file, image_name)
            if result == False:
                return render_template(
                    "admin/events/update_event.html",
                    event=event,
                    logo=logo,
                    logo_mobile=logo_mobile,
                    schedule=schedule,
                    blueprint=blueprint,
                    error=msg,
                )

        if blueprint_file:
            image_name = f"{updated_event.external_id}_blueprint"
            result, msg = EventsHandler.upload_image(blueprint_file, image_name)
            if result == False:
                return render_template(
                    "admin/events/update_event.html",
                    event=event,
                    logo=logo,
                    logo_mobile=logo_mobile,
                    schedule=schedule,
                    blueprint=blueprint,
                    error=msg,
                )

        if schedule_file:
            image_name = f"{updated_event.external_id}_schedule"
            result, msg = EventsHandler.upload_image(schedule_file, image_name)
            if result == False:
                return render_template(
                    "admin/events/update_event.html",
                    event=event,
                    logo=logo,
                    logo_mobile=logo_mobile,
                    schedule=schedule,
                    blueprint=blueprint,
                    error=msg,
                )

    return redirect(url_for("admin_api.events_dashboard"))

#####################################NNNNNNNNEEEEEEEEEEEEEEWWWWWWWWWW

@bp.get("/events/vue")
@requires_client_auth
def events_dashboard_vue():
    events_list = EventsFinder.get_all()

    if events_list is None or len(events_list) == 0:
        error = "No results found"
        return make_response(
            jsonify(
            {
            "events":[],
            "error":error,
            })
        )

    vue_events=[]
    now = datetime.utcnow()
    for event in events_list:
        if event.cvs_access_end:
            try:
                cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %b %Y, %a")
            except:
                cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %m %Y, %A")
            event.cvs_purgeable = now > cvs_access_end
        else:
            event.cvs_purgeable = False

        vue_event={
            "external_id":event.external_id,
            "name":event.name,
            "start_date":event.start_date,
            "end_date":event.end_date,
            "email":event.email,
            "location":event.location,
            "cvs_submission_start":event.cvs_submission_start,
            "cvs_submission_end":event.cvs_submission_end,
            "cvs_access_start":event.cvs_access_start,
            "cvs_access_end":event.cvs_access_end,
            "end_game_day":event.end_game_day,
            "end_game_time":event.end_game_time,
            "cvs_purged":event.cvs_purged,
            "facebook_event_link":event.facebook_event_link,
            "default":event.default,
            "cvs_purgeable":event.cvs_purgeable,
        }
        vue_events.append(vue_event)

        

    return make_response(
            jsonify(
            {
            "events":vue_events,
            "error":'',
            })
        )

@bp.post("/new-event-vue")
@requires_client_auth
def create_event_vue():

    name = request.form['name']
    
    start_date = request.form["start_date"]
 
    end_date = request.form["end_date"]

    cvs_submission_start = request.form["cvs_submission_start"]

    cvs_submission_end = request.form["cvs_submission_end"]

    cvs_access_start = request.form["cvs_access_start"]
   
    cvs_access_end = request.form["cvs_access_end"]
    
    end_game_day = request.form["end_game_day"]
    
    end_game_time = request.form["end_game_time"]
    
    email = request.form["email"]
    
    location = request.form["location"]
   
    default = request.form["default"]
 
    facebook_event_link = request.form["facebook_event_link"]
   
    facebook_link = request.form["facebook_link"]
  
    youtube_link = request.form["youtube_link"]
 
    instagram_link = request.form["instagram_link"]
   
    show_schedule = request.form["show_schedule"]
   
    show_registrations = request.form["show_registrations"]
   
    show_prizes = request.form["show_prizes"]
   

    

    if default == "True":
        default = True
    else:
        default = False

    if show_schedule == "True":
        show_schedule = True
    else:
        show_schedule = False

    if show_registrations == "True":
        show_registrations = True
    else:
        show_registrations = False

    if show_prizes == "True":
        show_prizes = True
    else:
        show_prizes = False

    event = EventsHandler.create_event(
        name=name,
        start_date=start_date,
        end_date=end_date,
        default=default,
        email=email,
        location=location,
        facebook_link=facebook_link,
        facebook_event_link=facebook_event_link,
        youtube_link=youtube_link,
        instagram_link=instagram_link,
        show_schedule=show_schedule,
        show_registrations=show_registrations,
        show_prizes=show_prizes,
        cvs_submission_start=cvs_submission_start,
        cvs_submission_end=cvs_submission_end,
        cvs_access_start=cvs_access_start,
        cvs_access_end=cvs_access_end,
        end_game_day=end_game_day,
        end_game_time=end_game_time,
    )


    if event is None:
        return "Failed to create event!",500


    # there can only be one default
    if default:
        default_events = EventsFinder.get_from_parameters({"default": True})
        for default_event in default_events:
            if default_event is not event:
                EventsHandler.update_event(event=default_event, default=False)

    try:
        image_file = request.files["event_image"]
    except: 
        image_file = None
    
    try:
        mobile_image_file = request.files["event_mobile_image"]
    except: 
        mobile_image_file = None

    try:
        blueprint_file = request.files["event_blueprint"]
    except: 
        blueprint_file = None

    try:
        schedule_file = request.files["event_schedule"]
    except: 
        schedule_file = None


    if image_file:
        result, msg = EventsHandler.upload_image(image_file, str(event.external_id))

        if result == False:
            EventsHandler.delete_event(event)
            return msg,500

    if mobile_image_file:
        image_name = f"{event.external_id}_mobile"
        result, msg = EventsHandler.upload_image(mobile_image_file, image_name)

        if result == False:
            EventsHandler.delete_event(event)
            return msg,500

    if blueprint_file:
        image_name = f"{event.external_id}_blueprint"
        result, msg = EventsHandler.upload_image(blueprint_file, image_name)



        if result == False:
            EventsHandler.delete_event(event)
            return msg,500


    if schedule_file:
        image_name = f"{event.external_id}_schedule"
        result, msg = EventsHandler.upload_image(blueprint_file, image_name)

        if result == False:
            EventsHandler.delete_event(event)
            return msg,500

    return ('', 204)

@bp.post("/event/info")
@requires_client_auth
def get_event_info():
    event = EventsFinder.get_from_external_id(json.loads(request.data.decode('utf-8'))["external_id"])

    if event is None:
        return make_response(
            jsonify({
                "event":{},
                "error":"Event not found"
            })
        )

    logo = EventsHandler.find_image_file(image_name=str(event.external_id))
    if logo:
        image1 = True
    else:
        image1 = False
    mobile_image_name = f"{event.external_id}_mobile"
    logo_mobile = EventsHandler.find_image_file(image_name=mobile_image_name)
    if logo_mobile:
        image2 = True
    else:
        image2 = False
    schedule_name = f"{event.external_id}_schedule"
    schedule = EventsHandler.find_image_file(image_name=schedule_name)
    if schedule:
        image3 = True
    else:
        image3 = False
    blueprint_name = f"{event.external_id}_blueprint"
    blueprint = EventsHandler.find_image_file(image_name=blueprint_name)
    if blueprint:
        image4 = True
    else:
        image4 = False

    vue_event={
            "external_id":event.external_id,
            "name":event.name,
            "start_date":event.start_date,
            "end_date":event.end_date,
            "email":event.email,
            "location":event.location,
            "cvs_submission_start":event.cvs_submission_start,
            "cvs_submission_end":event.cvs_submission_end,
            "cvs_access_start":event.cvs_access_start,
            "cvs_access_end":event.cvs_access_end,
            "end_game_day":event.end_game_day,
            "end_game_time":event.end_game_time,
            "facebook_event_link":event.facebook_event_link,
            "facebook_link":event.facebook_link,
            "youtube_link":event.youtube_link,
            "instagram_link":event.instagram_link,
            "image1":image1,
            "image2":image2,
            "image3":image3,
            "image4":image4,
        }

    if(event.default):
        vue_event["default"] = "True"
    
    else:
        vue_event["default"] = "False"
    
    if(event.show_schedule):
        vue_event["show_schedule"] = "True"
    
    else:
        vue_event["show_schedule"] = "False"

    if(event.show_registrations):
        vue_event["show_registrations"] = "True"
    
    else:
        vue_event["show_registrations"] = "False"

    if(event.show_prizes):
        vue_event["show_prizes"] = "True"
    
    else:
        vue_event["show_prizes"] = "False"

    

    return make_response(
            jsonify({
                "event":vue_event,
                "error":""
            })
        )

@bp.post("getimageevent1")
@requires_client_auth
def get_image_event1():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    event = EventsFinder.get_from_external_id(external_id)

    fileUp = EventsHandler.find_image_file(image_name=str(event.external_id))
    
    print(fileUp)

    if not fileUp:
        return '',404
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )

@bp.post("getimageevent2")
@requires_client_auth
def get_image_event2():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    event = EventsFinder.get_from_external_id(external_id)

    mobile_image_name = f"{event.external_id}_mobile"
    fileUp = EventsHandler.find_image_file(image_name=str(mobile_image_name))
    
    print(fileUp)

    if not fileUp:
        return '',404
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )

@bp.post("getimageevent3")
@requires_client_auth
def get_image_event3():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    event = EventsFinder.get_from_external_id(external_id)

    schedule_name = f"{event.external_id}_schedule"
    fileUp = EventsHandler.find_image_file(image_name=str(schedule_name))
    
    print(fileUp)

    if not fileUp:
        return '',404
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )

@bp.post("getimageevent4")
@requires_client_auth
def get_image_event4():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    event = EventsFinder.get_from_external_id(external_id)

    blueprint_name = f"{event.external_id}_blueprint"
    fileUp = EventsHandler.find_image_file(image_name=str(blueprint_name))
    
    print(fileUp)

    if not fileUp:
        return '',404
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )


@bp.post("/update-event-vue")
@requires_client_auth
def update_event_vue():
    event = EventsFinder.get_from_external_id(request.form['external_id'])
    if event is None:
        return APIErrorValue("Couldnt find event").json(500)

    name = request.form['name']

    start_date = request.form["start_date"]
 
    end_date = request.form["end_date"]

    cvs_submission_start = request.form["cvs_submission_start"]

    cvs_submission_end = request.form["cvs_submission_end"]

    cvs_access_start = request.form["cvs_access_start"]
   
    cvs_access_end = request.form["cvs_access_end"]
    
    end_game_day = request.form["end_game_day"]
    
    end_game_time = request.form["end_game_time"]
    
    email = request.form["email"]
    
    location = request.form["location"]
   
    default = request.form["default"]
 
    facebook_event_link = request.form["facebook_event_link"]
   
    facebook_link = request.form["facebook_link"]
  
    youtube_link = request.form["youtube_link"]
 
    instagram_link = request.form["instagram_link"]
   
    show_schedule = request.form["show_schedule"]
   
    show_registrations = request.form["show_registrations"]
   
    show_prizes = request.form["show_prizes"]

    if default == "True":
        default = True
    else:
        default = False

    if show_schedule == "True":
        show_schedule = True
    else:
        show_schedule = False

    if show_registrations == "True":
        show_registrations = True
    else:
        show_registrations = False

    if show_prizes == "True":
        show_prizes = True
    else:
        show_prizes = False

    updated_event = EventsHandler.update_event(
        event=event,
        name=name,
        start_date=start_date,
        end_date=end_date,
        default=default,
        email=email,
        location=location,
        facebook_link=facebook_link,
        facebook_event_link=facebook_event_link,
        youtube_link=youtube_link,
        instagram_link=instagram_link,
        show_schedule=show_schedule,
        show_registrations=show_registrations,
        show_prizes=show_prizes,
        cvs_submission_start=cvs_submission_start,
        cvs_submission_end=cvs_submission_end,
        cvs_access_start=cvs_access_start,
        cvs_access_end=cvs_access_end,
        end_game_day=end_game_day,
        end_game_time=end_game_time,
    )

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    mobile_image_name = f"{event.external_id}_mobile"
    logo_mobile = EventsHandler.find_image(image_name=mobile_image_name)
    schedule_name = f"{event.external_id}_schedule"
    schedule = EventsHandler.find_image(image_name=schedule_name)
    blueprint_name = f"{event.external_id}_blueprint"
    blueprint = EventsHandler.find_image(image_name=blueprint_name)

    if updated_event is None:
        return "Failed to update event", 500
        

    # there can only be one default
    if default:
        default_events = EventsFinder.get_from_parameters({"default": True})
        for default_event in default_events:
            if default_event is not updated_event:
                EventsHandler.update_event(event=default_event, default=False)

    current_app.logger.error(request.files)

    try:
        image_file = request.files["event_image"]
    except: 
        image_file = None
    
    try:
        mobile_image_file = request.files["event_mobile_image"]
    except: 
        mobile_image_file = None

    try:
        blueprint_file = request.files["event_blueprint"]
    except: 
        blueprint_file = None

    try:
        schedule_file = request.files["event_schedule"]
    except: 
        schedule_file = None

    if image_file:
        result, msg = EventsHandler.upload_image(
            image_file, str(updated_event.external_id)
        )
        if result == False:
            return msg, 500

    if mobile_image_file:
        image_name = f"{updated_event.external_id}_mobile"
        result, msg = EventsHandler.upload_image(mobile_image_file, image_name)
        if result == False:
            return msg, 500

    if blueprint_file:
        image_name = f"{updated_event.external_id}_blueprint"
        result, msg = EventsHandler.upload_image(blueprint_file, image_name)
        if result == False:
            return msg, 500

    if schedule_file:
        image_name = f"{updated_event.external_id}_schedule"
        result, msg = EventsHandler.upload_image(schedule_file, image_name)
        if result == False:
            return msg, 500

    return '',204

# @bp.post('/events/<string:event_external_id>/purge_cvs')
# @allowed_roles(['admin'])
# def purge_cvs(event_external_id):
#     event = EventsFinder.get_from_external_id(event_external_id)
#     if event is None:
#         return APIErrorValue('Couldnt find event').json(500)

#     #
#     #
#     #
