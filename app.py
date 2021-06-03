import streamlit as st
import re
import smtplib
import socket
import dns.resolver





def main():

	

	st.title("Verify Email Address")
	st.sidebar.title("Enter email here:")


	email = st.sidebar.text_input('Email to verify:')


    # GSHEET_LINK = st.sidebar.text_input('Link to "readable" GSHEET with input:')

	if st.sidebar.button('Verify'):
		if(email==""):
			st.write("Please input email")
		else:
			verify_email(email)


def verify_email(email):

	try:

		email_address = email

		#Step 1: Check email
		#Check using Regex that an email meets minimum requirements, throw an error if not
		addressToVerify = email
		match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

		if match == None:
		    st.write('Bad Syntax in ' + addressToVerify)
		    raise ValueError('Bad Syntax')

		#Step 2: Getting MX record
		#Pull domain name from email address
		domain_name = email_address.split('@')[1]

		#get the MX record for the domain
		records = dns.resolver.query(domain_name, 'MX')
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)

		#Step 3: ping email server
		#check if the email address exists

		# Get local server hostname
		host = socket.gethostname()

		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mxRecord)
		server.helo(host)
		server.mail('me@domain.com')
		code, message = server.rcpt(str(addressToVerify))
		server.quit()

		# Assume 250 as Success
		if code == 250:
		    st.write('Valid email 🟢')
		else:
		    print('Invalid email 🔴')


	except:
		st.write("Uncaught error. Improvements required")

	return


def write_data(dframe):
	st.write(dframe)




if __name__ == '__main__':
	main()
 
