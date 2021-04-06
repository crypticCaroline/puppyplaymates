


## Currently still under development and in testing

# Puppy Playmates 
![Main Mockup](readme_docs/playmates.png)

[Link to Live Website](https://puppy-playmates.herokuapp.com/)

[GitHub Repo](https://github.com/crypticCaroline/puppy-playmates)

*** 

## About  
Welcome to Puppyplaymates, a webapp to help dogs find love! 
This is a Python Flask app using MongoDB, cloudinary and Flask Mail to produce a social media style application.

PuppyPlaymates currently brings users together and allows them to get in contact with the pups they love! The application lets the users create a profile that allows them to add their dogs’ details, add photos, let other users know when the next walk with their dog is happening, add comments both public and private and add likes on other profiles.  The site offers the additional functionality, reset passwords, change passwords, reporting other users, contact us, editing and deleting comments, backend validation, profanity checking and birthday checking. Please look at the [features](#features) section for a more detailed description. 
The application has a lot of room for growth and a list of future features to implement. 

## Index – Table of Contents

* [User Experience (UX)](#user-experience) 
* [Features](#features)
* [Designs](#designs)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Known Bugs](#known-bugs)
* [Deployment](#deployment)
* [Acknowledgements](#credit)

*** 

## User Experience (UX)
## Strategy
With PuppyPlaymates I wanted to be able to give dog owners a way to communicate with other dog owners in a fun and safe way. By combining social media and data profile principles I have created a playmate finding service dedicated to human’s best friend.

### User Stories 

#### Reasons a user may visit the website
* A dog owner is looking for a playmate for their dog
* A dog owner is looking to chat to other dog owners
* A dog owner is looking to find puppy love for their dog

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
*Can Add Edit/ Delete info to my profile
    * Add/Edit Dog Information 
    * Add/Edit/Delete Images
    * Add/Edit/Delete Comments
    * Add/Edit/Delete Walk Information
* Can view other dog profiles
    * Add/Edit/Delete Comments 
    * Like other users’ profiles so I can find them again
* Can report users who make me feel uncomfortable 
* Add/Edit/Delete Events (outside current scope)
* Chat abilities (outside current scope)

#### As a developer / business I expect:
* To provide an easy-to-use website
* To enable users to communicate
* Add/Edit/Delete Images, Comments, Walk information


## Structure
The diagram below is of the information architecture of the Web App.  This shows the journeys the users can take throughout the website. Please see the [Features](#features) section to for more information on what user actions are on each page 
![Site Structure](readme_docs/structure.png)




## Designs

## Surface

#### Colour



#### Typography 



#### Call to Action


### Imagery   



***

## Skeleton 
Please see the [Features](#features) section to for more information on what user actions are on each page 
Please refer back to the [structure](#structure) to see the navigation and user pathways 


### Layout 

#### Homepage Wire Frame 


***

### Mockup
#### Home Page
#### form Pages
#### profile page
#### playmates 



## Features

#### Universal Features Across the Site

### Responsiveness

The website is fully responsive between different screen resolutions.  I have done this by using media queries, containers, rows and columns. I have chosen to hide the GIF images on small devices.  

### Accessibility

### Input Fields 

* Text Input Fields -Type specific and have validate patterns that have to match, they are also set with min and max length to ensure that the right data is entered. I have used the materialize validate class to turn the input box green when the field is valid, else the form will not be submitted. 
* Validators - I have used back-end validation as a fail-safe to check if the input matches the same pattern on the front end.  If it does not match the pattern, then the user will get a flash message explaining that it is not a valid input.  
* Profanity - At the same time the text input is passed through a profanity checker to check from a pre-set list of words to see if any of the words match.  If they do match, then the user will get a flash message asking them to refrain from using profanity and will not submit the message to the database.
* Date – I have created a JavaScript function to check the current date and limit the date options:	
    * DOB – the dog cannot have a future Dob and I have also limited the age of the dog to 20 years 
	* Upcoming walks – can be set to have the date from today onwards but not be set in the past. 


### Base Templates 

The base template is formed of the Meta Data, Navigation, and Footer.  The block content is rendered in between the navigation and footer.  The page description is also changed for each page. 
    #### Nav
    The Navigation Bar is at the top of the webpage. If the user is signed in, they have navigations to their Profile Page, Playmates and Sign Out. If a user is not logged in the user will view Login and Register. All change colour when they are hovered over. The active page is slightly lighter, so the user knows what page they are on.  The nav links direct the user to the correct page of the website. When the logo is clicked on it will take the user to the homepage. 
    #### Footer
    The footer consists of the company moto on the left-hand side and on the right the user can find more internal links.  If the user is logged in, they will see Contact Us, Report User, Change Password, Delete Account, Privacy Policy and Safe Spaces Policy and Sign Out. If the user is not logged in, they will be able to view Contact Us, Sign In, Register, Privacy Policy and Safe Spaces Policy.  
    ##### Meta data
    I have added keywords, author, and description to the meta data to make the website easier to find.  This increases traffic to the website.  I have also given each page a different name, so the user knows which tab they are on. 


### Error Pages 
    #### 404 
     * If the user is signed in, they will get a message that they are barking up the wrong tree and a button to take them back to their profile 
     * If the user is not signed in the button will take them back to the homepage

    #### 500 
    * If there is an internal server error the user will be shown a message to say the account may no longer be active (if the account has been deleted) or the profile is incomplete if it is their own profile and they didn't complete registration fully then they will be able to click the Build profile button to take them back to finish the set up. 
    * They will also get button to take them back to their profile if they are a session user and back to the homepage if not. 

    #### Not Session 
    * If the user does not have a session cookie then they will be redirected to the log in page with a flash message advising that they need to be logged in to view that page. 

    #### Flash Messages
    * Flash messages are displayed toward the top of the pages and includes a soft pink banner to alert users to the text they contain 


#### Features Specific to Pages

Please refer to the [structure](#structure) to see the navigation and user pathways 
### Profile 
    #### Profile Content
        * Like/ dislike overlay gif - adds to Admire/Pups I Admire when Session User not the Profile owner 
        * Birthday Display - if it’s the profiles dog birthday a cake will appear in the top right of profile
        * Profile Image - Displays users’ image - if profile owner when clicked toggles Edit Images Modal
        * Profile Bio/ dog details 
            * Displays user bio details - if profile owner when Edit Puppy button clicked toggles - Edit Profile Modal
            * Age is worked out from the profile users DOB and todays date using the check_date() function.
            * If the profile owner has specified, they are looking for a romantic match for their dog it will show in the profile as looking for Puppy Love and will have an Icon of a heart. Else it will render that they are looking for platonic playmates
            * If the profile owner has had their dog neutered or spade then the template will render "I have had the snip" and a pair of scissors. Else the profile will read "I've still got all my puppy making parts"
        * Profile Human - displays human info - when Edit Human button clicked toggles - Edit Human Modal
        * Walks - Displays next walk - when update clicked toggles - Add Walk Modal 
        * Images - user a loop to display all images in users image array
            * Lets users horizontal scroll through other users’ photos.
            * If profile owner when update images clicked toggles Edit Images Modal
            * When image clicked upon triggers a large image view in a Modal  
        * Admire - displays dogs that have liked the page, adds an object containing the likers - image, name and URL to the array and then adds the profile liked to the users Pups I love. 
        * Comments - uses a loop to go through the comments array in the database and shows newest at the top and adds edit and delete buttons to each comment and create individual modals dynamically 
            * Displays all comments on user profile 
            * If private only the author and user of that profile can see the message. 
            * The user of that profile can delete any message, and this will toggle delete comment Modal.  The author of the comment can edit their comments and when clicked the author can either edit or delete their own comment. The comments are displayed with the authors image, name, and a time stamp. 
        * Add Comment - all users can add comments and select whether they make them a private message. 

    #### Edit Modals 

        * Add Walk - brings up a form so the user can add a walk to their profile 
        * Edit Profile - Brings up a form to allow the user to change some of the dog’s details 
        * Edit Images –
* Uses a loop to create a card for each image and builds a make profile picture and delete image button.
* Enables user to upload a new image and give them the option to make it the profile image straight away – ( The image is uploaded to a cloudinary and a URL string is created and added to mongodb)
        * Edit Human - brings a form up so users can enter the human name and bio 
        * Image Modal - modal which displays a larger version of the image the user had added 
        * Edit Comment - allows authors to edit comments also renders a button to delete the comment as well
        * Delete Comment - allows authors or profile owners to delete comment. If the profile owner, it also brings up button to report user if comment makes them feel uncomfortable. 

### Playmates 
    #### Display - 
    * Uses a loop to build individual cards for each user containing:
        * Dog name
        * Dog profile photos
        * First 3 lines of dog description
        * If looking for love displays a heart icon
        * If neutered or spade displays a scissor icon 
        * Each card is clickable and take the user to that full profile if logged in, else send them to log in page with a flash message
    #### Search  
    * Allows user to search for other dogs by breed, size, location, gender, and name.

### Homepage
* Displays information about the company and the steps to create an account
* Shows a button so potential users can see the playmates section of the web app but when clicked on will prompt them to login

### Login
* The login page consists of the username/email and password fields
* A link to reset password 
* A link to register an account
* Checks that the login is valid and there is a profile else advises user that one or both fields are incorrect

### Register
* Create profile form - containing field for username, email, password, and repeat password.
* Checks to see if username or email already exists and will render a flask message if they do.
* Check to make sure passwords match 
* Checks validity of fields
* If all valid on submit will add the user to the database, add a session cookie using the username and direct them to build their profile.

### Build Profile 
* Allows users to fill out the rest of the following dogs’ details:
    * Name 
    * DOB
    * Size 
    * Breed
    * Preferences for platonic or love
    * Spade of Neutered 
    * Description
* Allows the user to add their name and description
* Input fields are put through a validator to check they are acceptable and text fields are put through the profanity filter     

### Form Pages - Contact Us - Register - Reset Password - Change Password - Build Profile 

### Delete Account 

### Future Features 

Below is a list of future features I would like to add into PuppyPlaymates 

* Maps - shows dogs by nearest location on the playmates page 
* Pagination on the playmates page 
* Preferences - multi search queries on playmates page 
* Ability to add multiple dogs to one human profile 
* Use a database call to render up to date photos on comments/ liker rather than using the image at time of posting.  
* Showcase all walk/events - option to promote your walk or keep it just on your profile  
* Keep a track of previous walks in another section of the profile page 
* Pagination for comments 
* Add a data store for all comments that are posted for safeguarding purposes.  If a user deletes or edits their comments, they will be stored on the database in a separate collection along with their username, time stamp, email address. This would be for the purpose of safeguarding so if the comments violate the safe spaces policy then action can be taken against the user. 
* Add all deleted accounts/emails to a separate nonuser visible collection - this would give the ability to ban certain users/email addresses if policies were violated. 
* Continue working on the profanity 
***

## Technologies Used 

* HTML5 - Mark-up language using semantic structure.
* CCS3 - Cascading style sheet used to style.
* JavaScript - Programming language.  
* Python
* Flask 
* Gitpod.io - for writing the code. Using the command line for committing and pushing to Git Hub
* GitHub - hosting repositories
* GIT - Pushing code to repositories
 
Design 

Front End
* [Google fonts](https://fonts.google.com/)  - for the font
* [Balsamiq wireframe](https://balsamiq.com/)  - for creating the wireframes
* [Beautifer](https://beautifier.io/) - for helping to keep code tidy


Backend 
https://miro.com/app/board/o9J_lTewBto=/
mongodb
herouku 
Testing 
* [HTML Validator](https://validator.w3.org/) - checking the validity of code
* [CSS Validator](https://validator.w3.org/) - checking the validity of code
* [JSHint](https://jshint.com/)- Testing and checking JS.  - checking for errors in code
* [Am I Responsive](http://ami.responsivedesign.is/#) - checking whether the site is responsive. 
* [Wave](https://wave.webaim.org/) - accessibility testing
* [Internet Marketing Ninjas](https://www.internetmarketingninjas.com/online-spell-checker.php) - spell check
* DEV Tools - Lighthouse

***

## Testing 

[TESTING DOC ](readme_docs/testing.md)

Please see the testing document for Testing logs 






## Deployment 

### Adding and Committing files

To add files to the repository take the following steps

In the command line type -
        git add .  
        git commit -m "This is being committed"
        git push

To add all new files or modified file use " ."  - To add a single file use the pathway to the file eg .index.html  or assets/css/style.css
When committing make sure your comments are clear about what changes have been made. 
Pushing will send your work to the repository

### Deployment 

The project was deployed with the following steps


### Forking

Forking the GitHub Repository


By forking the GitHub Repository, you can make a copy of the original repository in your own GitHub account.  This means we can view or make changes without making the changes affecting the original.

* Log into GitHub and locate the GitHub Repository.
* At the top of the Repository there is a "Fork" button about the "Settings" button on the menu.
* You should now have a new copy of the original repository in your own GitHub account.

### Cloning 

Making a Local Clone

* Log into your GitHub then find the gitpod repository
* Under the repository name there is a button that says "Clone or download". Click on this button.
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

## Known Bugs 


***

## Acknowledgements


### Credit

* Brian Macharia- Mentor support, guidance, tips, and key things to look out for throughout the project. Helping me to check for errors and looking at my code. 
* Matt Rudge - Template for gitpod.io 
* [Code Institute SampleREADME](https://github.com/Code-Institute-Solutions/SampleREADME)
* [Code Institute README Template](https://github.com/Code-Institute-Solutions/readme-template)
* [W3schools](https://www.w3schools.com/) - for various code information and trouble shooting.
* [Google fonts](https://fonts.google.com/) - CDN for the fonts were used in the project.
* [Balsamiq wireframe](https://balsamiq.com/) - To build wireframes in the design phase. 
* [HTML Validator](https://validator.w3.org/) - Testing validity of HTML.
* [CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) -Testing validity of CSS.
* [JSHint](https://jshint.com/)- Testing and checking JS. 
* [Am I Responsive](http://ami.responsivedesign.is/#) - Checking the responsive nature.
* [Beautifer](https://beautifier.io/) - Allowing me beautify my code.
* [HTML Online](https://html-online.com/articles/smart-404-error-page-redirect/) - Redirect page Inspiration
* [Coolors](https://coolors.co/palettes/trending) - colour inspiration
* [Internet Marketing Ninjas](https://www.internetmarketingninjas.com/online-spell-checker.php) - spell check
* /* solution to truncate found here-  https://stackoverflow.com/questions/11989546/wrap-a-text-within-only-two-lines-inside-div */



*** 


### Code:




### Content:

Code & Content (not already attributed): Rebecca Kelsall

### Inspiration & Research: 

