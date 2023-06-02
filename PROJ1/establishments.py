import math

class Establishment:
    def __init__(self, id_est: int, district: str, county: str, parish: str, address: str, latitude: float,
                 longitude: float, inspection_utility: float, inspection_time: float, opening_hours: list):
        self.id_est = id_est
        self.district = district
        self.county = county
        self.parish = parish
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.inspection_utility = inspection_utility
        self.inspection_time = inspection_time
        self.opening_hours = opening_hours
        self.visited = None

    def is_open(self, time: float):
        for start, end in self.opening_hours:
            if start <= time <= end:
                return True

        return False

    def next_opening(self, n):
        result = None
        for start, end in self.opening_hours:
            if start > n:
                result = start
                break

        if not result:
            result = self.opening_hours[0][0]
        return result

    def next_opening_2(self, n):
        result = None
        for start, end in self.opening_hours:
            if start <= n <= end:
                result = n
                break
            elif start >= n:
                result = start
                break

        if not result:
            result = self.opening_hours[0][0]
        return result

