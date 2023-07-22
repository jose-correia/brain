import json
from logging import warning
from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for, jsonify, make_response
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.auctions_handler import AuctionsHandler
from jeec_brain.models.company_users import CompanyUsers
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.companies_api.auctions.schemas import AuctionPath
from jeec_brain.apps.auth.wrappers import requires_client_auth

from datetime import datetime


@bp.get("/auction/<string:auction_external_id>")
@require_company_login
def auction_dashboard(company_user, path: AuctionPath):
    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        return APIErrorValue("Couldnt find auction").json(400)

    # check if company is allowed in auction
    if company_user.company not in auction.participants:
        return APIErrorValue("Company not allowed in this auction").json(400)

    # check if auction is open
    start = datetime.strptime(
        auction.starting_date + " " + auction.starting_time, "%d %b %Y, %a %H:%M"
    )
    end = datetime.strptime(
        auction.closing_date + " " + auction.closing_time, "%d %b %Y, %a %H:%M"
    )
    now = datetime.utcnow()
    auction.is_open = True if now > start and now < end else False

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    if highest_bid is None:
        highest_bid = None
        highest_bidder_logo = None
        highest_bidder_name = None
    else:
        # if highest bid is anonymous retrieve anonymous logo
        if highest_bid.is_anonymous is True:
            highest_bidder_logo = "/static/jeec_logo_mobile.svg"
            highest_bidder_name = "Anonymous bidder"
        else:
            highest_bidder = CompaniesFinder.get_from_company_user_id(highest_bid.company_user_id)
            company_logo = CompaniesHandler.find_image(highest_bidder.name)
            highest_bidder_logo = company_logo
            highest_bidder_name = highest_bidder.name

    # get all company bids
    company_bids = AuctionsFinder.get_company_bids_from_user(auction, company_user)

    # get all logos of companies in the auction
    participant_logos = []
    for participant in auction.participants:
        participant_logo = CompaniesHandler.find_image(participant.name)
        participant_logos.append(participant_logo)

    return render_template(
        "companies/auction/auction_dashboard.html",
        auction=auction,
        highest_bid=highest_bid,
        highest_bidder_name=highest_bidder_name,
        highest_bidder_logo=highest_bidder_logo,
        company_bids=company_bids,
        participant_logos=participant_logos,
        error=None,
        user=company_user,
        warning=request.args.get("warning", ""),
        search=None,
    )


@bp.post("/auction/<string:auction_external_id>/bid")
@require_company_login
def auction_bid(company_user, path: AuctionPath):
    try:
        value = float(request.form.get("value"))
    except:
        return redirect(
            url_for(
                "companies_api.auction_dashboard",
                auction_external_id=path.auction_external_id,
            )
        )

    is_anonymous = request.form.get("is_anonymous")

    if is_anonymous == "True":
        is_anonymous = True
    else:
        is_anonymous = False

    # get company
    company = CompaniesFinder.get_from_name(company_user.company.name)

    if company is None:
        return APIErrorValue("Couldnt find company").json(400)

    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(path.auction_external_id)

    if auction is None:
        return APIErrorValue("Couldnt find auction").json(400)

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)

    if highest_bid is None:
        highest_bid_value = 0
    else:
        highest_bid_value = highest_bid.value

    # check if value is bigger than current highest bid
    if value < auction.minimum_value:
        return redirect(
            url_for(
                "companies_api.auction_dashboard",
                auction_external_id=auction.external_id,
                warning="Must be higher than minimum bid",
            )
        )
    elif value < highest_bid_value:
        return redirect(
            url_for(
                "companies_api.auction_dashboard",
                auction_external_id=auction.external_id,
                warning="Must be higher than current highest bid",
            )
        )

    if AuctionsHandler.create_auction_bid(
        auction=auction,
        company_user=company_user,
        value=value,
        is_anonymous=is_anonymous,
    ):
        if highest_bid:
            highest_bidder = CompaniesFinder.get_from_company_user_id(
                highest_bid.company_user_id
            )
            if highest_bidder and not highest_bidder.id == company.id:
                company_particiants = AuctionsFinder.get_company_users_from_auction(
                    highest_bidder, auction
                )
                AuctionsHandler.send_bid_update_email(
                    company_particiants, auction, value
                )

    return redirect(
        url_for(
            "companies_api.auction_dashboard", auction_external_id=auction.external_id
        )
    )

