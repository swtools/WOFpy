from spyne.interface import InterfaceDocumentBase
import logging
from jinja2 import Environment, Template, PackageLoader, FileSystemLoader

# from sypne/interface/wsdl/wsdl1.py

def check_method_port(service, method):
    if len(service.__port_types__) != 0 and method.port_type is None:
        raise ValueError("""
            A port must be declared in the RPC decorator if the service
            class declares a list of ports
            Method: %r
            """ % method.name)

    if (not method.port_type is None) and len(service.__port_types__) == 0:
        raise ValueError("""
            The rpc decorator has declared a port while the service class
            has not.  Remove the port declaration from the rpc decorator
            or add a list of ports to the service class
            """)
    try:
        if (not method.port_type is None):
            index = service.__port_types__.index(method.port_type)

    except ValueError as e:
        raise ValueError("""
            The port specified in the rpc decorator does not match any of
            the ports defined by the service class
            """)

class WofWSDL_1_0(InterfaceDocumentBase):
    templates=None

    def __init__(self, interface=None, _with_partnerlink=False, templates=None):
        super(WofWSDL_1_0, self).__init__(interface)
        self.templates=templates

    def build_interface_document(self, url, templates):
        """This function is supposed to be called just once, as late as possible
        into the process start. It builds the interface document and caches it
        somewhere. The overriding function should never call the overridden
        function as this may result in the same event firing more than once.
        """
        # cb_binding = None
        # for s in self.interface.services:
        #     if not s.is_auxiliary():
        #         # cb_binding = self.add_bindings_for_methods(s, root,
        #         #                                    service_name, cb_binding)
        #         cb_binding = self.add_bindings_for_methods(s, None,
        #                                            None, cb_binding)
        doc = self.get_wsdl_1_0( url, templates )
        return doc

    def get_interface_document(self):
        """This function is called by server transports that try to satisfy the
        request for the interface document. This should just return a previously
        cached interface document.
        """

        raise NotImplementedError('Extend and override.')


    # def _add_port_to_service(self, service, port_name, binding_name):
    #     """ Builds a wsdl:port for a service and binding"""
    #
    #     pref_tns = self.interface.get_namespace_prefix(self.interface.tns)
    #
    #     wsdl_port = SubElement(service, WSDL11("port"))
    #     wsdl_port.set('name', port_name)
    #     wsdl_port.set('binding', '%s:%s' % (pref_tns, binding_name))
    #
    #     addr = SubElement(wsdl_port, WSDL11_SOAP("address"))
    #     addr.set('location', self.url)

    def get_wsdl_1_0(self, url, templates ):
            env = Environment(loader=FileSystemLoader(templates))
            template = env.get_template('wsdl_temp.wsdl')
            response = template.render(serv_loc=url)
            response = response.encode('utf-8')
            #response.headers['Content-Type'] = 'text/xml'

            return response

    def on_get_wsdl_1_0_(self, ctx ):
            env = Environment(loader=FileSystemLoader(self.templates))
            template = env.get_template('wsdl_temp.wsdl')
            reqstring = 'http://{0}{1}'.format(ctx.transport.req['HTTP_HOST'],ctx.transport.req['SCRIPT_NAME'])
            response = template.render(serv_loc=reqstring)
            response = response.encode('utf-8')
            #response.headers['Content-Type'] = 'text/xml'
            ctx.transport.wsdl = response
            return

class WofWSDL_1_1(InterfaceDocumentBase):
    templates=None
    templateName = 'wsdl_1_1_template.wsdl'

    def __init__(self, interface=None, _with_partnerlink=False, templates=None):
        super(WofWSDL_1_1, self).__init__(interface)
        self.templates=templates

    def build_interface_document(self, url, templates):
        """This function is supposed to be called just once, as late as possible
        into the process start. It builds the interface document and caches it
        somewhere. The overriding function should never call the overridden
        function as this may result in the same event firing more than once.
        """
        doc = self.get_wsdl_1_1( url, templates )
        return doc

    def get_interface_document(self):
        """This function is called by server transports that try to satisfy the
        request for the interface document. This should just return a previously
        cached interface document.
        """

        raise NotImplementedError('Extend and override.')

    # def _add_port_to_service(self, service, port_name, binding_name):
    #     """ Builds a wsdl:port for a service and binding"""
    #
    #     pref_tns = self.interface.get_namespace_prefix(self.interface.tns)
    #
    #     wsdl_port = SubElement(service, WSDL11("port"))
    #     wsdl_port.set('name', port_name)
    #     wsdl_port.set('binding', '%s:%s' % (pref_tns, binding_name))
    #
    #     addr = SubElement(wsdl_port, WSDL11_SOAP("address"))
    #     addr.set('location', self.url)

    def get_wsdl_1_1(self, url, templates ):

            env = Environment(loader=FileSystemLoader(templates))
            template = env.get_template(self.templateName)
            response = template.render(serv_loc=url)
            response = response.encode('utf-8')
            #response.headers['Content-Type'] = 'text/xml'

            return response

    def on_get_wsdl_1_1_(self, ctx ):
            env = Environment(loader=FileSystemLoader(self.templates))
            template = env.get_template(self.templateName)
            reqstring = 'http://{0}{1}'.format(ctx.transport.req['HTTP_HOST'],ctx.transport.req['SCRIPT_NAME'])
            response = template.render(serv_loc=reqstring)
            response = response.encode('utf-8')
            #response.headers['Content-Type'] = 'text/xml'
            ctx.transport.wsdl = response
            return