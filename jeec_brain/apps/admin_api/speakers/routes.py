from .. import bp
from flask import render_template, request, redirect, url_for, current_app, make_response, jsonify, send_file
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.handlers.speakers_handler import SpeakersHandler
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.speakers.schemas import *
from flask_login import current_user
from jeec_brain.services.files.rename_image_service import RenameImageService
from PIL import Image

from jeec_brain.apps.auth.wrappers import requires_client_auth


import json


@bp.get("/speakers")
@allow_all_roles
def speakers_dashboard():
    speakers_list = SpeakersFinder.get_all()

    if len(speakers_list) == 0:
        error = "No results found"
        return render_template(
            "admin/speakers/speakers_dashboard.html",
            speakers=None,
            error=error,
            search=None,
            role=current_user.role.name,
        )

    return render_template(
        "admin/speakers/speakers_dashboard.html",
        speakers=speakers_list,
        error=None,
        search=None,
        role=current_user.role.name,
    )


@bp.post("/speakers")
@allow_all_roles
def search_speaker():
    name = request.form.get("name")
    speakers_list = SpeakersFinder.search_by_name(name)

    if len(speakers_list) == 0:
        error = "No results found"
        return render_template(
            "admin/speakers/speakers_dashboard.html",
            speakers=speakers_list,
            error=error,
            search=name,
        )

    return render_template(
        "admin/speakers/speakers_dashboard.html",
        speakers=speakers_list,
        error=None,
        search=name,
    )


@bp.get("/new-speaker")
@allowed_roles(["admin", "speakers_admin"])
def add_speaker_dashboard():
    return render_template("admin/speakers/add_speaker.html")


@bp.post("/new-speaker")
@allowed_roles(["admin", "speakers_admin"])
def create_speaker():
    name = request.form.get("name")
    company = request.form.get("company")
    company_link = request.form.get("company_link")
    position = request.form.get("position")
    country = request.form.get("country")
    bio = request.form.get("bio")
    linkedin_url = request.form.get("linkedin_url")
    youtube_url = request.form.get("youtube_url")
    website_url = request.form.get("website_url")
    spotlight = request.form.get("spotlight")

    if spotlight == "True":
        spotlight = True
    else:
        spotlight = False

    speaker = SpeakersHandler.create_speaker(
        name=name,
        company=company,
        company_link=company_link,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url,
        youtube_url=youtube_url,
        website_url=website_url,
        spotlight=spotlight,
    )

    if speaker is None:
        return render_template(
            "admin/speakers/add_speaker.html", error="Failed to create speaker!"
        )

    if "speaker_image" in request.files:
        file = request.files["speaker_image"]
        if file.filename:
            result, msg = SpeakersHandler.upload_image(file, name)

            if result == False:
                SpeakersHandler.delete_speaker(speaker)
                return render_template("admin/speakers/add_speaker.html", error=msg)

    if speaker.company and "company_logo" in request.files:
        file = request.files["company_logo"]
        if file.filename:
            result, msg = SpeakersHandler.upload_company_logo(file, company)

            if result == False:
                SpeakersHandler.delete_speaker(speaker)
                return render_template("admin/speakers/add_speaker.html", error=msg)

    return redirect(url_for("admin_api.speakers_dashboard"))


@bp.get("/speaker/<string:speaker_external_id>")
@allowed_roles(["admin", "speakers_admin"])
def get_speaker(path: SpeakerPath):
    speaker = SpeakersFinder.get_from_external_id(path.speaker_external_id)

    image_path = SpeakersHandler.find_image(speaker.name)

    company_logo_path = None
    if speaker.company is not None:
        company_logo_path = SpeakersHandler.find_company_logo(speaker.company)

    return render_template(
        "admin/speakers/update_speaker.html",
        speaker=speaker,
        image=image_path,
        company_logo=company_logo_path,
        error=None,
    )


