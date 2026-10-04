"""
Realistic Dataset Generator for Scam, Fraud, and Legitimate Communications.
Generates comprehensive text samples (SMS, Email, Chat) and URLs for training and benchmarking.
"""

import random
import pandas as pd

def generate_dataset():
    # 1. SCAM / PHISHING TEMPLATES
    scam_templates = [
        # Banking & KYC
        "Dear {bank} customer, your savings account {acc_num} will be blocked within 24 hours due to uncompleted KYC. Update immediately at {scam_url}",
        "URGENT: Your {bank} netbanking has been suspended today. Verify your PAN card and Aadhaar details to restore access: {scam_url}",
        "{bank} Alert: Unauthorized transaction of Rs {amount} detected on your debit card. If this was not you, cancel immediately at {scam_url}",
        "Attention user: Your {bank} credit card reward points worth Rs {reward_val} are expiring tonight. Redeem cash now: {scam_url}",
        "Dear customer, your bank account is put on hold. Kindly update your mobile number and submit OTP at {scam_url} to unblock.",
        "RBI Notification: KYC verification mandatory for all bank accounts. Failure to update before 10 PM will freeze your account. Link: {scam_url}",
        
        # Electricity & Utility scams
        "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM from the power house because your previous month bill was not updated. Please contact our electricity officer at {phone_num} immediately.",
        "Urgent Notice: Electricity bill of Rs {amount} unpaid. Power supply disconnection order issued. Pay immediately via link {scam_url} or call {phone_num}",
        "Gas supply disconnection warning! Your gas pipeline service will be terminated today. Settle pending dues of Rs {amount} at {scam_url}",

        # Lottery & Fake Prizes
        "Congratulations! Your mobile number has won Rs {prize_val} in KBC Lucky Draw 2026. Send your bank details to claim on WhatsApp: {phone_num}",
        "Dear winner, you have been selected for a free iPhone 15 Pro and Rs 50,000 cash bonus. Click here to claim your gift now: {scam_url}",
        "Google Promotion Award: You have won £750,000 in Google Annual Lottery. Reply with your Name, Age, Country to {scam_email}",
        "Exclusive offer! Claim your Flipkart free gift card worth Rs 10,000 today only. Limited stock: {scam_url}",

        # Fake Job Offers
        "Part-time job offer! Earn Rs 3,000 - 8,000 daily working from home on your phone. Just like and subscribe YouTube videos. Contact HR on WhatsApp: {phone_num}",
        "Amazon Hiring: Earn Rs 45,000/month for simple order review tasks. No experience needed. Immediate joining. Register here: {scam_url}",
        "Work from home opportunity! Earn daily payout in USDT/Crypto. Daily 2 hours task. Contact manager on Telegram: @job_{num}",
        "Congratulations! Selected for Data Entry job at MNC. Daily payout Rs 2,500. Pay registration deposit fee of Rs 499 at {scam_url}",

        # Courier & Parcel delivery scams
        "FedEx Notification: Your parcel #FX-{num} could not be delivered due to incorrect street address. Update your address and pay Rs 45 re-delivery fee: {scam_url}",
        "India Post alert: Your shipment #IN{num} is held at regional customs hub. Update delivery address within 12 hours: {scam_url}",
        "DHL Express: Package delivery on hold due to unpaid duty charges of Rs {amount}. Confirm payment online now: {scam_url}",

        # Tech support & Virus warnings
        "CRITICAL SECURITY ALERT: Your computer is infected with Trojan Spyware. Bank credentials compromised. Call Microsoft Certified Tech at {phone_num} immediately.",
        "Your Apple ID has been locked for security reasons. Confirm your password and credit card immediately at {scam_url} to prevent permanent closure.",
        "Netflix Alert: Your membership subscription could not renew. Account will be terminated today. Update payment info: {scam_url}",

        # Crypto & Investment scams
        "Double your money in 24 hours! Join VIP Crypto Trading group with 100% guaranteed daily returns. Deposit minimum $50 to earn $500. Link: {scam_url}",
        "Stock Market Insider Tips: Guaranteed 500% profit in intraday trades. Zero loss strategy. Join private Telegram group: {scam_url}",

        # Extortion / Blackmail
        "We have hacked your webcam and recorded compromising videos of you. Pay 0.05 BTC ($3,000) within 48 hours to our Bitcoin wallet or we will broadcast to all contacts.",
        "Police Cyber Crime warning: Arrest warrant issued against you for illegal downloads. Pay fine of Rs 5,000 to avoid arrest warrant: {scam_url}"
    ]

    # 2. LEGITIMATE TEMPLATES
    legit_templates = [
        # Banking & Transaction updates
        "Dear customer, INR {amount}.00 debited from account ending in **{acc_last4} on {date} at {merchant}. Available balance is INR {balance}.00. If not done by you, SMS BLOCK to 567676.",
        "Your {bank} credit card statement for ending {acc_last4} is generated. Total amount due: INR {amount}.00, Due date: {date}. View statement on official app.",
        "Dear customer, INR {amount}.00 credited to your account ending **{acc_last4} through NEFT/IMPS on {date}. Ref no {ref_num}.",
        "Your OTP for login to {bank} Internet Banking is {otp_code}. Valid for 5 minutes. NEVER share this code with anyone, including bank staff.",
        "Dear customer, request for cheque book of 25 leaves for account ending **{acc_last4} has been registered successfully. Track status on official portal.",

        # E-Commerce & Deliveries
        "Your Amazon order #{order_id} has been dispatched and will arrive by tomorrow, 8:00 PM. Track your package in the Amazon app.",
        "Swiggy: Your delicious meal from {restaurant} has been delivered. Thank you for ordering with us! Rate your delivery partner.",
        "Zomato: Order confirmed! The chef is preparing your meal at {restaurant}. Estimated delivery in 35 minutes.",
        "Flipkart: Your order #{order_id} containing Wireless Earbuds has been out for delivery. Handover OTP is {otp_code}.",

        # Travel & Utility Bills
        "IRCTC PNR {pnr_num}: Booking confirmed for Train #{train_num}. Coach B4, Berth 42. Charting status will be updated 4 hours before departure.",
        "IndiGo flight 6E-{num} from Delhi to Bengaluru is on schedule. Web check-in opens 48 hours before departure. Check terminal details on official website.",
        "Payment receipt: Your electricity bill payment of INR {amount}.00 was successful on {date}. Biller ref: BBPS-{num}. Thank you.",
        "Airtel recharge of Rs 299 is successful for your number. Unlimited calls + 1.5GB/day valid till {date}. Enjoy Airtel 5G Plus.",

        # College / Academic / Work
        "Reminder: Department seminar on 'Advances in Machine Learning' will be held tomorrow at 11:00 AM in Seminar Hall 2. Attendance is mandatory for 7th semester students.",
        "Notice: The submission deadline for the 4th Year Mini Project synopsis has been extended to Friday, 5:00 PM. Submit files via Google Classroom.",
        "Hi team, please find attached the meeting notes from today's sprint planning. Please review the action items before tomorrow's standup.",
        "Campus Placement Drive: Infosys technical interview shortlist has been uploaded to the placement portal. Selected students report to Lab 3 at 9:00 AM.",
        "Dear Rahul, your library book 'Operating System Concepts' is due for return on {date}. Renew online through the college OPAC catalog.",
        "Meeting Invitation: Weekly project review meeting with Project Guide Dr. Sharma scheduled on Google Meet for Thursday at 3 PM.",

        # Personal / Friends
        "Hey! Are you coming to college today? Let's sit together in the library and work on the project PPT.",
        "Thanks for sharing the notes! The explanation of Naive Bayes and Logistic Regression was really clear.",
        "Hey bro, let me know once you reach home safely. Don't forget to send the dataset CSV file."
    ]

    banks = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Kotak Mahindra Bank", "Bank of Baroda"]
    merchants = ["Amazon India", "Flipkart", "Uber", "Zomato", "Starbucks", "Reliance Retail", "Blinkit", "Apollo Pharmacy"]
    restaurants = ["Domino's Pizza", "Burger King", "Haldiram's", "Subway", "Bikanervala", "Barbeque Nation"]
    
    scam_domains = [
        "http://sbi-netbanking-kyc-verify.xyz",
        "http://hdfc-account-unblock-portal.top",
        "http://update-pan-aadhaar-online.club",
        "http://192.168.1.155/bank/login.php",
        "http://electricity-bill-pay-officer.info",
        "http://fedex-customs-duty-track.buzz",
        "http://indiapost-parcel-reclaim.rest",
        "http://kbc-lottery-winner-cash.tk",
        "http://free-netflix-vip-recharge.work",
        "http://crypto-binance-double-profit.country",
        "http://urgent-verification-notice.link",
        "http://security-appleid-unlock.top/signin",
        "http://tax-refund-gov-credit.xyz/claim"
    ]

    legit_domains = [
        "https://www.onlinesbi.sbi",
        "https://www.hdfcbank.com",
        "https://www.icicibank.com",
        "https://www.amazon.in",
        "https://www.flipkart.com",
        "https://www.irctc.co.in",
        "https://github.com",
        "https://www.google.com",
        "https://en.wikipedia.org",
        "https://www.microsoft.com",
        "https://www.coursera.org"
    ]

    # Ambiguous / Boundary test cases (promotions, genuine urgent notices, conversational alerts)
    ambiguous_legit = [
        "Urgent: Dr. Sharma's lecture has been rescheduled to 2:00 PM today. Please reach Classroom 402 immediately.",
        "Amazon Big Billion Sale! Flash discount of 70% ending tonight at 12 AM. Shop now on Amazon official app.",
        "Security Alert: A new login to your Google account from Windows device in Delhi. If this was you, no action needed.",
        "Urgent reminder: Submit your final semester project synopsis before 5 PM today or admission ticket will be delayed.",
        "Your Swiggy Super membership expires in 3 days. Renew now to enjoy free delivery on all orders.",
        "SBI Customer Care: Beware of fraudsters asking for OTP or remote app download. SBI never asks for confidential details.",
        "HDFC Alert: Your credit card transaction of Rs 85,000 at Reliance Digital was approved. Contact customer care if not done by you.",
        "Hurry! 50% discount on Zomato Gold renewal. Offer valid till midnight today only.",
        "Notice from Examination Branch: Hall tickets for 7th semester practical exams available for download on college portal.",
        "Dear customer, you have earned 500 bonus reward points on your recent fuel purchase. Redeem on your next statement billing."
    ]

    # Subtle / evasive scam samples (trying to evade spam filters)
    subtle_scams = [
        "Hi, are you looking for remote flexible work? We have openings for content evaluators paying weekly. Details here: http://work-remotely-global.club",
        "Your order package delivery status is pending address confirmation. Kindly reconfirm street address: http://delivery-customs-duty.xyz",
        "Dear subscriber, your cloud storage quota is 99% full. To prevent email suspension, verify storage space: http://drive-quota-upgrade.top",
        "Greeting from HR department. Your resume has been shortlisted for senior analyst role. Schedule phone interview at: http://careers-portal-shortlist.work",
        "Dear cardholder, seasonal reward points credited. Redeem gift voucher worth 2500 by checking: http://points-redemption-rewards.info"
    ]

    data = []

    # Generate 1200 Scam samples
    for _ in range(1200):
        tmpl = random.choice(scam_templates)
        text = tmpl.format(
            bank=random.choice(banks),
            acc_num="XXXX" + str(random.randint(1000, 9999)),
            amount=random.choice([1499, 4999, 12500, 25000, 54999]),
            reward_val=random.choice([2500, 5000, 8500, 15000]),
            prize_val=random.choice(["25 Lakh", "50 Lakh", "1 Crore"]),
            phone_num=f"+91 9{random.randint(100000000, 999999999)}",
            scam_url=random.choice(scam_domains),
            scam_email="claim-award@lottery-winner-portal.xyz",
            num=random.randint(10000, 99999)
        )
        data.append({"text": text, "label": 1, "type": "scam"})

    # Add subtle scams
    for s in subtle_scams * 20:
        data.append({"text": s, "label": 1, "type": "scam"})

    # Generate 1200 Legit samples
    for _ in range(1200):
        tmpl = random.choice(legit_templates)
        text = tmpl.format(
            bank=random.choice(banks),
            acc_last4=str(random.randint(1000, 9999)),
            amount=random.choice([150, 480, 1200, 3450, 15000]),
            balance=random.choice([8400, 24500, 68000, 120000]),
            date=f"{random.randint(1, 28)}-Oct-2026",
            merchant=random.choice(merchants),
            restaurant=random.choice(restaurants),
            ref_num=f"TXN{random.randint(10000000, 99999999)}",
            otp_code=str(random.randint(100000, 999999)),
            order_id=f"40{random.randint(100, 999)}-{random.randint(1000000, 9999999)}",
            pnr_num=f"{random.randint(200, 899)}-{random.randint(1000000, 9999999)}",
            train_num=str(random.randint(12000, 12999)),
            num=random.randint(100, 999)
        )
        data.append({"text": text, "label": 0, "type": "legitimate"})

    # Add ambiguous legit samples (creates realistic FP/FN rates)
    for a in ambiguous_legit * 10:
        data.append({"text": a, "label": 0, "type": "legitimate"})

    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # 3. URL Dataset with realistic variations
    url_data = []
    # Scam URLs
    for _ in range(500):
        url = random.choice(scam_domains) + "/" + random.choice(["login.php", "verify", "secure/auth", "kyc-update", "claim-reward"])
        url_data.append({"url": url, "label": 1})
    
    # Legit URLs
    for _ in range(500):
        url = random.choice(legit_domains) + "/" + random.choice(["portal", "services/accounts", "about-us", "docs/api", "track-shipment"])
        url_data.append({"url": url, "label": 0})
    
    # Borderline URLs (marketing subdomains, URL shorteners)
    borderline_urls = [
        ("https://marketing.hdfcbank.com/offers/festive-deal", 0),
        ("https://auth.github.com/login", 0),
        ("https://aws.amazon.com/free/tier", 0),
        ("http://bit.ly/secure-login-3921", 1),
        ("http://tinyurl.com/sbi-verify-kyc", 1),
        ("https://support.apple.com/en-in/HT201232", 0)
    ]
    for b_url, b_lbl in borderline_urls * 10:
        url_data.append({"url": b_url, "label": b_lbl})

    df_urls = pd.DataFrame(url_data).sample(frac=1, random_state=42).reset_index(drop=True)

    return df, df_urls

if __name__ == "__main__":
    df_text, df_urls = generate_dataset()
    df_text.to_csv("ml_engine/scam_text_dataset.csv", index=False)
    df_urls.to_csv("ml_engine/scam_url_dataset.csv", index=False)
    print(f"Generated text dataset with {len(df_text)} samples.")
    print(f"Generated URL dataset with {len(df_urls)} samples.")
