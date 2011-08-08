

class BaseDao(object):

    def get_all_sites(self):
        """
        Returns a list of all the Sites in the data source.
        """
        raise NotImplementedError("Method not implemented.")

    def get_site_by_code(self, site_code):
        """
        Returns a single Site identified by its code.
        """
        raise NotImplementedError("Method not implemented.")

    def get_sites_by_codes(self, site_codes_arr):
        """
        Returns a list of Sites identified by the given site code list.
        """
        raise NotImplementedError("Method not implemented.")

    def get_all_variables(self):
        """
        Returns a list of all Variables in the data source.
        """
        raise NotImplementedError("Method not implemented.")

    def get_variable_by_code(self, var_code):
        """
        Returns a single Variable identified by its code.
        """
        raise NotImplementedError("Method not implemented.")

    def get_variables_by_codes(self, var_codes_arr):
        """
        Returns a list of Variables identified by the given variable code list.
        """
        raise NotImplementedError("Method not implemented.")

    def get_series_by_sitecode(self, site_code):
        """
        Returns a list of Series for the given site code.
        """
        raise NotImplementedError("Method not implemented.")

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        """
        Returns a list of Series for the given site code and variable
        code combination.
        """
        raise NotImplementedError("Method not implemented.")

    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        """
        Returns a list of DataValues for the given site code and variable code,
        filtered by the optional begin and end datetimes.
        """
        raise NotImplementedError("Method not implemented.")

    def get_method_by_id(self, method_id):
        """
        Returns a single Method identified by the given id.
        """
        raise NotImplementedError("Method not implemented.")

    def get_methods_by_ids(self, method_id_arr):
        """
        Returns a list of Methods identified by the given id list.
        """
        raise NotImplementedError("Method not implemented.")

    def get_source_by_id(self, source_id):
        """
        Returns a single Source identified by the given id.
        """
        raise NotImplementedError("Method not implemented.")

    def get_sources_by_ids(self, source_id_arr):
        """
        Returns a list of Sources identified by the given id list.
        """
        raise NotImplementedError("Method not implemented.")

    def get_qualifier_by_id(self, qualifier_id):
        """
        Returns a single Qualifier identified by the given id.
        """
        raise NotImplementedError("Method not implemented.")

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        """
        Returns a list of Qualifiers identified by the given id list.
        """
        raise NotImplementedError("Method not implemented.")

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        """
        Returns a single QualityControlLevel identified by the given id.
        """
        raise NotImplementedError("Method not implemented.")

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        """
        Returns a list of QualityControlLevels identified by the given id list.
        """
        raise NotImplementedError("Method not implemented.")

    def get_offsettype_by_id(self, offset_type_id):
        """
        Returns a single OffsetType identified by the given id.
        """
        raise NotImplementedError("Method not implemented.")

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        """
        Returns a list of OffsetTypes identified by the given id list.
        """
        raise NotImplementedError("Method not implemented.")
