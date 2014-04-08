#!/usr/bin/env python
__author__ = 'jcranwellward'

import os, argparse
from urlparse import urljoin

import requests
from requests.auth import HTTPBasicAuth


class ActivityInfoClient(object):
    """ ActivityInfo python client to allow the following requests:

        List all databases visible to the client: /databases
        Retrieve the structure of database id 504: /database/504/schema
        Retrieve all sites in activity 33: /sites?activity=33
        Retrieve all sites in activity 33 in GeoJSON format: /sites/points?activity=33
        List all administrative levels in Lebanon (country code LB): /country/LB/adminLevels
        List all administrative entities in level 1370: /adminLevel/1370/entities
        List all administrative entities in level 1370 in GeoJSON format: /adminLevel/1370/entities/features
        List all location types in Lebanon: /country/LB/locationTypes
        List all locations of type 1370: /locations/type=1370

    """

    def __init__(self,
                 username=None,
                 password=None,
                 base_url='https://www.activityinfo.org/resources/'):
        self.base_url = base_url
        if username and password:
            self.auth = HTTPBasicAuth(username, password)

    def build_path(self, path=None):
        """ Builds the full path to the service.

        Args:
            path (string): The part of the path you want to append
            to the base url.

        Returns:
            A string containing the full path to the endpoint.
            e.g if the base_url was "http://woo.com" and the path was
            "databases" it would return "http://woo.com/databases/"
        """
        if path is None:
            return self.base_url
        return urljoin(
            self.base_url,
            '{}{}'.format(
                os.path.normpath(path), '/'
            )
        )

    def make_request(self, path, **params):

        full_path = self.build_path(path)
        response = requests.get(
            full_path,
            params=params,
            auth=getattr(self, 'auth', ())
        )
        return response

    def get_databases(self):
        return self.make_request('databases').json()

    def get_database(self, db_id):
        return self.make_request('database/{}/schema'.format(db_id)).json()

    def get_sites(self, activity=None, indicator=None):
        sites = self.make_request('sites', activity=activity if activity else None).json()
        if indicator:
            sites = [
                site for site in sites
                if 'indicatorValues' in site.keys() and
                   str(indicator) in site['indicatorValues'].keys()]
        return sites


def main():
    """

    """
    parser = argparse.ArgumentParser(description='ActivityInfo API Python Client')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--database',
                       type=int,
                       help='Database to query')
    group.add_argument('-a', '--activity',
                       type=int,
                       help='Filter results by activty')
    parser.add_argument('-i', '--indicator',
                        type=int,
                        default=None,
                        help='Filter results by indicator')
    parser.add_argument('-u', '--username',
                        type=str,
                        default='',
                        help='Optional username for authentication')
    parser.add_argument('-p', '--password',
                        type=str,
                        default='',
                        help='Optional password for authentication')

    args = parser.parse_args()

    try:
        client = ActivityInfoClient(
            username=args.username,
            password=args.password,
        )
        if args.database:
            response = client.get_database(args.database)
        elif args.activity:
            response = client.get_sites(args.activity, args.indicator)
        else:
            response = client.get_sites()

        print response

    except Exception as exp:
        print str(exp)


if __name__ == '__main__':
    main()











