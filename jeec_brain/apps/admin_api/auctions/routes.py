from .. import bp
from flask import render_template, request, redirect, url_for
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.handlers.auctions_handler import AuctionsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.values.api_error_value import APIErrorValue


# Auction routes
@bp.route('/auctions', methods=['GET'])
@allowed_roles(['admin'])
def auctions_dashboard():
    auctions_list = AuctionsFinder.get_all()
    
    if auctions_list is None:
        error = 'No results found'
        return render_template('admin/auctions/auctions_dashboard.html', auctions=None, error=error)

    return render_template('admin/auctions/auctions_dashboard.html', auctions=auctions_list, error=None)


@bp.route('/new-auction', methods=['GET'])
@allowed_roles(['admin'])
def add_auction_dashboard():
    return render_template('admin/auctions/add_auction.html', \
        error=None)


@bp.route('/new-auction', methods=['POST'])
@allowed_roles(['admin'])
def create_auction():
    name = request.form.get('name')
    description = request.form.get('description')
    is_open = request.form.get('is_open')
    closing_date = request.form.get('closing_date')

    try:
        minimum_value = float(request.form.get('minimum_value'))
    except:
        return 'Invalid minimum value inserted', 404

    if is_open == 'True':
        is_open = True
    else:
        is_open = False

    # create new auction
    auction = AuctionsHandler.create_auction(
            name=name,
            description=description,
            is_open=is_open,
            minimum_value=minimum_value,
            closing_date=closing_date
        )

    if auction is None:
        return render_template('admin/auctions/add_auction.html', \
            error="Failed to create auction!")

    return redirect(url_for('admin_api.auctions_dashboard'))


@bp.route('/auctions/<string:auction_external_id>', methods=['GET'])
@allowed_roles(['admin'])
def get_auction(auction_external_id):
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        error = 'Non existant auction'
        return render_template('admin/auctions/auctions_dashboard.html', auctions=None, error=error)

    return render_template('admin/auctions/update_auction.html', \
        auction=auction, \
        error=None)


@bp.route('/auctions/<string:auction_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_auction(auction_external_id):
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(500)

    name = request.form.get('name')
    description = request.form.get('description')
    closing_date = request.form.get('closing_date')

    try:
        minimum_value = float(request.form.get('minimum_value'))
    except:
        return APIErrorValue('Wrong value format input').json(400)

    is_open = request.form.get('is_open')

    if is_open == 'True':
        is_open = True
    else:
        is_open = False

    updated_auction = AuctionsHandler.update_auction(
        auction=auction,
        name=name,
        description=description,
        minimum_value=minimum_value,
        is_open=is_open,
        closing_date=closing_date
    )
    
    if updated_auction is None:
        return render_template('admin/auctions/update_auction.html', \
            auction=auction, \
            error="Failed to update auction!")

    return redirect(url_for('admin_api.auctions_dashboard'))


@bp.route('/auctions/<string:auction_external_id>/delete', methods=['GET'])
@allowed_roles(['admin'])
def delete_auction(auction_external_id):
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(500)
        
    if AuctionsHandler.delete_auction(auction):
        return redirect(url_for('admin_api.auctions_dashboard'))

    else:
        return render_template('admin/auctions/update_aution.html', auction=auction, error="Failed to delete auction!")


# Members management
@bp.route('/auctions/<string:auction_external_id>/participants', methods=['GET'])
@allowed_roles(['admin'])
def auction_participants_dashboard(auction_external_id):
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(400)

    not_participants = AuctionsFinder.get_not_participants(auction)

    if len(auction.participants) == 0:
        error = 'No results found'
        return render_template('admin/auctions/auction_participants_dashboard.html', auction=auction, not_participants=not_participants, error=error)

    return render_template('admin/auctions/auction_participants_dashboard.html', auction=auction, not_participants=not_participants, error=None)


@bp.route('/auctions/<string:auction_external_id>/add-participant', methods=['POST'])
@allowed_roles(['admin'])
def add_auction_participant(auction_external_id):
    auction = AuctionsFinder.get_auction_by_external_id(auction_external_id)

    if auction is None:
        return APIErrorValue('Couldnt find auction').json(400)

    company_external_id = request.form.get('company_external_id')

    if company_external_id is None:
        return redirect(url_for('admin_api.auction_participants_dashboard', auction_external_id=auction_external_id))

    company = CompaniesFinder.get_from_external_id(company_external_id)

    if company is None:
        return APIErrorValue('Couldnt find company').json(400)

    AuctionsHandler.add_auction_participant(auction, company)
    
    return redirect(url_for('admin_api.auction_participants_dashboard', auction_external_id=auction_external_id))
