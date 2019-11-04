from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.auctions_handler import AuctionsHandler
from jeec_brain.values.api_error_value import APIErrorValue


@bp.route('/auction/<string:auction_external_id>', methods=['GET'])
@require_company_login
def auction_dashboard(auction_external_id):
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)

    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(400)

    # check if company is allowed in auction
    if current_user.company not in auction.participants:
        return APIErrorValue('Company not allowed in this auction').json(400)

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    if highest_bid is None:
        highest_bid = 0

    if highest_bid.is_anonymous is True:
        highest_bidder_logo = '/static/jeec_logo_mobile.svg'
        highest_bidder_name = 'Anonymous bidder'
    else:
        highest_bidder = CompaniesFinder.get_from_id(highest_bid.company_id)
        company_logo = CompaniesHandler.find_image(highest_bidder.name)
        highest_bidder_logo = company_logo
        highest_bidder_name = highest_bidder.name

    # get all company bids
    company_bids = AuctionsFinder.get_company_bids(auction, current_user.company)

    return render_template('companies/auction/auction_dashboard.html', \
        auction=auction, \
        highest_bid=highest_bid, \
        highest_bidder_name=highest_bidder_name,
        highest_bidder_logo=highest_bidder_logo,
        company_bids=company_bids, \
        error=None, \
        search=None)


@bp.route('/auction/<string:auction_external_id>/bid', methods=['POST'])
@require_company_login
def auction_bid(auction_external_id):
    try:
        value = float(request.form.get('value'))
    except:
        return APIErrorValue('Insert a valid value').json(400)

    is_anonymous = request.form.get('is_anonymous')
    
    if is_anonymous == 'True':
        is_anonymous = True
    else:
        is_anonymous = False

    # get company
    company = CompaniesFinder.get_from_name(current_user.company.name)

    if company is None:
        return APIErrorValue('Couldnt find company').json(400)
    
    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(400)

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    if highest_bid is None:
        highest_bid = 0

    # check if value is bigger than current highest bid
    if value <= highest_bid.value:
        company_bids = AuctionsFinder.get_company_bids(auction, company)
        return render_template('companies/auction/auction_dashboard.html', \
        auction=auction, \
        highest_bid=highest_bid, \
        company_bids=company_bids, \
        error="Bid value must be higher than the current highest bid!")

    bid = AuctionsHandler.create_auction_bid(
        auction=auction,
        company=company,
        value=value,
        is_anonymous=is_anonymous
    )
    
    if bid is None:
        company_bids = AuctionsFinder.get_company_bids(auction, company)
        return render_template('companies/auction/auction_dashboard.html', \
        auction=auction, \
        highest_bid=highest_bid, \
        company_bids=company_bids, \
        error="Failed to create bid!")

    return redirect(url_for('companies_api.auction_dashboard', auction_external_id=auction.external_id))

