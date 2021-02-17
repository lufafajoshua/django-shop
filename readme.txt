
This app uses django version == 2.2
this application uses various users ie customer, seller and customer care agent
registration for the customer is found at 127.0.0.1:8000/user_profiles/register-customer
registration for seller at 127.0.0.1:8000/seller/register-seller
registration for agent at 127.0.0.1:8000/user_profiles/register-agent
The payment gateway used is MTN-momo API but can be integrated by other like paypal
This is not a complete project, the chat application is to be improved with additon and support of video calls, capturing pictures
Also the seller page is to be updated to show only products sold in a given period of time for example today for better statistics
This app uses redis-server and django channels to support the chat functionality and has been fully tested on linux 
for windows users 'try your luck'
Database configuration has been done with Mysql database
TODO's 

Better Frontend
Adding credit cart payments like paypal