from datetime import datetime
from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_

from dateutil.parser import parse

from wof.dao import BaseDao
import sqlalch_odm2_models as model
import api.ODM2.models as odm2_models
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy.sql import func

import re

class Odm2Dao(BaseDao):

    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string, convert_unicode=True,
            pool_size=100)
        # Default application pool size is 5. Use 100 to improve performance.
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        #odm2_models.Base.query = self.db_session.query_property()

    def __del__(self):
        self.db_session.close()

    def get_all_sites(self):
        s_Arr = []
        s_rArr = self.db_session.query(odm2_models.Results,
                                       odm2_models.Sites).\
            distinct(odm2_models.Sites.SamplingFeatureID).\
            join(odm2_models.FeatureActions).\
            join(odm2_models.SamplingFeatures).\
            join(odm2_models.Specimens).\
            filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                   odm2_models.Sites.SamplingFeatureID == odm2_models.RelatedFeatures.RelatedFeatureID).all()
        for s_r in s_rArr:
            s = model.Site(s_r.Sites)
            s_Arr.append(s)

        return s_Arr

    def get_site_by_code(self, site_code):
        w_s = None
        try:
            s = self.db_session.query(odm2_models.Sites).\
                join(odm2_models.SamplingFeatures).\
                filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code).one()
        except:
            s = None
        if s is not None:
            w_s = model.Site(s)

        return w_s

    def get_sites_by_codes(self, site_codes_arr):
        s_arr = []
        for site_code in site_codes_arr:
            w_s = self.get_site_by_code(site_code)
            if w_s is not None:
                s_arr.append(w_s)
        return s_arr

    def get_sites_by_box(self, west,south,east,north):
        """
        north - ymax - latitude
        south - ymin - latitude
        west - xmin - longitude
        east - xmax - longitude
        """
        s_Arr = []
        s_rArr = self.db_session.query(odm2_models.Results,
                                       odm2_models.Sites).\
            distinct(odm2_models.Sites.SamplingFeatureID).\
            join(odm2_models.FeatureActions).\
            join(odm2_models.SamplingFeatures).\
            join(odm2_models.Specimens).\
            filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                   odm2_models.Sites.SamplingFeatureID == odm2_models.RelatedFeatures.RelatedFeatureID,
                   odm2_models.Sites.Latitude >= south,
                   odm2_models.Sites.Latitude <= north,
                   odm2_models.Sites.Longitude >= west,
                   odm2_models.Sites.Longitude <= east).all()
        for s_r in s_rArr:
            s = model.Site(s_r.Sites)
            s_Arr.append(s)

        return s_Arr

    def get_variable_params(self, var_code):
        """
        For machataria timeseries data: Variable code::unit id-sample medium
        """
        unitid = None
        samplemedium = None
        items = re.split('::|-',var_code)
        numofparams = len(items)
        if numofparams == 1:
            var_code = items[0]
        elif numofparams == 2:
            var_code = items[0]
            unitid = items[1]
        elif numofparams == 3:
            var_code = items[0]
            unitid = items[1]
            samplemedium = items[2]
        return var_code,unitid,samplemedium

    def get_variables_from_results(self,var_codes=None):
        l_var_codes = None
        if var_codes is not None:
            if not isinstance(var_codes, list):
                l_var_codes = []
                l_var_codes.append(var_codes)
            else:
                l_var_codes = var_codes

        r_m_Arr = []
        if l_var_codes is None:
            r_m = self.db_session.query(odm2_models.MeasurementResults).\
                    distinct(odm2_models.Results.VariableID,
                             odm2_models.Results.UnitsID,
                             odm2_models.Results.SampledMediumCV).\
                    join(odm2_models.Results).all()
            r_m_Arr.append(r_m)
        else:
            for item in l_var_codes:
                var_code, unitid, samplemedium = self.get_variable_params(item)

                q = self.db_session.query(odm2_models.MeasurementResults).\
                    distinct(odm2_models.Results.VariableID,
                             odm2_models.Results.UnitsID,
                             odm2_models.Results.SampledMediumCV).\
                    join(odm2_models.Results).\
                    join(odm2_models.Variables)
                q = q.filter(odm2_models.Variables.VariableCode == var_code)

                if unitid is not None:
                    q = q.filter(odm2_models.Results.UnitsID == int(unitid))
                if samplemedium is not None:
                    q = q.filter(odm2_models.Results.SampledMediumCV == samplemedium)
                r_m = q.all()
                r_m_Arr.append(r_m)

        v_arr = []
        if len(r_m_Arr) is not 0:
            for result_m in r_m_Arr:
                for result in result_m:
                    v = result.ResultObj.VariableObj
                    u = result.ResultObj.UnitsObj
                    s = result.ResultObj.SampledMediumCV
                    t = result.TimeUnitObj
                    ti = result.TimeAggregationInterval
                    w_v = model.Variable(v,s,u,t,ti)
                    v_arr.append(w_v)
        return v_arr

    def get_all_variables(self):
        v_arr = self.get_variables_from_results()
        return v_arr

    def get_variable_by_code(self, var_code):
        w_v = None
        v_arr = self.get_variables_from_results(var_code)
        if len(v_arr) is not 0:
            w_v = v_arr.pop()
        return w_v

    def get_variables_by_codes(self, var_codes_arr):
        v_arr = self.get_variables_from_results(var_codes_arr)
        return v_arr

    def get_series_by_sitecode(self, site_code):

        site = self.get_site_by_code(site_code)
        if site is None:
            return None
        r = self.db_session.query(odm2_models.Results.VariableID.label('vid'),
                                      odm2_models.Results.UnitsID.label('unitid'),
                                      odm2_models.Results.SampledMediumCV.label('samplemedium'),
                                      func.min(odm2_models.Actions.BeginDateTime).label("begindate"),
                                      func.max(odm2_models.Actions.EndDateTime).label("enddate")).\
                group_by(odm2_models.Results.VariableID,
                         odm2_models.Results.UnitsID,
                         odm2_models.Results.SampledMediumCV).\
                join(odm2_models.FeatureActions).\
                join(odm2_models.Actions).\
                join(odm2_models.SamplingFeatures).\
                join(odm2_models.Specimens).\
                filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                       odm2_models.RelatedFeatures.RelatedFeatureID == site.SiteID).all()

        result = self.db_session.query(odm2_models.Results).\
                distinct(odm2_models.Results.VariableID,
                         odm2_models.Results.UnitsID,
                         odm2_models.Results.SampledMediumCV).\
                join(odm2_models.FeatureActions).\
                join(odm2_models.SamplingFeatures).\
                join(odm2_models.Specimens).\
                filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                       odm2_models.RelatedFeatures.RelatedFeatureID == site.SiteID).all()

        r_arr = []
        aff = None
        first_flag = True
        for series in result:
            for item in r:
                if item.vid == series.VariableID and item.unitid == series.UnitsID:
                    if first_flag:
                        first_flag = False
                        aff = self.db_session.query(odm2_models.Affiliations).\
                                filter(odm2_models.Affiliations.OrganizationID == series.FeatureActionObj.ActionObj.MethodObj.OrganizationID).first()
                    w_r = model.Series(series,aff,item.begindate,item.enddate)
                    r_arr.append(w_r)

        return r_arr

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):

        site = self.get_site_by_code(site_code)
        if site is None:
            return None
        r = self.db_session.query(odm2_models.Results.VariableID.label('vid'),
                                      odm2_models.Results.UnitsID.label('unitid'),
                                      odm2_models.Results.SampledMediumCV.label('samplemedium'),
                                      func.min(odm2_models.Actions.BeginDateTime).label("begindate"),
                                      func.max(odm2_models.Actions.EndDateTime).label("enddate")).\
                group_by(odm2_models.Results.VariableID,
                         odm2_models.Results.UnitsID,
                         odm2_models.Results.SampledMediumCV).\
                join(odm2_models.FeatureActions).\
                join(odm2_models.Actions).\
                join(odm2_models.SamplingFeatures).\
                join(odm2_models.Specimens).\
                join(odm2_models.Variables).\
                filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                       odm2_models.RelatedFeatures.RelatedFeatureID == site.SiteID,
                       odm2_models.Variables.VariableCode == var_code).all()

        result = self.db_session.query(odm2_models.Results).\
                distinct(odm2_models.Results.VariableID,
                         odm2_models.Results.UnitsID,
                         odm2_models.Results.SampledMediumCV).\
                join(odm2_models.FeatureActions).\
                join(odm2_models.SamplingFeatures).\
                join(odm2_models.Variables).\
                join(odm2_models.Specimens).\
                join(odm2_models.Variables).\
                filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                       odm2_models.RelatedFeatures.RelatedFeatureID == site.SiteID,
                       odm2_models.Variables.VariableCode == var_code).all()

        r_arr = []
        aff = None
        first_flag = True
        for series in result:
            for item in r:
                if item.vid == series.VariableID and item.unitid == series.UnitsID:
                    if first_flag:
                        first_flag = False
                        aff = self.db_session.query(odm2_models.Affiliations).\
                                filter(odm2_models.Affiliations.OrganizationID == series.FeatureActionObj.ActionObj.MethodObj.OrganizationID).first()
                    w_r = model.Series(series,aff,item.begindate,item.enddate)
                    r_arr.append(w_r)

        return r_arr

    def get_specimen_data(self):
        q = self.db_session.query(odm2_models.MeasurementResultValues).\
                    join(odm2_models.MeasurementResults).\
                    join(odm2_models.Results).\
                    join(odm2_models.FeatureActions).\
                    join(odm2_models.SamplingFeatures).\
                    join(odm2_models.Specimens).\
                    join(odm2_models.Variables)
        return q

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):

        site = self.get_site_by_code(site_code)
        var_code, unitid, samplemedium = self.get_variable_params(var_code)
        if site is None:
            return None

        if (not begin_date_time or not end_date_time):
            try:
                q = self.get_specimen_data()
                q = q.filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                        odm2_models.RelatedFeatures.RelatedFeatureID == site.SiteID,
                             odm2_models.Variables.VariableCode == var_code)
                if unitid is not None:
                    q = q.filter(odm2_models.Results.UnitsID == int(unitid))
                if samplemedium is not None:
                    q = q.filter(odm2_models.Results.SampledMediumCV == samplemedium)
                valueResultArr = q.all()
            except:
                valueResultArr = []
        else:
            begin_date_time = parse(begin_date_time)
            end_date_time = parse(end_date_time)
            try:
                q = self.get_specimen_data()
                q = q.filter(odm2_models.Specimens.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                    odm2_models.RelatedFeatures.RelatedFeatureID == site.SiteID,
                           odm2_models.Variables.VariableCode == var_code,
                           odm2_models.MeasurementResultValues.ValueDateTime >= begin_date_time,
                           odm2_models.MeasurementResultValues.ValueDateTime <= end_date_time)
                if unitid is not None:
                    q = q.filter(odm2_models.Results.UnitsID == int(unitid))
                if samplemedium is not None:
                    q = q.filter(odm2_models.Results.SampledMediumCV == samplemedium)
                valueResultArr = q.all()
            except:
                valueResultArr = []

        v_dict = {}
        v_arr = []
        if len(valueResultArr) is not 0:
            aff = None
            first_flag = True
            if unitid is None and samplemedium is None:
                for valueResult in valueResultArr:
                    variable_key = '%s::%s-%s' % (valueResult.MeasurementResultObj.ResultObj.VariableObj.VariableCode,
                                              valueResult.MeasurementResultObj.ResultObj.UnitsID,
                                              valueResult.MeasurementResultObj.ResultObj.SampledMediumCV)
                    if first_flag:
                        first_flag = False
                        org_id = valueResult.MeasurementResultObj.ResultObj.FeatureActionObj.ActionObj.MethodObj.OrganizationID
                        aff = self.db_session.query(odm2_models.Affiliations).\
                            filter(odm2_models.Affiliations.OrganizationID == org_id).first()
                    w_v = model.DataValue(valueResult,aff)

                    if v_dict.has_key(variable_key):
                        a_list = v_dict.get(variable_key)
                        a_list.append(w_v)
                    else:
                        v_dict[variable_key] = []
                        v_dict[variable_key].append(w_v)
                return v_dict
            else:
                for valueResult in valueResultArr:
                    if first_flag:
                        first_flag = False
                        org_id = valueResult.MeasurementResultObj.ResultObj.FeatureActionObj.ActionObj.MethodObj.OrganizationID
                        aff = self.db_session.query(odm2_models.Affiliations).\
                            filter(odm2_models.Affiliations.OrganizationID == org_id).first()
                    w_v = model.DataValue(valueResult,aff)
                    v_arr.append(w_v)
                return v_arr

    def get_method_by_id(self, method_id):
        m = self.db_session.query(odm2_models.Methods).\
            filter(odm2_models.Methods.MethodID == method_id).first()
        w_m = model.Method(m)
        return w_m

    def get_methods_by_ids(self, method_id_arr):
        m = self.db_session.query(odm2_models.Methods).\
            filter(odm2_models.Methods.MethodID.in_(method_id_arr)).all()
        m_arr = []
        for i in range(len(m)):
            w_m = model.Method(m[i])
            m_arr.append(w_m)
        return m_arr

    def get_source_by_id(self, source_id):
        aff = self.db_session.query(odm2_models.Affiliations).\
            filter(odm2_models.Affiliations.AffiliationID == source_id).one()
        w_aff = model.Source(aff)
        return w_aff

    def get_sources_by_ids(self, source_id_arr):
        aff = self.db_session.query(odm2_models.Affiliations).\
            filter(odm2_models.Affiliations.AffiliationID.in_(source_id_arr)).all()
        aff_arr = []
        for i in range(len(aff)):
            w_a = model.Source(aff[i])
            aff_arr.append(w_a)
        return aff_arr

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        pl = self.db_session.query(odm2_models.ProcessingLevels)\
            .filter(odm2_models.ProcessingLevels.ProcessingLevelID == qual_control_lvl_id).first()
        w_pl = model.QualityControlLevel(pl)
        return w_pl

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        pl = self.db_session.query(odm2_models.ProcessingLevels)\
            .filter(odm2_models.ProcessingLevels.ProcessingLevelID.in_(qual_control_lvl_id_arr)).all()
        pl_arr = []
        for i in range(len(pl)):
            w_pl = model.QualityControlLevel(pl[i])
            pl_arr.append(w_pl)
        return pl_arr
