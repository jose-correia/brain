from jeec_brain.apps.companies_api import bp
from flask import Response, render_template, session
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.auctions_handler import AuctionsHandler
from jeec_brain.values.api_error_value import APIErrorValue


@bp.route('/auction/<string:auction_external_id>', methods=['GET'])
#@require_company_login
def auction_dashboard(auction_external_id):
    # get company
    company_name = session['COMPANY']
    company = CompaniesFinder.get_from_name(company_name)

    if company is None:
        return APIErrorValue('Couldnt find company').json(400)

    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(400)

    # check if company is allowed in auction
    if company not in auction.participants:
        return APIErrorValue('Company not allowed in this auction').json(400)

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    if highest_bid is None:
        highest_bid = 0

    # TODO
    if highest_bid.is_anonymous is True:
        # highest_bidder_logo = jeec_logo
        # highest_bidder_name = Anonymous
    else:
        # get company_logo
        # highest_bidder_logo = company_logo
        # highest_bidder_name = company.name
    
    total_bids = len(auction.bids)
    highest_bid_value = highest_bid.value

    # get all company bids
    company_bids = AuctionsFinder.get_company_bids(auction, company)

    return render_template('companies/auction/auction_dashboard.html', error=None, search=None)


@bp.route('/auction/<string:auction_external_id>/bid', methods=['POST'])
#@require_company_login
def auction_bid(auction_external_id):
    try:
        value = float(request.form.get('value'))
    except:
        return render_template('companies/auction/auction_dashboard.html', error="Insert a valid value!")

    is_anonymous = request.form.get('is_anonymous')

    if is_anonymous == 'True':
        is_anonymous = True
    else:
        is_anonymous = False

    # get company
    company_name = session['COMPANY']
    company = CompaniesFinder.get_from_name(company_name)

    if company is None:
        return APIErrorValue('Couldnt find company').json(400)
    
    # get auction
    auction = AuctionsFinder.get_auction_by_external_id(external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(400)

    # get auction highest bid
    highest_bid = AuctionsFinder.get_auction_highest_bid(auction)
    if highest_bid is None:
        highest_bid = 0

    # check if value is bigger than current highest bid
    if value <= highest_bid:
        return render_template('companies/auction/auction_dashboard.html', error="Value must be higher than the current highest bid!")

    bid = AuctionsHandler.create_auction_bid(
        auction=auction
        company=company,
        value=value,
        is_anonymous=is_anonymous
    )
    
    if bid is None:
        return render_template('companies/auction/auction_dashboard.html', error="Failed to add bid!")

    return redirect(url_for('companies_api.auction_dashboard'))

