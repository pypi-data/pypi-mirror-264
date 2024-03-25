import copy
import csv
import json
import jsonschema
import logging
import os
import urllib.request
import sys

# Rule structure
    # {
    #       "fullDescription": {
    #         "text": "Long description"
    #       },
    #       "messageStrings": {
    #         "pass": {
    #           "text": "The problem is {0}."
    #         }
    #       },
    #       "name": "Rule Name",
    #       "ruleId": "ruleId",
    #       "shortDescription": {
    #         "text": "short description of the rule. One short sentence."
    #       }
    #     }


# Result structure
# {
#           "level": "note",
#           "message": {
#             "arguments": [
#               "Hi, I am the problem!"
#             ],
#             "id": "pass"
#           },
#           "ruleId": "ruleId"
#         }


class Sarif():
    def __init__(self, file=None, validate=True, recreate=False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        stderr_handler.setFormatter(formatter)
        self.logger.addHandler(stderr_handler)
        
        if file:
           # check if file exists...
            self.filename = file
            if os.path.isfile(file) and not recreate:
                # read file
                try:
                    with open(file) as f:
                        self.sarif = json.load(f)
                        self.logger.info("Opened SARIF file.")
                        if validate and not self.verify_sarif():
                            raise ValueError("The SARIF did not pass validation and cannot be opened.")
                        return
                except json.JSONDecodeError:
                    self.logger.warning("Provided SARIF file is empty and will be deleted.")
                    os.remove(file)
            else:
                if recreate and os.path.isfile(file):
                    self.logger.info("Deleting existing file with same filename.")
                    os.remove(file)
                
                self.logger.info("Initializing self.sarif.")
                self.sarif = {
                "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json",
                "version": "2.1.0",
                "runs": [
                    {
                        "results": [],         
                        "tool": {
                            "driver": {
                                "name": "Scribe Platform API TOOL",
                                "rules": []
                            }
                        }
                    }
                ]
            }
        else:
            self.logger.info("Initializing self.sarif.")
            self.sarif = {
                "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.4.json",
                "version": "2.1.0",
                "runs": [
                    {
                        "results": [],         
                        "tool": {
                            "driver": {
                                "name": "Scribe Platform API TOOL",
                                "rules": []
                            }
                        }
                    }
                ]
            }


    def add_rule(self, name, ruleId, shortDescription, fullDescription,  messageStrings, properties=None):
        # properties: If usef - if string it is a tag, else - any json object
        # Check if rule exists and warn
        for rule in self.sarif['runs'][0]["tool"]["driver"]["rules"]:
            if rule["id"] == ruleId:
                self.logger.warning("Rule with ruleId " + ruleId + " already exists. Overwriting rule.")
                self.sarif['runs'][0]["tool"]["driver"]["rules"].remove(rule)

        if not properties:
            rule_obj = {
                "name": name,
                "id": ruleId,
                "fullDescription": {
                    "text": fullDescription
                },
                "shortDescription": {
                    "text": shortDescription
                },
                "messageStrings": messageStrings,
            }
        else:
            rule_obj = {
                "name": name,
                "id": ruleId,
                "fullDescription": {
                    "text": fullDescription
                },
                "shortDescription": {
                    "text": shortDescription
                },
                "messageStrings": messageStrings,
                "properties": properties
            }

        self.logger.info("Adding new rule.")
        self.sarif['runs'][0]["tool"]["driver"]["rules"].append(rule_obj)


    def add_result(self, ruleId, level, message_id, arguments, properties=None, locations=None):
        # Check if rule exists. If not warn and return
        rule_exists = False
        for rule in self.sarif['runs'][0]["tool"]["driver"]["rules"]:
            if rule["id"] == ruleId:
                rule_exists = True
                break
        if not rule_exists:
            self.logger.warning("Rule with ruleId " + ruleId + " does not exist. Skipping result.")
            return
    
        result_obj = {
            "ruleId": ruleId,
            "level": level,
            "message": {
                "arguments": arguments,
                "id": message_id
            }
        }

        if locations:
            result_obj["locations"] = locations

        if properties:
            result_obj["properties"] = properties

        self.logger.info(f"Adding new result for rule {ruleId}.")
        self.sarif['runs'][0]['results'].append(result_obj)

    def get_sarif(self):
        return self.sarif

    def save(self, validate=False, filename=None):
        try:
            if not filename and self.filename:
                filename = self.filename
        except AttributeError:
            if not filename:
                self.logger.error("The sarif cannot be written to a file as no filename was provided.")
                return
        
        if validate and not self.verify_sarif():
                self.logger.error("Unable to save sarif because it is formatted incorrectly.")
                return
        self.logger.info("Dumping SARIF to file.")
        with open(filename, 'w') as outfile:
            json.dump(self.sarif, outfile, indent=4, sort_keys=False)

    def get_table_result(self, ruleName, ruleId, level, shortDescription, message, ruleProperties, resultProperties):
        return {
            "ruleName": ruleName,
            "ruleId": ruleId,
            "level": level,
            "shortDescription": shortDescription,
            "message": message,
            "ruleProperties": ruleProperties,
            "resultProperties": resultProperties
        }

    def to_table(self, add_properties=True):
        """
        Converts SARIF (Static Analysis Results Interchange Format) results to a table format.

        This function processes SARIF results from a SARIF-formatted report stored in `self.sarif`.
        It extracts information about each result and its corresponding rule, and formats this 
        information into a table-like data structure (list of dictionaries).

        Each entry in the table contains details about a specific analysis result, including the rule
        name, rule ID, result level, a short description of the rule, and a formatted message.
        Optionally, properties of the rule and the result can be included.

        Parameters:
        add_properties (bool): If True, include rule and result properties in the table as a json string. 
                If False, these properties are not included. Defaults to True.

        Returns:
        list: A list of dictionaries, where each dictionary represents a row in the table. Each row
            contains details about a specific analysis result, such as rule name, rule ID, 
            result level, short description, message, and optionally, properties.
    """
        result_table = []
        rules = self.sarif['runs'][0]["tool"]["driver"]["rules"]
        # conver to dictionary with ruleId as key
        rules_dict = {}
        for rule in rules:
            rules_dict[rule["id"]] = rule

        for result in self.sarif['runs'][0]['results']:
            rule = rules_dict[result["ruleId"]]
            message = result["message"]["id"].format(*result["message"]["arguments"])
            if add_properties:
                ruleProperties = json.dumps(rule["properties"]) if "properties" in rule else json.dumps({})   
            else:
                ruleProperties = None

            if add_properties:
                resultProperties = json.dumps(result["properties"]) if "properties" in result else json.dumps({})
            else:
                resultProperties = None
            result_table.append(self.get_table_result(rule["name"], rule["id"], result["level"], rule["shortDescription"]["text"], message, ruleProperties, resultProperties))
        self.logger.info("Successfully converted to table.")
        return result_table

    def to_csv(self, filename, add_properties=True):
        """ 
        Writes data to a CSV file.

        This function converts data obtained from the to_table method 
        to a CSV format and writes it to a file. The first row of the CSV file 
        will contain the headers, which are the keys of the dictionaries returned 
        by to_table. Each subsequent row represents one data record.

        Parameters:
        filename (str): The name of the file to which the CSV data will be written. 
                        This should include the full path and the .csv extension.

        Returns:
        None
        """
        with open(filename, 'w', newline='') as file:
            data = self.to_table(add_properties=add_properties)
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()  # Writing the headers
            writer.writerows(data)  # Writing the data
            self.logger.info("CSV successfully written.")

    def rfilter_out(self, ruleIDs=None, levels=None, filename=None):
        if not ruleIDs and not levels:
            self.logger.error("Unable to complete operation because both 'ruleIDs' and 'levels' are empty.")
            return
        if filename == None:
            pass
        elif os.path.isfile(filename):
            with open(filename) as file:
                self.sarif = json.load(file)
        else:
            self.logger.error("Unable to read file because it does not exist.")
            return
        filtered_sarif = copy.deepcopy(self.sarif)
        
        for run_index, run in enumerate(self.sarif["runs"]):
            del_count = 0
            for index, item in enumerate(run["results"]):
                if ruleIDs and levels:
                    if item['ruleId'] in ruleIDs and item['level'] in levels:
                        index -= del_count
                        del filtered_sarif["runs"][run_index]["results"][index]
                        del_count += 1
                elif ruleIDs:
                    if item["ruleId"] in ruleIDs:
                        index -= del_count
                        del filtered_sarif["runs"][run_index]["results"][index]
                        del_count += 1
                elif levels:
                    if item['level'] in levels:
                        index -= del_count
                        del filtered_sarif["runs"][run_index]["results"][index]
                        del_count += 1
            
        self.logger.info("SARIF has been successfully filtered.")
        self.sarif = filtered_sarif
    
    def rfilter_only(self, ruleIDs=None, levels=None, filename=None):
        if not ruleIDs and not levels:
            self.logger.error("Unable to complete operation because both 'ruleIDs' and 'levels' are empty.")
            return
        if filename == None:
            pass
        elif os.path.isfile(filename):
            with open(filename) as file:
                self.sarif = json.load(file)
        else:
            self.logger.error("Unable to read file because it does not exist.")
            return
        filtered_sarif = copy.deepcopy(self.sarif)
        
        for run_index, run in enumerate(self.sarif["runs"]):
                del_count = 0
                for index, item in enumerate(run["results"]):
                    if ruleIDs and levels:
                        if item['ruleId'] not in ruleIDs or item['level'] not in levels:
                            index -= del_count
                            del filtered_sarif["runs"][run_index]["results"][index]
                            del_count += 1
                    elif ruleIDs:
                        if item["ruleId"] not in ruleIDs:
                            index -= del_count
                            del filtered_sarif["runs"][run_index]["results"][index]
                            del_count += 1
                    elif levels:
                        if item['level'] not in levels:
                            index -= del_count
                            del filtered_sarif["runs"][run_index]["results"][index]
                            del_count += 1
        
        self.logger.info("SARIF has been successfully filtered.")                
        self.sarif = filtered_sarif
    
    def find_results(self, ruleIDs=None, levels=None, filename=None):
        if not ruleIDs and not levels:
            self.logger.error("Unable to complete operation because both 'ruleIDs' and 'levels' are empty, meaning there is nothing to search for.")
            return
        try:
            if not filename and self.filename:
                filename = self.filename
        except AttributeError:
            if not filename or not os.path.isfile():
                self.logger.error("The SARIF cannot be read because no filename was provided or the file does not exist.")
                return
        with open(filename) as file:
            data = json.load(file)
        found_data = []
        
        self.logger.info("Checking for results.")
        for run in data["runs"]:
            for item in run["results"]:
                if ruleIDs and levels:
                    if item["ruleId"] in ruleIDs and item["level"] in levels:
                        found_data.append(item)
                elif ruleIDs:
                    if item["ruleId"] in ruleIDs:
                        found_data.append(item)
                elif levels:
                    if item["level"] in levels:
                        found_data.append(item)
        
        self.logger.info("Completed results search. Returning data.")
        return found_data
    
    def find_rule(self, ruleIDs, filename=None):
        try:
            if not filename and self.filename:
                filename = self.filename
        except AttributeError:
            if not filename or not os.path.isfile():
                self.logger.error("The SARIF cannot be read because no filename was provided or the file does not exist.")
                return
        with open(filename) as file:
            data = json.load(file)
        found_data = []
        
        self.logger.info("Checking for matching rules.")
        for run in data['runs']:
            for rule in run['tool']['driver']['rules']:
                if rule['id'] in ruleIDs:
                    found_data.append(rule)
        
        self.logger.info("Completed rule search. Returning data.")
        return found_data
                        
    def aggregate_results(self, fail_type="one", remove_aggregated=True, filename=None):
        fail_type = fail_type.lower()
        if fail_type not in {"one", "all"}:
            self.logger.error("Invalid fail_type.")
            return
        if remove_aggregated not in {True, False}:
            self.logger.error("Invalid value for remove_aggregated.")
            return
        if filename == None:
            pass
        elif os.path.isfile(filename):
            with open(filename) as file:
                self.sarif = json.load(file)
        else:
            self.logger.error("Unable to read file because it does not exist.")
            return
        
        rules = []
        rule_name = []
        sarif_copy = copy.deepcopy(self.sarif)
        
        for run in self.sarif["runs"]:
            for item in run['tool']['driver']['rules']:
                if item['id'] not in rules:
                    rules.append(item['id'])
                    rule_name.append(item['name'])
        
        for run_index, run in enumerate(sarif_copy["runs"]):
            if run_index:
                self.logger.warning("More than one run exists, but all results will be in run 0.")
            del_count = 0
            for rule_index, rule in enumerate(rules):
                results = 0
                message = ""
                if fail_type == "all":
                    final_result = "error"
                else:
                    final_result = "note"
                result_strings = []
                for index, item in enumerate(run["results"]):
                    if item["ruleId"] == rule:
                        results += 1
                        if fail_type == "one" and item["level"] == "error":
                            message = item["message"]["id"]
                            final_result = "error" 
                        elif fail_type == "all" and item["level"] == "note":
                            message = item["message"]["id"]
                            final_result = "note"
                        
                        if fail_type == "one" and message == "" and item["level"] == "note":
                            message = item["message"]["id"]
                        elif fail_type == "all" and message == "" and item["level"] == "error":
                            message = item["message"]["id"]
                            
                        result_strings.append(item["message"]["id"].format(*item["message"]["arguments"]))
                        true_index = index
                        if remove_aggregated:
                            index -= del_count
                            del self.sarif["runs"][run_index]["results"][index]
                            del_count += 1
                        
                if results >= 2:
                    if final_result == 'note':
                        result_txt = "aggregated result: note \n{0}"
                        complete_result = ['\n'.join(result_strings)]
                    else:
                        complete_result = result_strings
                        result_txt = '\n'.join(f"id{i + 1}\n{{{i}}}" for i, _ in enumerate(result_strings))
                    self.logger.info(f"More than two results have been found for rule {rule}, meaning a new rule for aggregating the results will be added.")
                    self.add_rule(f"Aggregated {rule_name[rule_index]}", f"aggregated-{rule}", f"Aggregated results for rule {rule}.", 
                                  "To make SARIF files more concise, rules can be aggregated and given a final result. That is what this rule is for.", 
                                  {
                                      "note": {
                                          "text": result_txt
                                      },
                                      "error": {
                                          "text": result_txt
                                      }
                                  })  
                    self.add_result(f"aggregated-{rule}", final_result, result_txt, complete_result)
                    self.logger.info("Aggregated result added.")
                elif results == 1:
                    self.logger.info(f"Only one result was found for rule {rule}, meaning no new rule will be added.")
                    self.sarif["runs"][0]["results"].append(run['results'][true_index])
                    
        self.logger.info("SARIF result aggregation complete.")
        
    def verify_sarif(self, filename=None):
        if filename == None:
            pass
        elif os.path.isfile(filename):
            with open(filename) as file:
                self.sarif = json.load(file)
        try:
            self.logger.info("Getting $schema file.")
            url = self.sarif["$schema"]
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
                schema = json.loads(data)
        except urllib.error.URLError as e:
            self.logger.warning(f"Error fetching SARIF schema from {url}: {e}")
            return True
        except KeyError:
            self.logger.warning("Unable to download schema because $schema key does not exist.")
            return True
        
        try:
            self.logger.info("Validating SARIF file against schema.")
            jsonschema.validate(instance=self.sarif, schema=schema)
            self.logger.info("SARIF verification passed.")
        except jsonschema.exceptions.ValidationError as e:
            self.logger.error(f"SARIF validation failed: {e}")
            return False

        return True

        
        
# Examples:
# s = Sarif()
# s.add_rule("SourceVersionControlled", "GGS001","The code must be version-controlled.", "Every change to the source is tracked in a version control system that meets the following requirements:\n\n[Change history] There exists a record of the history of changes that went into the revision. Each change must contain: the identities of the uploader and reviewers (if any), timestamps of the reviews (if any) and submission, the change description/justification, the content of the change, and the parent revisions.\n\n[Immutable reference] There exists a way to indefinitely reference this particular, immutable revision. In git, this is the {repo URL + branch/tag/ref + commit ID}.\n\nMost popular version control system meet this requirement, such as git, Mercurial, Subversion, or Perforce.\n\nNOTE: This does NOT require that the code, uploader/reviewer identities, or change history be made public. Rather, some organization must attest to the fact that these requirements are met, and it is up to the consumer whether this attestation is sufficient.",
#     {
#         "pass": {
#             "text": "The code is version-controlled in {0}."
#         }
#     })

# s.add_result("GGS001", "note", "pass", ["Hey"])

# j = s.get_sarif()

# s.save("test.sarif")
            
# TODO: Add support for location object in result