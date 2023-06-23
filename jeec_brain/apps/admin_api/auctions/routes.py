from re import I
from .. import bp
from flask import render_template, request, redirect, url_for, jsonify, make_response
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.handlers.auctions_handler import AuctionsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.auctions.schemas import AuctionPath
import json

from jeec_brain.apps.auth.wrappers import requires_client_auth

from datetime import datetime

@bp.post("/auctions/get_vue")
@requires_client_auth
def get_auction_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    auction_external_id = response['auction_external_id']
    
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
               {'auction': '', 'error': error}),
            )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #           {'auction': '', 'error': error}),
    #        )
    #    return response
    
    if auction == '':
        error = "Non existant auction"
        response = make_response(jsonify(
               {'auction': '', 'error': error}),
            )
        return response

    vue_participants = []
    
    for part in auction.participants:
        vue_participants.append({"name": part.name, "external_id": part.external_id})
        
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    
    vue_auction = {
        "name": auction.name,
        "external_id": auction.external_id,
        "minimum_value": auction.minimum_value, "description": auction.description, 
        "starting_date": auction.starting_date, 'closing_date': auction.closing_date,
        "starting_time": auction.starting_time, 'closing_time': auction.closing_time, 'highest_bid': highest_bid,
        'participants': vue_participants,
        }
    
    response = make_response(jsonify(
               {'auction': vue_auction, 'error': ''}),
            )
    return response


@bp.post("/auctions_vue")
@requires_client_auth
def update_auction_vue():
    response = json.loads(request.data.decode('utf-8'))
    auction_external_id = response['auction_external_id']

    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
               {'auction': '', 'error': error}),
            )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #           {'auction': '', 'error': error}),
    #        )
    #    return response
    
    if auction == '':
        response = make_response(jsonify(
            {'auction': auction, 'error': "Couldnt find auction"}),
        )
        return response

    vue_participants = []
    
    for part in vue_participants:
        vue_participants.append({"name": part.name, "external_id": part.external_id})
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    
    vue_auction = {
        "name": auction.name,
        "external_id": auction.external_id,
        "minimum_value": auction.minimum_value, "description": auction.description, 
        "starting_date": auction.starting_date, 'closing_date': auction.closing_date,
        "starting_time": auction.starting_time, 'closing_time': auction.closing_time, 'highest_bid': highest_bid,
        'participants': vue_participants,
        }
    
    name = response['name']
    description = response['description']
    starting_date = response['starting_date']
    closing_date = response['closing_date']
    starting_time = response['starting_time']
    closing_time = response['closing_time']

    try:
        minimum_value = float(response['minimum_value'])
    except:
        response = make_response(jsonify(
            {'auction': auction, 'error': "Wrong value format input"}),
        )
        return response

    updated_auction = AuctionsHandler.update_auction(
        auction=auction,
        name=name,
        description=description,
        minimum_value=minimum_value,
        starting_date=starting_date,
        closing_date=closing_date,
        starting_time=starting_time,
        closing_time=closing_time,
    )
    
    if updated_auction == '':
        response = make_response(jsonify(
               {'auction': vue_auction, 'error': "Failed to update auction!"}),
            )
        return response
    
    up_highest_bid = AuctionsFinder.get_auction_highest_bid(updated_auction)
    
    vue_updated_auction = {
        "name": updated_auction.name,
        "external_id": updated_auction.external_id,
        "minimum_value": updated_auction.minimum_value, "description": updated_auction.description, 
        "starting_date": updated_auction.starting_date, 'closing_date': updated_auction.closing_date,
        "starting_time": updated_auction.starting_time, 'closing_time': updated_auction.closing_time, 'highest_bid': up_highest_bid
        }

    response = make_response(jsonify(
            {'auction': vue_updated_auction, 'error': ""}),
        )
    return response


