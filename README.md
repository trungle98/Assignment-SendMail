
# Assignment Send mail application

The python mail sender gives simplified console application for simulate sending email service in real world. In this case, the application support python 3, please install requirements.txt to install all required libs

  

## Feature

* Read input as a command line: contact file (csv) and template (json), path_to_error_file, path_to_success_file

* Send email by template and contact input

* All email was sent and was not send to path was given

  

## Sending simple mail
### Using docker
`docker pull trunglqtcs19033/assignment-send-mail:assignment-send-mail`

`docker run -it 7e4a13e5f55d`

### Run project:
cd to project folder

`cd /Assignment/api/`

then run

` python3 MailAPI.py -c path_to_contacts_file.csv -t path_to_template_email.json -o path_to_output_success -e path_to_error_file `

* Path_to_contacts_file and path_to_template_email are required, path_to_output_success, path_to_error_file if not given, default is empty, so output of success and error file is in root project folder.
* Sample cmd

`python3 MailAPI.py -t /Assignment/sample_resources/email_template.json -c /Assignment/sample_resources/contacts_file.csv -o /Assignment/output/ -e /Assignment/output/error.csv`

* Sample input

Contact file:

TITLE| FIRST_NAME| LAST_NAME| EMAIL
---|---|---|---|
MR| Trung| Le| tests@gmail.com

Template file:

```json
{

"from": "The Marketing Team<marketing@example.com>",

"subject": "A new product is being launched soon...",

"mimeType": "text/plain",

"body": "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}, \nToday, {{TODAY}}, we would like to tell you that... \nSincerely,\nThe Marketing Team "

}
```
* Sample output
Error file:

TITLE| FIRST_NAME| LAST_NAME| EMAIL
---|---|---|---|
MR| Trung| Le| 

Output email:
```json
[
{

"from": "The Marketing Team<marketing@example.com>",

"to": "tests@gmail.com",

"subject": "A new product is being launched soon...",

"mimeType": "text/plain",

"body": "Hi MR Trung Le, \nToday, 14 Sep 2021, we would like to tell you that... \nSincerely,\nThe Marketing Team "

},

{

"from": "The Marketing Team<marketing@example.com>",

"to": "tru3@fpt.edu.vn",

"subject": "A new product is being launched soon...",

"mimeType": "text/plain",

"body": "Hi MR Quang Le, \nToday, 14 Sep 2021, we would like to tell you that... \nSincerely,\nThe Marketing Team "

}
]
```
## Project structure
```

```python
Assignment
├── api
│   └── MailAPI.py
│── services
|   └── DateTimeService.py
|   └── IOService.py
|   └── MailService.py
└── logger
    └── Logger.py
```

## Classes and Methods

*  **Class IOService**

><p> Provide some methods to read and write file </p>

*  **Class DateTimeService**
` get_current_date_time(self, type)`

>This method return a custom type of date-time, default type is "%d %b %Y" (ex: 14 Sep 2021)
* **Class Logger**

> <p>  Provide some method to write log, log file will be save to root folder of project </p>

* **Class MailService**

`__init__(self, sender_email, sender_password, contact_file, email_template)`

>This method init MailService object, which have 4 inputs: sender_email, sender_password: email and password of sender, contact_file: a csv file, its format in section above
>If email is empty, this contact will be save to error file, else it will be save to success file





`verify_email(self, sender, recipt, server)`

>This method is created to verify this email is already exist or not and the email format is correct or not, to minimize sending cost in real-world, in this scope of project, it not be used cause we need to check the email field empty or not.

`gen_email_body(self, template_body, input_contact)`

>Then body of email. by matching contact info with template, include: title, first name, last name and sending date.

`send_email(self, done_output_path, error_output_path)`

>Read email template and contact file to send email. All error and success mail will be save to your given folder location.
>This return an dictionary 
```json
{
"done": number_of_email_was_sent,
"error": number_of_email_was_not_sent
}
```
`send_large_email(self, done_output_path, error_output_path, number_of_chunk)`
> Reduce memory usages when input contact is very large by using pandas chunk
`send_smtp_email(self, done_output_path, error_output_path)`
> Using to send email via smtp by reading from config in MailAPI.py
> Your email have to enable less secure (link: [https://www.google.com/settings/security/lesssecureapps) to send email using smtp (gmail)

* **Class MailAPI**

`get_args(**kwargs)`

>Receive cmd args as an input and return it as a dictionary

` main`

>Call MailServie with the return of method get_args() as an input Assignment Send mail application
>The python mail sender gives simplified console application for simulate sending email service in real world. In this case, the application support python 3, please install requirements.txt to install all require libs
>**By using dictionary as an input of send_smtp_email(), we can custom anything we need to send email via any mail server, for instance:**
```python
#enter your email, password as sender email
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
#init MailService with dictionary as a input param to customize send mail
mail_service = MailService(cfg_dict, cfg['contacts_file'], cfg['email_template'])
```


  