################################################################################
# bid_auction() - Receives as arguments the user, the bid value, if the bid    #
# was anonymous and the auction's external id. From the user we get the company#
# that made the bid. This endpoint is only reached when a bid is made. It sends#
# data back to the frontend relative to the auction, such as the updated       #
# highest bid and the new bid history.
################################################################################


@bp.post("/auctiondashboard_vue/bid")
@requires_client_auth
def bid_auction():
   
    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    bid_value = response['bid_value']
    is_anonymous = response['is_anonymous']
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
    external_id = response['auction_ex_id']

  
    # get company
    company = CompaniesFinder.get_from_name(company_user.company.name)

    if company is None:
        return make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Couldn't find auction"
            })
        )

    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(external_id)

    if auction is None:
        return  make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Company not allowed in this auction"
            })
        )

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)

    if AuctionsHandler.create_auction_bid(
        auction=auction,
        company_user=company_user,
        value=bid_value,
        is_anonymous=is_anonymous,
    ):
        if highest_bid:
            highest_bidder = CompaniesFinder.get_from_company_id(
                highest_bid.company_user_id
            )
            if highest_bidder and not highest_bidder.id == company.id:
                company_particiants = AuctionsFinder.get_company_users_from_auction(
                    highest_bidder, auction
                )
                AuctionsHandler.send_bid_update_email(
                    company_particiants, auction, bid_value
                )

    start = datetime.strptime(
        auction.starting_date + " " + auction.starting_time, "%d %b %Y, %a %H:%M"
    )
    end = datetime.strptime(
        auction.closing_date + " " + auction.closing_time, "%d %b %Y, %a %H:%M"
    )
    now = datetime.utcnow()
    auction.is_open = True if now > start and now < end else False

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    if highest_bid is None:
        highest_bid = None
        highest_bidder_logo = None
        highest_bidder_name = None
    else:
        # if highest bid is anonymous retrieve anonymous logo
        if highest_bid.is_anonymous is True:
            highest_bidder_logo = "brain.png"
            highest_bidder_name = "Anonymous bidder"
        else:
            highest_bidder = CompaniesFinder.get_from_company_user_id(highest_bid.company_user_id)
            image_name = highest_bidder.name
            image_name = image_name.lower()
            image_name = image_name.replace(" ", "_")
            image_name = image_name + ".png"
            highest_bidder_logo = image_name
            highest_bidder_name = highest_bidder.name

    # get all company bids
    company_bids = AuctionsFinder.get_company_bids_from_user(auction, company_user)
  
    # get all logos of companies in the auction
    participant_logos = []
    for participant in auction.participants:
        image_name = participant.name
        image_name = image_name.lower()
        image_name = image_name.replace(" ", "_")
        image_name = image_name + ".png"
        participant_logos.append(image_name)

    jsonbids = []
    for bid in auction.bids:
        jsonbid={
            "is_anonymous" : bid.is_anonymous,
            "value" : bid.value
        }
        jsonbids.append(jsonbid)

    jsoncompanybids = []
    for bid in company_bids:
        jsoncompanybid={
            "is_anonymous" : bid.is_anonymous,
            "value" : bid.value,
            "created_at":bid.created_at
        }
        jsoncompanybids.append(jsoncompanybid)
    
    return make_response(
            jsonify({
            "auction":{
                "name": auction.name,
                "bids":jsonbids,
                "bids_len":len(jsonbids),
                "description":auction.description,
                "minimum_value":auction.minimum_value,
                "is_open":auction.is_open,
                "starting_date":auction.starting_date,
                "starting_time":auction.starting_time,
                "closing_date":auction.closing_date,
                "closing_time":auction.closing_time,
            },
            "user_name": user.username,
            "company_name":company.name,
            "error": "",
            "warning": "",
            "highest_bid":{"value":highest_bid.value,
                            "created_at": highest_bid.created_at},
            "highest_bidder_name":highest_bidder_name,
            "highest_bidder_logo":highest_bidder_logo,
            "participant_logos":participant_logos,
            "company_bids":jsoncompanybids,
            "company_bids_len":len(jsoncompanybids)
           
            })
        )
 

