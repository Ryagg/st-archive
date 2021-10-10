# ST-Archive

ST-Archive provides an overview of the novels from the various series across the Star Trek universe. Users can see the novels sorted by series, add books and/or reviews to the database, create, add, and delete favourites to or from their profiles and manage their data.

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ryagg/st-archive?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/ryagg/st-archive?style=plastic)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/ryagg/st-archive?style=plastic)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/ryagg/st-archive/flask?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/ryagg/st-archive?style=plastic)

## Deployed project

## User Experience

---

---

### User stories:

---

#### As a casual user:

-   I want to be able to browse through the content without having to register first.
-   I want to be able to search for books by title.
-   I want to be able to see in what order the books have been published and/or should be read.
-   I want to be able to read reviews or some form of rating from other users.

#### As a returning user:

-   I want to be able to write a review for a book and post it to the site.
-   I want to be able to save books and series as favourites.
-   I want to be able to distinguish between books that I have read and that I haven't read yet.
-   I want to be able to see which books of a series I need to read to complete it or to be up to date.
-   I want to be able to add books that I haven't read or that haven't been published yet to add to a wish list.
-   I want to be able to add books to the site.
-   I want to be able to edit or delete my reviews, lists and reading progress.
-   I want to be able to contact the site owner with queries.
-   I want to be able to navigate the site by using a keyboard only.
-   I want to be able to hear the content by using a screen reader.

#### As the site owner/admin:

-   I want to be able to add new collections to the site.
-   I want to be able to edit collections.
-   I want to be able to delete collections.
-   I want to be able to delete reviews from users if they are spam, include hate speech, violate copyrights or any other form of inacceptable content.

### Design

---

#### Colour Scheme

To match the site's theme, the following colour scheme was created:
![Colour palette](images/readme/colour-palette.png) It aims to replicate the colours used for LCARS in Star Trek: The Next Generation, which are familiar to every Star Trek fan. Please refer to the Credit section for more info.

#### Typography

To match the site's theme, the following fonts were used:

For headings the Millennium font, which is used on the hull of Starfleet vessels in the Star Trek movies and TV series, is used. A webfonts licence for 250000 pageviews was purchased at [fontshop.com](https://www.fontshop.com/).
![Millennium](images/readme/millenium-20px.png)

For all other text the Okuda font, which is based on the computer lettering (the LCARS system) created by Mike Okuda for Star Trek: The Next Generation, is used. A licence for personal, non-commercial purposes without limitations to the amount of prints, pages, or other medium to be produced using them, was obtained from the author at [pixelsagas.com](https://www.pixelsagas.com/).

![Okuda](images/readme/okuda-20px.png)

#### Icons

#### Imagery

### Wireframes

---

I used Balsamiq to plan the site’s layout for different viewports (mobile, tablet and desktop). To better demonstrate the differences, I sort my wireframes by page and show the versions for mobile, tablet and desktop next to each other.
All wireframes for this project can be found in the [wireframes sub-directory](https://github.com/Ryagg/st-archive/tree/main/wireframes).

### Database Schema

---

![Database Schema](images/readme/db-scheme.png)
The project uses 4 collections which are stored in MongoDB.

-   The **users** collection stores the username, password and email to enable the user to create an account with a profile page and - as a future feature - to be notified if new books are added to series from his favourites list. Books that have been added to either the favourites list or the whish list, and series that have been added to the favourites list are also stored. Furthermore, information about whether a user is also an admin are stored.

-   The **series** collection stores the name and the code (e.g. 'DIS' for 'Discovery') for each series. It also stores information about whether the series has ended.

-   The **books** collection stores the title, ISBN, blurb and number (within a series) of each book. It also holds the URL for the book cover as well as information about in which format (e-book, paper book and audiobook) the book is available and whether it is part of a mini-series. The 'timespan_start' is the 'stardate' at which the story starts and can be used - as a future feature - to sort books by 'stardate'. The status can be either 'published' or 'announced'.

-   The **reviews** collection stores the ObjectId and username from the user that wrote the review, and the title of the book being reviewed.

## Features

---

---

### Existing Features

---

### Features to be implemented

---

## Technologies Used

---

### Languages

---

-   [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
-   [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
-   [Python](https://www.python.org/)
-   [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### Libraries & Frameworks

---

-   [Bulma](https://bulma.io/)
-   [Flask](https://flask.palletsprojects.com/en/2.0.x/)
-   [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
-   [Font Awesome](https://fontawesome.com/)

### Tools

---

-   [VSCode](https://code.visualstudio.com/)
-   [GitHub](https://github.com/)
-   [Heroku](https://www.heroku.com/)
-   [Google Chrome Developer Tools](https://developer.chrome.com/docs/devtools/)
-   [Sizzy](https://sizzy.co/)
-   [Balsamiq](https://balsamiq.com/)
-   [Coolors colour palette generator](https://coolors.co/)
-   [W3C HTML Validation Service](https://validator.w3.org/)
-   [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
-   [JSHint](https://jshint.com)

## Testing

---

---

### Testing User Stories

---

Please refer to the separate [TESTING.md](TESTING.md)

### Functionality Testing

---

Please refer to the separate [TESTING.md](TESTING.md)

### Usability Testing

---

Please refer to the separate [TESTING.md](TESTING.md)

### Compatibility Testing

---

Please refer to the separate [TESTING.md](TESTING.md)

## Bugs

---

---

## Deployment

---

---

ADD HEROKU DEPLOYMENT STEPS!!!!!

-   Forking
    If you wish to use this repository as a starting point or to propose changes to this project, you can fork it. Follow the steps below.

    1. Navigate to the repository [Ryagg/st-archive](https://github.com/Ryagg/st-archive)
    2. Click 'Fork' in the top-right corner.

-   Cloning
    Cloning a repository creates a local copy on your computer. Follow the steps below.
    1. Navigate to the repository [Ryagg/st-archive](https://github.com/Ryagg/st-archive)
    2. Click 'Code' above the list of files.
    3. In the new window, cloning using HTTPS is the default option. Copy the provided link manually or by clicking on the clipboard symbol.
    4. Open Git Bash.
    5. Navigate to your desired directory for the cloned project.
    6. Type 'git clone' followed by the URL copied in step 3.
    7. Press **Enter** to create your local clone.

## Credits

---

---

The colours for my colour palette were taken from [Steven Cote's](https://codepen.io/Mokurunner) superb [LCARS Hex Chart on codepen](https://codepen.io/Mokurunner/pen/eqtHl). The licence can be found [here](https://codepen.io/Mokurunner/details/eqtHl) at the bottom of the page.

### Media

---

### Content

---

ST-Archive uses content derived from [Memory Alpha](http://memory-alpha.wikia.com/), therefore it is safe to assume that most of ST-Archive's content is licensed under [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). For details on Memory Alpha licensing see this [link](https://memory-alpha.fandom.com/wiki/Memory_Alpha:Copyrights).

ST-Archive also uses content from [Memory Beta](http://memory-beta.wikia.com/), therefore some parts of the data is licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). For details on Memory Beta licensing see this [link](https://memory-beta.fandom.com/wiki/Memory_Beta:Copyrights).

### Code

---

### Acknowledgements

---

Many thanks to:

-   Amy O'Shea for her webinar 'Preparing for your MS3' and for allowing me to use and adapt her raw code for the table showing the status of the navigation buttons depending on the user status in my readme.
