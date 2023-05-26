from rstcloth import RstCloth
import json
import sys


input_file_path = sys.argv[1]

with open(input_file_path, "r") as content:
    object = json.load(content)
    
    requirements = object["List Artifact Info"]
    with open("ouput_task2.rst", "w") as f:
        rstData = RstCloth(f)
        rstData.title(object["Module Name"])
        rstData.newline()
        for requirement in requirements:
            if requirement["Attribute Type"] == "Heading":
                rstData.heading(requirement["Title"],"*")
                rstData.newline()
            if requirement["Attribute Type"] == "Information":
                rstData.directive(name="sw_req",fields=[("id",str(requirement["Identifier"])), ("artifact_type",requirement["Attribute Type"])])
                rstData.newline()
                rstData.content(requirement["ReqIF.Text"])
                rstData.newline()
            if requirement["Attribute Type"] == "MO_FUNC_REQ" or requirement["Attribute Type"] == "MO_NON_FUNC_REQ":
                rstData.directive(name="sw_req",fields=[("status",requirement["Status"]), 
                                                        ("id",str(requirement["Identifier"])), 
                                                        ("safety_level",requirement["Safety Classification"]),
                                                        ("artifact_type", requirement["Attribute Type"]),
                                                        ("crq",requirement["CRQ"])])
                rstData.newline()
                rstData.content(requirement["ReqIF.Text"])
                rstData.newline()
                rstData.directive(name="verify",content=requirement["Verification Criteria"])
                rstData.newline()
    print("Data migration complete.\nOutput file is at " + f.name)