################################################################################
# auction_dashboard_vue() - Receives as arguments the user and the auction's   #
# external id.This endpoint is reached when an auction is selected.It sends    #
# data back to the frontend relative to the auction, such as the               #
# highest bid, the bid history and the participant logos.
################################################################################

@bp.post("/auctiondashboard_vue/:auction_external_id")
@requires_client_auth
def auction_dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    external_id = response['auction_ex_id']
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
    
    if len(external_id) != 36:
        return make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Couldn't find auction, this might be due to an URL being manually changed",
            "valid": False
            })
        )

    auction = AuctionsFinder.get_auction_by_external_id(external_id)

    if auction is None:
        return make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Couldn't find auction, this might be due to an URL being manually changed",
            "valid": False
            })
        )

    # check if company is allowed in auction
    if company_user.company not in auction.participants:
        return make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Company not allowed in this auction",
            "valid":False
            })
        )

    # check if auction is open
    start = datetime.strptime(
        auction.starting_date + " " + auction.starting_time, "%d %b %Y, %a %H:%M"
    )
    end = datetime.strptime(
        auction.closing_date + " " + auction.closing_time, "%d %b %Y, %a %H:%M"
    )
    now = datetime.utcnow()
    auction.is_open = True if now > start and now < end else False

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
   
    if highest_bid is None:
        highest_bid = None
        highest_bidder_logo = None
        highest_bidder_name = None
    else:
        # if highest bid is anonymous retrieve anonymous logo
        if highest_bid.is_anonymous is True:
            highest_bidder_logo = "brain.png"
            highest_bidder_name = "Anonymous bidder"
        else:
            highest_bidder = CompaniesFinder.get_from_company_user_id(highest_bid.company_user_id)
            image_name = highest_bidder.name
            image_name = image_name.lower()
            image_name = image_name.replace(" ", "_")
            image_name = image_name + ".png"
            highest_bidder_logo = image_name
            highest_bidder_name = highest_bidder.name

    # get all company bids

    company_bids = AuctionsFinder.get_company_bids_from_user(auction, company_user)

    # get all logos of companies in the auction
    participant_logos = []
    for participant in auction.participants:
        image_name = participant.name
        image_name = image_name.lower()
        image_name = image_name.replace(" ", "_")
        image_name = image_name + ".png"
        participant_logos.append(image_name)

    jsonbids = []
    for bid in auction.bids:
        jsonbid={
            "is_anonymous" : bid.is_anonymous,
            "value" : bid.value
        }
        jsonbids.append(jsonbid)

    jsoncompanybids = []
    for bid in company_bids:
        jsoncompanybid={
            "is_anonymous" : bid.is_anonymous,
            "value" : bid.value,
            "created_at":bid.created_at
        }
        jsoncompanybids.append(jsoncompanybid)

    return make_response(
            jsonify({
            "auction":{
                "name": auction.name,
                "bids":jsonbids,
                "bids_len":len(jsonbids),
                "description":auction.description,
                "minimum_value":auction.minimum_value,
                "is_open":auction.is_open,
                "starting_date":auction.starting_date,
                "starting_time":auction.starting_time,
                "closing_date":auction.closing_date,
                "closing_time":auction.closing_time,
            },
            "user_name": user.username,
            "company_name":company.name,
            "error": "",
            "warning": "",
            "highest_bid":{"value":highest_bid.value,
                            "created_at": highest_bid.created_at},
            "highest_bidder_name":highest_bidder_name,
            "highest_bidder_logo":highest_bidder_logo,
            "participant_logos":participant_logos,
            "company_bids":jsoncompanybids,
            "company_bids_len":len(jsoncompanybids),
            "valid":True
           
            })
        )
