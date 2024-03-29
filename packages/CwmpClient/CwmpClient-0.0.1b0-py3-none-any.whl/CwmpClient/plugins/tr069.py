from CwmpClient.nodes import *
import aiohttp
import logging
import xml.dom as xmldom
log = logging.getLogger("TR-069")

SOAPNS = 'http://schemas.xmlsoap.org/soap/envelope/'
CWMPNS = 'urn:dslforum-org:cwmp-1-0'

class Tr69Request:
    def __init__(self, config) -> None:
        self.deviceId = "0"
        self.config = config
        self.protocols = "1.4,1.3,1.2,1.1,1.0"

    def makeDeviceStruct(self, doc):
        device = doc.createElementNS(CWMPNS, 'cwmp:DeviceId')

        Manufacturer = doc.createElementNS(CWMPNS, 'cwmp:Manufacturer')
        Manufacturer.appendChild(doc.createTextNode(str(self.config['Device']['DeviceInfo']['Manufacturer'])))
        device.appendChild(Manufacturer)

        Oui = doc.createElementNS(CWMPNS, 'cwmp:OUI')
        Oui.appendChild(doc.createTextNode(str(self.config['Device']['DeviceInfo']['ManufacturerOUI'])))
        device.appendChild(Oui)

        ProductClass = doc.createElementNS(CWMPNS, 'cwmp:ProductClass')
        ProductClass.appendChild(doc.createTextNode(str(self.config['Device']['DeviceInfo']['ProductClass'])))
        device.appendChild(ProductClass)

        SerialNumber = doc.createElementNS(CWMPNS, 'cwmp:SerialNumber')
        SerialNumber.appendChild(doc.createTextNode(str(self.config['Device']['DeviceInfo']['SerialNumber'])))
        device.appendChild(SerialNumber)

        return device

    def todom(self):
        from argparse import Namespace

        impl = xmldom.getDOMImplementation()
        self.document = impl.createDocument(None, 'Envelope', None)
        self.header = self.document.createElementNS(SOAPNS, 'soap:Header')
        self.body = self.document.createElementNS(SOAPNS, 'soap:Body')
        device_id = self.document.createElementNS(CWMPNS, 'cwmp:ID')
        doc  = impl.createDocument(None, 'Envelope', None)
        doc.documentElement.setAttributeNS(xmldom.XMLNS_NAMESPACE, 'xmlns:soap', SOAPNS)
        doc.documentElement.setAttributeNS(xmldom.XMLNS_NAMESPACE, 'xmlns:cwmp', CWMPNS)
        header = doc.createElementNS(SOAPNS, 'soap:Header')
        body = doc.createElementNS(SOAPNS, 'soap:Body')

        # device_id = doc.createElementNS(CWMPNS, 'cwmp:ID')
        # device_id.appendChild(doc.createTextNode("0"))
        # header.appendChild(device_id)

        # if self.protocols.find('1.4') != -1:
        #     cwmp_version = doc.createElementNS(CWMPNS, 'cwmp:SupportedCWMPVersions')
        #     cwmp_version.appendChild(doc.createTextNode(self.protocols))
        #     header.appendChild(cwmp_version)
        
        doc.documentElement.appendChild(header)
        doc.documentElement.appendChild(body)
        return Namespace(document=doc, header=header, body=body)
        

    def toxml(self):
        return self.todom().document.toxml()