@bp.post("/speaker/<string:speaker_external_id>")
@allowed_roles(["admin", "speakers_admin"])
def update_speaker(path: SpeakerPath):

    speaker = SpeakersFinder.get_from_external_id(path.speaker_external_id)

    if speaker is None:
        return APIErrorValue("Couldnt find speaker").json(500)

    name = request.form.get("name")
    company = request.form.get("company")
    company_link = request.form.get("company_link")
    position = request.form.get("position")
    country = request.form.get("country")
    bio = request.form.get("bio")
    linkedin_url = request.form.get("linkedin_url")
    youtube_url = request.form.get("youtube_url")
    website_url = request.form.get("website_url")
    spotlight = request.form.get("spotlight")

    if spotlight == "True":
        spotlight = True
    else:
        spotlight = False

    image_path = SpeakersHandler.find_image(name)
    company_logo_path = SpeakersHandler.find_company_logo(company)

    old_speaker_name = speaker.name
    old_company_name = speaker.company

    updated_speaker = SpeakersHandler.update_speaker(
        speaker=speaker,
        name=name,
        company=company,
        company_link=company_link,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url,
        youtube_url=youtube_url,
        website_url=website_url,
        spotlight=spotlight,
    )

    if updated_speaker is None:
        return render_template(
            "admin/speakers/update_speaker.html",
            speaker=speaker,
            image=image_path,
            company_logo=company_logo_path,
            error="Failed to update speaker!",
        )

    # Handle Speaker image ------------------------------------
    if old_speaker_name != name:
        RenameImageService("static/speakers", old_speaker_name, name).call()

    if "file" in request.files:
        file = request.files["file"]
        if file.filename:

            result, msg = SpeakersHandler.upload_image(file, name)

            if result == False:
                return render_template(
                    "admin/speakers/update_speaker.html",
                    speaker=updated_speaker,
                    image=image_path,
                    company_logo=company_logo_path,
                    error=msg,
                )

    # Handle Speaker's Company image ---------------------------
    if old_company_name != company:
        RenameImageService(
            "static/speakers/companies", old_company_name, company
        ).call()

    if updated_speaker.company and "company_logo" in request.files:
        file = request.files["company_logo"]
        if file.filename:
            result, msg = SpeakersHandler.upload_company_logo(file, company)

            if result == False:
                return render_template(
                    "admin/speakers/update_speaker.html",
                    speaker=updated_speaker,
                    image=image_path,
                    company_logo=company_logo_path,
                    error=msg,
                )

    return redirect(url_for("admin_api.speakers_dashboard"))


@bp.get("/speaker/<string:speaker_external_id>/delete")
@allowed_roles(["admin", "speakers_admin"])
def delete_speaker(path: SpeakerPath):
    speaker = SpeakersFinder.get_from_external_id(path.speaker_external_id)

    if speaker is None:
        return APIErrorValue("Couldnt find speaker").json(500)

    name = speaker.name
    company = speaker.company

    if SpeakersHandler.delete_speaker(speaker):
        return redirect(url_for("admin_api.speakers_dashboard"))

    else:
        image_path = SpeakersHandler.find_image(name)
        return render_template(
            "admin/speakers/update_speaker.html",
            speaker=speaker,
            image=image_path,
            company_logo=CompaniesHandler.find_image(company.name),
            error="Failed to delete speaker!",
        )

# #versao vue
@bp.get("/speakerss")
@requires_client_auth
def speakers_dashboard_vue():
    
    speakers_list = SpeakersFinder.get_all()
    
    if len(speakers_list) == 0:
        error = 'No results found'
        
        response = make_response(
        jsonify({
            "speakers": [],
        })
        )
        return response
    speakers = []
    for speaker in speakers_list:
        vue_speaker = {
            "id": speaker.id,
            "name": speaker.name,
            "company": speaker.company,
            "company_link": speaker.company_link,
            "position": speaker.position,
            "country": speaker.country,
            "bio": speaker.bio,
            "linkedin_url": speaker.linkedin_url,
            "youtube_url": speaker.youtube_url,
            "website_url": speaker.website_url,
            "spotlight": speaker.spotlight,
            "external_id": speaker.external_id
        }
        speakers.append(vue_speaker)

    response = make_response(
    jsonify({
        "speakers": speakers,
    })
    )
    return response


@bp.post("/speakers/create_url_error_speaker")
@requires_client_auth
def create_url_error_speaker_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    speaker = SpeakersFinder.get_from_external_id(external_id)
    speaker_name = speaker.name
    
    fileUp = SpeakersHandler.get_image_speaker(speaker_name)
    
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

@bp.post("/speakers/create_url_error_company")
@requires_client_auth
def create_url_error_company_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    speaker = SpeakersFinder.get_from_external_id(external_id)
    speaker_company = speaker.company
    
    fileUp=None
    if(speaker.company!=''):
        fileUp = SpeakersHandler.get_image_company(speaker_company)
    
    if fileUp == None:
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




@bp.post("getimagespeakerrrr")
@requires_client_auth
def getimagespeakerrrr_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    speaker = SpeakersFinder.get_from_external_id(external_id)
    speaker_name = speaker.name
    print(speaker_name)
    
    fileUp = SpeakersHandler.get_image_speaker(speaker_name)
    
    print(fileUp)

    if not fileUp:
        return "Invalid zip file",200
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )
    
@bp.post("getimagescompany")
@requires_client_auth
def getimagescompany_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    speaker = SpeakersFinder.get_from_external_id(external_id)
    speaker_company = speaker.company
    fileUp=None
    if(speaker.company!=''):
        fileUp = SpeakersHandler.get_image_company(speaker_company)
    
    

    if fileUp == None:
        return "Invalid zip file",200
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )


