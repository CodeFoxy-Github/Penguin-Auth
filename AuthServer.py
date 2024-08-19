import os
import random
import smtplib
from email.mime.text import MIMEText
from flask import Flask, session, redirect, request, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

# Environment setup
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(24)
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# OAuth setup
oauth = OAuth(app)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid email profile'}
)

user_info = {}

@app.route('/info', methods=['GET', 'POST'])
def zz():
    global user_info
    a = user_info
    user_info = {}
    return jsonify(a)

@app.route('/logingoogle')
def login():
    nonce = str(random.randint(100000, 999999))
    session['nonce'] = nonce
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authgoogle')
def auth():
    global user_info
    token = oauth.google.authorize_access_token()
    nonce = session.pop('nonce', None)
    user_info = oauth.google.parse_id_token(token, nonce=nonce)
    return "<script>window.open('', '_self').close();</script>"

@app.route("/email")
def send_email_verify_code():  # Removed unused code argument
    global rnd
    rnd = random.randint(100000, 999999)
    htmlexample = "<html lang=\"\" dir=\"ltr\"> <head>     <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">     <meta name=\"viewport\" content=\"width=100%, initial-scale=1, user-scalable=yes\">     <meta name=\"format-detection\" content=\"telephone=no, date=no, address=no, email=no, url=no\">     <meta name=\"x-apple-disable-message-reformatting\">     <style type=\"text/css\">         /* MEDIA QUERIES */         @media all and (max-width:639px){             .wrapper{ width:100%!important; }             .container{ width:100%!important; min-width:100%!important; padding: 0 !important; }             .row{padding-left: 20px!important; padding-right: 20px!important;}             .col-mobile {width: 20px!important;}             .col{display: block!important; width: 100%!important;}             .mobile-center{text-align: center!important; float: none!important;}             .mobile-mx-auto {margin: 0 auto!important; float: none!important;}             .img{ width:100% !important; height:auto !important; }             .ml-btn { width: 100% !important; max-width: 100%!important;}             .ml-btn-container { width: 100% !important; max-width: 100%!important;}             *[class=\"mobileOff\"] { width: 0px !important; display: none !important; }             *[class*=\"mobileOn\"] { display: block !important; max-height:none !important; }             .mlContentTable{ width: 100%!important; min-width: 10%!important; margin: 0!important; float: none!important; }             .mlContentButton a { display: block!important; width: auto!important; }             .mlContentOuter { padding-bottom: 0px!important; padding-left: 15px!important; padding-right: 15px!important; padding-top: 0px!important; }             .mlContentSurvey { float: none!important; margin-bottom: 10px!important; width:100%!important; }             .multiple-choice-item-table { width: 100% !important; margin-bottom: 20px !important; min-width: 10% !important; float: none !important; }         }     </style>     <style>         /* RESET STYLES */         html, body, .document { margin: 0 !important; padding: 0 !important; width: 100% !important; height: 100% !important; }         body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; text-rendering: optimizeLegibility;}         img { border: 0; outline: none; text-decoration: none;  -ms-interpolation-mode: bicubic; }         table { border-collapse: collapse; }         table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }         body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }         h1, h2, h3, h4, h5, p { margin:0;}         /* iOS BLUE LINKS */         a[x-apple-data-detectors] {             color: inherit !important;             text-decoration: none !important;             font-size: inherit !important;             font-family: inherit !important;             font-weight: inherit !important;             line-height: inherit !important;         }         /* ANDROID CENTER FIX */         div[style*=\"margin: 16px 0;\"] { margin: 0 !important; }          /* Carousel style */         @media screen and (-webkit-min-device-pixel-ratio: 0) {             .webkit {                 display: block !important;             }         }           @media screen and (-webkit-min-device-pixel-ratio: 0) {             .non-webkit {                 display: none !important;             }         }           @media screen and (-webkit-min-device-pixel-ratio: 0) {             /* TARGET OUTLOOK.COM */             [class=\"x_non-webkit\"] {                 display: block !important;             }         }           @media screen and (-webkit-min-device-pixel-ratio: 0) {             [class=\"x_webkit\"] {                 display: none !important;             }         }     </style>     <style type=\"text/css\">@import url(\"https://assets.mlcdn.com/fonts-v2.css?version=1722844\");</style>     <style type=\"text/css\">         @media screen {             body {                 font-family: Arial, Helvetica, sans-serif;             }         }     </style>     <link rel=\"stylesheet\" href=\"https://unpkg.com/mdui@3/mdui.css\">     <script>         function copyToClipboard() {             const code = document.getElementById(\"verification-code\").innerText;             navigator.clipboard.writeText(code).then(() => {                 alert(\"Verification code copied to clipboard!\");             }).catch(err => {                 console.log(\"Failed to copy: \", err);             });         }     </script> </head> <body style=\"margin: 0 !important; padding: 0 !important; background-color:#f6f6f6;\">     <div class=\"document\" role=\"article\" aria-roledescription=\"email\" aria-label=\"\" lang=\"\" dir=\"ltr\" style=\"background-color:#f6f6f6; line-height: 100%; font-size:medium; font-size:max(16px, 1rem); display: flex; justify-content: center; align-items: center; height: 100vh;\">         <table width=\"100%\" align=\"center\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\">             <tr>                 <td background=\"\" align=\"center\" valign=\"top\">                     <table class=\"wrapper\" align=\"center\" width=\"640\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"max-width: 640px; border-radius: 10px; overflow: hidden; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);\">                         <tr>                             <td align=\"center\">                                 <table class=\"ml-default\" width=\"100%\" bgcolor=\"\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">                                     <tr>                                         <td style=\"\">                                             <table class=\"container ml-4 ml-default-border\" width=\"640\" bgcolor=\"#ffffff\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"color: #000000; width: 640px; min-width: 640px;\">                                                 <tr>                                                     <td class=\"ml-default-border container\" height=\"20\" style=\"line-height: 20px; min-width: 640px;\"></td>                                                 </tr>                                                 <tr>                                                     <td class=\"row\" style=\"padding: 0 50px;\">                                                         <h1 style=\"font-family: Arial, Helvetica, sans-serif; color: #000000; font-size: 24px; line-height: 125%; font-weight: bold; text-decoration: none; margin-bottom: 0;\"><strong>Penguin Auth</strong></h1>                                                         <p style=\"font-family: Arial, Helvetica, sans-serif; color: #6B6B6B; font-size: 14px; line-height: 125%; margin-top: 10px;\">Thank you for choosing Penguin Auth. We are committed to keeping your account secure and ensuring that you have the best experience possible.</p>                                                     </td>                                                 </tr>                                                 <tr>                                                     <td height=\"20\" style=\"line-height: 20px;\"></td>                                                 </tr>                                             </table>                                             <table class=\"container ml-6 ml-default-border\" width=\"640\" bgcolor=\"#ffffff\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"color: #000000; width: 640px; min-width: 640px;\">                                                 <tr>                                                     <td class=\"ml-default-border container\" height=\"10\" style=\"line-height: 10px; min-width: 640px;\"></td>                                                 </tr>                                                 <tr>                                                     <td class=\"row\" style=\"padding: 0 50px;\">                                                         <h3 style=\"font-family: Arial, Helvetica, sans-serif; color: #000000; font-size: 16px; line-height: 125%; font-weight: bold; text-decoration: none; margin-bottom: 0;\"><strong>Your Verification Code</strong></h3>                                                         <p id=\"verification-code\" style=\"font-family: Arial, Helvetica, sans-serif; color: #000000; font-size: 24px; line-height: 125%; margin-top: 10px; font-weight: bold;\">{CODEFR}</p> <!-- Replace with dynamic code -->                                                     </td>                                                 </tr>                                                 <tr>                                                     <td height=\"20\" style=\"line-height: 20px;\"></td>                                                 </tr>                                             </table>                                             <table class=\"container ml-8 ml-default-border\" width=\"640\" bgcolor=\"#ffffff\" align=\"center\" border=\"0\" cellspacing=\"0\"                                             <table class=\"container ml-8 ml-default-border\" width=\"640\" bgcolor=\"#ffffff\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"color: #000000; width: 640px; min-width: 640px;\">                                                 <tr>                                                     <td class=\"ml-default-border container\" height=\"20\" style=\"line-height: 20px; min-width: 640px;\"></td>                                                 </tr>                                                 <tr>                                                     <td class=\"row\" style=\"padding: 0 50px;\">                                                         <button onclick=\"copyToClipboard()\" style=\"font-family: Arial, Helvetica, sans-serif; background-color: #007bff; color: #ffffff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold;\">Copy Code</button>                                                     </td>                                                 </tr>                                                 <tr>                                                     <td class=\"ml-default-border container\" height=\"40\" style=\"line-height: 40px;\"></td>                                                 </tr>                                             </table>                                             <table class=\"container ml-10 ml-default-border\" width=\"640\" bgcolor=\"#ffffff\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"color: #000000; width: 640px; min-width: 640px;\">                                                 <tr>                                                     <td class=\"ml-default-border container\" height=\"20\" style=\"line-height: 20px; min-width: 640px;\"></td>                                                 </tr>                                                 <tr>                                                     <td class=\"row\" style=\"padding: 0 50px;\">                                                         <p style=\"font-family: Arial, Helvetica, sans-serif; color: #6B6B6B; font-size: 14px; line-height: 125%; margin-top: 10px;\">If you didn\'t request this code, please ignore this email or delete it.</p>                                                         <p style=\"font-family: Arial, Helvetica, sans-serif; color: #6B6B6B; font-size: 14px; line-height: 125%; margin-top: 10px;\">And if you keep receiving this email, please report it to abuse@codefoxy.link</p>                                                     </td>                                                 </tr>                                                 <tr>                                                     <td height=\"20\" style=\"line-height: 20px;\"></td>                                                 </tr>                                             </table>                                         </td>                                     </tr>                                     <tr>                                         <td class=\"ml-default-border container\" height=\"40\" style=\"line-height: 40px;\"></td>                                     </tr>                                 </table>                             </td>                         </tr>                     </table>                 </td>             </tr>         </table>     </div> </body> </html>"
    # receivers = f"'{request.args.get('email')}'"#i need to get the email using url parameters"
    msg = MIMEText(htmlexample.replace("{CODEFR}", str(rnd)), 'html', 'us-ascii')
    msg['Subject'] = 'Verify Your Email'
    msg['From'] = 'verify@codefoxy.link'
    msg['To'] = request.args.get('email')
    try:
      smtp = smtplib.SMTP('mail.smtp2go.com', 2525)
      smtp.ehlo()
      smtp.starttls()
      smtp.login("penguinverify", os.getenv('Auth_Password_SMTP'))
      status = smtp.send_message(msg)    # 改成 send_message
      if status == {}:  #     receivers = request.args.get('email')
        print('Yipee')
        return 'Success'
      else:
        print('Awww')
        return 'Failure'
    except Exception as e:
      print(e)
      return 'Failure'
    finally:
      smtp.quit()

@app.route("/check")
def check():
  return str(str(request.args.get("code")) == str(rnd))


if __name__ == "__main__":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