class Tr69Inform(Tr69Request):
    def __init__(self, config, events) -> None:
        super().__init__(config)
        self.events = events
        self.retry = 0
        self.parameters = ParameterListValue(config)
        self.parameters.addPath('Device.RootDataModelVersion')
        self.parameters.addPath('Device.DeviceInfo.')
        self.parameters.addPath('Device.ManagementServer.ParameterKey')

    def todom(self):
        from datetime import datetime
        doc = super().todom()

        inform = doc.document.createElementNS(CWMPNS, 'cwmp:Inform')
        MaxEnvelopes = doc.document.createElementNS(CWMPNS, 'cwmp:MaxEnvelopes')
        MaxEnvelopes.appendChild(doc.document.createTextNode("1"))
        inform.appendChild(MaxEnvelopes)

        CurrentTime = doc.document.createElementNS(CWMPNS, 'cwmp:CurrentTime')
        CurrentTime.appendChild(doc.document.createTextNode(datetime.now().isoformat()))
        inform.appendChild(CurrentTime)

        RetryCount = doc.document.createElementNS(CWMPNS, 'cwmp:RetryCount')
        RetryCount.appendChild(doc.document.createTextNode(str(self.retry)))
        inform.appendChild(CurrentTime)
        inform.appendChild(self.makeDeviceStruct(doc.document))

        ParameterListNode = self.parameters.todom(doc.document)
        inform.appendChild(ParameterListNode)

        EventList = doc.document.createElementNS(CWMPNS, 'cwmp:Event')
        EventList.setAttributeNS(SOAPNS, 'soap:arrayType', "cwmp:EventStruct[%d]" % len(self.events))
        for event in self.events:
            EventStruct = doc.document.createElement('EventStruct')
            eventid = doc.document.createElementNS(CWMPNS, 'cwmp:EventCode')
            eventid.appendChild(doc.document.createTextNode(event))
            EventStruct.appendChild(eventid)
            EventList.appendChild(EventStruct)
        inform.appendChild(EventList)

        doc.body.appendChild(inform)
        return doc

async def loader(rootnode):
    log.debug('Load defaults parameters')
    rootnode['Device']['ManagementServer']['ConnectionRequestURL'] = ROParameter(str)
    rootnode['Device']['ManagementServer']['ConnectionRequestPassword'] = Parameter(str)
    rootnode['Device']['ManagementServer']['ConnectionRequestUsername'] = Parameter(str)
    rootnode['Device']['ManagementServer']['URL'] = Parameter(str, "http://acs.dites.team/")
    rootnode['Device']['ManagementServer']['Password'] = Parameter(str)
    rootnode['Device']['ManagementServer']['Username'] = Parameter(str)
    rootnode['Device']['ManagementServer']['PeriodicInformEnable'] = Parameter(bool, False)
    rootnode['Device']['ManagementServer']['PeriodicInformInterval'] = Parameter(int, 300)
    rootnode['Device']['DeviceInfo']['Manufacturer'] = Parameter(str, "Dites Telecom")
    rootnode['Device']['DeviceInfo']['ManufacturerOUI'] = Parameter(str, "FFFFFF")
    rootnode['Device']['DeviceInfo']['ProductClass'] = Parameter(str, "DTBox1")
    rootnode['Device']['DeviceInfo']['SerialNumber'] = Parameter(str, "0123456")
    rootnode['Device']['DeviceInfo']['ProvisioningCode'] = Parameter(str, "")
    rootnode['Device']['DeviceInfo']['SoftwareVersion'] = Parameter(str, "0.0.1")
    rootnode['Device']['DeviceInfo']['HardwareVersion'] = Parameter(str, "1.0.0")
    rootnode['Device']['ManagementServer']['ParameterKey'] = Parameter(str, "")
    rootnode['Device']['RootDataModelVersion'] = Parameter(str, "2.15")

class SessionRequest:
    def __init__(self, session, config, node) -> None:
        self.session = session
        self.method = None
        self.config = config
        self.RequestId = None

    async def exec(self, app):
        raise NotImplementedError()
    
    def getAnswer(self, app):
        ans = Tr69Request(app)
        parts = ans.todom()
        answer = parts.document.createElementNS(CWMPNS, "cwmp:%sResponse" % self.method)
        
        RequestId = parts.document.createElementNS(CWMPNS, 'cwmp:ID')
        RequestId.appendChild(parts.document.createTextNode(self.RequestId))
        RequestId.setAttributeNS(SOAPNS, 'soap:mustUnderstand', "1")
        parts.header.appendChild(RequestId)

        parts.body.appendChild(answer)
        return parts, answer

