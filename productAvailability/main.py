import smtplib
import time
import schedule
from lxml import html
import requests
from time import sleep
from email.mime.text import MIMEText

sender_email = "***"
email_password = "***"
to_email = "***"
product_url = "https://aax-us-iad.amazon.com/x/c/JAhTdT8hr5CQGz8BNuwd8I0AAAGRnmjLhQEAAAH0AQBvbm9fdHhuX2JpZDEgICBvbm9fdHhuX2ltcDEgICCsYeW6/http://www.amazon.com/dp/B0CTQQ65QP/ref=syn_sd_onsite_desktop_0?ie=UTF8&psc=1&pf_rd_p=d77a94d7-221a-4129-af34-3c16ad136bb7&pf_rd_r=TRWWEHZYCC70S20S3266&pd_rd_wg=jUs9X&pd_rd_w=Neq1S&pd_rd_r=883578ef-e062-4b19-ac62-985f0a5a25e5&aref=533Fc597bE"
HEADERS = {
    "User-Agent": "***",
    "Accept-Language": "en-US,en;q=0.9"
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def check_product():
    response = requests.get(product_url,headers=HEADERS)    #to send HTTP requests
    doc = html.fromstring(response.content)

    try:
        availability=doc.xpath(
                '//*[@id="availability"]/span/text()'
            )[0].strip()
        print(f"Product availability status: {availability}")

        if "In stock" in availability:
            info_mail()
        else:
            print("Product is not in stock. Will check again later.")

    except IndexError:
            print("Sorry. There might be a network error or Amazon might have blocked the request or the product page structure has changed.")



def info_mail():
    subject = "Your Amazon Product Availability Notification"
    body = f"The product you want to ship is now available. Check it out here : {product_url}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

schedule.every(10).minutes.do(check_product)

if __name__ == "__main__":
    print("Starting Amazon product availability checker...")
    while True:
        schedule.run_pending()
        sleep(1)



