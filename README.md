# City-Sushi
A web app for managing sushi restaraunt and ordering sushi. 

To develop the project we chose to use the Django framework for the following reasons:
- Django greatly simplifies our database management. To do database management we learned how to work with Django Models. Django Models help us generate our SQLite database. The models.py file has all of the classes which we write to have working databases corresponding to E/R diagram which was submitted in the previous report.
- Django helps us handle the backend, frontend and database management all in one package.

# Final Thoughts on the Project
The challenges we had with this project was learning Django's framework and functionalities. Overall, Django's documentation is very specific, so researching what we need to implement was not easy. We spent some time researching how Django's model and form are created, and how we were able to use it to our advantage. Another problem we had to deal with was user authentication, and how we were suppose to inherit some of the features in our models into these users. Another thing was trying to understand how Django renders our HTML files and our functionalities. Although you mentioned that our project looks very similiar to a database project, many of the functionalities we wrote still have to deal with other aspects that Django does not offer. What we should've done to make it look less of a database project was maybe to implement styles into our HTML, such as CSS and JS, however we did not have much time to do this. Our main goal for this project was to ensure that we had the functionalties we needed to make this web application work the way it is suppose to and then focus on the formatting and look of the web pages afterwards. By the time we were understanding Django very well, we ran out of time to finish the rest of the project, however, we believe that we cover the main aspects and functionalities that almost every food web application should have. We apolgize for the fact that we did not meet every specification you required.

# Instructions for Running
1) In order to run this program you need to have Python installed, and you can install django using pip in the terminal command:
  - `python -m pip install django`
2) Clone this repository and change directory of the terminal into it. 
3) Run the command: `python manage.py runserver`
4) Open localhost server 127.0.0.1:8000
5) If you want to log in as manager go to 127.0.0.1:8000/admin/
    login name: admin
    password: citysushi
   After log in as manager you can modify any part of database, such as mark as blacklisted customer or make customer vip person and any other modifications.
6) If you want to log in as customer go to 127.0.0.1:8000/accounts/login/
7) If you log in as admin, you will be able to let your cooks confirm and tell the customers that if the orders are cooked using the link below:     
    `http://127.0.0.1:8000/orders/cooking/`

