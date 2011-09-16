from datetime import timedelta
import csv

from dateutil.parser import parse
from dateutil.tz import tzoffset as tz

from wof.dao import BaseDao
import wof.models as wof_base

import csv_model

class CsvDao(BaseDao):
    def __init__(self, sites_file_path, values_file_path):
        self.sites_file_path = sites_file_path
        self.values_file_path = values_file_path
        
        # Build a dictionary of variables indexed by code
        variable_dict = {}

        stage = csv_model.Variable()
        stage.VariableCode = 'Stage_ft'
        stage.VariableName = 'Stage'
        stage_units = wof_base.BaseUnits()
        stage_units.UnitsName = 'international foot'
        stage_units.UnitsType = 'Length'
        stage_units.UnitsAbbreviation = 'ft'
        stage.VariableUnits = stage_units
        variable_dict['Stage_ft'] = stage
        
        flow = csv_model.Variable()
        flow.VariableCode = 'Discharge_cfs'
        flow.VariableName = 'Discharge'
        flow_units = wof_base.BaseUnits()
        flow_units.UnitsName = 'cubic feet per second'
        flow_units.UnitsType = 'Flow'
        flow_units.UnitsAbbreviation = 'cfs'
        flow.VariableUnits = flow_units
        variable_dict['Discharge_cfs'] = flow
        
        self.variable_dict = variable_dict

    def __del__(self):
        pass # Could end database session here for more sophisticated DAOs

    def create_site_from_row(self, csv_row):
        site = csv_model.Site()
        site.SiteCode = csv_row[0]
        site.SiteName = csv_row[1]
        site.Latitude = csv_row[2]
        site.Longitude = csv_row[3]
        return site

    def get_all_sites(self):
        sites = []
        with open(self.sites_file_path, 'rb') as f:
            reader = csv.reader(f)
            at_header = True
            for row in reader:
                if at_header:
                    at_header = False
                    continue
                
                site = self.create_site_from_row(row)
                sites.append(site)
        return sites

    def get_site_by_code(self, site_code):
        with open(self.sites_file_path, 'rb') as f:
            reader = csv.reader(f)
            at_header = True
            for row in reader:
                if at_header:
                    at_header = False
                    continue
                
                if row[0] == site_code:
                    site = self.create_site_from_row(row)
                    return site

    def get_sites_by_codes(self, site_codes_arr):
        sites = []
        with open(self.sites_file_path, 'rb') as f:
            reader = csv.reader(f)
            at_header = True
            for row in reader:
                if at_header:
                    at_header = False
                    continue
                
                if row[0] in site_codes_arr:
                    site = self.create_site_from_row(row)
                    sites.append(site)
        return sites

    def get_all_variables(self):
        return self.variable_dict.values()

    def get_variable_by_code(self, var_code):
        if var_code in self.variable_dict:
            return self.variable_dict[var_code]

    def get_variables_by_codes(self, var_codes_arr):
        vars = []
        for var_code in var_codes_arr:
            if var_code in self.variable_dict:
                vars.append(self.variable_dict[var_code])
        return vars

    def get_series_by_sitecode(self, site_code):
        series_list = []
        site = self.get_site_by_code(site_code)
        if site:
            # stage
            series = self.get_series_by_sitecode_and_varcode(
                site_code, 'Stage_ft')
            series_list.extend(series)
            # discharge
            series = self.get_series_by_sitecode_and_varcode(
                site_code, 'Discharge_cfs')
            series_list.extend(series)

        return series_list            
            

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        series_list = []
        site = self.get_site_by_code(site_code)
        if site:
            var = self.get_variable_by_code(var_code)
            if var: 
                series = csv_model.Series()
                series.SiteCode = site.SiteCode
                series.SiteName = site.SiteName
                series.VariableCode = var.VariableCode
                series.VariableName = var.VariableName
                series.VariableUnitsID = var.VariableUnitsID
                series.VariableUnitsName = var.VariableUnits.UnitsName
                series.SampleMedium = var.SampleMedium
                series.ValueType = var.ValueType
                series.TimeSupport = var.TimeSupport
                series.TimeUnitsID = var.TimeUnitsID
                series.TimeUnitsName = var.TimeUnits.UnitsName
                series.DataType = var.DataType
                series.GeneralCategory = var.GeneralCategory
                series.Site = site
                series.Variable = var
                
                series_list.append(series)

        return series_list

    def parse_date_strings(self, begin_date_time_string, end_date_time_string):
        """Returns a list with parsed datetimes in the local time zone.

        Required Arguments:
            begin_date_time (begin datetime as text)
            end_date_time (end datetime as text)
        Remarks:
            The returned list has two items:
                begin datetime as datetime.datetime object
                end datetime as datetime.datetime object
        
        """
        
        # Convert input strings to datetime objects
        try:
            if begin_date_time_string:
                b = parse(begin_date_time_string)
            else:
                # Provide default start date at beginning of period of record
                b = parse('2008-01-01T00:00-06')
        except:
            raise ValueError('invalid start date: ' + \
                             str(begin_date_time_string))
        try:
            if end_date_time_string:
                e = parse(end_date_time_string)
            else:
                # Provide default end date at end of period of record
                e = parse('2008-04-30T00:00-06')
        except:
            raise ValueError('invalid end date: ' + str(end_date_time_string))

        # If we know time zone, convert to local time.  Otherwise, assume
        # local time.
        # Remove tzinfo in the end since datetimes from data file do not have
        # tzinfo either.  This enables date comparisons.
        local_time_zone = tz(None, -21600) # Six hours behind UTC, in seconds
        if b.tzinfo:
            b = b.astimezone(local_time_zone)
            b = b.replace(tzinfo=None)
        if e.tzinfo:
            e = e.astimezone(local_time_zone)
            e = e.replace(tzinfo=None)

        return [b, e]

    def create_datavalue_from_row(self, row, value_index):
        datavalue = csv_model.DataValue()

        datavalue.DataValue = row[value_index]

        # All values are in local time. For this example, local time is always
        # six hours behind UTC time.
        value_date = parse(row[1])
        datavalue.LocalDateTime = value_date.isoformat() + '-06'

        value_date = value_date + timedelta(hours=6)
        datavalue.DateTimeUTC = value_date.isoformat() + 'Z'
        
        return datavalue

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        # Find the site and variable
        siteResult = self.get_site_by_code(site_code)
        varResult = self.get_variable_by_code(var_code)
        valueResultArr = []

        if siteResult and varResult:
            # Determine which column has the values
            if var_code == 'Stage_ft':
                value_index = 2
            else:
                value_index = 3
            
            # Parse input dates
            parse_result = self.parse_date_strings(begin_date_time,
                                                   end_date_time)
            b = parse_result[0] # begin datetime
            e = parse_result[1] # end datetime

            # Read values            
            with open(self.values_file_path, 'rb') as f:
                reader = csv.reader(f)
                at_header = True
                values = []
                for row in reader:
                    if at_header:
                        at_header = False
                        continue

                    # Make sure we're within input date range                    
                    value_date = parse(row[1])
                    if (value_date >= b and value_date <= e and
                        row[0] == site_code):
                        # Add data value to result list
                        datavalue = self.create_datavalue_from_row(row,
                                                                   value_index)
                        valueResultArr.append(datavalue)
            
        return valueResultArr

    def get_methods_by_ids(self, method_id_arr):
        method = csv_model.Method()
        methods = []
        if method.MethodID in method_id_arr:
            methods.append(method)
        return methods

    def get_sources_by_ids(self, source_id_arr):
        sources = []
        if 1 in source_id_arr:
            sources.append(csv_model.Source())
        return sources

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        return []

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        return []