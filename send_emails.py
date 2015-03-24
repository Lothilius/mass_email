__author__ = 'Lothilius'

import smtplib
import sys
import authentication
import csv
import numpy as np


#Pull data from CSV file
def array_from_file(filename):
    """Given an external file containing numbers,
            create an array from those numbers."""
    dataArray = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            dataArray.append(row)
    return dataArray

# Create email addresses.
def create_email_address(name):
    email = name.replace(' ', '.')
    email = email + '@bazaarvoice.com'

    return email

# Create the body of the message
def create_body(full_name):
    first_name = full_name.split()[0]
    body = 'Hello ' + first_name + ',\n' + """      In an effort to reduce our licensing costs, BizApps is looking to identify unused \"Email to Case Premium\" licenses.

Please lake a moment to consider your use of the \"New Comment\" button on the Case screen.
If it has been a while since you have used the \"New Comment\", please let us know.

We appreciate your help in our efforts.

Thank you

Martin A Valenzuela
Business Applications Administrator
m:  915.217.8558
Martin.Valenzuela@bazaarvoice.com"""

    return body


# Build and send the emails
def send_message(smtp_object, subject, body, receiver='martin.valenzuela@bazaarvoice.com',
                  sender='martin.valenzuela@bazaarvoice.com'):

    full_message = """From:""" + sender + '\n' + 'To:' + receiver + '\n' \
              + 'Subject: ' + subject + '\n\n' + body


    try:
        smtp_object.sendmail(sender, [receiver], full_message)
        print "Successfully sent email to " + receiver
    except Exception, exc:
        sys.exit("mail failed; %s" % str(exc)) # give a error message


if __name__ == '__main__':
    try:
        smtp_object = smtplib.SMTP('smtp.office365.com', 587)
        smtp_object.ehlo()
        smtp_object.starttls()
        username, password = authentication.smtp_login()
        smtp_object.login(username, password)
    except Exception, exc:
        sys.exit("mail failed; %s" % str(exc)) # give a error message


    file = ''
    # while file != 'exit':
    try:
        file_name = raw_input('Please enter file name: ')
        file = '/Users/martin.valenzuela/Box Sync/Documents/Austin Office/Data/' + file_name + '.csv'
        csv_info = array_from_file(file)
    except IOError, error:
        print 'Try Again ' + str(error) # give a error message

    # names = np.array(csv_info)
    # names = names[:, 1]
    #
    # print(names)
    i = 0
    for each in csv_info[1:]:

        if each[1].find(' ') != -1 and each[3] == 'E2CP' and each[9] == 'true':
            print each[1]
            body = create_body(each[1])
            i += 1
            # send_message(smtp_object, 'License usage in SFDC', body, create_email_address(each[1]))

    print i