class ParameterList:
    def __init__(self, config) -> None:
        self.config = config
        self.parameters = dict()

    def addPath(self, path: str) -> None:
        path_parts = path.split('.') if len(path) > 0 else []
        self._get_parameters(self.config, path_parts)

    def _get_parameters(self, currentNode : BaseNode, path: list[str], prefix: str = "") -> None:
        log.debug("Prefix: %s, Path: %s", prefix, path)
        if isinstance(currentNode, Parameter):
            self.parameters.update({prefix: currentNode})
        elif len(path) == 0:
            self.parameters.update({prefix + '.' + name: child for name, child in currentNode.childs.items()})
        else:
            node_name = path.pop(0)
            if len(node_name) == 0:
                self.parameters.update({prefix + '.' + name: child for name, child in currentNode.childs.items()})
            elif node_name == '*':
                for node_name in currentNode.childs:
                    self._get_parameters(currentNode[node_name], path, prefix + '.' + node_name if len(prefix) > 0 else node_name)
            else:
                self._get_parameters(currentNode[node_name], path, prefix + '.' + node_name if len(prefix) > 0 else node_name)

    def todom(self, document):
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "ParameterList[ %s ]" % ", ".join(" = ".join([key, str(value)]) for key, value in self.parameters.items())

class ParameterListValue(ParameterList):
    def todom(self, document):
        pl = document.createElement('ParameterList')
        pl.setAttributeNS(SOAPNS, 'soap:arrayType', "cwmp:ParameterValueStruct[%d]" % len(self.parameters))
        for key, value in self.parameters.items():
            pis = document.createElement('ParameterValueStruct')
            name = document.createElement('Name')
            name.appendChild(document.createTextNode( key.lstrip(".") ))
            pis.appendChild(name)
            writable = document.createElement('Value')
            writable.appendChild(document.createTextNode(str(value)))
            pis.appendChild(writable)
            pl.appendChild(pis)
        return pl
    
class ParameterLisName(ParameterList):
    def todom(self, document):
        pl = document.createElement('ParameterList')
        pl.setAttributeNS(SOAPNS, 'soap:arrayType', "cwmp:ParameterInfoStruct[%d]" % len(self.parameters))
        for key, value in self.parameters.items():
            pis = document.createElement('ParameterInfoStruct')
            name = document.createElement('Name')
            name.appendChild(document.createTextNode( key.lstrip(".") ))
            pis.appendChild(name)
            writable = document.createElement('Writable')
            writable.appendChild(document.createTextNode("1" if value.writable else "0"))
            pis.appendChild(writable)
            pl.appendChild(pis)
        return pl

class RequestGetParameterNames(SessionRequest):
    def __init__(self, session, config, node) -> None:
        super().__init__(session, config, node)
        self.method = 'GetParameterNames'
        log.debug("Get Request GetParameterNames (%s)", node.toxml())
        NextLevelNode = node.getElementsByTagName('NextLevel')
        if len(NextLevelNode) != 1:
            raise Exception("NextLevel node in GetParameterNames must be set")
        self.nextLevel = NextLevelNode[0].firstChild.data == "1" if NextLevelNode[0].hasChildNodes() else True

        # Find Path
        ParameterPathNode = node.getElementsByTagName('ParameterPath')
        if len(ParameterPathNode) != 1:
            raise Exception("ParameterPath node in GetParameterNames must be set")
        self.parameterPath = ParameterPathNode[0].firstChild.data if ParameterPathNode[0].hasChildNodes() else ""

        log.debug("Parsed Path: %s, Next level %s", self.parameterPath, self.nextLevel)
        self.parameters = ParameterLisName(config)
        self.parameters.addPath(self.parameterPath)

    async def exec(self, app):
        dom, ans = self.getAnswer(app)
        ans.appendChild(self.parameters.todom(dom.document))
        acs_url = str(app.root['Device']['ManagementServer']['URL'])
        log.debug("Full response GetParamtersNames : %s", dom.document.toxml())
        async with self.session.post(acs_url, data=dom.document.toxml(), headers={'SOAPAction': ''}) as data:
            return data.status, await data.text()

class RequestGetParameterValues(SessionRequest):
    def __init__(self, session, config, node) -> None:
        super().__init__(session, config, node)
        self.method = 'GetParameterValues'
        log.debug("Get Request GetParameterValues (%s)", node.toxml())

        ParameterNode = node.getElementsByTagName('ParameterNames')[0]
        self.parameters = ParameterListValue(config)
        for item in ParameterNode.childNodes:
            if item.tagName != "string":
                log.error("Bad tagname in ParameterNames %s", item.tagName)
                continue
            else:
                self.parameters.addPath(item.firstChild.data)

    async def exec(self, app):
        dom, ans = self.getAnswer(app)
        ans.appendChild(self.parameters.todom(dom.document))
        acs_url = str(app.root['Device']['ManagementServer']['URL'])
        log.debug("Full response GetParameterValues : %s", dom.document.toxml())
        async with self.session.post(acs_url, data=dom.document.toxml(), headers={'SOAPAction': ''}) as data:
            return data.status, await data.text()

