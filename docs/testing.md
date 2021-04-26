*** 

## Testing Index 

* [User Stories](#User) 
* [Browser Compatibility](#browser-Compatibility)
* [Validators](#Validators)
* [OS Compatibility](#os-compatibility)
* [Performance Testing](#performance-testing)
* [Usability Testing](#usability-testing)
* [User Testing](#testing-logs)

assess functionality, usability, responsiveness and data management

### User Stories

### Function Testing

Every function written was passed individually through a [Python Tutor](http://pythontutor.com/), I assigned input variables stepped through each line of code to ensure expected outcomes.  

### Temp Mail


### Validators
    

Every page of the website was run through [HTML Validator](https://validator.w3.org/) because of flask being a templating language the code wouldn't show as valid html. I copied the code from within DEV Tools and pasted it into the validators to check the validaty at render. - All pages PASSED


I passed the css file through [CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) - PASSED


Every Python file has been run through to check for Pep8 compliances and to test the validiaty of the code. [Pep8 Online](http://pep8online.com/) - PASSED


The JavaScript file has been run through a JavaScript to test the validiaty of the code. [JSHint](https://jshint.com/) - PASSED


### Performance Testing
I passed every page through Dev Tools Lighthouse to check to see how well the website was functioning. Please see the below screen shots of the homepage, playmates and profile.  

### Browser Compatibility

Tested on Chrome, Firefox, Brave, Internet Explorer, Microsoft Edge, Safari.

When using Internet Explorer the test doesn't run, the buttons are not built and the colour scheme is not shown. This is because Internet Explorer is not compatible with some of the latest JavaScript and CSS releases.  I have added a message at the bottom of the instructions to let users know to use an alternative browser to run the test.  In  a future releases of the project given more time I would like to make the test compatible with Internet Explorer. 

### OS Compatibility
 iOS, Android 10, and Windows 10. -
Tested for responsiveness using Chrome DevTools. Runs well on both IOS and Android 10. 


### Usability 

### User Testing 
I put the site out to a small group of users to feedback on how they found the WebApp.  Please see the logs below to see what feedback was recieved and how this feedback was used in the testing process

## Testing Logs

| Feedback  |Investigation | Fix |   Decision |   
|---|---|---|---|
|  Can't remember if Name and About were options on signup, I feel like I put dummy data in here? |  Hadn’t included human in the profile set up, users expected it |  Added these fields in the build profile part of the site |  Implemented |   
| The line remains yellow "as if indicating the password doesn’t match  | Goes green when you click somewhere else on the page but not key up  |  Could write a function to change the materlize class to work on key up | Could be used added in a future release  |   
|  Special character for password: I would mention which ones are allowed as I think the - might not be working, I tried different passwords before I could be accepted |  Present, no way for users to know which character are accepted  |  Added helper text including the characters needed for password validation |  Implemented  |   
| Instinctively I wanted to click on the image placeholder to add the image of my dog  |  Images were only unloadable from the edit images button | Changed so that containing image and content is an anchor  | Implemented  |   
|  No safari just didn't work for me |  Tried passing through a safari test enviroment and could find the same bug | Asked user to try again to see if problem still persisting   |  Still ongoing |   
|  If I go to edit my pup I had clicked he'd been neutered but it didn't bring back the original setting so when I clicked update it changed it so he had not been neutered |  Form wasn't inheriting values from the data base |  Added a switch statement in the template to toggle the switch accordingly |  Implemented |   
| On the calendar for a date of birth I can added a future date, and as a result I got Age of -1  | Lack of defensive programming  |  Create a function to find todays date and set the min/max dates | Implemented  |   
|  On mobile when the menu is open, there is a weird dark overlay at the bottom, that appears only if you click on the menu if you are at the bottom of the page(footer level) |   |   |   |   
|  When I went to the list of playmates, it only allows me to click on a profile only if  hover on top of the dog's name. At the beginning, I was trying to click the image, I thought it was a bug |  Currently name was used as an anchor tag  | Change to make the whole card a clickable link  |  Implemented |   
|  With the comments, what is the purpose of me putting a comment on my own dog? Is this intentional? | Comments are allowed for both guests and profile  |  Add helper text to also reassure profile owner that they can comment on own profile with updates |   |   
|  Perhaps it would be nice to have a dropdown menu which takes the values from your database for the breeds etc | Currently the search is text based  |  Could add a database for different dog breeds allowing for a check list of breeds, however this is an extension of scope | May be implemented in future feature  |   
|   |   |   |   |   



 
