# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, current_app, jsonify, request
import flask
from server.decorators import crossdomain
from server.models import Products, ModelObjectManager, Tags, Taggings, Shops
from server.search import Search

api = Blueprint('api', __name__)

def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
@crossdomain(origin='*')
def search():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    tags = request.args.getlist('tags[]')
    radius = request.args.get('radius')
    limit = request.args.get('count')

    required_params = [lat, lng]
    for param in required_params:
        if not param or param in ['', None]:
            flask.abort(400)
    try:
        lat = float(lat)
        lng = float(lng)

        if radius and radius not in ['', None]:
            radius = float(float(radius) * 0.000621371)
    except ValueError:
        logging.error('Error in casting position')
        flask.abort(400)

    taggings = []
    if tags and tags not in ['', None, []] and isinstance(tags, list):
        tags = Tags.objects.filter({'tag__in': tags})
        tag_ids = [i.id for i in tags]
        if tag_ids:
            taggings = Taggings.objects.filter({'tag_id__in': tag_ids})


    if taggings:
        shops = Shops.objects.filter({'id__in': [i.shop_id for i in taggings]})
    else:
        shops = Shops.objects.all()

    print(shops)

    search = Search()
    search.set_shops(shops)

    product_list = []
    search.query(lat, lng, radius, int(limit)/10)
    shops = search.get_nearby_shops()

    for shop in shops:
        product_list += Products.objects.filter(
            {'shop_id': shop.id},
            ('popularity', ModelObjectManager.SORT_BY_DESCENDING)
        )

    if limit and limit not in ['', None]:
        try:
            limit = int(limit)
        except ValueError:
            flask.abort(400)
    else:
        limit = len(product_list)

    return jsonify({'products': [i.to_dict() for i in product_list[0:limit]]})
