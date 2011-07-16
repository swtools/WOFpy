from wof import dao, models


class TestSite(models.BaseSite):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


test_sites = {
    'SITE_A': TestSite(
        SiteID='1',
        SiteCode='SITE_A',
        SiteName='Site A',
        Latitude=50,
        Longitude=60),
    'SITE_B': TestSite(
        SiteID='2',
        SiteCode='SITE_B',
        SiteName='Site B',
        Latitude=55,
        Longitude=-13),
    'SITE_C': TestSite(
        SiteID='3',
        SiteCode='SITE_C',
        SiteName='Site C',
        Latitude=59,
        Longitude=10),
    }


class TestDao(dao.BaseDao):
    def get_all_sites(self):
        return test_sites.values()

    def get_sites_by_codes(self, site_codes):
        return [test_sites[site_code] for site_code in site_codes]
