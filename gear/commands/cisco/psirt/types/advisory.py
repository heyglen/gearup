# -*- coding: utf-8 -*-


class Advisory(object):
    """Creates an Advisory object"""

    def __init__(self, advisory_dict, parse_cvrf, adv_format):
        self.parse_cvrf = parse_cvrf
        self.adv_format = adv_format
        self.sir = advisory_dict["sir"]
        self.advisory_id = advisory_dict["advisoryId"]
        self.first_published = advisory_dict["firstPublished"]
        self.last_updated = advisory_dict["lastUpdated"]
        self.cves = advisory_dict["cves"]
        self._cvrf = None
        if self.adv_format == "cvrf":
            self.cvrf_url = advisory_dict["cvrfUrl"]
        else:
            self.oval_urls = advisory_dict["oval"]

    @property
    def cvrf(self):
        if self.parse_cvrf and not self._cvrf:
            self._cvrf = Cvrf.fromXML(self.cvrf_url)
        return self._cvrf
