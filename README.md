# Puppy Playmates 
![Main Mockup](docs/images/playmates.png)

[Link to Live Website](https://puppy-playmates.herokuapp.com/)

[GitHub Repo](https://github.com/crypticCaroline/puppy-playmates)


*** 

## About  
Welcome to Puppyplaymates, a webapp to help dogs find love! 
This is a Python Flask app using MongoDB, cloudinary and Flask Mail to produce a social media style application.

PuppyPlaymates currently brings users together and allows them to get in contact with the pups they love! The application lets the users create a profile that allows them to add their dogs’ details, add photos, let other users know when the next walk with their dog is happening, add comments both public and private and add likes on other profiles.  The site offers the additional functionality; reset passwords, change passwords, reporting other users, contact us, editing and deleting comments, backend validation, profanity checking and birthday checking. Please look at the [features](#features) section for a more detailed description. 
The application has a lot of room for growth and a list of future features to implement. 

## Index – Table of Contents

- [User Experience (UX)](#user-experience--ux-)
- [Strategy](#strategy)
  * [User Stories](#user-stories)
- [Scope](#scope)
- [Structure](#structure)
- [Database](#database)
- [Validation](#validation)
  * [Backend Validation](#backend-validation)
  * [Front End Validation](#front-end-validation)
- [Security](#security)
- [Features](#features)
- [Design](#design)
- [Skeleton](#skeleton)
  * [Layout](#layout)
- [Surface](#surface)
  * [Typography](#typography)
  * [Call to Action](#call-to-action)
  * [Imagery](#imagery)
- [Technologies](#technologies)
    + [Languages & Frameworks](#languages---frameworks)
    + [Front End](#front-end)
    + [Backend](#backend)
    + [Helpers](#helpers)
    + [Planning](#planning)
  * [Flask](#flask)
    + [Testing Tools](#testing-tools)
    + [Technology Configuration](#technology-configuration)
    + [MongoDB](#mongodb)
  * [Cloudinary](#cloudinary)
  * [Flask Mail](#flask-mail)
- [Testing](#testing)
- [Deployment](#deployment)
  * [Configuration](#configuration)
    + [Local Environment](#local-environment)
  * [Adding and Committing files](#adding-and-committing-files)
  * [Deploying](#deploying)
  * [Forking](#forking)
  * [Cloning](#cloning)
- [Known Bugs](#known-bugs)
- [Acknowledgements](#acknowledgements)
  * [Credit](#credit)
      - [People](#people)
      - [Additional Testers](#additional-testers)
      - [Tools and Docs](#tools-and-docs)
  * [Code:](#code-)
  * [Content:](#content-)
  * [Inspiration & Research:](#inspiration---research-)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


*** 

## User Experience (UX)
## Strategy
With PuppyPlaymates I wanted to be able to give dog owners a way to communicate with other dog owners in a fun and safe way. By combining social media and dating profile principles I have created a playmate finding service dedicated to human’s best friend.

### User Stories 

#### New User
* I would like to find out what the site is about
* I would like to see if the site is for me without registering 
* I would like to easily register 
* I would like to be able to add my dog’s details


#### Existing User
* I want to be able to sign in and out easily
* I would like to be able to delete my account
* I would like to be able to add/edit/delete comments to my own and other profiles
* I would like to be able to reset my password

#### All Users 
* I would like to get user feedback when I take actions on the site
* I would like to be able to contact PuppyPlaymates
* I would like to be able to add comments and details about my walks
* I would like to be able to track what pages I have liked and that like me
* I would like to be able to message or comment on other profiles
* I would like to feel safe when using the platform
* I would like to be able to search for other users 
* I would like to be able to add/edit/delete images and change my profile image
* I would like to be able to add/edit/delete dog information
* I would like to be able to add/edit/delete my information

#### Reasons for the website
A way to bring together dog owner for:
* Playmate finding
* Walk arranging 
* Promoting interactions between owners
*  Potential Breeding

## Scope 
#### A Playmates user may expect: 
* Easy to navigate website
* Good presentation and visually appealing
* Links and functions work as expected
* Can Add / Edit / Delete info on my profile
* Can view other dog profiles
* Can interact with other users 
* Can delete profile 
* Can get in contact with site owners 


#### What a user may want: 
* Can Add Edit/ Delete info to my profile
    * Add/Edit Dog Information 
    * Add/Edit/Delete Images
    * Add/Edit/Delete Comments
    * Add/Edit/Delete Walk Information
* Can view other dog profiles
    * Add/Edit/Delete Comments 
    * Like other users’ profiles so I can find them again
* Can report users who make me feel uncomfortable 
* Add/Edit/Delete Events (outside current scope)
* Live Chat abilities WOOFCHAT (outside current scope)

#### As a developer / business I expect:
* To provide an easy-to-use website
* To enable users to communicate
* Add/Edit/Delete Images, Comments, Walk information, profile functionality 
* To make the website fun and enjoyable
* To deliver an easy sign up and log in process
* I want to allow users to be able to reset their passwords if they forget their details
* To safeguard users’ content and only allow the author or profile owner to edit/delete content
* To safeguard users by having a report pathway and to be able to remove inappropriate comments, images, and accounts 


***


## Structure
The diagram below is of the information architecture of the Web App.  This shows the journeys the users can take throughout the website. Please see the [Features](#features) section for more information on what user actions are on each page 
![Site Structure](docs/images/structure.png)


***

## Database 
#### Database Schema 
I have used a non-relational database which has meant that I have kept all of a user’s data stored within one document and used Key Value pairs with nested arrays and objects to store and access the appropriate data.  Most the data I have stored as "strings" If they are text based, all of which will have to pass through [validation](#validation), "bools" for switches, dates for DOB and Walks and ObjectIds. I have chosen to set the time of the walk and the date/time of the comments as strings this is because this information is only for user info and will serve no function in sorting through the data/time as a searchable function, this removes the need to reformat the data on entry and retrieval of the database. The nested arrays / objects are also passed through backend [validation](#validation) to ensure they fit the schema for the database. 



![Database Schema](docs/database/schema.png)


I have used backend validation to make sure the data is formatted correctly before being sent to the database. Booleans are set to a default False, Dates are formatted before insertions, string fields are checked to make sure they are strings.  I ran the database through [Studio 3T](https://studio3t.com/) To check to make sure all my data was conforming to my intended Schema.


![Database Scheme Check](docs/database/database_schema.png)
 

##### Object Instance in the Database


![Database Object Instances](docs/database/object_instance.png)


##### Below are the user input types that the user experiences in the front end


![Database Input](docs/database/input_types.png)


##### Sample of filled in Document


![Database Sample](docs/database/sample_data.png)

##### Archives

When a user is deleted, I have chosen to add them into an archive.  This means that if a user is accidentally deleted, we have the means to access the data.  The schema is identical to above and directly transferred over before the user is removed from the user’s collection. If a user does want to rejoin with the same details the document can be copied to the users collection.  I have specified in the privacy policy that removal of profile doesn't remove their data automatically.  They can however use the contact form to ask for the data to be removed. 


***


## Validation

### Backend Validation 

All users’ inputs are passed through the appropriate validators to ensure no bad data enters the database. The users are notified through a flash message if any of these checks fails.  


Check Length - Makes sure in text fields there is a length.  The length argument is passed to the function with the text and replaces sets the max length. 


Check Size - checks to make sure the user’s input is "Small", "Medium" or "Large"


Check Gender - checks to make sure the user’s input is "Male" or "Female" 


Date Format - Using stringfy, if the data cannot be formatted it will throw an error and will not be able to be input to the database


Booleans - default set to False unless the switch is activated to == "on" the  bool will then be True    


Check Extension - Checks the extension of the users upload to make sure it is allowed 


Not Valid Password - Checks to make sure password matches Regular Expression 


Not Valid Username - Checks to make sure username matches Regular Expression 


Not Valid Email - Checks to make sure the email address matches an email Regular Expression


Not Valid Text - Checks to make sure the text input is not just white spaces


Profanity Checker - Looks at a predefined list of curse words to check if the user has used any. The curse words can be added to at any time. They are within the varibles.py file in the variables folder in the main folder.  


### Front End Validation 

I have used the following attributes along with the [Materialize](https://materializecss.com/) class of validate to provide the user with front end validations
* minlength
* maxlength
* min
* max
* pattern
* type 
If any of these fail the box will turn red to show that it has not met the requirements.  I have used helper text and titles on hover to help the user pass both validations. 


***


##  Security

Username -  The username can only exist once in the database and at registration the username is checked against the current usernames

Passwords - The password must contact a mixture of uppercase and lowercase letters, digits, and a special character. It must be at least 8 characters long.  The password is salted and hashed using from [werkzeug.security](https://werkzeug.palletsprojects.com/en/1.0.x/utils/) when it is collected from the user.


Login - At login, the user must match their username/email to the correct password.  It will check to make sure that the password the user enters meets the check_password_hash.  If successful, the user will be assigned a session cookie.  If the user is unsuccessful then they will be notified that one of the fields is incorrect.  I have chosen not to notify the user which field is incorrect so that their details remain private and are harder to guess. 


Session Cookie - The user is assigned a session cookie on successful login.  This allows the user to navigate their own profile, add edit and delete information.  The user is not able to make any changes to pages that their session cookie does not match the username.  


Reset Password - If the user tries to reset their password, they are sent an email to the email address we have on file.  They are sent a random string temporary password and a link to the reset password page.  Once they have clicked the link, they will need to enter the username attached to the email address as an extra measure. 


Data Input - In the app.py the session user is compared with the username to see if that user can make changes. 
Most functions will find the details of the document to update using the session user’s cookie. This means even if the user manages to pass the front end security, they will only end up updating their own document. 
There are a couple of exceptions for example, delete/edit comments, delete images and delete profile.  This checks to see if the user is an author of the post or if the session user is admin (which can remove if necessary)  


***


## Features 


[FEATURES DOC ](docs/features.md)

Please see the testing document for a break down of the features


## Design 

## Skeleton 
Please see the [Features](#features) section for more information on what user actions are on each page 
Please refer to the [structure](#structure) to see the navigation and user pathways 

### Layout 

Initial Wireframe - 
![original](docs/wireframes/original.png)

I started working on the wireframe for the profile page first as this is where most of the site functionality would be.  The original wireframe is slightly different from the final one due to changing the WOOF Chat tab in the navigation to be comments on the user’s page instead.  This was because I decided to reduce the scope and include the live chat app functionality in a future release. 
The other difference is the size of the user’s image from spanning the entire width on desktop to taking half the width. The image still takes up the full width on smaller devices.  

Please see the [Wireframes](docs/wireframes) for the final wireframes


Please see [Mobile Site Images](docs/images/mobile-images) for images of each page of the application from a mobile view


Please see [Testing DOC](docs/testing.md) for a walk through of the site on a desktop



***

## Surface 

The colours I have used in web app closely resembles the colours used in the gifs/ images of the webapp.  I have chosen to go with a bright and fun colour scheme of yellow, off whites, dark blue/black, light blue, and soft pink.  The yellow and off-white colour combination of the dark blue for contrast have been used to make the features standout. Notes of slightly varying shades and opacity of blue and pink are used throughout the website to give subtle accents.  I have often used a slight difference in shade between cards and the profile containers to give a sense of depth.  

I often used the same colour as the images/gif for the background colour of elements to create a more cohesive user experience. 

![Colours](docs/images/colours.png)


### Typography
I have chosen to use a font from Google fonts I have used Montserrat. This font is a sans serif font which means it does not have decoration at the end of the letter. This can cause issues with readability seen in serif fonts. The Montserrat font playful and offers nice spacing between the letters as standard.

For headings I have increased the letter spacing, font weight and font size to make them stand out. 

I have used media queries to adjust the font so that the text is always easy to read. 

I imported using the following code at the top of my style.css file:

    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,800&display=swap');


### Call to Action
For the buttons and links (styled as buttons) I have changed the colour on hover. This is to show the user that the button can be clicked. For edit/add/login/register/navigation I have used yellow with dark writing, when hovered the colours switch.  For the delete/remove options the button starts red with light writing and then changes to black and yellow when hovered. 

On other clickable links, cards, and images I have used a more subtle call to action where the mouse changes to a cursor pointer to show the user the element can be clicked.

For the nav bar I have used a shading on the tabs to indicate they can be clicked. 


### Imagery

#### Background 
I designed the background image in [Canva](https://www.canva.com/) using a pawprint Icon. I have repeated this across the page and alternated the colour between a similar yellow to the navbar, blue and pink on a light-coloured background. 


![Paw Print](static/images/prints.png)

#### Profile image 
I designed the default profile image using [Canva](https://www.canva.com/) I gave the cartoon a transparent background and enclosed the image within a circle. 


![Profile Image](static/images/dog-avatar.png)

##### Icon
I created the Icon image in [Canva](https://www.canva.com/) using the same colours that have been used throughout the website, using the same image as the default profile image.  


![Icon](static/images/avatar-icon.png)

##### Bullet Points
For bullet points I have used a paw print found on [Canva](https://www.canva.com/) with a transparent background. These have been used on the Homepage, Safespaces Policy and Privacy Policy


![Paw](static/images/paw.png)

#### Homepage
[Homepage Image](https://www.freepik.com/free-photo/group-portrait-adorable-puppies_3532149.htm#page=1&query=puppy%20love&position=2)


For smaller devices I have cropped the image to include the first 3 dogs. 


#### Gifs


[Waiting Dog](https://dribbble.com/shots/6335402-Dog)

[Happy and Angry Dogs ](https://dribbble.com/imargarita)

[Delete Dog](https://dribbble.com/shots/4842912-Old-Dog)

[Reset Dog](https://dribbble.com/shots/3011370-This-is-my-dog-Meshi)

[Break Dancer(Human)](https://dribbble.com/shots/13996136-Breakdance)

[Dog Walk](https://dribbble.com/shots/7189098-Walking-dog)

[Group Dogs](https://dribbble.com/shots/6539601-)

[Space Puppy](https://dribbble.com/shots/4382758-Puppy-Day)

#### Error Pages
[Dog Barking](https://dribbble.com/shots/2652719-barking-up-the-wrong-tree)

#### Sizing 
To ensure the application was fully responsive I chose not to set a height and width for more user images.  I mostly used them as background images and filled the space. This does mean on some screens the images are zoomed in and it would be nice to add the option for users to crop their images as a future feature. This could be by utilising Cloudinarys transitions on input. 


***


## Technologies
#### Languages & Frameworks 
* HTML5 - Mark-up language using semantic structure.
* CCS3 - Cascading style sheet used to style.
* JavaScript - Programming language.  
* Python - Programming language
* [Flask](#flask) - Framework + Extensions
* [Materialize](https://materializecss.com/) - CSS Framework for structure, buttons, and some styling
* [jQuery](https://jquery.com/) - Materialize initialising
* Gitpod.io - for writing the code. Using the command line for committing and pushing to Git Hub
* GitHub - hosting repositories
* GIT - Pushing code to repositories

#### Front End
* [Google fonts](https://fonts.google.com/)  - for the font
* [Font Awesome](https://fontawesome.com/) - for icons used
* [Canva](https://www.canva.com/)- Designing the background, default image and Icon

#### Backend 
* [MongoDB](https://www.mongodb.com/)
* [Heroku](https://dashboard.heroku.com/)
* [Cloudinary](https://cloudinary.com/)

#### Helpers
* [Beautifier](https://beautifier.io/) - for helping to keep code tidy 
* [Random Key Gen](https://randomkeygen.com/)
* [Power Mapper](https://www.powermapper.com/) to check for browser compatibility
* [Temp Mail](https://temp-mail.org/en/)

#### Planning
[Miro](https://miro.com/app/dashboard/) - for planning of site flow, creating wire frames and general mind mapping

### Flask
The application was built using the [Flask](https://flask.palletsprojects.com/en/1.1.x/) Framework which is reliant on the [Jinja](https://www.palletsprojects.com/p/jinja/) templating language. The application was written in python. 

I used the following Extensions:
* [Flask Mail](https://pythonhosted.org/Flask-Mail/) - For emailing users
* [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) - For interacting with the MongoDB database
* [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/utils/) - For providing security’s, password_hash, check_password_hash


#### Testing Tools
* [HTML Validator](https://validator.w3.org/) - checking the validity of code
* [CSS Validator](https://validator.w3.org/) - checking the validity of code
* [JSHint](https://jshint.com/)- Testing and checking JS.  - checking for errors in code
* [Pep8 Online](http://pep8online.com/) - Testing and checking PEP8 compliance 
* [Am I Responsive](http://ami.responsivedesign.is/#) - checking whether the site is responsive. 
* [Internet Marketing Ninjas](https://www.internetmarketingninjas.com/online-spell-checker.php) - spell check
* [Python Tutor](http://pythontutor.com/) - For function testing 
* [Studio 3T](https://studio3t.com/) - Testing Database Schema 
* [Regrex101](https://regex101.com/r/OnE0BG/1/) - Testing Regrex Patterns
* DEV Tools - Lighthouse


***
#### Technology Configuration

#### MongoDB 

[MongoDB](https://www.mongodb.com/) was used as the database to store the users details to set up MongoDB follow the steps below

* Sign up to MongoDB
* Create a new shared Cluster
* Select a Cloud provider and region (I used AWS and Ireland)
* For free use  m0 cluster tier
* Give your cluster a name
* Go to collections and add a database
* Go to database access and add a username and password

Connecting - via application
* Go back to the cluster overview
* Click the CONNECT button.
* Select 'connect your application'
* Select your language/ driver (I used Python 3.6 or later)
* Copy the connection string and change the details. 
* Set the cluster name, collection name, URI connection string and password as environmental - see [Configuration](#Configeration) to set up your application configurations


### Cloudinary 
[Cloudinary](https://cloudinary.com/) is an Upload API and image store
I added cloudinary to my application using the following steps:
* Create a Cloudinary Account, I called mine PuppyPlaymates
* Configure your env.py file with the Cloud name, API Key and API Secret - see [Configuration](#Configeration) to set up your application configurations
![Cloudinary config](docs/images/cloudinary.png)
* Set up a folder to store your images, I called mine user_images
* Go to settings in the top right 
* Click the upload section in settings:
    * Create an upload preset with a name of your choice
    * Set it as unsigned
    * Use filename or externally defined public ID : true 
    * Unique filename: false 
    * Delivery type: 
    * Upload Access mode: public

 ![Preset Image](docs/images/upload-preset.png)   

When a user uploads, I used the following code to create the correct path and upload to cloudinary. I have chosen to transform all the files to a low-quality image to reduce the rendering time. 
        
        filename = secure_filename(item.filename)
        filename, file_extension = os.path.splitext(filename) 
        public_id = (<username> + '/q_auto:low/' + <filename>)

        cloudinary.uploader.unsigned_upload(
                            item,
                            <upload_preset>,
                            cloud_name=<cloud_name>,
                            folder='/user_images/',
                            public_id=public_id)

I then saved the full URL for that image into the MongoDB database.  I saved the base cloudinary URL in my variables folder and added the public_id to the end. The base URL is in the dashboard of your cloudinary account. I specified the folder in my URL string 

        cloudinary_url = ('https://res.cloudinary.com/puppyplaymate/image/upload/user_images/')

### Flask Mail 
I have chosen to use Gmail as my mail provider alongside [Flask Mail](https://pythonhosted.org/Flask-Mail/) to send mail to users from within the app. 
You will need to ensure you set your email provider up  to Allow less secure apps otherwise Gmail will block you being able to send/receive emails through the application.  
You will also need to enable IMAP as well.  You can find some helpful tips [Flask Mail Help](https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html)
I have used Gmail’s smtp server.  -  see [Configuration](#Configeration) to set up your application configurations


***

## Testing 

[TESTING DOC ](docs/testing.md)

Please see the testing document for Testing


***


## Deployment 

### Configuration 
Beneath your imports you will need to configure your app.py file.  You will need to import your local env.py for local environments.  For [configuration for Heroku](#deploying). 

Configure as follows:

        if os.path.exists('env.py'):
            import env


        app = Flask(__name__)

        app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
        app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
        app.secret_key = os.environ.get('SECRET_KEY')
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )

        app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
        app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
        app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
        app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

        mongo = PyMongo(app)
        mail = Mail(app)

To start your application, you will need to user the following at the bottom of your app.py file. You will need to ensure that debug=False prior to deployment.

        if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
                    port=int(os.environ.get('PORT')),
                    debug=False)

You will need to add a Procfile and ensure your requirements.txt are up to date. 
In your root folder in the terminal type - touch Procfile -  this will create a Procfile
Add the following with the following 
    web: python app.py

To install the requirements.txt use the following command in the terminal command line
    pip3 install -r requirements.txt



#### Local Environment
Create env.py file in the same file system.  In your route folder type - touch env.py - to create the file. 
Your virtual configurations should look similar to this. You will need to create a SECRET_KEY and input the IP and PORT settings. I used [Random Key Gen](https://randomkeygen.com/).

        import os

        # App config
        os.environ.setdefault("IP", "0.0.0.0")
        os.environ.setdefault("PORT", "5000")
        os.environ.setdefault("SECRET_KEY", "<Your secret key>")

        # MongoDB config
        os.environ.setdefault(
            "MONGO_URI", "mongodb+srv://<user>:<password>@<project>.af8bz.mongodb.net/<database>?retryWrites=true&w=majority")
        os.environ.setdefault("MONGO_DBNAME", "<database>")

        # Cloudinary config
        os.environ.setdefault("CLOUDINARY_CLOUD_NAME", "<Your cloud name>")
        os.environ.setdefault("CLOUDINARY_API_KEY", "<Your API Key>")
        os.environ.setdefault("CLOUDINARY_API_SECRET", "<Your Secret Key>")

        # Mail config
        os.environ.setdefault('MAIL_SERVER', 'smtp.gmail.com')
        os.environ.setdefault("MAIL_PORT", "465")
        os.environ.setdefault("MAIL_USE_SSL", "True")
        os.environ.setdefault("MAIL_USE_TLS", "False")
        os.environ.setdefault("MAIL_USERNAME", "<Your email>")
        os.environ.setdefault("MAIL_PASSWORD", "<Your email password>")
        os.environ.setdefault("MAIL_DEFAULT_SENDER", "<Your email>")



### Adding and Committing files

To add files to the repository, take the following steps

In the command line type -
        git add .  
        git commit -m "This is being committed"
        git push

To add all new files or modified file use " ."  - To add a single file, use the pathway to the file eg .index.html  or assets/css/style.css
When committing make sure your comments are clear about what changes have been made. 
Pushing will send your work to the repository


### Deploying 
Requirements for deploying:
* Cloudinary Account
* MongoDB Account
* Heroku Account
* Email account

Deploying to [Heroku](https://dashboard.heroku.com/)

* You will need to sign up to [Heroku](https://dashboard.heroku.com/)
* Once logged in click the create new app button
* Select the region closest to you and give the APP a name
* Set your deployment method to 'GitHub'
* Connect to GitHub and login
* Search for the repository you wish to deploy from
* You will need to head to settings and click 'Config Vars'
    * You will now need to set up your Configuration Vars the same way as you did for your env.py
![Config Vars](docs/images/config.png)    
* Make sure you have set up your Procfile and you have updated the requirements.txt prior to deploying    
* Click the deploy tab and go to manual deploy
* Select the branch you wish to deploy and deploy the application
* Once it is deployed you will be able to view the app
* You can set it to automatically deploy every time you push to the repository by enabling the Automatic deploys


### Forking

Forking the GitHub Repository

By forking the GitHub Repository, you can make a copy of the original repository in your own GitHub account.  This means we can view or make changes without making the changes affecting the original.

* Log into GitHub and locate the GitHub Repository.
* At the top of the Repository there is a "Fork" button about the "Settings" button on the menu.
* You should now have a new copy of the original repository in your own GitHub account.
* You will need to install the requirements.txt using the following command the command line
        pip3 install -r requirements.txt
* You will need to set up your local environments and key value pairs for deployment

### Cloning 

Making a Local Clone

* Log into your GitHub then find the gitpod repository
* Under the repository name there is a button that says, "Clone or download". Click on this button.
* If cloning with HTTPS "Clone with HTTPS", copy this link.
* Open Gitbash
* Change the current working directory to the location where you want the cloned directory to be.
* Type git clone, and then paste the URL you copied earlier.

        $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
        Press - Enter- Your local clone will be created.
        $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
                > Cloning into `CI-Clone`...
                > remote: Counting objects: 10, done.
                > remote: Compressing objects: 100% (8/8), done.
                > remove: Total 10 (delta 1), reused 10 (delta 1)
                > Unpacking objects: 100% (10/10), done.
[Click Here](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository) for more info on cloning. 

You will need to install the requirements.txt using the following command the command line
        pip3 install -r requirements.txt
* You will need to set up your local environments and key value pairs for deployment and running the application in your local environment. 


*** 

## Known Bugs 

Using the [Materialize](https://materializecss.com/) validate class it validates the field on focus out rather than on change.  With more time I would write my own validation class to work on change or key up so the fields would validate quicker for the user. 


***

## Acknowledgements
### Credit

##### People 
* Brian Macharia- Mentor support, guidance, tips, and key things to look out for throughout the project. Helping me to check for errors and looking at my code. 
* Matt Rudge - Template for gitpod.io 
* Anthony Lomax - Code Review, Testing, and support
* Callum Hewitt - Testing website, review, inspiration, and discussions
* Rob Beaney - Front End recommendations and discussions 

##### Additional Testers
* William Hone
* Harry Smith
* David Savage
* Ciaran Concannon
* Coding Novas Team 
* Double Shamrock Team


##### Tools and Docs
* [Code Institute SampleREADME](https://github.com/Code-Institute-Solutions/SampleREADME)
* [Code Institute README Template](https://github.com/Code-Institute-Solutions/readme-template)
* [W3schools](https://www.w3schools.com/) - for various code information and trouble shooting.
* [solution to truncate found here](https://stackoverflow.com/questions/11989546/wrap-a-text-within-only-two-lines-inside-div) 
* [Help to build age check](https://www.geeksforgeeks.org/python-program-to-calculate-age-in-year/)
* [GitHub Emoji for Markdown](https://gist.github.com/rxaviers/7360908)
* [Flask Mail Help](https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html)
* [Load more content](https://codepen.io/elmahdim/pen/sGkvH)

For all technologies used head to [Technologies](#technolgies)

*** 


### Code: 
I have used Materialize for some of my front-end styling and JavaScript. 
Please see the code below it initialise the Materialize functions using jQuery altered 

    $(document).ready(function () {
        $(".button-collapse").sideNav();
        $('select').material_select();
        $('.chips').material_chip();
        $('.collapsible').collapsible();
        $('.modal').modal({
            // inDuration: 500
        });
        $('.datepicker').pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15, // Creates a dropdown of 15 years to control year,
            today: 'Today',
            clear: 'Clear',
            close: 'Ok',
            closeOnSelect: false, // Close upon selecting a date,
            container: undefined, // ex. 'body' will append picker to body
        });

    });

### Content:
I asked users to create profile, most of the profiles have been created by test users, friends, and family. The images they have used are of their own dogs or from the internet. 

Code & Content (not already attributed): Rebecca Kelsall


***

## Inspiration and Research:
The vast majority of research focused on Social Media website and Dating applications.  Such as :
* [Facebook](www.facebook.com)
* [Bumble](https://bumble.com/)
* [Instagram](https://www.instagram.com/)

I also looked at the following sites related to dogs or dating for dog lovers
* [Pet Lover](https://www.petloversdatingonline.com/uk/?utm_source=bing&utm_campaign=petldo+uk+modified+ma&utm_term=%2Bdog%20%2Bdating&msclkid=151435a0e1151c0cb9ba552b10b4c6c1)
* [Waggel](https://www.waggel.co.uk/)
* [Doggy Dating Agency](https://doggydatingagency.com/)
* [Doggy Date](http://www.doggydate.com/)
