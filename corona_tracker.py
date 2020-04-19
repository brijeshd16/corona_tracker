import requests, json
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

RAW_DATA = "https://api.covid19india.org/raw_data.json"
DAILY_DATA = "https://api.covid19india.org/data.json"
STATE_DATA = "https://api.covid19india.org/v2/state_district_wise.json"
# request = requests.get(DAILY_DATA)

# with open("daily_data.json", "wb") as file:
#     file.write(request.content)


def daily():
    try:
        day = datetime.now().day - 1
        month = datetime.now().strftime("%B")
        req = requests.get(DAILY_DATA)
        if req.status_code != 200:
            data = json.dumps({"error": "failed to call the API", "status": "failure"})
            print("Status code for API " + str(req.status_code) + "")
            return data
        else:
            data = req.json()
            for doc in data["cases_time_series"]:
                if doc["date"] == f"{day} {month} ":
                    daily = doc
            for doc in data["statewise"]:
                if doc["state"] == "Total":
                    total = doc
                if doc["state"] == "Maharashtra":
                    mh = doc
            # print(data["statewise"][0]["state"])
            send_mail(total, mh, daily)
    except Exception as e:
        print(e)


def get_detail():
    req = requests.get(RAW_DATA)
    if req.status_code != 200:
        data = json.dumps({"error": "failed to call the API", "status": "failure"})
        print("Status code for API " + str(req.status_code) + "")
        return data
    else:
        data = req.json()
        for doc in data["raw_data"]:
            if doc["detectedcity"] == "Vasai-Virar":
                vasai_virar = json.dumps(doc)
                return vasai_virar


def send_mail(total, mh, daily):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        recipients = [
            "djboy.rok@gmail.com",
            "sarveshdubey151@gmail.com",
            "djboy.roks@gmail.com",
        ]

        me = "brijeshd16@gmail.com"
        # you = "djboy.rok@gmail.com; sarveshdubey151@gmail.com; djboy.roks@gmail.com"
        me_pwd = "ygqjmelhnhrtsqzi"

        server.login(me, me_pwd)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "[CORONA] Daily update !! "
        msg["From"] = me
        msg["To"] = ", ".join(recipients)

        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = f"""\
        <html>

        <head></head>

        <body>
            <p>Hello ,</p>
            <p>Hope you are doing fine.</p>
            <h3>Here are today's stat on Corona :</h3>
            <table style="float: left" border="1">
                <tbody>
                    <tr>
                        <td>&nbsp;</td>
                        <td><strong>Total &nbsp;&nbsp;</strong></td>
                        <td><strong>Maharashtra</strong></td>
                        <td><strong>Daily Count</strong></td>
                    </tr>
                    <tr>
                        <td><strong>Total cases</strong></td>
                        <td>{total['confirmed']}</td>
                        <td>{mh['confirmed']}</td>
                        <td>{daily['dailyconfirmed']}</td>
                    </tr>
                    <tr>
                        <td><strong>Active cases</strong></td>
                        <td>{total['active']}</td>
                        <td>{mh['active']}</td>
                        <td>{daily['dailyconfirmed']}</td>
                    </tr>
                    <tr>
                        <td><strong>Total death</strong></td>
                        <td>{total['deaths']}</td>
                        <td>{mh['deaths']}</td>
                        <td>{daily['dailydeceased']}</td>
                    </tr>
                    <tr>
                        <td><strong>Recovered</strong></td>
                        <td>{total['recovered']}</td>
                        <td>{mh['recovered']}</td>
                        <td>{daily['dailyrecovered']}</td>
                    </tr>
                </tbody>
            </table>

            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>

            <p>Regards,</p>
            <p>Brijesh Dubey</p>
            <h4>Note : these stats are as on : "{daily['date']} 2020"</h4>

            <br>
            <br>
            <br>

            <p>&nbsp;</p>
            <p>&nbsp;</p>

        </body>

        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(me, recipients, msg.as_string())

        # server.login("brijeshd16@gmail.com", "ygqjmelhnhrtsqzi")

        # subject = "[CORONA] Daily update !! "
        # body = f"""<h1>Today's update </h1>
        # Total Cases : {total['confirmed']}
        # Active Cases : {total['active']}
        # """
        # msg = f"Subject: {subject}\n\n{body}"
        # server.sendmail("brijeshd16@gmail.com", "djboy.rok@gmail.com", msg)
        print("Mail sent successfully !")
    except Exception as e:
        print(e)
    finally:
        server.quit()


daily()
