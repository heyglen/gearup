# https://developer.cisco.com/site/support-apis/docs/#eox

import logging
import datetime

import requests
# import oauth2 as oauth

from gear.utils.configuration import configuration
from gear.utils.dot_dict import DotDict

logger = logging.getLogger(__name__)


EOX_TYPES = {
    'announce': 'EO_EXT_ANNOUNCE_DATE',
    'sale': 'EO_SALES_DATE',
    'failure_analysis': 'EO_FAIL_ANALYSIS_DATE',
    'service_attachment': 'EO_SVC_ATTACH_DATE',
    'software_maintenance': 'EO_SW_MAINTENANCE_DATE',
    'security_vulnerability': 'EO_SECURITY_VUL_SUPPORT_DATE',
    'contract_renewal': 'EO_CONTRACT_RENEW_DATE',
    'last_support': 'EO_LAST_SUPPORT_DATE',
    'update_timestamp': 'UPDATE_TIMESTAMP (default)',
}


class Eox(object):
    """
        https://developer.cisco.com/site/support-apis/docs/#eox/SWReleaseStringType
    """
    _token_url = 'https://cloudsso.cisco.com/as/token.oauth2'
    _base_url = 'https://api.cisco.com/supporttools/eox/rest/5/'
    _request_type = {
        'date': 'EOXByDates',
        'product': 'EOXByProductID',
        'product': 'EOXByProductID',
        'serial': 'EOXBySerialNumber',
        'software': 'EOXBySWReleaseString',
    }
    _base_params = {
        'responseencoding': 'json',
    }
    # https://developer.cisco.com/site/support-apis/docs/#eox/SWReleaseStringType
    _os_types = [
        'ACNS',
        'ACSW',
        'ALTIGAOS',
        'ASA',
        'ASYNCOS',
        'CATOS',
        'CDS-IS',
        'CDS-TV',
        'CDS-VN',
        'CDS-VQE',
        'CTS',
        'ECDS',
        'FWSM-OS',
        'GSS',
        'IOS',
        'IOS XR',
        'IOS-XE',
        'IPS',
        'NAM',
        'NX-OS',
        'ONS',
        'PIXOS',
        'SAN-OS',
        'STAR OS',
        'TC',
        'TE',
        'UCS NX-OS',
        'VCS',
        'VDS-IS',
        'WAAS',
        'WANSW BPX/IGX/IPX',
        'WEBNS',
        'WLC',
        'WLSE-OS',
        'XC',
    ]

    def __init__(self):
        self._session = requests.Session()

    def _url_page_index(self, request_type):
        base_url = self._base_url
        request_type = self._request_type[request_type]
        base_url = f'{base_url}/{request_type}'
        for page_index in range(50):
            yield f'{base_url}/{page_index}'

    def _date_urls(self, start_date, end_date):
        for page_index_url in self._url_page_index('date'):
            yield f'{page_index_url}/{start_date}/{end_date}'

    def _get_headers(self):
        if not hasattr(self, '_headers'):
            logger.debug('Building request headers')
            access_token = self._get_access_token()
            self._headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        return self._headers

    def _get_access_token(self):
        if not hasattr(self, '_access_token'):
            logger.debug('Authenticating')
            params = {
                'client_id': configuration.cisco.psirt.username,
                'client_secret': configuration.cisco.psirt.password
            }
            data = {'grant_type': 'client_credentials'}

            # consumer = oauth.Consumer(key=username, secret=password)
            # request_token_url = self._token_url.format(username, password)
            # oauth.Client(consumer)

            response = self._session.post(
                self._token_url,
                params=params,
                data=data,
            )
            response.raise_for_status()
            logger.debug(response.text.strip())
            self._access_token = response.json()['access_token']
            logger.debug('Access Token Retrieved')
        return self._access_token

    def _get(self, url):
        headers = self._get_headers()
        logger.debug(f'GET {url}')
        logger.debug(f'headers: {headers}')
        response = self._session.get(url, headers=headers)
        logger.debug(f'Response: {response.text}')
        return response.json()

    def get(self, item):
        advisory = None
        if item.startswith('CVE'):
            logger.debug('Getting CVE advisory {}'.format(item))
            url = self._build_url('cve/{}'.format(item))
            advisory = self._get(url).get('advisories')
        else:
            logger.debug('Getting advisory client_id {}'.format(item))
            url = self._build_url('advisory/{}'.format(item))
            advisory = self._get(url).get('advisories')
        return advisory

    def by_date(self, start_date, end_date):
        for unvalidated_date in [start_date, end_date]:
            datetime.datetime.strptime(unvalidated_date, '%Y-%m-%d')
        for date_url in self._date_urls():
            self._session.get(date_url)