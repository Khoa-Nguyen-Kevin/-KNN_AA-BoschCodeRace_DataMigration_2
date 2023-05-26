from bs4 import BeautifulSoup
from reqif.parser import ReqIFParser
import json
import sys



input_file_path = sys.argv[1]
data = {}

reqif_bundle = ReqIFParser.parse(input_file_path)
for specification in reqif_bundle.core_content.req_if_content.specifications:
    ModuleName = specification.long_name
    ModuleType = specification.specification_type
    ModuleType = reqif_bundle.lookup.spec_types_lookup[ModuleType].long_name

    data["Module Name"] = ModuleName
    data["Module Type"] = ModuleType

    reqIFtext = None
    Identifier = None
    CreatedOn = None
    Description = None
    Type = None
    ModifiedOn = None
    Contributor = None
    Title = None
    Creator = None
    
    hierachy = reqif_bundle.iterate_specification_hierarchy(specification)
    InfoList = []
    for h2 in hierachy:
        obj = reqif_bundle.get_spec_object_by_ref(h2.spec_object)
        Type = reqif_bundle.get_spec_object_type_by_ref(obj.spec_object_type)
        InfoDict = {}

        Type = Type.long_name #Attribute Type
        for attribute in obj.attributes:
            ref = attribute.definition_ref
            name = reqif_bundle.lookup.spec_types_lookup[obj.spec_object_type].attribute_map[ref].long_name
            if name == "ReqIF.Description": #Description
                Description = attribute.value
            if name == "ReqIF.ForeignCreatedOn": #Created on
                CreatedOn = attribute.value
            if name == "ReqIF.ForeignModifiedBy": #Contributor
                Contributor = attribute.value
            if name == "ReqIF.ForeignID": #Identifier
                Identifier = attribute.value
            if name == "ReqIF.ForeignModifiedOn": #Modified on
                ModifiedOn = attribute.value
            if name == "ReqIF.ForeignCreatedBy": #Creator
                Creator = attribute.value
            if name == "ReqIF.Text": #ReqIF.Text
                reqIFtext = attribute.value
            if name == "ReqIF.Name": #Title
                Title = BeautifulSoup(attribute.value_stripped_xhtml, 'html.parser')
                div_element = Title.find('div')
                Title = div_element.get_text()

            if Type == "MO_FUNC_REQ" or Type == "MO_NON_FUNC_REQ":
                if name == "Status": #Status
                    StatusRef = attribute.definition_ref
                    StatusValueRef = attribute.value[0]
                    T_StatusRef = reqif_bundle.lookup.spec_types_lookup[obj.spec_object_type].attribute_map[StatusRef].datatype_definition
                    Status = reqif_bundle.lookup.data_types_lookup[T_StatusRef].values_map[StatusValueRef].long_name
                if name == "CRQ": #CRQ
                    CRQ = attribute.value
                if name == "VAR_FUNC_SYS": #VAR_FUNC_SYS
                    VFS = attribute.value
                if name == "Allocation": #Allocation
                    Allocation = attribute.value
                if name == "Safety Classification": #Safety classification
                    SafetyRef = attribute.definition_ref
                    SafetyValueRef = attribute.value[0]
                    T_SafetyRef = reqif_bundle.lookup.spec_types_lookup[obj.spec_object_type].attribute_map[SafetyRef].datatype_definition
                    Safety_Classification = reqif_bundle.lookup.data_types_lookup[T_SafetyRef].values_map[SafetyValueRef].long_name
                if name == "Verification Criteria": #Verification Criteria
                    Verification_Criteria = attribute.value
                
            if Type == "Heading":
                if name == "ReqIF.ChapterName":
                    reqIFtext = attribute.value

        if Type == "MO_FUNC_REQ" or Type == "MO_NON_FUNC_REQ": #Extra values for MO_FUNC_REQ and MO_NON_FUNC_REQ
            InfoDict["Status"] = Status
            InfoDict["Created On"] = CreatedOn
            InfoDict["Description"] = "" if Description == None else Description
            InfoDict["CRQ"] = CRQ
            InfoDict["Attribute Type"] = Type
            InfoDict["Modified On"] = ModifiedOn
            InfoDict["Title"] = Title
            InfoDict["Contributor"] = Contributor
            InfoDict["Verification Criteria"] = Verification_Criteria
            InfoDict["Creator"] = Creator
            InfoDict["VAR_FUNC_SYS"] = VFS
            InfoDict["ReqIF.Text"] = reqIFtext
            InfoDict["Identifier"] = int(Identifier)
            InfoDict["Allocation"] = Allocation
            InfoDict["Safety Classification"] = Safety_Classification
        
        
        InfoDict["ReqIF.Text"] = reqIFtext
        InfoDict["Identifier"] = int(Identifier)
        InfoDict["Created On"] = CreatedOn
        InfoDict["Description"] = "" if Description == None else Description
        InfoDict["Attribute Type"] = Type
        InfoDict["Modified On"] = ModifiedOn
        InfoDict["Contributor"] = Contributor
        InfoDict["Title"] = Title
        InfoDict["Creator"] = Creator
        InfoList.append(InfoDict)
    data["List Artifact Info"] = InfoList
    json_data = json.dumps(data, indent=2)

    with open("output_task1.json","w") as f:
        f.write(json_data)
        print("Data Migration complete.\nOutput file is at " + f.name)
