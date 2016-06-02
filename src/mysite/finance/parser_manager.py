import re
import xmltodict
import dicttoxml
import xml.etree.cElementTree as cElementTree
import csv
import json
import simplejson
import logging
import datetime
from decimal import Decimal
# from logging.config import dictConfig
# from config.logger_settings import LOG_SETTINGS
# dictConfig(LOG_SETTINGS)
logger = logging.getLogger(__name__)


valuedict = {"&amp;": "&",
             "&apos;": "'",
             "&quot;": "\"",
             "&lt;": "<",
             "&gt;": ">"
             }


class Parser:
    '''
        :Notes: Parser class performs the parsing operation based on the input of the parse method.
    '''

    def parse(
            self,
            input,
            from_type,
            to_type,
            csv_dict_row=False,
            dict_csv_file=None,
            fieldnames=None,
            headless=0):
        """
            :Notes: This method will decide to which function should be called based on
            input arguments and return the output.

            :Args:
                input (str) : input
                from_type (XML) : type of the input attribute (XML, JSON..)
                to_type (XML) : expected output type (XML, JSON..)
                csv_dict_row : bool True : if dict is rowwise
                                    False : if dict is columnwise
                dict_csv_file : csv file name with path
            :Returns :
             call the appropriate function and give the expected output type.
        """

        try:
            if from_type == "XML" and to_type == "DICT":
                logger.info("Calling the function xmltodict")
                return self.ParsetoDict(input)

            elif from_type == "DICT" and to_type == "XML":
                logger.info("Calling the function dictToXML")
                return self.dictToXML(input)

            elif from_type == "CSV" and to_type == "DICT" and csv_dict_row:
                logger.info("Calling the function CSVtoDict_row_wise")
                return self.CSVtoDict_row_wise(input, fieldnames)

            elif from_type == "CSV" and to_type == "DICT" and csv_dict_row == False:
                return self.CSVtoDict_column_wise(input, fieldnames)

            elif from_type == "DICT" and to_type == "CSV" and dict_csv_file:
                return self.DicttoCSV(input, dict_csv_file, fieldnames, headless)

            elif from_type == "JSON" and to_type == "DICT":
                return self.JSONtoDict(input)

            elif from_type == "DICT" and to_type == "JSON":
                return self.DicttoJSON(input)

            elif from_type == "OBJECT" and to_type == "JSON":
                return self.to_json(input)

            elif from_type == "OBJECT" and to_type == "DICT":
                return self.to_dict(input)

        except Exception as e:
            raise Exception("Unhandled exception while parsing the request", e)

    def __getMultiDict(self, xmlTree, xmlDict, cnt=0):
        """
        :Notes: Populates the Dictionary.

        :Args:
            xmlTree (XML): XML object of Request
            xmlDict (dict) : Dictionary to be populated

        Recursively generates all the (key,value) pairs as Dictionary.

        """

        if cElementTree.iselement(xmlTree) and xmlTree.getchildren():
            if xmlTree.tag in xmlDict:
                tag_count = len([i for i in xmlDict if i.startswith(xmlTree.tag)])
                key = xmlTree.tag + "_" + str(tag_count)
            else:
                key = xmlTree.tag
            xmlDict[key] = {}
            for elem in xmlTree.getchildren():
                self.__getMultiDict(elem, xmlDict[key])
        elif cElementTree.iselement(xmlTree) and not xmlTree.getchildren():
            if xmlTree.text:
                for key in valuedict:
                    if key in xmlTree.text:
                        xmlTree.text = xmlTree.text.replace(key, valuedict[key])
            if xmlTree.tag in xmlDict:
                tag_count = len([i for i in xmlDict if i.startswith(xmlTree.tag)])
                xmlDict[xmlTree.tag + "_" + str(tag_count)] = (xmlTree.text or "").strip() or None
            else:
                xmlDict[xmlTree.tag] = (xmlTree.text or "").strip() or None
        return xmlDict

    def __getDict(self, xmlTree, xmlDict):
        """
        :Notes: Populates the Dictionary.

        :Args:
            xmlTree: XML object of Request
            xmlDict: Dictionary to be populated

        Recursively generates all the (key,value) pairs as Dictionary.

        """

        if cElementTree.iselement(xmlTree) and xmlTree.getchildren():
            xmlDict[xmlTree.tag] = {}
            for elem in xmlTree.getchildren():
                self.__getDict(elem, xmlDict[xmlTree.tag])
        elif cElementTree.iselement(xmlTree) and not xmlTree.getchildren():
            if xmlTree.text:
                for key in valuedict:
                    if key in xmlTree.text:
                        xmlTree.text = xmlTree.text.replace(key, valuedict[key])
            xmlDict[xmlTree.tag] = (xmlTree.text or '').strip()
        return xmlDict

    def ParsetoDict(self, strXMLReq, multitags=False):
        """
        :Notes: Builds an XML object and parse it.

        Is a copy of requestparser xmlParseDict method, handling the encoding of special charectors in xml.

        :Args:

            strXMLReq: Request as XML string.
            parentTag: The main parent tag of the XML request.

        Build an XML object
        Parses the XML object and populate the clientDict

        Note:

        Applicable only in the case where XML request doesn't contain
        same tag appearing more than once at the same level.

        """

