
class BaseDao(object):

    def get_all_sites(self):
        """
        Returns a list of all the Sites in the data source
        """
        pass

    def get_site_by_code(self, site_code):
        pass

    def get_sites_by_codes(self, site_codes_arr):
        pass

    def get_all_variables(self):
        pass

    def get_variable_by_code(self, var_code):
        pass

    def get_variables_by_codes(self, var_codes_arr):
        pass

    def get_series_by_sitecode(self, site_code):
        pass

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        pass

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        pass

    def get_method_by_id(self, method_id):
        pass

    def get_methods_by_ids(self, method_id_arr):
        pass

    def get_source_by_id(self, source_id):
        pass

    def get_sources_by_ids(self, source_id_arr):
        pass

    def get_qualifier_by_id(self, qualifier_id):
        pass

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        pass

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        pass

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        pass

    def get_offsettype_by_id(self, offset_type_id):
        pass

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        pass
