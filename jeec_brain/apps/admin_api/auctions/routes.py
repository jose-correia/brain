from re import I
from .. import bp
from flask import render_template, request, redirect, url_for
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.handlers.auctions_handler import AuctionsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.auctions.schemas import AuctionPath

from datetime import datetime


# Auction routes
@bp.get("/auctions")
@allowed_roles(["admin"])
def auctions_dashboard():
    auctions_list = AuctionsFinder.get_all()

    for auction in auctions_list:
        auction.highest_bid = AuctionsFinder.get_auction_highest_bid(auction)

        now = datetime.utcnow()
        start = datetime.strptime(
            auction.starting_date + " " + auction.starting_time, "%d %b %Y, %a %H:%M"
        )
        end = datetime.strptime(
            auction.closing_date + " " + auction.closing_time, "%d %b %Y, %a %H:%M"
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

    start = datetime.strptime(starting_date + " " + starting_time, "%d %b %Y, %a %H:%M")
    end = datetime.strptime(closing_date + " " + closing_time, "%d %b %Y, %a %H:%M")
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