@bp.post("/auctions/delete_vue")
@requires_client_auth
def delete_auction_vue():
    response = json.loads(request.data.decode('utf-8'))

    auction_external_id = response['auction_external_id']

    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
               {'auction': '', 'error': error}),
            )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #           {'auction': '', 'error': error}),
    #        )
    #    return response
    
    if auction == "":
        error = "Couldnt find auction"
        response = make_response(jsonify(
            {'auction': auction, 'error': error}),
        )
        return response
    
    vue_participants = []
    
    for part in auction.participants:
        vue_participants.append({"name": part.name, "external_id": part.external_id})

    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    
    vue_auction = {
        "name": auction.name,
        "external_id": auction.external_id,
        "minimum_value": auction.minimum_value, "description": auction.description, 
        "starting_date": auction.starting_date, 'closing_date': auction.closing_date,
        "starting_time": auction.starting_time, 'closing_time': auction.closing_time, 'highest_bid': highest_bid,
        'participants': vue_participants,
        }
    
    print('Vamos ver se conseguimos apagar a auction')
    print(vue_auction)
    if AuctionsHandler.delete_auction(auction):
        print('Conseguimos')
        response = make_response(jsonify(
            {'auction': vue_auction, 'error': ""}),
        )
        return response

    else:
        print('Nao conseguimos')
        response = make_response(jsonify(
            {'auction': vue_auction, 'error': "Failed to delete auction!"}),
        )
        return response
        
        
# Members management
@bp.post("/auctions/participants_vue")
@requires_client_auth
def auction_participants_dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))
    auction_external_id = response['auction_external_id']
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
               {'auction': '', 'not_participants': '', 'error': error}),
            )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #           {'auction': '', 'not_participants': '', 'error': error}),
    #        )
    #    return response
    
    if auction == '':
        error = "Couldnt find auction"
        response = make_response(jsonify(
               {'auction': auction, 'not_participants': not_participants, 'error': error}),
            )
        return response

    vue_participants = []
    
    for part in auction.participants:
        vue_participants.append({"name": part.name, "external_id": part.external_id})
    
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    
    vue_auction = {
        "name": auction.name,
        "external_id": auction.external_id,
        "minimum_value": auction.minimum_value, "description": auction.description, 
        "starting_date": auction.starting_date, 'closing_date': auction.closing_date,
        "starting_time": auction.starting_time, 'closing_time': auction.closing_time, 'highest_bid': highest_bid,
        'participants': vue_participants,
        }
    
    not_participants = AuctionsFinder.get_not_participants(auction)

    vue_not_participants = []
    
    for not_part in not_participants:
        vue_not_participants.append({"name": not_part.name, "external_id": not_part.external_id})
    
    if len(auction.participants) == 0:
        error = "No results found"
        response = make_response(jsonify(
               {'auction': vue_auction, 'not_participants': vue_not_participants, 'error': error}),
            )
        return response

    response = make_response(jsonify(
               {'auction': vue_auction, 'not_participants': vue_not_participants, 'error': ''}),
            )
    return response


@bp.post("/auctions/add-participant_vue")
@requires_client_auth
def add_auction_participant_vue():
    response = json.loads(request.data.decode('utf-8'))
    auction_external_id = response['auction_external_id']
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
               {'auction_external_id': auction_external_id, 'error': error}),
            )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #           {'auction_external_id': auction_external_id, 'error': error}),
    #        )
    #    return response
    
    if auction == '':
        response = make_response(jsonify(
               {'auction_external_id': auction_external_id, 'error': 'Couldnt find auction'}),
            )
        return response
    

    company_external_id = response['company_external_id']

    if company_external_id == '':
        error = 'Couldnt find company'
        response = make_response(jsonify(
               {'auction_external_id': auction_external_id, 'error': error}),
            )
        return response

    company = CompaniesFinder.get_from_external_id(company_external_id)

    if company == '':
        response = make_response(jsonify(
               {'auction_external_id': auction_external_id, 'error': 'Couldnt find company'}),
            )
        return response

    AuctionsHandler.add_auction_participant(auction, company)

    response = make_response(jsonify(
               {'auction_external_id': auction_external_id, 'error': ''}),
            )
    return response

@bp.get("/auctions/get-name-auctions-dashboard_vue")
@requires_client_auth
def nomenaoimporta_vue():
    return 'Auctions Dashboard'

@bp.post("/auctions/post-description-auctions-dashboard_vue")
@requires_client_auth
def nomenaoimportaa_vue():
    response = json.loads(request.data.decode('utf-8'))
    return response['descriptionn']

