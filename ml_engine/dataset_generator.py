"""
Realistic & High-Coverage Dataset Generator for Scam, Fraud, and Legitimate Communications.
Generates comprehensive text samples (SMS, Email, Chat, WhatsApp) in English and Hinglish
across Banking, E-Commerce, Utility, Lottery, Job, Extortion, and Daily Conversations.
"""

import random
import pandas as pd

def generate_dataset():
    # 1. SCAM / FRAUD / MALICIOUS TEMPLATES (English & Hinglish)
    scam_templates = [
        # Banking, KYC, & Card Scams
        "Dear {bank} customer, your savings account {acc_num} will be blocked within 24 hours due to pending KYC. Update immediately at {scam_url}",
        "URGENT: Your {bank} netbanking has been suspended today. Verify your PAN card and Aadhaar details to restore access: {scam_url}",
        "{bank} Alert: Unauthorized transaction of Rs {amount} detected on your debit card. If this was not you, cancel immediately at {scam_url}",
        "Attention user: Your {bank} credit card reward points worth Rs {reward_val} are expiring tonight. Redeem cash now: {scam_url}",
        "Dear customer, your bank account is put on hold. Kindly update your mobile number and submit OTP at {scam_url} to unblock.",
        "RBI Notification: KYC verification mandatory for all bank accounts. Failure to update before 10 PM will freeze your account. Link: {scam_url}",
        "Dear cardholder, your {bank} ATM Debit Card has been blocked due to suspicious activity. Unblock immediately: {scam_url}",
        "Urgent: Your loan of Rs 5,00,000 has been pre-approved by {bank}. Deposit processing fee of Rs {amount} to disburse: {scam_url}",
        "Income Tax Department Alert: Refund of Rs {amount} pending due to incorrect bank IFSC. Submit bank credentials to receive: {scam_url}",

        # Utility & Disconnection Scams
        "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM from the power house because your previous month bill was not updated. Please contact our electricity officer at {phone_num} immediately.",
        "Urgent Notice: Electricity bill of Rs {amount} unpaid. Power supply disconnection order issued. Pay immediately via link {scam_url} or call {phone_num}",
        "Gas supply disconnection warning! Your gas pipeline service will be terminated today. Settle pending dues of Rs {amount} at {scam_url}",
        "BSNL / MTNL Alert: Your mobile SIM service will be suspended within 2 hours due to pending KYC. Call customer officer at {phone_num} now.",

        # Lottery, Prize, & Freebie Lures
        "Congratulations! Your mobile number has won Rs {prize_val} in KBC Lucky Draw 2026. Send your bank details to claim on WhatsApp: {phone_num}",
        "Dear winner, you have been selected for a free iPhone 15 Pro and Rs 50,000 cash bonus. Click here to claim your gift now: {scam_url}",
        "Google Promotion Award: You have won £750,000 in Google Annual Lottery. Reply with your Name, Age, Country to claim award: {scam_url}",
        "Exclusive offer! Claim your Flipkart free gift card worth Rs 10,000 today only. Limited stock: {scam_url}",
        "Jio 5G Celebration: Get 500 GB free 5G data and 1 year free Disney+ Hotstar recharge. Activate link now: {scam_url}",
        "Free mobile recharge offer! Get Rs 499 free recharge on any SIM by clicking: {scam_url}",

        # Fake Job Offers & Task Scams
        "Part-time job offer! Earn Rs 3,000 - 8,000 daily working from home on your phone. Just like and subscribe YouTube videos. Contact HR on WhatsApp: {phone_num}",
        "Amazon Hiring: Earn Rs 45,000/month for simple order review tasks. No experience needed. Immediate joining. Register here: {scam_url}",
        "Work from home opportunity! Earn daily payout in USDT/Crypto. Daily 2 hours task. Contact manager on Telegram: @job_{num}",
        "Congratulations! Selected for Data Entry job at MNC. Daily payout Rs 2,500. Pay registration deposit fee of Rs 499 at {scam_url}",
        "Google Rating Job: Earn Rs 500 per Google Map review. Payout instantly via UPI. Message our HR manager on WhatsApp: {phone_num}",

        # Courier, Delivery, & Customs Scams
        "FedEx Notification: Your parcel #FX-{num} could not be delivered due to incorrect street address. Update your address and pay Rs 45 re-delivery fee: {scam_url}",
        "India Post alert: Your shipment #IN{num} is held at regional customs hub. Update delivery address within 12 hours: {scam_url}",
        "DHL Express: Package delivery on hold due to unpaid duty charges of Rs {amount}. Confirm payment online now: {scam_url}",
        "BlueDart Courier: Address incomplete for parcel #BD{num}. Reschedule delivery and verify phone number at: {scam_url}",

        # Legal, Cyber Crime, & Extortion Threats
        "Police Cyber Crime warning: Arrest warrant issued against you for illegal downloads. Pay fine of Rs {amount} to avoid arrest warrant: {scam_url}",
        "Traffic Police E-Challan: Pending challan of Rs {amount} against your vehicle. Pay within 24 hours to avoid vehicle seizure: {scam_url}",
        "We have hacked your webcam and recorded compromising videos of you. Pay 0.05 BTC ($3,000) within 48 hours to our Bitcoin wallet or we will broadcast to all contacts.",
        "CBI / Narcotics Bureau: Illegal drugs found in package registered under your Aadhaar. Contact investigating officer at {phone_num} immediately.",

        # Tech Support & Account Compromise
        "CRITICAL SECURITY ALERT: Your computer is infected with Trojan Spyware. Bank credentials compromised. Call Microsoft Certified Tech at {phone_num} immediately.",
        "Your Apple ID has been locked for security reasons. Confirm your password and credit card immediately at {scam_url} to prevent permanent closure.",
        "Netflix Alert: Your membership subscription could not renew. Account will be terminated today. Update payment info: {scam_url}",

        # Crypto & Investment Fraud
        "Double your money in 24 hours! Join VIP Crypto Trading group with 100% guaranteed daily returns. Deposit minimum $50 to earn $500. Link: {scam_url}",
        "Stock Market Insider Tips: Guaranteed 500% profit in intraday trades. Zero loss strategy. Join private Telegram group: {scam_url}",

        # Hinglish / Bilingual Scams (Very common in real world)
        "Dear customer, aapka {bank} khata block kar diya gaya hai kyc na hone ke karan. Turant update kare is link par: {scam_url}",
        "Bijli ka bill bhare nahi to aaj raat bijli kat di jayegi power house se. Turant officer se baat kare: {phone_num}",
        "Badhai ho! Aapka number KBC lucky draw me select hua hai aur aapne jita hai {prize_val}. Paise claim karne ke liye WhatsApp kare: {phone_num}",
        "Ghar baithe kamaye daily 3000 se 5000 rs youtube video like karke. Contact HR on WhatsApp: {phone_num}",
        "Aapka traffic police e-challan kata hai Rs {amount} ka. Turant jama kare nahi to gaadi seize hogi: {scam_url}",
        "Free recharge offer! Sabhi dosto ko mil raha hai 3 mahine ka free recharge. Abhi click kare: {scam_url}",
        "Aapka ATM card block ho gaya hai. Dobara chalu karne ke liye apna 16 digit card number aur OTP bheje.",
        "SBI yono account suspend ho gaya hai. PAN card verify karne ke liye yaha login kare: {scam_url}",
        "Loan pass ho gaya hai Rs 2 lakh ka. Sirf 500 rs file charge jama kare aur turant paise paaye: {scam_url}"
    ]

    # 2. LEGITIMATE / SAFE TEMPLATES (Conversations, receipts, academic, personal, normal chats)
    legit_templates = [
        # Daily Conversations & Chat
        "Hello, how are you doing today?",
        "Good morning! Hope you have a wonderful and productive day ahead.",
        "Hey bro, are you coming to college today? Let's meet at the canteen.",
        "Can we schedule our project discussion call today around 4:00 PM?",
        "Thanks a lot for your help yesterday! Really appreciate the support.",
        "Happy Birthday! Wishing you good health, happiness, and great success.",
        "I have reached home safely. Let me know once you reach as well.",
        "Did you finish the assignment for Digital Communication? Send me your reference link.",
        "Let's work together on the final year project presentation slides this evening.",
        "What time is our next class? Is Prof. Sharma taking the lecture today?",
        "Hey, can you please share the PDF notes from yesterday's machine learning class?",
        "Are you free this weekend? We were planning a lunch get-together with the team.",
        "Great work on the project demo! The presentation went really well.",
        "Please review the attached document and let me know if any changes are needed.",
        "Running a few minutes late for the meeting. Please start without me, joining shortly.",
        "Bro, can you transfer 500 rupees on GPay? Will pay you back tonight at dinner.",
        "Did you receive the email from the training and placement cell about tomorrow's drive?",
        "The weather is so nice today! Let's go for a walk in the evening.",
        "Don't forget to submit the lab record book before 5 PM today.",
        "Where are you right now? I am waiting near the college main gate.",

        # Real Bank Transaction Receipts (Legitimate alerts)
        "Dear customer, INR {amount}.00 debited from account ending in **{acc_last4} on {date} at {merchant}. Available balance is INR {balance}.00. If not done by you, SMS BLOCK to 567676.",
        "Your {bank} credit card statement for ending {acc_last4} is generated. Total amount due: INR {amount}.00, Due date: {date}. View statement on official app.",
        "Dear customer, INR {amount}.00 credited to your account ending **{acc_last4} through NEFT/IMPS on {date}. Ref no {ref_num}.",
        "Your OTP for login to {bank} Internet Banking is {otp_code}. Valid for 5 minutes. NEVER share this code with anyone, including bank staff.",
        "Dear customer, request for cheque book of 25 leaves for account ending **{acc_last4} has been registered successfully. Track status on official portal.",
        "Salary credited: INR {balance}.00 has been credited to your {bank} account ending **{acc_last4} on {date}.",
        "Dear customer, cash withdrawal of INR {amount}.00 successful at {bank} ATM on {date}. Available balance: INR {balance}.00.",

        # E-Commerce & Deliveries
        "Your Amazon order #{order_id} has been dispatched and will arrive by tomorrow, 8:00 PM. Track your package in the Amazon app.",
        "Swiggy: Your delicious meal from {restaurant} has been delivered. Thank you for ordering with us! Rate your delivery partner.",
        "Zomato: Order confirmed! The chef is preparing your meal at {restaurant}. Estimated delivery in 35 minutes.",
        "Flipkart: Your order #{order_id} containing Wireless Earbuds has been out for delivery. Handover OTP is {otp_code}.",
        "Blinkit: Your grocery delivery has arrived at your doorstep. Thank you for choosing Blinkit!",
        "Uber: Your trip receipt for INR {amount}.00 on {date}. Driver rating: 5 stars. Thanks for riding with Uber.",

        # Travel & Utility Bills (Genuine)
        "IRCTC PNR {pnr_num}: Booking confirmed for Train #{train_num}. Coach B4, Berth 42. Charting status will be updated 4 hours before departure.",
        "IndiGo flight 6E-{num} from Delhi to Bengaluru is on schedule. Web check-in opens 48 hours before departure. Check terminal details on official website.",
        "Payment receipt: Your electricity bill payment of INR {amount}.00 was successful on {date}. Biller ref: BBPS-{num}. Thank you.",
        "Airtel recharge of Rs 299 is successful for your number. Unlimited calls + 1.5GB/day valid till {date}. Enjoy Airtel 5G Plus.",
        "Jio: Your prepaid recharge of Rs 666 is active. Valid for 84 days with 1.5GB/day data.",

        # Academic / College Notices
        "Reminder: Department seminar on 'Advances in Machine Learning' will be held tomorrow at 11:00 AM in Seminar Hall 2. Attendance is mandatory for 7th semester students.",
        "Notice: The submission deadline for the 4th Year Mini Project synopsis has been extended to Friday, 5:00 PM. Submit files via Google Classroom.",
        "Hi team, please find attached the meeting notes from today's sprint planning. Please review the action items before tomorrow's standup.",
        "Campus Placement Drive: Infosys technical interview shortlist has been uploaded to the placement portal. Selected students report to Lab 3 at 9:00 AM.",
        "Dear Rahul, your library book 'Operating System Concepts' is due for return on {date}. Renew online through the college OPAC catalog.",
        "Meeting Invitation: Weekly project review meeting with Project Guide Dr. Sharma scheduled on Google Meet for Thursday at 3 PM.",
        "Internal assessment marks for Semester 7 have been displayed on the notice board. Queries may be raised before Friday.",

        # Hinglish / Casual Everyday Talks
        "Bhai kal college aayega kya? Ek saath library me baith kar PPT complete karte hain.",
        "Maine notes WhatsApp group me bhej diye hain, dekh kar bata dena sab sahi hai na.",
        "Sir, maine assignment submit kar diya hai Google Classroom par. Please check kar lijiye.",
        "Chalo canteen chalte hain, bohot bhookh lagi hai.",
        "Ghar pahuche to phone karna, dhyan se jana.",
        "Project ka research paper almost complete hai, kal sir ko draft dikha denge.",
        "Bhai 200 rupaye GPay kar de, canteen me online payment nahi chal raha.",
        "Viva ki taiyari shuru kar di kya tune? Machine learning ke questions tough puchte hain."
    ]

    banks = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Kotak Mahindra Bank", "Bank of Baroda", "Canara Bank", "Union Bank"]
    merchants = ["Amazon India", "Flipkart", "Uber", "Zomato", "Starbucks", "Reliance Retail", "Blinkit", "Apollo Pharmacy", "Myntra", "BookMyShow"]
    restaurants = ["Domino's Pizza", "Burger King", "Haldiram's", "Subway", "Bikanervala", "Barbeque Nation", "KFC", "Pizza Hut"]
    
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
        "http://tax-refund-gov-credit.xyz/claim",
        "http://traffic-echallan-pay-portal.click",
        "http://pm-yojna-free-laptop-gift.store"
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
        "https://www.coursera.org",
        "https://parivahan.gov.in",
        "https://incometax.gov.in"
    ]

    data = []

    # Generate 1,800 diverse Scam samples
    for _ in range(1800):
        tmpl = random.choice(scam_templates)
        text = tmpl.format(
            bank=random.choice(banks),
            acc_num="XXXX" + str(random.randint(1000, 9999)),
            amount=random.choice([1499, 4999, 12500, 25000, 54999, 500, 1000]),
            reward_val=random.choice([2500, 5000, 8500, 15000]),
            prize_val=random.choice(["25 Lakh", "50 Lakh", "1 Crore", "10 Lakh"]),
            phone_num=f"+91 9{random.randint(100000000, 999999999)}",
            scam_url=random.choice(scam_domains),
            scam_email="claim-award@lottery-winner-portal.xyz",
            num=random.randint(10000, 99999)
        )
        data.append({"text": text, "label": 1, "type": "scam"})

    # Generate 1,800 diverse Legitimate samples
    for _ in range(1800):
        tmpl = random.choice(legit_templates)
        text = tmpl.format(
            bank=random.choice(banks),
            acc_last4=str(random.randint(1000, 9999)),
            amount=random.choice([150, 480, 1200, 3450, 15000, 500, 250]),
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

    df = pd.DataFrame(data).sample(frac=1, random_state=42).reset_index(drop=True)

    # 3. URL Dataset with realistic variations
    url_data = []
    for _ in range(600):
        url = random.choice(scam_domains) + "/" + random.choice(["login.php", "verify", "secure/auth", "kyc-update", "claim-reward", "payment-link"])
        url_data.append({"url": url, "label": 1})
    
    for _ in range(600):
        url = random.choice(legit_domains) + "/" + random.choice(["portal", "services/accounts", "about-us", "docs/api", "track-shipment", "login"])
        url_data.append({"url": url, "label": 0})
    
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
    print(f"Generated text dataset with {len(df_text)} samples.")
    print(f"Generated URL dataset with {len(df_urls)} samples.")
