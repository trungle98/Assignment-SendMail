import json, pandas as pd
import os.path
import time
import sys
sys.path.insert(0, '../logger')
from Logger import Logger
from DateTimeService import DateTimeService
class IOService:
    def __init__(self):
        print('')
    # save list emails was sent
    def save_sent_email(self, list_sent, output_path):
        try:
            file_name = "output"
            if output_path[-1] != "\\":
                output_path = output_path+"\\"+file_name
            else:
                output_path = output_path+file_name
            output_exist = self.check_file_exist(output_path+".json")
            if output_exist:
                curr_time = DateTimeService.get_current_date_time(self,"%x-%X")
                output_path = output_path+"-"+str(curr_time).replace("/",'-').replace(":","-")
                with open("{}.json".format(output_path), "w") as outfile:
                    json.dump(list_sent, outfile)
            else:
                 with open("{}.json".format(output_path), "w") as outfile:
                    json.dump(list_sent, outfile)   
                    
        except IOError as ex:
            print(ex)
            Logger.log().error(ex)


    #save list email was not sent
    def save_not_sent_email(self, list_not_sent, error_path):
        try:
            output_exist = self.check_file_exist(error_path)
            if output_exist:
                error_file = pd.DataFrame(list_not_sent)
                error_file.to_csv("%s"%error_path, sep='\t',encoding='utf-8', mode='a', header=False, index=False)
            else:
                error_file = pd.DataFrame(list_not_sent, columns=["TITLE", "FIRST_NAME", "LAST_NAME", "EMAIL"])
                error_file.to_csv("%s"%error_path, sep='\t',encoding='utf-8', mode='w', index=False)
        except Exception as ex:
            print(ex)
            Logger.log().error(ex)
    def read_json(self, json_file):
        try:
            df = pd.read_json(json_file, orient="index")
            return df
        except Exception as ex:
            print(ex)
            Logger.log().error(ex)
    def check_file_exist(self, file_name):
        if os.path.isfile(file_name):
            return True
        else:
            return False