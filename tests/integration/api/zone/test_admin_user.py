import pytest
import json
from collections import namedtuple

from powerdnsadmin.lib.validators import validate_zone
from powerdnsadmin.lib.schema import DomainSchema
from tests.fixtures import client, initial_data, basic_auth_admin_headers
from tests.fixtures import zone_data


class TestIntegrationApiZoneAdminUser(object):
    def test_empty_get(self, client, initial_data, basic_auth_admin_headers):
        res = client.get("/api/v1/pdnsadmin/zones",
                         headers=basic_auth_admin_headers)
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data == []

    def test_create_zone(self, client, initial_data, zone_data,
                         basic_auth_admin_headers):
        res = client.post("/api/v1/pdnsadmin/zones",
                          headers=basic_auth_admin_headers,
                          data=json.dumps(zone_data),
                          content_type="application/json")
        data = res.get_json(force=True)
        data['rrsets'] = []

        validate_zone(data)
        assert res.status_code == 201

        zone_url_format = "/api/v1/pdnsadmin/zones/{0}"
        zone_url = zone_url_format.format(zone_data['name'].rstrip("."))
        res = client.delete(zone_url, headers=basic_auth_admin_headers)

        assert res.status_code == 204

    def test_get_multiple_zones(self, client, initial_data, zone_data,
                                basic_auth_admin_headers):
        res = client.post("/api/v1/pdnsadmin/zones",
                          headers=basic_auth_admin_headers,
                          data=json.dumps(zone_data),
                          content_type="application/json")
        data = res.get_json(force=True)
        data['rrsets'] = []

        validate_zone(data)
        assert res.status_code == 201

        res = client.get("/api/v1/pdnsadmin/zones",
                         headers=basic_auth_admin_headers)
        data = res.get_json(force=True)
        fake_domain = namedtuple("Domain", data[0].keys())(*data[0].values())
        domain_schema = DomainSchema(many=True)

        json.dumps(domain_schema.dump([fake_domain]))
        assert res.status_code == 200

        zone_url_format = "/api/v1/pdnsadmin/zones/{0}"
        zone_url = zone_url_format.format(zone_data['name'].rstrip("."))
        res = client.delete(zone_url, headers=basic_auth_admin_headers)

        assert res.status_code == 204

    def test_delete_zone(self, client, initial_data, zone_data,
                         basic_auth_admin_headers):
        res = client.post("/api/v1/pdnsadmin/zones",
                          headers=basic_auth_admin_headers,
                          data=json.dumps(zone_data),
                          content_type="application/json")
        data = res.get_json(force=True)
        data['rrsets'] = []

        validate_zone(data)
        assert res.status_code == 201

        zone_url_format = "/api/v1/pdnsadmin/zones/{0}"
        zone_url = zone_url_format.format(zone_data['name'].rstrip("."))
        res = client.delete(zone_url, headers=basic_auth_admin_headers)

        assert res.status_code == 204
