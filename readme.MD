# Etsy Listing Data Analysis

I'm going to do analysis on which tags do best in getting viewership.

## Starting off

0. Prerequisites
   a. You should already have etsy-keystring and callback-url in your .env file
   b. You can get etsy-keystring from the etsy api page and callback-url from pipedreams.com

1. Get the authentication code
   a. Run get_authcode.py
   b. Click the link and log in to send a get request
   c. Check pipedreams.com to get your code. Copy & paste value into etsy-code in .env file
   d. From the terminal print statement, copy and paste the etsy-state and code-verifier into the .env file.

2. Get the token
   You need a token in order to make API GET requests. After copying the authentication code into the .env file, you should be able to run the etsy_initial_token.py file to get a token.

3. Get the shop id ## skip this step
   a. Copy and paste the token into the etsy_shop_id.py file to get the shop ID. You need this shopID to make get requests to your specific shop.

4. Get etsy listing data.
   a. Copy and paste token into the etsy_listings.py file in the token= variable.
   b. On etsy_listings.py, use this shop_id to get the shop_id.
