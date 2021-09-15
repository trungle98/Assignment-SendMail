import pandas as pd, datetime
from IOService import IOService
import sys
sys.path.insert(0, '../logger')
from Logger import Logger
from DateTimeService import DateTimeService
import smtplib
from validate_email import validate_email
import progressbar

class MailService:

    # we can init MailService with custom params
    def __init__(self, cfg_dict, contact_file, email_template):
        self.contact_file = contact_file
        self.email_template = email_template
        self.cfg_dict = cfg_dict

    # Gen email body
    def gen_email_body(self, template_body, input_contact):
        title = str(input_contact["TITLE"])
        first_name = str(input_contact["FIRST_NAME"])
        last_name = str(input_contact["LAST_NAME"])
        if title == "nan":
            title = "Mrs/Ms"
        if first_name == "nan":
            first_name = ""
        if last_name == "nan":
            last_name = ""

        generated_email = (
            template_body.replace("{{TITLE}}", title)
            .replace("{{FIRST_NAME}}", first_name)
            .replace("{{LAST_NAME}}", last_name)
            .replace("{{TODAY}}", DateTimeService.get_current_date_time(self, ""))
        )
        return generated_email

    # In real-world, to save mail's fee when send a large email, we have to check an email already exist or not
    def verify_email(self, sender, recipt, smtp_server):
        is_valid = validate_email(email_address=recipt)
        return is_valid

    # Send email
    def send_email(self, done_output_path, error_output_path):
        listError = []
        listDone = []
        num_progress = 0
        worker = IOService()
        msg_template = worker.read_json(self.email_template)
        email_target = pd.read_csv(self.contact_file)
        bar = self.display_status(len(email_target))
        for index, row in email_target.iterrows():
            try:
                if str(row["EMAIL"]) != "nan":
                    listDone.append(
                        {
                            "from": msg_template[0]["from"],
                            "to": row["EMAIL"],
                            "subject": msg_template[0]["subject"],
                            "mimeType": msg_template[0]["mimeType"],
                            "body": self.gen_email_body(msg_template[0]["body"], row),
                        }
                    )
                else:
                    listError.append(row)
            except Exception as ex:
                Logger.error_log(ex)
            num_progress += 1
            self.update_progress(bar, num_progress)
        bar.finish()
        worker.save_sent_email(listDone, done_output_path)
        worker.save_not_sent_email(listError, error_output_path)

        return {"done": len(listDone), "error": len(listError)}

    # Send large email: if we have to send a large email, we can using this function to reduce memory usage when load contacts file.
    def send_large_email(self, done_output_path, error_output_path, number_of_chunk):
        listError = []
        listDone = []
        worker = IOService()
        msg_template = worker.read_json(self.email_template)
        email_target = pd.read_csv(self.contact_file, chunksize=number_of_chunk)
        for chunk in email_target:
            for index, row in chunk.iterrows():
                try:
                    if str(row["EMAIL"]) != "nan":
                        listDone.append(
                            {
                                "from": msg_template[0]["from"],
                                "to": row["EMAIL"],
                                "subject": msg_template[0]["subject"],
                                "mimeType": msg_template[0]["mimeType"],
                                "body": self.gen_email_body(
                                    msg_template[0]["body"], row
                                ),
                            }
                        )
                    else:
                        listError.append(row)
                except Exception as ex:
                    Logger.error_log(ex)
        worker.save_sent_email(listDone, done_output_path)
        worker.save_not_sent_email(listError, error_output_path)

        return {"done": len(listDone), "error": len(listError)}

    def smtp_email(self, msg, sender, recipt, server):

        user = self.cfg_dict["sender_email"]

        pwd = self.cfg_dict["sender_password"]

        # check service have to send email already exist

        if self.verify_email(user, recipt, server):
            try:
                server.ehlo()
                server.starttls()
                server.login(user, pwd)
                server.sendmail(sender, recipt, msg)
                server.close()
                return True
            except Exception as ex:
                print(ex)
                Logger.log().error(ex)
                return False
        return False

    # Send email
    def send_smtp_email(self, done_output_path, error_output_path):
        listError = []
        listDone = []
        worker = IOService()
        num_progress = 0
        msg_template = worker.read_json(self.email_template)
        email_target = pd.read_csv(self.contact_file)
        smtp_server = self.cfg_dict["smtp_server"]
        smtp_port = self.cfg_dict["smtp_port"]
        server = smtplib.SMTP(smtp_server, smtp_port)
        bar = self.display_status(len(email_target))
        for index, row in email_target.iterrows():
            try:
                if str(row["EMAIL"]) != "nan":
                    subject = "subject: {}".format(msg_template[0]["subject"])
                    body = self.gen_email_body(msg_template[0]["body"], row)
                    message = subject + body
                    sender = self.cfg_dict["sender_email"]
                    recipt = row["EMAIL"]
                    is_sent = self.smtp_email(message, sender, recipt, server)
                    if is_sent:
                        listDone.append(
                            {
                                "from": msg_template[0]["from"],
                                "to": row["EMAIL"],
                                "subject": msg_template[0]["subject"],
                                "mimeType": msg_template[0]["mimeType"],
                                "body": self.gen_email_body(
                                    msg_template[0]["body"], row
                                ),
                            }
                        )
                    else:
                        listError.append(row)
                else:
                    listError.append(row)
            except Exception as ex:
                print(ex)
                Logger.error_log(ex)
            num_progress += 1
            self.update_progress(bar, num_progress)
        bar.finish()
        server.close()
        worker.save_sent_email(listDone, done_output_path)
        worker.save_not_sent_email(listError, error_output_path)
        
        return {"done": len(listDone), "error": len(listError)}
    def display_status(self, max_val):
        bar = progressbar.ProgressBar(maxval=max_val, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        return bar
    def update_progress(self, bar, num):
        bar.update(num)