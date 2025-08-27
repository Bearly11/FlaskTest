from app import app
from flask import render_template, request, redirect, url_for, jsonify
from flask_mail import Mail, Message
from datetime import date
from noti_to_tel import send_message
import json
import re

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'forjx2m@gmail.com'
app.config['MAIL_PASSWORD'] = 'fgpy zhrp gniv cbqx'
app.config['MAIL_DEFAULT_SENDER'] = 'forjx2m@gmail.com'

mail = Mail(app)


@app.route('/send', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get("email", "").strip()

        if not EMAIL_RE.match(email):
            return jsonify(ok=False, error='bad_email', message='Please enter a valid email.'), 400
        phone = request.form.get('phone')
        address = request.form.get('address')
        cart_data = json.loads(request.form.get('cart_data') or '[]')
        total = request.form.get('total')

        msg = Message(
            subject=f"Hi {name}, Your Invoice!",
            recipients=[email],
        )

        rows = "".join(
            f"""
            <tr>
                <td>{item['title']}</td>
                <td align="right">{item['quantity']}</td>
                <td align="right">${float(item['price']):.2f}</td>
                <td align="right">${float(item['total']):.2f}</td>
            </tr>
            """
            for item in cart_data
        )

        msg.html = f"""
        <h2>Invoice for {name}</h2>
        <p>Email: {email}</p>
        <p>Address: {address}</p>
        <p>Phone Number: {phone}</p>
        <p>Date: {date.today()}</p>
        <table border="1" cellpadding="8" cellspacing="0" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th align="left">Item</th>
                    <th align="right">Qty</th>
                    <th align="right">Price</th>
                    <th align="right">Total</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <p style="margin-top:20px;"><strong>Grand Total: ${total}</strong></p>
        <p>Thanks for your purchase!</p>
        """
        msg.body = msg.html  # optional: plain text fallback

        mail.send(msg)

        telegram_text = f"""🧾 *Invoice #{date.today().strftime('%Y%m%d')}*
👤 {name}
📧 {email}
📅 {date.today()}
🏷️ Order Summary:
{'=' * 32}
""" + "\n".join(
            f"{i}. {item['title']}  x{item['quantity']} = ${float(item['total']):.2f}"
            for i, item in enumerate(cart_data, 1)
        ) + f"\n{'=' * 32}\n💰 *Total: ${total}*"

        send_message(telegram_text)

        # After POST, redirect to avoid form resubmission
        return redirect(url_for('send_email'))

    return render_template('email.html')