@bp.post("/auctions/get-current_user.role.name_vue")
@requires_client_auth
def getCurrentUserRoleName_vue():
    response = json.loads(request.data.decode('utf-8'))
    username = response['username']
    if username == '':
        return ''
    user = UsersFinder.get_user_from_username(username)
    return user.role


@bp.post("/auctions/get-auctions_vue")
@requires_client_auth
def getAuctions_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
               {'auctions': {}, 'error': error}),
            )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #           {'auctions': {}, 'error': error}),
    #        )
    #    return response
    
    auctions_list = AuctionsFinder.get_all()
    for auction in auctions_list:
        auction.highest_bid = AuctionsFinder.get_auction_highest_bid(auction)

        now = datetime.utcnow()
        start = datetime.strptime(
            auction.starting_date + " " + auction.starting_time, "%d %m %Y, %A %H:%M"
        )
        end = datetime.strptime(
            auction.closing_date + " " + auction.closing_time, "%d %m %Y, %A %H:%M"
        )

        auction.is_open = True if now > start and now < end else False

    if auctions_list == "":
        error = "No results found"
        response = make_response(jsonify(
               {'auctions': {}, 'error': error}),
            )
        return response
    
    error=''
   
    auctions_listt = []
    for auction in auctions_list:
        
        vue_participants = []
    
        for part in vue_participants:
            vue_participants.append({"name": part.name, "external_id": part.external_id})
        
        highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
        
        vue_auction = {
        "name": auction.name,
        "external_id": auction.external_id,
        "minimum_value": auction.minimum_value, "description": auction.description, 
        "starting_date": auction.starting_date, 'closing_date': auction.closing_date,
        "starting_time": auction.starting_time, 'closing_time': auction.closing_time, 'highest_bid': highest_bid,
        'participants': vue_participants,
        }
        auctions_listt.append(vue_auction)
        
    response = make_response(jsonify(
               {'auctions': auctions_listt, 'error': error}),
            )
    return response


@bp.post("/auctions/post-new-auction_vue")
@requires_client_auth
def postNewAuction_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    if response['username'] == "":
        error = 'You need to log in'
        return error
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin':
    #    error = 'ACCESS DENIED'
    #    return error
    
    start = datetime.strptime(response['starting_date'] + " " + response['starting_time'], "%d %m %Y, %A %H:%M")
    end = datetime.strptime(response['closing_date'] + " " + response['closing_time'], "%d %m %Y, %A %H:%M")
    if start > end:
        error="Starting date higher then closing!"
        return error
    
    try:
        minimum_value = float(response['minimum_value'])
    except:
        return "Invalid minimum value inserted"
        
    auction = AuctionsHandler.create_auction(name = response['name'], description = response['description'], minimum_value = response['minimum_value'], 
        starting_date = response['starting_date'], starting_time = response['starting_time'], closing_date = response['closing_date'], 
        closing_time = response['closing_time'])
    
    if auction is None:
        error="Failed to create auction!"
        return error

    return ''

# old

# Auction routes
@bp.get("/auctions")
@allowed_roles(["admin"])
def auctions_dashboard():
    auctions_list = AuctionsFinder.get_all()

    for auction in auctions_list:
        auction.highest_bid = AuctionsFinder.get_auction_highest_bid(auction)

        now = datetime.utcnow()
        start = datetime.strptime(
            auction.starting_date + " " + auction.starting_time, "%d %m %Y, %A %H:%M"
        )
        end = datetime.strptime(
            auction.closing_date + " " + auction.closing_time, "%d %m %Y, %A %H:%M"
        )

        auction.is_open = True if now > start and now < end else False

    if auctions_list is None:
        error = "No results found"
        return render_template(
            "admin/auctions/auctions_dashboard.html", auctions=None, error=error
        )

    return render_template(
        "admin/auctions/auctions_dashboard.html", auctions=auctions_list, error=None
    )


@bp.get("/new-auction")
@allowed_roles(["admin"])
def add_auction_dashboard():
    return render_template("admin/auctions/add_auction.html", error=None)


