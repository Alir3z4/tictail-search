# -*- coding: utf-8 -*-
import logging
import hashlib

from flask import Blueprint, jsonify, request
import flask

from server.decorators import crossdomain
from server.models import Products, ModelObjectManager, Tags, Taggings, Shops
from server.search import Search
from server.utils import get_cash, cache

api = Blueprint('api', __name__)


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

    if limit and limit not in ['', None]:
        try:
            limit = int(limit)
        except ValueError:
            flask.abort(404)
    else:
        flask.abort(404)

    ckey = hashlib.md5('.'.join(i for i in request.args.values())).hexdigest()
    result = get_cash(ckey)
    if result:
        return jsonify(result)

    taggings = []
    invalid_tag_values = ['', None, [], u'', [''], [u'']]
    if tags and tags not in invalid_tag_values and isinstance(tags, list):
        tags = get_cash(
            key='.'.join([i for i in tags]),
            new_value=Tags().objects.filter({'tag__in': tags})
        )
        tag_ids = [i.id for i in tags] if tags else []
        if tag_ids:
            taggings = get_cash(
                key=''.join(tag_ids),
                new_value=Taggings().objects.filter({'tag_id__in': tag_ids})
            )

    if taggings:
        shop_ids = [i.shop_id for i in taggings]
        shops = get_cash(
            key=hashlib.md5(''.join(shop_ids)).hexdigest(),
            new_value=Shops().objects.filter({'id__in': shop_ids})
        )
    else:
        shops = get_cash(key='all_shops', new_value=Shops().objects.all())

    search = Search()
    search.set_shops(shops)

    product_list = []
    search.query(lat, lng, radius, 50)
    shops = search.get_nearby_shops()

    for shop in shops:
        if len(product_list) >= limit:
            break

        product_list += get_cash(
            key="shop_products.{0}".format(shop.id),
            new_value=Products().objects.filter(
                {'shop_id': shop.id},
                ('popularity', ModelObjectManager.SORT_BY_DESCENDING)
            )
        )

    result = {'products': [i.to_dict() for i in product_list[0:limit]]}
    cache.set(ckey, result, timeout= 3*60)

    return jsonify(result)