#         parentTag = 'TransactionInfo'
        tree = None
        try:
            tree = cElementTree.fromstring(strXMLReq)
        except Exception as e:
            print e
            raise Exception("Invalid Input - not XML", e)

        clientDict = {}
        if multitags:
            self.__getMultiDict(tree, clientDict)
        else:
            self.__getDict(tree, clientDict)
#         clientDict = clientDict[parentTag]
        return clientDict

    def dictToXML(self, input):
        """
        :Args:
            input (dict) : Dictionary
        :Returns:
        XML : output_dict
        """

        try:
            output_dict = dicttoxml.dicttoxml(input)
            return output_dict
        except Exception as e:
            raise Exception("Invalid Input", e)

    def CSVtoDict_column_wise(self, file_path, fieldnames):
        """
        :Args:

        file_path (str ): path of the file which we want to convert to CSV

        :Returns:
        Dict : result

        """

        try:
            reader = csv.DictReader(open(str(file_path)), fieldnames=fieldnames)
        except Exception as e:
            raise Exception("Invalid Input", e)

        result = {}
        for row in reader:
            for column, value in row.iteritems():
                result.setdefault(column, []).append(value)

        return result

    def CSVtoDict_row_wise(self, file_path, fieldnames):
        """
        :Args:

        file_path (str ): path of the file which we want to convert to CSV

        :Returns:
        Dict : result

        """

        try:
            reader = csv.DictReader(open(str(file_path)), fieldnames=fieldnames)
        except Exception as e:
            raise Exception("Invalid Input", e)

        result = []
        for row in reader:
            result.append(row)
        return result

    def DicttoCSV(self, input, dict_csv_file, fieldnames, headless):
        '''
        :Args:
        dict_csv_file : path of the file
        '''
        try:
            print "******"
            writer = csv.DictWriter(open(str(dict_csv_file), 'wb'), fieldnames)
        except Exception as e:
            raise Exception("Invalid Input", e)
        if headless == 0:
            writer.writeheader()
        writer.writerows(input)

    def JSONtoDict(self, json_doc):
        """
        :Args:
        json_doc (json) : json object

        :Returns:
        dict : returns dict
        """

        try:
            return simplejson.loads(json_doc)
        except Exception as e:
            raise Exception("Invalid Input", e)

    def DicttoJSON(self, input):
        """
        :Args:

        input (dict) : dictionary
        :Returns:
        json : returns JSON object
        """

        try:
            return simplejson.dumps(input)
        except Exception as e:
            raise Exception("Invalid Input", e)

    def str_serializer(self, obj):
        """
        Note : This method converts the following data types to string
                > datetime object
                > date object
                > Decimal object
        :param: object : any class object
        :returns: string of the object provided
        """
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return float(obj)

    def object_to_dict(self, obj):
        """
        Note : This method identifies the property instance available in an object to
                convert into dictionary.
        :param: any class object
        :return: python dictionary
        """
        obj_dict = {}
        for name, value in vars(obj.__class__).items():
            if isinstance(value, property):
                obj_dict[name] = getattr(obj, name)
        return obj_dict

    def to_json(self, obj):
        """Represent instance of a class as JSON.
        Arguments:
        obj -- any object
        Return:
        String that represent JSON-encoded object.
        """
        def serialize(obj):
            """Recursively walk object's hierarchy."""
            if isinstance(obj, (bool, int, long, float, basestring)):
                return obj
            elif isinstance(obj, dict):
                obj = obj.copy()
                for key in obj:
                    obj[key] = serialize(obj[key])
                return obj
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(serialize([item for item in obj]))
            elif hasattr(obj, '__dict__'):
                return serialize(self.object_to_dict(obj))
            else:
                return self.str_serializer(obj)
        return json.dumps(serialize(obj))

    def to_dict(self, obj):
        """Represent instance of a class as JSON.
        Arguments:
        obj -- any object
        Return:
        String that represent JSON-encoded object.
        """
        def serialize(obj):
            """Recursively walk object's hierarchy."""
            if isinstance(obj, (bool, int, long, float, basestring)):
                return obj
            elif isinstance(obj, dict):
                obj = obj.copy()
                for key in obj:
                    obj[key] = serialize(obj[key])
                return obj
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(serialize([item for item in obj]))
            elif hasattr(obj, '__dict__'):
                return serialize(self.object_to_dict(obj))
            else:
                return self.str_serializer(obj)
        return serialize(obj)


