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
    }


class TestDao(dao.BaseDao):
    def get_all_sites(self):
        return test_sites.values()
