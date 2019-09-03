from flask_restful import reqparse

create_comapny_parser = reqparse.RequestParser(bundle_errors=True)
create_comapny_parser.add_argument('name', required=True, location='json')
create_comapny_parser.add_argument('business_area', required=True, location='json')
create_comapny_parser.add_argument('link', required=True, location='json')
create_comapny_parser.add_argument('email', required=True, location='json')


update_comapny_parser = reqparse.RequestParser(bundle_errors=True)
update_comapny_parser.add_argument('name', location='json')
update_comapny_parser.add_argument('business_area', location='json')
update_comapny_parser.add_argument('link', location='json')
update_comapny_parser.add_argument('email', location='json')