if __name__ == '__main__':
    class C(object):
        """
        @summary: Convert a single class object to JSON
        """

        def __init__(self, a=None, b=None):
            self._a = a
            self._b = b

        @property
        def a(self):
            return self._a

        @a.setter
        def a(self, value):
            if isinstance(value, datetime.datetime):
                self._a = value

        @property
        def b(self):
            return self._b

        @b.setter
        def b(self, value):
            if isinstance(value, datetime.date):
                self._b = value
    par = Parser()
    o = C()
    o.a = datetime.datetime.now()
    o.b = datetime.date.today()
    print type(o)
    json_obj = par.parse(o, 'OBJECT', 'JSON')
    print type(json_obj)
    print 'Converted to JSON (single class object) --> ', json_obj, type(json_obj)

    json_obj = par.parse(o, 'OBJECT', 'DICT')
    print type(json_obj)
    print 'Converted to JSON (single class object) --> ', json_obj, type(json_obj)

    #     #input= "<note><to>Tove</to><from>Jani</from><heading>Reminder</heading><body>Don't forget me this weekend!</body></note>"
#     input = """<BankAccountVerifyService>
#                         <Authentication>
#                             <UserName>%s</UserName>
#                             <Password>%s</Password>
#                             <Source>TMS</Source>
#                             <OTP>0</OTP>
#                         </Authentication>
#                         <PersonnalInfo>
#                               <CustID>%s</CustID>
#                               <CustFName>%s</CustFName>
#                               <CustLName >%s</CustLName>
#                               <CustDOB>%s</CustDOB>
#                               <EmailID>%s</EmailID>
#                               <MobilePhone>%s</MobilePhone>
#                               <HouseNumber>%s</HouseNumber>
#                               <HouseName>%s</HouseName>
#                               <Street>%s</Street>
#                               <PostCode>%s</PostCode>
#                         </PersonnalInfo>
#                         <LoanInfo>
#                               <SortCode>%s</SortCode>
#                               <AccountNumber>%s</AccountNumber>
#                         </LoanInfo>
#                 </BankAccountVerifyService>"""
#     print "XML to DICT"
#     print par.parse(input, "XML", "DICT")
#
#     dictinput = {
#         'Authentication': {
#             'UserName': '%s',
#             'Source': 'TMS',
#             'Password': '%s',
#             'OTP': '0'},
#         'PersonnalInfo': {
#             'EmailID': '%s',
#             'MobilePhone': '%s',
#             'HouseName': '%s',
#             'HouseNumber': '%s',
#             'CustDOB': '%s',
#             'CustFName': '%s',
#             'CustLName': '%s',
#             'PostCode': '%s',
#             'CustID': '%s',
#             'Street': '%s'},
#         'LoanInfo': {
#             'SortCode': '%s',
#             'AccountNumber': '%s'}}
#     print "Dict to xml"
#     print par.parse(dictinput, "DICT", "XML")
#
#     # Dict to Json
# #     dict={
# #     "glossary": {
# #         "title": "example glossary",
# #         "GlossDiv": {
# #             "title": "S",
# #             "GlossList": {
# #                 "GlossEntry": {
# #                     "ID": "SGML",
# #                     "SortAs": "SGML",
# #                     "GlossTerm": "Standard Generalized Markup Language",
# #                     "Acronym": "SGML",
# #                     "Abbrev": "ISO 8879:1986",
# #                     "GlossDef": {
# #                         "para": "A meta-markup language, used to create markup languages such as DocBook.",
# #                         "GlossSeeAlso": ["GML", "XML"]
# #                     },
# #                     "GlossSee": "markup"
# #                 }
# #             }
# #         }
# #     }
# # }
#     dict = {'key': 'value'}
#
#     print "Dict to Json"
#     json_data = par.parse(dict, "DICT", "JSON")
#     print json_data
#
#     # Encoding to json
# #     JSONEncoder().encode(dict)
#     print "Json to DICT"
#     print par.parse(json_data, "JSON", "DICT")

#  Dict to CSV
#     par = Parser()
#     dict=[{'name':'krishna','age':'13'},{'name':'sachin','age':'42','size':'3'}]
#     fieldnames = ['name','age','size']
#     doc = "/host/lendingstream/src/core/lib/foundation/csvfile.csv"
#     print "Dict to CSV"
#     par.parse(dict, "DICT","CSV",dict_csv_file=doc,fieldnames=fieldnames)

# CSV to Dict  Use Case
#     pars = Parser()
#     csvfile='/host/lendingstream/docs/sample.csv'
#     fieldnames=['User Name','First Name','Last Name','Display Name']
#     #dict=pars.parse(csvfile,"CSV","DICT",fieldnames=fieldnames)
#     dict=pars.parse(csvfile,"CSV","DICT",csv_dict_row=True,fieldnames=fieldnames)
#     dict=pars.parse(csvfile,"CSV","DICT",fieldnames=fieldnames)
#     print dict
