# -*- coding: utf-8 -*-

import cStringIO
from lxml import etree


class CvrfFactory(object):
    # https://github.com/CiscoPSIRT/openVulnAPI/blob/master/openVulnQuery/openVulnQuery/advisory_object.py
    @classmethod
    def xml_get(cls, xml):
        """ Parses XML to prepare arguments for CVRF object """
        cvrfs = list()
        tree = etree.parse(cStringIO.StringIO(xml))
        vuln_args = []
        vulnerability = CvrfFactory._get_xml_element(tree, "vuln_ns:Vulnerability")
        for index, r in enumerate(vulnerability, start=1):
            # Multiple BugIds are stored in Note
            # under Vulnerabilities for latest cvrf 1.1 advisories
            bug_id_ns = "vuln_ns:Vulnerability[{}]/vuln_ns:Notes" \
                        "/vuln_ns:Note[@Title='Cisco Bug IDs']"
            bug_ids = CvrfFactory.get_text(tree, bug_id_ns.format(index))
            if bug_ids == "NA":
                bug_ids = CvrfFactory.get_text(tree, "vuln_ns:Vulnerability[{}]/vuln_ns:ID".format(
                    index
                ))
            # multiple vulnerabilities are seperated by ordinal number
            base_score_ns = "vuln_ns:Vulnerability[{}]/vuln_ns:CVSSScoreSets" \
                            "/vuln_ns:ScoreSet/vuln_ns:BaseScore"
            arg = {
                "title": CvrfFactory.get_text(tree, "vuln_ns:Vulnerability[{}]/vuln_ns:Title".format(index)),
                "cve": CvrfFactory.get_text(tree, "vuln_ns:Vulnerability[{}]/vuln_ns:CVE".format(index)),
                "bug_ids": bug_ids.split(","),
                "base_score": CvrfFactory.get_text(tree, base_score_ns.format(index))
            }

            publication_ns = "cvrf_ns:DocumentReferences/cvrf_ns:Reference/cvrf_ns:URL"
            full_product_name_list_ns = "prod_ns:ProductTree/prod_ns:FullProductName"
            kwargs = {
                "document_title": CvrfFactory.get_text(tree, "cvrf_ns:DocumentTitle"),
                "summary": CvrfFactory.get_text(tree, "cvrf_ns:DocumentNotes/cvrf_ns:Note"),
                "publication_url": CvrfFactory.get_text(tree, publication_ns),
                "full_product_name_list": CvrfFactory.get_text(tree, full_product_name_list_ns),
                "vuln_list": vuln_args
            }
            cvrf = Cvrf()
            cvrf.document_title = document_title
            cvrf.summary = summary
            cvrf.publication_url = publication_url
            cvrf.full_product_name_list = full_product_name_list
            cvrf.vulnerabilities = full_product_name_list
            cvrfs.append(cvrf)
        return cvrfs

    @staticmethod
    def _get_xml_element(tree, path):
        """Returns node element in parsed xml pointed by xpath"""

        cvrf_ns = "http://www.icasi.org/CVRF/schema/cvrf/1.1"
        prod_ns =  "http://www.icasi.org/CVRF/schema/prod/1.1"
        vuln_ns = "http://www.icasi.org/CVRF/schema/vuln/1.1"
        result = tree.xpath("/cvrf_ns:cvrfdoc/%s" % path,
                            namespaces = {"cvrf_ns" : cvrf_ns,
                                          "prod_ns" : prod_ns,
                                          "vuln_ns" : vuln_ns})
        return result

    @staticmethod
    def get_text(tree, path):
        """Returns text value in parsed xml pointed by xpath"""

        elems = CvrfFactory._get_xml_element(tree, path)
        if len(elems) == 0:
            return "NA"
        if len(elems) == 1:
            return elems.pop().text
        return [e.text for e in elems]

