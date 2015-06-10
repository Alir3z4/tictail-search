from numpy import inf
from scipy import spatial


class Search(object):
    shops = []
    shops_index = {}
    locations = [(), ]
    ckdtree = None
    last_points = []

    def query(self, latitude, longitude, distance=0.02, max_locations=25):
        """
        :type latitude: float
        :type longitude: float
        :type distance: float
        :type max_locations: int

        :rtype: None
        """
        latitude = float(latitude)
        longitude = float(longitude)
        locations = self.get_locations()

        dst, idc = self.ckdtree.query(
            (latitude, longitude),
            k=max_locations,
            distance_upper_bound=distance
        )

        self.last_points = [locations[idx] for idx, max_locations
                            in zip(idc, dst) if max_locations != inf]

    def get_locations(self):
        """
        :rtype: list of tuple
        """
        return self.locations

    def get_ckdtree(self):
        """
        :rtype: spatial.cKDTree
        """
        return self.ckdtree

    def get_last_points(self):
        """
        :rtype: list of tuple
        """
        return self.last_points

    def get_nearby_shops(self):
        """
        :type list of Shops
        """
        points = self.get_last_points()
        shops = []

        for point in points:
            shops.append(self.shops_index[point])

        return shops

    def set_shops(self, shops):
        self.shops = shops
        self.locations = [(i.lat, i.lng) for i in self.shops]
        self.ckdtree = spatial.cKDTree(self.locations)

        for shop in self.shops:
            self.shops_index[(shop.lat, shop.lng)] = shop