@bp.post("/new-auction")
@allowed_roles(["admin"])
def create_auction():
    name = request.form.get("name")
    description = request.form.get("description")
    starting_date = request.form.get("starting_date")
    closing_date = request.form.get("closing_date")
    starting_time = request.form.get("starting_time")
    closing_time = request.form.get("closing_time")

    try:
        minimum_value = float(request.form.get("minimum_value"))
    except:
        return "Invalid minimum value inserted", 500

    start = datetime.strptime(starting_date + " " + starting_time, "%d %m %Y, %A %H:%M")
    end = datetime.strptime(closing_date + " " + closing_time, "%d %m %Y, %A %H:%M")
    if start > end:
        return render_template(
            "admin/auctions/add_auction.html",
            error="Starting date higher then closing!",
        )

    # create new auction
    auction = AuctionsHandler.create_auction(
        name=name,
        description=description,
        minimum_value=minimum_value,
        starting_date=starting_date,
        closing_date=closing_date,
        starting_time=starting_time,
        closing_time=closing_time,
    )

    if auction is None:
        return render_template(
            "admin/auctions/add_auction.html", error="Failed to create auction!"
        )

    return redirect(url_for("admin_api.auctions_dashboard"))


@bp.get("/auctions/<string:auction_external_id>")
@allowed_roles(["admin"])
def get_auction(path: AuctionPath):
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        error = "Non existant auction"
        return render_template(
            "admin/auctions/auctions_dashboard.html", auctions=None, error=error
        )

    return render_template(
        "admin/auctions/update_auction.html", auction=auction, error=None
    )


@bp.post("/auctions/<string:auction_external_id>")
@allowed_roles(["admin"])
def update_auction(path: AuctionPath):
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        return APIErrorValue("Couldnt find auction").json(500)

    name = request.form.get("name")
    description = request.form.get("description")
    starting_date = request.form.get("starting_date")
    closing_date = request.form.get("closing_date")
    starting_time = request.form.get("starting_time")
    closing_time = request.form.get("closing_time")

    try:
        minimum_value = float(request.form.get("minimum_value"))
    except:
        return APIErrorValue("Wrong value format input").json(400)

    updated_auction = AuctionsHandler.update_auction(
        auction=auction,
        name=name,
        description=description,
        minimum_value=minimum_value,
        starting_date=starting_date,
        closing_date=closing_date,
        starting_time=starting_time,
        closing_time=closing_time,
    )

    if updated_auction is None:
        return render_template(
            "admin/auctions/update_auction.html",
            auction=auction,
            error="Failed to update auction!",
        )

    return redirect(url_for("admin_api.auctions_dashboard"))


@bp.get("/auctions/<string:auction_external_id>/delete")
@allowed_roles(["admin"])
def delete_auction(path: AuctionPath):
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        return APIErrorValue("Couldnt find auction").json(500)

    if AuctionsHandler.delete_auction(auction):
        return redirect(url_for("admin_api.auctions_dashboard"))

    else:
        return render_template(
            "admin/auctions/update_aution.html",
            auction=auction,
            error="Failed to delete auction!",
        )


# Members management
@bp.get("/auctions/<string:auction_external_id>/participants")
@allowed_roles(["admin"])
def auction_participants_dashboard(path: AuctionPath):
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        return APIErrorValue("Couldnt find auction").json(400)

    not_participants = AuctionsFinder.get_not_participants(auction)

    if len(auction.participants) == 0:
        error = "No results found"
        return render_template(
            "admin/auctions/auction_participants_dashboard.html",
            auction=auction,
            not_participants=not_participants,
            error=error,
        )

    return render_template(
        "admin/auctions/auction_participants_dashboard.html",
        auction=auction,
        not_participants=not_participants,
        error=None,
    )


@bp.post("/auctions/<string:auction_external_id>/add-participant")
@allowed_roles(["admin"])
def add_auction_participant(path: AuctionPath):
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        return APIErrorValue("Couldnt find auction").json(400)

    company_external_id = request.form.get("company_external_id")

    if company_external_id is None:
        return redirect(
            url_for(
                "admin_api.auction_participants_dashboard",
                auction_external_id=path.auction_external_id,
            )
        )

    company = CompaniesFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue("Couldnt find company").json(400)

    AuctionsHandler.add_auction_participant(auction, company)

    return redirect(
        url_for(
            "admin_api.auction_participants_dashboard",
            auction_external_id=path.auction_external_id,
        )
    )