class RequestReboot(SessionRequest):
    def __init__(self, session, node) -> None:
        super().__init__(session)

    async def exec(self, app):
        """
        Simulation of Reboot with Inform
        """
        acs_url = str(app.root['Device']['ManagementServer']['URL'])
        req = Tr69Inform(app.root, ['1 BOOT', 'M Reboot'])
        async with self.session.post(acs_url) as data:
            log.debug("Send Reboot simulation. Status %d, Headers: %s, Data: %s", data.status, data.headers, await data.text())

class RequestSetParameterValues(SessionRequest):
    def __init__(self, session, config, node) -> None:
        super().__init__(session, config, node)
        self.method = "SetParameterValues"
        self.parameters = ParameterListValue(config)
        ParametersValues = node.getElementsByTagName('ParameterValueStruct')

        for item in ParametersValues:
            name = None
            value = None
            for itemNode in item.childNodes:
                if itemNode.tagName == "Name":
                   name = itemNode.firstChild.data
                elif itemNode.tagName == "Value":
                   value = itemNode
                else:
                    log.error("Unknown tag: %s in ParameterValueStruct", itemNode.tagName)
                    raise Exception("Unknown tag: %s in ParameterValueStruct", itemNode.tagName)
            self.parameters.addPath(name)
            self.parameters.parameters[name](value.firstChild.data)

    async def exec(self, app):
        dom, ans = self.getAnswer(app)
        ans.appendChild(self.parameters.todom(dom.document))
        acs_url = str(app.root['Device']['ManagementServer']['URL'])
        log.debug("Full response SetParameterValues : %s", dom.document.toxml())
        async with self.session.post(acs_url, data=dom.document.toxml(), headers={'SOAPAction': ''}) as data:
            return data.status, await data.text()

supported_methods = {
    'GetParameterNames': RequestGetParameterNames,
    'Reboot': RequestReboot,
    'GetParameterValues': RequestGetParameterValues,
    'SetParameterValues': RequestSetParameterValues,
}

class CloseSession(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Session closed by ACS", *args)

async def get_next_request(app, session, status, textdata):
    from xml.dom.minidom import parseString
    log.debug("Get request from ACS Status %s, Data: %s", status, textdata)
    if status != 200:
        raise CloseSession()

    answer = parseString(textdata)
    body = answer.getElementsByTagNameNS(SOAPNS, 'Body')[0]
    RequestId = answer.getElementsByTagNameNS(CWMPNS, 'ID')
    for req in body.childNodes:
        node_name = req.tagName.split(':')[1] if req.tagName.find(':') != -1 else req.tagName
        if node_name not in supported_methods:
            log.error("Receive unsupported method: %s" % node_name)
            raise Exception("Receive unsupported method: %s" % node_name)
        else:
            RequestMethod = supported_methods[node_name](session, app.root, req)
            if len(RequestId) > 0:
                RequestMethod.RequestId = RequestId[0].firstChild.data
            yield RequestMethod

async def start(app):
    """
    Start TR69 Client. Send Boot event and start interval
    """
    acs_url = str(app.root['Device']['ManagementServer']['URL'])
    log.debug("Start session boot %s" % acs_url)
    
    async with aiohttp.ClientSession() as session:
        req = Tr69Inform(app.root, ['1 BOOT', 'M Reboot'])
        log.debug("Send new session Inform %s", req.toxml())

        async with session.post(acs_url, data=req.toxml()) as boot:
            log.debug("Get Inform answer from ACS Status %s, Headers %s, Data: %s", boot.status, boot.headers, await boot.text())
        try:
            async with session.post(acs_url, data="") as data:
                text = await data.text()
                status = data.status

            while True:
                async for method in get_next_request(app, session, status, text):
                    status, text = await method.exec(app)
            
        except CloseSession:
            pass

        print("End session")