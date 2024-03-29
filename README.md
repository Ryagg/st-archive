# **ST-Archive**

ST-Archive provides an overview of the novels from the various series across the Star Trek universe. Users can see the novels sorted by titel and by series, add books and/or reviews to the database, add favourites to their profiles, and delete reviews from their profiles.

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ryagg/st-archive?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/ryagg/st-archive?style=plastic)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/ryagg/st-archive?style=plastic)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/ryagg/st-archive/flask?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/ryagg/st-archive?style=plastic)

## **Deployed project**

The deployed project can be found [here](https://ms3-st-archive.herokuapp.com/).

## **User Experience**

---

---

### **User stories:**

---

#### **As a casual user:**

-   I want to be able to browse through the content without having to register first.
-   I want to be able to search for books by title.
-   I want to be able to see in what order the books have been published and/or should be read.
-   I want to be able to read reviews or some form of rating from other users.

#### **As a returning user:**

-   I want to be able to write a review for a book and post it to the site.
-   I want to be able to save books and series as favourites.
-   I want to be able to distinguish between books that I have read and that I haven't read yet.
-   I want to be able to see which books of a series I need to read to complete it or to be up to date.
-   I want to be able to add books that I haven't read or that haven't been published yet to add to a wish list.
-   I want to be able to add books to the site.
-   I want to be able to edit or delete my reviews, lists and reading progress.
-   I want to be able to contact the site owner with queries.
-   I want to be able to navigate the site by using a keyboard only.
-   I want to be able to hear the content by using a screen-reader.

#### **As the site owner/admin:**

-   I want to be able to add new collections to the site.
-   I want to be able to edit collections.
-   I want to be able to delete collections.
-   I want to be able to delete reviews from users if they are spam, include hate speech, violate copyrights or any other form of unacceptable content.

### **Design**

---

#### **Colour Scheme**

To match the site's theme, the following colour scheme was created:
![Colour palette](documentation/readme/colour-palette.png) It aims to replicate the familiar colours used for LCARS in Star Trek: The Next Generation. Please refer to the Credit section for more info.

#### **Typography**

To match the site's theme, the following fonts were used:

For headings, the Millennium font, which is used on the hull of Starfleet vessels in the Star Trek movies and TV series, is used. A web fonts licence for 250000 pageviews was purchased at [fontshop.com](https://www.fontshop.com/).

![Millennium](documentation/readme/millenium-20px.png)

For all other text, the BlinkMacSystemFont is used.

![BlinkMacSystemFont](documentation/readme/blink-mac-system-font-20px.png)

Initially, the Okuda font was intended as the standard font. But due to user feedback about bad readability, the font was replaced with the BlinkMacSystemFont.

#### **Icons**

All icons on the pages are from [Font Awesome](https://fontawesome.com). Please refer to the Bug section for info about why not all buttons have been styled with icons.

The favicon was purchased from [Iconfinder](https://www.iconfinder.com/icons/5680359/book_fiction_planet_science_space_icon).

#### **Imagery**

All background images were taken from [Unsplash](https://unsplash.com). Credit for the individual pictures is given below in the media section. All book covers were obtained from [Memory Alpha](https://memory-alpha.fandom.com/wiki/Portal:Main). For information about the license, please refer to the media section. For sources for each book cover, please refer to the separate external [SOURCES.md](https://docs.google.com/spreadsheets/d/1WIVuwc7z_7EODd8w8-m4ykPebElq2aatHh4y49E0bAU/edit?usp=sharing).

### **Wireframes**

---

I used Balsamiq to plan the site’s layout for different viewports (mobile, tablet and desktop). To better demonstrate the differences, I sort my wireframes by page and show the versions for mobile, tablet and desktop next to each other.
All wireframes for this project can be found in the [wireframes sub-directory](https://github.com/Ryagg/st-archive/tree/main/wireframes).

### **Database Schema**

---

![Database Schema](documentation/readme/db-scheme.png)
The project uses 4 collections which are stored in MongoDB.

-   The **users** collection stores the username, password and email to enable the user to create an account with a profile page and - as a future feature - to be notified when new books are added to a series from his favourites list. Books that have been added to either the favourites list or the wish list and series that have been added to the favourites list, books that have been marked as finished and all reviews by the user are also stored. Furthermore, information about whether a user is also an admin are stored.

-   The **series** collection stores the name and the code (e.g. 'DSC' for 'Discovery') for each series. It also stores information about whether the series has ended.

-   The **books** collection stores the title, ISBN, blurb and number (within a series) of each book. It also holds the URL for the book cover as well as information about in which format (e-book, paper book and audiobook) the book is available and whether it is part of a mini-series. The 'timespan_start' is the year the story starts and can be used - as a future feature - to sort books by 'timespan'. The status can be either 'published' or 'announced'.

-   The **reviews** collection stores the ObjectId, the username from the user that wrote the review, the title and series of the book being reviewed, and the review itself.

## **Features**

---

---

### **Existing Features**

---

#### **Features on all pages: navbar**

The navigation menu is fixed to the top to allow the user quick and easy navigation through the site. For the series page, a dynamically generated dropdown menu is used to allow easy access without taking up too much space.
The available navigation menu items depend on whether a user is logged in and for some options also on whether a user is an admin:

| Nav Link           | Not logged in | Logged in as user | Logged in as admin |
| :----------------- | :------------ | :---------------- | :----------------- |
| Logo(back to home) | &#9989;       | &#9989;           | &#9989;            |
| All books          | &#9989;       | &#9989;           | &#9989;            |
| Series             | &#9989;       | &#9989;           | &#9989;            |
| Reviews            | &#9989;       | &#9989;           | &#9989;            |
| Account            | &#9989;       | &#9989;           | &#9989;            |
| Register           | &#9989;       | &#10060;          | &#10060;           |
| Log In             | &#9989;       | &#10060;          | &#10060;           |
| Profile            | &#10060;      | &#9989;           | &#9989;            |
| Add Series         | &#10060;      | &#10060;          | &#9989;            |
| Add Books          | &#10060;      | &#10060;          | &#9989;            |
| Log Out            | &#10060;      | &#9989;           | &#9989;            |
| Copyright          | &#9989;       | &#9989;           | &#9989;            |
| Contact            | &#9989;       | &#9989;           | &#9989;            |

#### **Features on all pages: footer**

The footer is located at the bottom of each page and includes links to reach the website author on social media. The links open in a new browser tab.

#### **Home page: welcome section with CTA**

The welcome section consists of several short paragraphs informing the user about the site's aim, features and current status as a work in progress. It also includes a CTA in form of a prominent link to the registration page.

#### **All books and Series page features**

The All books page lists all Star Trek novels from the database sorted by title.
The series page lists Star Trek novels sorted by series, e.g. "The Next Generation" or "Discovery". Currently, only a handful of books are included in the database, but the aim is to eventually list all books for all series. At the top of the page, a search bar is included where users can search both within book titles and blurbs. Results will be displayed beneath the search bar and can be cleared using the 'Reset' button.

At the start of the section for each series, users can add the whole series to their favourites.

The entry for each book includes the following information/data:

-   the book cover
-   the book number in the series or the info "Unnumbered book"
-   checkmarks indicating the available formats (ebook, paperback, and audiobook)
-   checkmark indicating whether the book is part of a miniseries
-   the blurb from the book cover
-   buttons for the user to add the book to his favourites, his wish list, to mark it as finished and to write a review

#### **All books page: pagination**

To improve both the user experience and loading times, pagination has been added.

#### **Reviews page features**

The reviews page contains all reviews sorted by series. The card for each review displays the book title, the review text and the review author. The page is read-only for all users and admins.

#### **Register page features**

The register page contains a short instruction informing users which fields must be completed and also informs users that the fields for "Favourite series", "Favourite books", "Books in wish list", and "Finished books" can't be interacted with and that data from the user profile will be added there later automatically. To improve both user experience and accessibility each required field has "(required)" added next to the label and the fields for the user lists all have the read-only value of "leave empty". To further enhance user experience a "Clear form" button is placed next to the "Submit" button.

#### **Login page features**

The login page contains fields for users to enter their username and password and a "Log in" button. If wrong credentials are entered a generic error message is displayed to prevent hackers from getting information about usernames or passwords in the database.

#### **Profile page features**

The profile page greets users with a personalised flash message and heading. It contains the user's list for favourite series, favourite books, wish list and reviews. From here users can both edit and delete their reviews. In the case of deleting reviews, a modal with a confirmation dialogue gets displayed. At this point, users can either abort the process by clicking on "Cancel" or closing the modal by clicking on the "x" button in the top right corner of the modal. Only by clicking on "Delete review" inside the modal ca users delete their reviews.

#### **Logout features**

After logging out a confirmation flash gets displayed. The session status is cleared.

#### **Contact page**

The contact page features a contact form. The form uses form validation and all input fields except the subject have to be filled out for the user to be able to submit the form. Users have the option to clear the form content. When the user submits the form a flash message informs the user about the successful submission and the form is cleared. Flask-Mail in combination with Mailtrap is used to inform the site owner about user messages including the message text and the user's email address.

#### **404 page**

Users who enter an incorrect URL for the site are being directed to the 404 page. The page features the numerical error code, a space-related image and a Star Trek related short explanation that there is no page to be displayed. Beneath, they can click on the link to be "beamed" back to the homepage.

#### **500 page**

In case of internal server errors, a 500 page is displayed. The page features the numerical error code, a space-related image and a Star Trek related short explanation that the request currently can't be fulfilled. Beneath, they can click on the link to "take a shuttle" back to the homepage.

#### **Admin features**

Admins can add both series and books to the database. They can also check user reviews before adding them to the reviews collection.

#### **Security features**

Flask-Talisman and Flask-SeaSurf are used to improve the application's security. Login and admin decorators are used to prevent unauthorized access.

#### **Accessibility features**

All elements and interactions on the site are accessible for keyboard-only users. Color alone is never used to transport meaning. The color scheme focuses heavily on blue colours because fewer users are negatively impacted by blue colours than by other colours. Clear instructions, ARIA-labels and tooltips are used to facilitate the usage of the site by users with different forms of disabilities.

#### **General Data Protection Regulation compliance**

The site features both a site notice and a privacy policy. Both pages can be reached through links in the footer. A paid subscription has been bought at [e-recht24.de](https://www.e-recht24.de/) to ensure compliance with all applicable regulations.

### **Features to be implemented**

---

#### **Review-check by admin before publishing**

Currently, all reviews are viewable on the site immediately after they have been added by users. To prevent spam or any form of unacceptable content, e.g. hate speech, in a future update reviews will be added to a separate collection for review before being added to the site by admin.

#### **E-Mail notifications**

For users who have added series to their favourites, e-mail notifications about newly announced books in those series are planned.

#### **Password reset function**

For users who forgot their password, a password reset function is planned.

## **Technologies Used**

---

### **Languages**

---

-   [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
-   [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
-   [Python](https://www.python.org/)
-   [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### **Libraries & Frameworks**

---

-   [Bulma](https://bulma.io/)

    CSS framework to build responsive web sites

-   [Flask](https://flask.palletsprojects.com/en/2.0.x/)

    Python framework for the project

-   [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)

    Templating engine for the project

-   [Font Awesome](https://fontawesome.com/)

    All icons are from Font Awesome

### **Tools**

---

-   [VSCode](https://code.visualstudio.com/)

    IDE used for coding

-   [GitHub](https://github.com/)

    Used to store the source code for this project

-   [Heroku](https://www.heroku.com/)

    Used to deploy and host the live website

-   [Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)

    Used to enable HTTP Strict Transport Security and use HTTP security headers for Flask

-   [Seasurf](https://flask-seasurf.readthedocs.io/en/latest/)

    used for protection against cross-site request forgery

-   [flask-paginate](https://github.com/lixxu/flask-paginate)

    used to add pagination to the all_books and series pages

-   [Cloudinary](https://cloudinary.com/)

    used to host book covers and add transformations, e.g. credit for the book covers

-   [Google Chrome Developer Tools](https://developer.chrome.com/docs/devtools/)

    Used to check the styling, colour contrast and responsiveness of the site

-   [Sizzy](https://sizzy.co/)

    Used to check the responsiveness of the site by comparing various viewports next to each other

-   [Balsamiq](https://balsamiq.com/)

    Used to create the wireframes

-   [Coolors colour palette generator](https://coolors.co/)

    Used to create the colour palette

-   [W3C HTML Validation Service](https://validator.w3.org/)

    HTML Validator

-   [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)

    CSS Validator

-   [JSHint](https://jshint.com)

    JS validator

-   [TinyJPG](https://tinyjpg.com/)

    Used to optimize images

-   [Mailtrap](https://mailtrap.io/)

    Used to receive emails when users send an email through the contact form

## **Testing**

---

---

Please refer to the separate [TESTING.md](TESTING.md) for all forms of testing and the documentation of bugs.

## **Deployment**

---

---

### **Forking**

If you wish to use this repository as a starting point or to propose changes to this project, you can fork it. Follow the steps below.

1. Navigate to the repository [Ryagg/st-archive](https://github.com/Ryagg/st-archive)
2. Click 'Fork' in the top-right corner.

---

### **Cloning**

Cloning a repository creates a local copy on your computer. Follow the steps below.

1. Navigate to the repository [Ryagg/st-archive](https://github.com/Ryagg/st-archive)
2. Click 'Code' above the list of files.
3. In the new window, cloning using HTTPS is the default option. Copy the provided link manually or by clicking on the clipboard symbol.
4. Open Git Bash.
5. Navigate to your desired directory for the cloned project.
6. Type git `clone https://github.com/Ryagg/st-archive.git` or paste the copied address from step 3.
7. Press **Enter** to create your local clone.

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Ryagg/st-archive)

---

### **Deploy remotely**

To deploy the site remotely on [Heroku](https://www.heroku.com/) please follow the steps below.

1. Create either a **requirements.txt** file with `pip install -r requirements.txt` or a **Pipfile** with `pipenv sync` , if using pipenv, to enable Heroku to install the required dependencies for the app.
2. Create a **Procfile** with the content `web:python app.py`. Remove any blank lines at the end as they may cause errors.
3. Register a free Heroku account, if you don't have one already, sign in and create the app.
4. Select the **Deploy** tab and choose **Github** as **Deployment method**.
5. Select the **Settings** tab and click on **Reveal Config Vars** in the section **Config Vars**. Enter your key-value-pairs from your **env.py** file without the quotes. The following variables should be added:
    - IP: `0.0.0.0`
    - PORT: `5000` (other ports may work as well)
    - SECRET_KEY: `<your secret key>`
    - MONGO_URI
        - Follow these steps to obtain your MONGO_URI:
        - Log in to your MongoDB account
        - Click on `Collections` and select the appropriate database
        - Click on `Command Line Tools`
        - Under the Heading 'Connect To Your Cluster' click on `Connect Instructions`
        - In the newly opened modal, select `Connect your application`
        - Select `Python` as the driver and your Python version
        - Copy the connection string and follow the instructions to replace `<password>` with your MongoDB password and then replace `<myFirstDatabase>` with the name of your database.
    - MONGO_DBNAME: `<your database name>`
        - Please refer to the Database schema section for information on how to set up the database
    - CLOUDINARY_CLOUD_NAME: after creating a free [Coudinary](https://cloudinary.com/) account to host the book covers downloaded from [Memory Alpha](https://memory-alpha.fandom.com/wiki/Portal:Main) either use the automatically assigned Cloudinary cloud name or change it in your account settings
    - CLOUDINARY_API_KEY: you can generate and access your API key in the security settings
    - CLOUDINARY_API_SECRET: you can generate and access your API secret in the security settings
    - DEBUG: False
        - Set this value to 'True' when updating the code.
        - **In any other case set it to 'False' to avoid remote code execution!**
6. Push the **Procfile** to your Github repo.
7. Back under the **Deploy** tab in Heroku enable **Automatic deploys**.
8. Select the **main branch** and click on **Deploy branch**.
9. Wait for the message 'Your app was successfully deployed' and then click **View** to start your app in the browser.

## **Credits**

---

---

The colours for my colour palette were taken from [Steven Cote's](https://codepen.io/Mokurunner) superb [LCARS Hex Chart on codepen](https://codepen.io/Mokurunner/pen/eqtHl). The licence can be found [here](https://codepen.io/Mokurunner/details/eqtHl) at the bottom of the page.

### **Media**

---

Photos used as background for all pages were obtained from [Unsplash](https://unsplash.com).

#### **all pages except error pages**

Starry sky: Photo by [Aperture Vintage](https://unsplash.com/@aperturevintage) on [Unsplash](https://unsplash.com/collections/kTCNECqjMRM/ms3-space/d1868ea4c622efa83b6e01d20cb1dea3?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

#### **404.html**

Solar eclipse: Photo by [Mathew Schwartz](https://unsplash.com/@cadop) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

#### **500.html**

Earth viewed from a space capsule: Photo by [NASA](https://unsplash.com/@nasa?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/collections/kTCNECqjMRM/ms3-space/d1868ea4c622efa83b6e01d20cb1dea3?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

All book cover images were obtained from [Memory Alpha](https://memory-alpha.fandom.com/wiki/Portal:Main) and are published here under the following terms:

-   **License**

    Fair Use - the material is copyrighted but used here under [Fair Use](http://en.wikipedia.org/wiki/Fair_Use) guidelines.

-   **Owner/Creator**

    Pocket Books and its corporate heir, Gallery Books, a subsidiary of Simon & Schuster.

-   **Source**

    Please refer to the separate [SOURCES.md](https://docs.google.com/spreadsheets/d/1WIVuwc7z_7EODd8w8-m4ykPebElq2aatHh4y49E0bAU/edit?usp=sharing) for sources for each book cover image. Please note that this links to a Google docs spreadsheet with read-only access to enable me to add more books and sources for those books after project submission without affecting the git commit history.

### **Content**

---

ST-Archive uses content derived from [Memory Alpha](http://memory-alpha.wikia.com/), therefore it is safe to assume that most of ST-Archive's content is licensed under [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). For details on Memory Alpha licensing see this [link](https://memory-alpha.fandom.com/wiki/Memory_Alpha:Copyrights).

ST-Archive also uses content from [Memory Beta](http://memory-beta.wikia.com/), therefore some parts of the data are licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). For details on Memory Beta licensing see this [link](https://memory-beta.fandom.com/wiki/Memory_Beta:Copyrights).

### **Code**

---

All code not written by me has the source for the code added as comment above the relevant code. For longer pieces of code the credit is repeated beneath.

-   Text shadow effect for h1 and h2: https://css-tricks.com/almanac/properties/t/text-shadow/

-   CSS tooltips: https://blog.logrocket.com/creating-beautiful-tooltips-with-only-css/

-   Shadow effects for buttons: https://neumorphism.io/

-   Pagination: Ed Bradley @ https://github.com/Edb83/self-isolution/blob/master/app.py

-   Disable unbalanced tuple unpacking in Pylint: Amy OShea @ https://github.com/AmyOShea/MS3-Cocktail-Hour/blob/master/app.py

### **Websites and Documentation**

-   [Bulma docs](https://bulma.io/documentation/)
-   [Flask docs](https://flask.palletsprojects.com/en/2.0.x/)
-   [Jinja docs](https://jinja.palletsprojects.com/en/3.0.x/)
-   [MongoDB docs](https://docs.mongodb.com/)
-   [Stackoverflow](https://stackoverflow.com/)
-   [CSS-tricks](https://css-tricks.com/)
-   [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
-   [Flask-SeaSurf](https://flask-seasurf.readthedocs.io/en/latest/)

### **Acknowledgements**

---

Many thanks to:

-   My mentor, Tim Nelson, for his outstanding support and advice.
-   Amy O'Shea for her webinar 'Preparing for your MS3' and for allowing me to use and adapt her raw code for the table showing the status of the navigation buttons depending on the user status in my readme.
-   The tutors from Code Institute for their guidance.
-   Erik P. for his suggestions regarding the site's styling.
-   The always helpful and supportive CI slack community.
-   My boss, who once again allowed me to leave work early quite often to work on my project instead.