@bp.post("/new-speaker-vue")
@requires_client_auth
def create_speaker_vue():
    
    name = request.form["name"]
    company = request.form["company"]
    company_link = request.form["company_link"]
    position = request.form["position"]
    country = request.form["country"]
    bio = request.form["bio"]
    linkedin_url = request.form["linkedin_url"]
    youtube_url = request.form["youtube_url"]
    website_url = request.form["website_url"]
    spotlight = request.form["spotlight"]
    
    
    if spotlight == "True":
        spotlight = True
    else:
        spotlight = False

    speaker = SpeakersHandler.create_speaker(
        name=name,
        company=company,
        company_link=company_link,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url,
        youtube_url=youtube_url,
        website_url=website_url,
        spotlight=spotlight,
    )

    if speaker is None:
        response = make_response(
        jsonify({
            "error" : 'Failed to create speaker!',
        })
        )
        return response

    if "speaker_image" in request.files:
        file = request.files["speaker_image"]
        if file.filename:
            result, msg = SpeakersHandler.upload_image(file, name)

            if result == False:
                SpeakersHandler.delete_speaker(speaker)
                response = make_response(
                jsonify({
                    "error" : msg,
                })
                )
                return response

    if "company_logo" in request.files:
        file = request.files["company_logo"]
        if file.filename:
            result, msg = SpeakersHandler.upload_company_logo(file, company)

            if result == False:
                SpeakersHandler.delete_speaker(speaker)
                response = make_response(
                jsonify({
                    "error" : msg,
                })
                )
                return response

    response = make_response(
    jsonify({
        "error" : '',
    })
    )
    return response


@bp.post("/getspeaker")
@requires_client_auth
def getspeaker_vue():
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    speaker = SpeakersFinder.get_from_external_id(external_id)

    image_path = SpeakersHandler.find_image(speaker.name)

    company_logo_path = None
    if speaker.company != '':
        company_logo_path = SpeakersHandler.find_company_logo(speaker.company)

    vue_speaker = {
    "name": speaker.name,
    "company": speaker.company,
    "company_link": speaker.company_link,
    "position": speaker.position,
    "country": speaker.country,
    "bio": speaker.bio,
    "linkedin_url": speaker.linkedin_url,
    "youtube_url": speaker.youtube_url,
    "website_url": speaker.website_url,
    "spotlight": speaker.spotlight,
    "external_id": speaker.external_id
    }

    
    response = make_response(
    jsonify({
        "speaker" : vue_speaker,
        "error" : '',
        "image" : image_path,
        "company_logo": company_logo_path,
    })
    )
    return response


@bp.post("/speaker/speaker_external_id")
@requires_client_auth
def update_speaker_vue():
    
    name = request.form["name"]
    external_id = request.form["external_id"]
    company = request.form["company"]
    company_link = request.form["company_link"]
    position = request.form["position"]
    country = request.form["country"]
    bio = request.form["bio"]
    linkedin_url = request.form["linkedin_url"]
    youtube_url = request.form["youtube_url"]
    website_url = request.form["website_url"]
    spotlight = request.form["spotlight"]
    
    if spotlight == "True":
        spotlight = True
    else:
        spotlight = False
        
    speaker = SpeakersFinder.get_from_external_id(external_id)
    
    if speaker is None:
       
        msg = "Couldnt find speaker"
        response = make_response(
            jsonify({
                "error" : msg,
            })
        )
        return response

    

    old_speaker_name = speaker.name
    old_company_name = speaker.company
    

    updated_speaker = SpeakersHandler.update_speaker(
        speaker=speaker,
        name=name,
        company=company,
        company_link = company_link,
        linkedin_url=linkedin_url,
        youtube_url=youtube_url,
        website_url=website_url,
        spotlight=spotlight,
        position=position,
        country=country,
        bio=bio
    )

    if updated_speaker is None:
        error="Failed to update speaker!"
        response = make_response(
        jsonify({
            "error" : error,
        })
        )
        return response
    
    # Handle Speaker image ------------------------------------
    print(name)
    print(old_speaker_name)
    if old_speaker_name != name:
        RenameImageService("static/speakers", old_speaker_name, name).call()

    if "speaker_image" in request.files:
        file = request.files["speaker_image"]
        print(file.filename)
        if file.filename:

            result, msg = SpeakersHandler.upload_image(file, name)

            if result == False:
                response = make_response(
                jsonify({
                    "error" : msg,
                })
                )
                return response

    # Handle Speaker's Company image ---------------------------
    if old_company_name != company:
        RenameImageService(
            "static/speakers/companies", old_company_name, company
        ).call()

    if "company_logo" in request.files:
        file = request.files["company_logo"]
        if file.filename:
            result, msg = SpeakersHandler.upload_company_logo(file, company)

            if result == False:
                response = make_response(
                jsonify({
                    "error" : msg,
                })
                )
                return response

    response = make_response(
        jsonify({
            "error" : '',
        })
    )
    return response


@bp.post("/speaker/delete")
@requires_client_auth
def delete_speaker_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    
    external_id = response['external_id'] 
    speaker = SpeakersFinder.get_from_external_id(external_id)

    if speaker is None:
        error = 'Couldnt find speaker'
        response = make_response(
        jsonify({
            "error" : error,
        })
        )
        return response

    name = speaker.name
    company = speaker.company

    if SpeakersHandler.delete_speaker(speaker):
        response = make_response(
        jsonify({
            "error" : '',
        })
        )
        return response

    else:
        error='Failed to delete speaker!'
        response = make_response(
        jsonify({
            "error" : error,
        })
        )
        return response
