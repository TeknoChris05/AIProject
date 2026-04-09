"""
create_dataset.py  —  Run this once to generate data/sample_emails.csv
Usage: python3 create_dataset.py
"""

import csv, os

os.makedirs("data", exist_ok=True)

emails = [
    # PHISHING
    (1,"phishing","URGENT: Verify Your Account Now","Dear Customer, suspicious activity detected on your account. Verify immediately at http://secure-login-update.xyz/verify or your account will be closed within 24 hours. Provide your username, password, and credit card number."),
    (2,"phishing","You Have Won $1500000!","Congratulations! You won the International Lottery. Reply with your full name, address, and bank account details. A processing fee of $250 is required. Contact lottery.claim99@gmail.com"),
    (3,"phishing","Your PayPal Account Has Been Limited","Dear PayPal Member, unusual activity detected. Restore access at http://paypal-account-restore.net/confirm within 48 hours or your account will be permanently suspended."),
    (4,"phishing","IT Department - Password Reset Required","This is the IT Help Desk. All employees must reset passwords immediately due to a security breach. Visit http://internal-it-reset.co/reset and enter your current credentials. Mandatory compliance required."),
    (5,"phishing","Your Netflix Subscription Has Expired","Dear Netflix User, your payment was declined. Update billing at http://netflix-billing-update.info/pay within 12 hours or your account and watch history will be permanently deleted."),
    (6,"phishing","IRS: Unclaimed Tax Refund","The IRS has identified an unclaimed refund of $3742 in your name. Verify your SSN and bank account at http://irs-refund-gov.net within 5 business days or forfeit the refund permanently."),
    (7,"phishing","Amazon Order - Unauthorized Purchase","Your Amazon account placed an order for iPhone 15 Pro ($1299). If unauthorized click http://amazon-dispute-center.xyz/cancel within 2 hours. Enter your login and payment details to cancel."),
    (8,"phishing","LinkedIn: 50 Recruiters Viewed Your Profile","50 recruiters viewed your profile! Get LinkedIn Premium FREE 3 months at http://linkedin-premium-offer.net/activate. Use your LinkedIn credentials. Expires in 24 hours."),
    (9,"phishing","Bank of America Security Alert","ALERT: Login attempt from unrecognized device in Russia. Verify your identity at http://bofa-security-check.org/verify. Provide your account number and PIN to secure your account now."),
    (10,"phishing","Microsoft: Your Account Will Be Deleted","Your Microsoft account will be deleted due to inactivity. Sign in at http://microsoft-account-keep.net/verify within 24 hours or all emails, documents, and OneDrive files will be permanently erased."),
    (11,"phishing","FedEx: Redelivery Fee Required","FedEx was unable to deliver your package. Pay a redelivery fee of $2.99 at http://fedex-redelivery.xyz/pay within 24 hours or the package will be returned to sender."),
    (12,"phishing","HR: W-2 Form Update Required","Due to a tax system update all employees must resubmit W-2 information at http://hr-w2-update.net/submit. Enter your SSN and direct deposit information. Deadline is end of business today."),
    (13,"phishing","Crypto Investment: 300% Returns Guaranteed","I am a crypto trader with 10 years experience. Turn your $500 into $1500 in 48 hours. Send Bitcoin to my wallet. 300% profit guaranteed. Trusted by 10000 clients. Act now, limited spots!"),
    (14,"phishing","Apple ID: Unusual Purchase Detected","Your Apple ID purchased Final Cut Pro ($299.99) from an unrecognized Mac in China. Cancel at http://apple-id-dispute.net/cancel. Provide your Apple ID and credit card CVV for a full refund."),
    (15,"phishing","Google: Verify Your Gmail Account","We received a request to delete your Gmail account. Stop this at http://google-account-verify.net/confirm within 6 hours. Enter your Google password to prevent permanent deletion."),
    # LEGITIMATE
    (16,"legitimate","Team Lunch Thursday","Hey everyone, team lunch Thursday noon at Rosarios on Main Street. Let me know dietary restrictions by Wednesday. - Mike"),
    (17,"legitimate","Re: Project Meeting Notes","Hi Sarah, meeting notes look accurate. I will follow up with the design team about mockups by Friday. - Tom"),
    (18,"legitimate","Your GitHub pull request has been merged","Your pull request #47 (Fix authentication bug) has been successfully merged into main by reviewer jdoe. Thanks for your contribution!"),
    (19,"legitimate","Order Confirmation - Best Buy","Thank you for your order! Your Samsung 27-inch Monitor has been placed. Estimated delivery March 18-20 2026. View your order at bestbuy.com/orders."),
    (20,"legitimate","CS 4130 Assignment 3 Due Friday","Reminder: Assignment 3 on neural network backpropagation is due Friday 11:59 PM via Moodle. Include chain rule derivations. Office hours Tue/Wed 2-4 PM. - Prof. Johnson"),
    (21,"legitimate","Thanksgiving plans","Hi honey, confirming you are coming home for Thanksgiving. Dinner at 3pm, aunt Linda and uncle Bob will be here too. Let me know if you need a ride. Love Mom"),
    (22,"legitimate","Zoom Meeting: Sprint Review","Zoom meeting invite: Q2 Sprint Review. April 11 2026 at 2:00 PM EST. Join at zoom.us Meeting ID 123456789 Passcode sprint42. Review the sprint board beforehand. - Agile Team"),
    (23,"legitimate","Netflix - New episodes available","New episodes of your favorite show are now available on Netflix. Watch at netflix.com. Update email preferences at netflix.com/account. - Netflix"),
    (24,"legitimate","Your prescription is ready for pickup","Walgreens Pharmacy: Your Amoxicillin 500mg prescription is ready for pickup at our 15 Mile Road location. Hours 8am-10pm daily. Thank you for choosing Walgreens."),
    (25,"legitimate","Internship Application Update","Dear Applicant, thank you for applying to Tech Corp Software Engineering Intern. We would like to schedule a phone screening. Please use our scheduling link to pick a time. - Recruiting Team"),
    (26,"legitimate","Your annual car insurance renewal","Dear Policyholder, your auto insurance policy renews May 1 2026. Annual premium $1247.00 with a 3% clean driving discount. Log in at progressive.com/myaccount to review and renew."),
    (27,"legitimate","Library book due soon","Utica Public Library: Clean Code by Robert C. Martin is due in 3 days. Renew online at uticapubliclibrary.org/account. Late fee $0.25 per day."),
    (28,"legitimate","Re: Server maintenance window tonight","Team, scheduled maintenance on production servers tonight 2:00-4:00 AM EST. Brief outage expected. Please save your work. Confirmation email will follow. - DevOps"),
    (29,"legitimate","Dentist appointment reminder","Dr. Williams Dental: You have an appointment April 15 2026 at 9:30 AM for a routine cleaning. Arrive 10 minutes early. To reschedule call at least 24 hours in advance."),
    (30,"legitimate","Stack Overflow - Your answer was accepted","Your answer on Stack Overflow about Python async/await was voted accepted with 47 upvotes. You earned the Populist badge! Keep contributing. - Stack Overflow Team"),
]

with open("data/sample_emails.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["id", "label", "subject", "body"])
    writer.writerows(emails)

print(f"Created data/sample_emails.csv with {len(emails)} emails")