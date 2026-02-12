import smtplib, os
from dotenv import load_dotenv
import data_manager

load_dotenv()
getting_data_obj = data_manager.SheetyDataManager()
client_emails = getting_data_obj.get_client_emails()


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.my_email = os.getenv("GMAIL_APP_MAIL")
        self.my_password = os.getenv("GMAIL_APP_PASSWORD")

    ## to myself only
    # def sending_mail(self, body):
    #     with smtplib.SMTP("smtp.gmail.com") as my_connection:
    #         my_connection.starttls()
    #         my_connection.login(user=self.my_email, password=self.my_password)
    #         my_connection.sendmail(
    #             from_addr=self.my_email,
    #             to_addrs=self.my_email,
    #             msg=f"Subject: Super hot flight deals!\n\n{body}",
    #         )
    def sending_mail(self, body):
        with smtplib.SMTP("smtp.gmail.com") as my_connection:
            my_connection.starttls()
            my_connection.login(user=self.my_email, password=self.my_password)
            for client_email in client_emails:
                my_connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=client_email,
                    msg=f"Subject: Super hot flight deals!\n\n{body}",
                )
