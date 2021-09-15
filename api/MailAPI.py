import sys
sys.path.insert(0, '../logger')
sys.path.insert(0, '../services')
import argparse
from Logger import Logger
from MailServices import MailService


class MailAPI:
    def __init__(self):
        Logger.log().info("init MailAPI")

    

    def get_args(**kwargs):
        cfg = kwargs
        parser = argparse.ArgumentParser(description='Send email and record them',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-t', '--email-template', metavar='email_template', type=str, nargs='?', default='',
                            help='email template', dest='email_template')
        parser.add_argument('-c', '--contact-file', metavar='contacts_file', type=str, nargs='?', default='',
                            help='email contacts', dest='contacts_file')
        parser.add_argument('-o', '--output-done', metavar='output_done', type=str, nargs='?', default='done.json',
                            help='output done', dest='output_done')
        parser.add_argument('-e', '--output-error', metavar='output_error', type=str, nargs='?', default='error.csv',
                            help='output error', dest='output_error')
        args = vars(parser.parse_args())

        # for k in args.keys():
        #     cfg[k] = args.get(k)
        cfg.update(args)

        return dict(cfg)
    if __name__ == '__main__':
        cfg = get_args()
        sender_email = "examples@gmail.com"
        sender_password = "Poozal1998"
        smtp_server ="smtp.gmail.com"
        smtp_port = 587
        #We can using cfg_dict to set smtp and port when using smtp
        cfg_dict ={
            "sender_email":sender_email,
            "sender_password": sender_password,
            "smtp_server": smtp_server,
            "smtp_port":smtp_port
           
        }
        mail_service = MailService(cfg_dict, cfg['contacts_file'],  cfg['email_template'])
        result = mail_service.send_email(cfg['output_done'],cfg['output_error'])
        print('Done, total mail was sent: {}, total mail was not sent {}'.format(result['done'], result['error']))
