# Finance web page simulator for CS50 course

This is a project work done for the CS50 course at Harvard University. Reference link: [https://finance.cs50.net](https://finance.cs50.net/)

# **Description**

It is a web page designed to act as a stock market buying and selling simulator. It allows users to query a database for available stocks as of March 20, 2023. Additionally, it enables users to create accounts with passwords and an initial cash balance of $10,000. Users can buy and sell stocks and analyze transaction history.

*Note*: It is worth noting that it is possible to modify the page to make it real-time by simply requiring an API key.

## **Web page workflow:**

- Before Login
    - Contains a [login](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21) and [register](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21) page where passwords are encrypted using the "werkzeug.security" Python library.
- After Login:
    - [Index page](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21): Displays a table containing the stocks, the quantity of shares purchased, the unit price of each share, and the total amount.
    - [Quote page](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21): Allows users to query a stock with its corresponding symbol and retrieve its price.
    - [Buy page](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21): Enables users to purchase a certain stock by entering the symbol and the quantity of shares.
    - [Sell page](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21): Allows users to sell any acquired stocks and specify the quantity of shares.
    - [History page](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21): Provides information on the number of transactions made, with the share value being either positive or negative to identify it as a purchase or sale.
- [Error page](https://www.notion.so/Finance-web-page-simulator-for-CS50-course-929951605e814c86860c4f6f79a99805?pvs=21):
    - For cases where errors occur, the page displays an image with information about the error code and its description, including:
        - Inadequate amount
        - Empty form fields
        - Cases where users manipulate HTML and data is not in the correct format
        - Stock not found
        - And others.

![Figure 1. Login page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled.png)

Figure 1. Login page

![Figure 2. Register page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled%201.png)

Figure 2. Register page

![Figure 3. Index page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled%202.png)

Figure 3. Index page

![Figure 4. Quote page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled%203.png)

Figure 4. Quote page

![Figure 5. Buy page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled%204.png)

Figure 5. Buy page

![Figure 6. Sell page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Screenshot_from_2024-03-20_12-48-07.png)

Figure 6. Sell page

![Figure 7. History page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled%205.png)

Figure 7. History page

![Figure 8. Error customize page](Finance%20web%20page%20simulator%20for%20CS50%20course%20929951605e814c86860c4f6f79a99805/Untitled%206.png)

Figure 8. Error customize page
