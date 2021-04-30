## Features Table of Index

- [Features](#features)
  * [Responsiveness](#responsiveness)
  * [Accessibility](#accessibility)
  * [Flash Messages](#flash-messages)
  * [Input Fields](#input-fields)
  * [Base Templates](#base-templates)
    + [Nav](#nav)
    + [Footer](#footer)
      - [Meta data](#meta-data)
  * [Error Pages](#error-pages)
    + [404](#404)
    + [500](#500)
    + [403](#403)
    + [Not Session](#not-session)
- [Features Specific to Pages](#features-specific-to-pages)
  * [Profile](#profile)
    + [Profile Content](#profile-content)
    + [Admin](#admin)
    + [Edit Modals](#edit-modals)
  * [Playmates](#playmates)
    + [Display](#display)
    + [Search](#search)
  * [Homepage](#homepage)
  * [Delete Account](#delete-account)
  * [Safe Spaces Policy](#safe-spaces-policy)
  * [Privacy Policy](#privacy-policy)
  * [Form Pages](#form-pages)
  * [Login](#login)
  * [Register](#register)
  * [Build Profile](#build-profile)
  * [Contact Us](#contact-us)
  * [Report User](#report-user)
  * [Reset Password](#reset-password)
  * [Change Password](#change-password)
- [Future Features](#future-features)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


***

## Features

#### Universal Features Across the Site

### Responsiveness

The website is fully responsive between different screen resolutions.  I have done this by using media queries, containers, rows, and columns. I have chosen to hide the GIF images on small devices.  

### Accessibility

* Used bright colours with high contrast throughout the website.  
* Used meaningful aria-labels where appropriate to ensure ease of use with a screen reader. 
* Used auto-completes for new-password and current-password to help screen readers navigate and prompt users.  
* Used headings to help users navigate the website.  
* Ensured that the logo has an aria-label of 'Home' to make navigation easier. 

### Flash Messages
Flash messages are displayed toward the top of the pages and includes a soft pink banner to alert users to the text they contain when the  


### Input Fields 

* Text Input Fields -Type specific and have validate patterns that have to match, they are also set with min and max length to ensure that the right data is entered. I have used the materialize validate class to turn the input box green when the field is valid, else the form will not be submitted. 
* Validators - I have used back-end validation as a fail-safe to check if the input matches the same pattern on the front end.  If it does not match the pattern, then the user will get a flash message explaining that it is not a valid input.  
* Profanity - At the same time the text input is passed through a profanity checker to check from a pre-set list of words to see if any of the words match.  If they do match, then the user will get a flash message asking them to refrain from using profanity and will not submit the message to the database.
* Date – I have created a JavaScript function to check the current date and limit the date options:	
    * DOB – the dog cannot have a future Dob and I have also limited the age of the dog to 20 years 
	* Upcoming walks – can be set to have the date from today onwards but not be set in the past. 


*** 

### Base Templates 

The base template is formed of the Meta Data, Navigation, and Footer.  The block content is rendered in between the navigation and footer.  The page description is also changed for each page. 
#### Nav
The Navigation Bar is at the top of the webpage. If the user is signed in, they have navigations to their Profile Page, Playmates and Sign Out. If a user is not logged in the user will view Login and Register. All change colour when they are hovered over. The active page is slightly lighter, so the user knows what page they are on.  The nav links direct the user to the correct page of the website. When the logo is clicked on it will take the user to the homepage. 
#### Footer
The footer consists of the company moto on the left-hand side and on the right the user can find more internal links.  If the user is logged in, they will see Contact Us, Report User, Change Password, Delete Account, Privacy Policy and Safe Spaces Policy and Sign Out. If the user is not logged in, they will be able to view Contact Us, Sign In, Register, Privacy Policy and Safe Spaces Policy.  
##### Meta data
I have added keywords, author, and description to the meta data to make the website easier to find.  This increases traffic to the website.  I have also given each page a different name, so the user knows which tab they are on. 


*** 

### Error Pages 
#### 404 
* If the user is signed in, they will get a message that they are barking up the wrong tree and a button to take them back to their profile 
* If the user is not signed in the button will take them back to the homepage

#### 500 
* If there is an internal server error the user will be shown a message to say  the error has occurred.
* They will also get button to take them back to their profile if they are a session user and back to the homepage if not. 

#### 403

* Access forbidden with a note to advise the user they cannot see the page
* If the user is signed in, they will get a button to take them back to their profile 
* If the user is not signed in the button will take them back to the homepage


#### Not Session 
* If the user does not have a session cookie, then they will be redirected to the log in page with a flash message advising that they need to be logged in to view that page. 


***

## Features Specific to Pages

### Profile 
#### Profile Content
* Like/ dislike overlay gif - adds to Admire/Pups I Admire when Session User not the Profile owner 
* Birthday Display - if it is the profiles dog birthday a cake will appear in the top right of profile
* Profile Image - Displays users’ image - if profile owner when clicked toggles Edit Images Modal
* Profile Bio/ dog details: 
    * Displays user bio details - if profile owner when Edit Puppy button clicked toggles - Edit Profile Modal
    * Age is worked out from the profile users DOB and today’s date using the check_date() function.
    * If the profile owner has specified, they are looking for a romantic match for their dog it will show in the profile as looking for Puppy Love and will have an Icon of a heart. Else it will render that they are looking for platonic playmates
    * If the profile owner has had their dog neutered or spade then the template will render "I have had the snip" and a pair of scissors. Else the profile will read "I've still got all my puppy making parts"
* Profile Human - displays human info - when Edit Human button clicked toggles - Edit Human Modal
* Walks - Displays next walk - when update clicked toggles - Add Walk Modal 
* Images - user a loop to display all images in users image array
    * Lets users horizontal scroll through other users’ photos.
    * If profile owner when update images clicked toggles Edit Images Modal
    * When image clicked upon triggers a large image view in a Modal  
    * The most recent images are shown first
* Admire - displays dogs that have liked the page, adds an object containing the likers - image, name and URL to the array and then adds the profile liked to the users Pups I love. 
* Comments - uses a loop to go through the comments array in the database and shows newest at the top and adds edit and delete buttons to each comment and create individual modals dynamically 
    * Displays all comments on user profile 
    * If private only the author and user of that profile can see the message. 
    * The user of that profile can delete any message, and this will toggle delete comment Modal.  The author of the comment can edit their comments and when clicked the author can either edit or delete their own comment. The comments are displayed with the authors image, name, and a time stamp. 
    * The page shows 5 comments to start with.  If there are more comments, then when you click how more it will reveal further comments.
* Add Comment - all users can add comments and select whether they make them a private message. 
* Up toggle so the user can navigate back to the top of the page



#### Admin
* If the user is admin, they will be able to delete any comment on the site, delete images and delete profiles if they feel like there has been inappropriate behaviour.   
* When visiting the admin profile, instead of the above there are buttons that sends the user to contact us, report and back to profile 


#### Edit Modals 

* Add Walk - brings up a form so the user can add a walk to their profile:
    * The date can only be set from today date onwards as past dates are not useful

* Edit Profile - Brings up a form to allow the user to change some of the dog’s details 
    * Not all details can be changed such as the Name, Gender and DOB as this should not change for the dog.  The user can rebuild their whole profile using the rebuild profile navigation in the footer and can also be directed to the build_profile page from the delete page where they are offered the chance to add change all the dog details.
    *  The fields are prefilled out with the users details from accessed from the database
* Edit Images 
    * Uses a loop to create a card for each image and builds a make profile picture and delete image button.
    * Enables user to upload a new image and give them the option to make it the profile image straight away – ( The image is uploaded to a cloudinary and a URL string is created and added to MongoDB)
    * The upload tab is held within a collapsible, so it does not take up the entire space of the modal
    * The file extension is checked prior to upload and only allow if jpg, png, gif and jpeg
    * If the image is set as the profile image, when is it deleted the default avatar replaces the profile image
    * If the image is not the profile image, then a button will appear to make it the profile image
* Edit Human - brings a form up so users can enter the human name and bio 
* Image Modal - modal which displays a larger version of the image the user had added 
* Edit Comment - allows authors to edit comments also renders a button to delete the comment as well
* Delete Comment - allows authors or profile owners to delete comment. If the profile owner, it also brings up button to report user if comment makes them feel uncomfortable. 


### Playmates 
#### Display 
* Uses a loop to build individual cards for each user containing:
    * Dog Name
    * Dog Profile Photos
    * First 3 lines of dog description
    * Dogs Gender
    * If looking for love displays a heart icon
    * If neutered or spade displays a scissor icon 
    * Each card is clickable and take the user to that full profile if logged in, else send them to login page with a flash message
    * I have used a See More button at the button of the page so the user can click to reveal the next group of dogs.  If there are no more dogs the button will disappear. This will help to reduce load time for the user and provides a better UI experience. 
    * There is an up arrow on the right-hand side then when clicked will take the user back to the top of the page. 

#### Search  
* Allows user to search for other dogs by breed, size, location, gender, and name.

### Homepage
* Displays information about the company and the steps to create an account
* Shows a button so potential users can see the playmates section of the web app but when clicked on will prompt them to login

### Delete Account 
* Button to take user back to their profile
* Button to ask if the user wants to change their dogs’ details - this will take them back to build profile and allows the user to change all the details. 
* Button to delete their profile that triggers the modal
* Delete Modal helps to stop users accidentally deleting their accounts
*  The entire document will be added to the archives in case of accidental removal


### Safe Spaces Policy
Shows the user the company Safe Spaces Policy 

### Privacy Policy 
Shows the user the company Privacy Policy 

### Form Pages
#### Contact Us - Report User - Reset Password - Change Password - Register - Login
All the form pages have the following features:
* On a small device will show the form and fields
* On Medium and larger devices, the user will see a gif of a dog/dogs (on reset, change password, register and login)
* Each field is passed through validations both on front and backend prior to being submitted to the database

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
* links and confirmation that the privacy and safeguarding policy have been agreed to
* If all valid on submit will add the user to the database, add a session cookie using the username and direct them to build their profile.

### Build Profile 
* Allows users to fill out the rest of the following dogs’ details and types:
    * Name - text - input to database as string
    * DOB
    * Size 
    * Breed
    * Preferences for platonic or love
    * Spade of Neutered 
    * Description
* Allows the user to add their own name and description
* Input fields are put through a validator to check they are acceptable and text fields are put through the profanity filter  
* The date of birth field has a date range of today and up to 20 years.  This is to stop users giving their dog a future date or a date that does not exists
* If the user has already built their profile these fields will be prefilled out, so the user does not have to re-enter them.    

### Contact Us
* Has a field for the email address if the user is not signed in so they can enter their email
* If the user is signed in it find their email from the database and does not display the email field
* Asks the user to enter a message.  When sent the user is sent a copy of the email to their inbox and the email is sent to PuppyPlaymates 
 
### Report User 
* Has a field for the username they are reporting 
* Asks the user to enter a message explaining what they are reporting. When sent the user is sent a copy of the email to their inbox and the email is sent to PuppyPlaymates 

### Reset Password
* Asks user for email address and send a random generated string to the user’s emails address if they are a registered user. 
* If they are not a registered user, they will receive a flash message informing them that the email address is not registered
* The random string is saved into the users document with the key to temp_password 

### Change Password
* The change password page can be accessed either through the link sent to the users email address or internally if they are signed in
* The current password field requires the user to use either the temp_password they were assigned when they reset their password or current password
*  The repeat password and new password must match
* On a successful password change the temp_password field is given a new ransom string so it cannot be used again. 


***


## Future Features 

Below is a list of future features I would like to add into PuppyPlaymates 

* Maps - shows dogs by nearest location on the playmates page 
* WOOFCHAT - Live chat app using web sockets, was in the original plans for playmates but outside the scope at this point
* Pagination on the playmates page 
* Pagination for comments 
* Image crop for all user images
* Preferences - multi search queries on playmates page 
* Ability to add multiple dogs to one human profile 
* Use a database call to render up to date photos on comments/ liker rather than using the image at time of posting.  
* Showcase all walk/events - option to promote your walk or keep it just on your profile  
* Keep a track of previous walks in another section of the profile page 
* Pagination for comments 
* Add a data store for all comments that are posted for safeguarding purposes.  If a user deletes or edits their comments, they will be stored on the database in a separate collection along with their username, time stamp, email address. This would be for the purpose of safeguarding so if the comments violate the safe spaces policy, then action can be taken against the user. 
* Continue working on the profanity checker


***
