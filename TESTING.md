## **Testing User Stories**

### **User Requirements and Expectations**

The following user requirements and expectations were developed based on the user stories.

#### **Expectation: being able to browse through the content without having to register first**

-   Requirement: allow users to easily access the main content of the site without having to register or log in
-   Implementation: both the page for all books (sorted by title) and the page for all books of the selected series can be accessed through the navbar. The sticky navbar at the top of the page furthermore facilitates easy navigation. See the screenshots [here](images/readme/usertests/user-expectation-1.jpg) and [here](images/readme/usertests/user-expectation-1-example-2.jpg).

#### **Expectation: being able to search for books by title**

-   Requirement: allow users to search the database for book titles and display the result.
-   Implementation: using the Python interpreter in the command line a text index was created to allow users to search for titles and text from the blurbs within the books' collection:

          mongo.db.books.create_index([("title", "text"), ("blurb", "text")])

    A search bar has been placed at the top of the all_books and series pages. Search results are displayed beneath the search bar and by clicking on 'Reset' the user is redirected to the originating page. See a screenshot for a search result [here](images/readme/usertests/user-expectation-2.jpg).

#### **Expectation: being able to see in what order the books have been published and/or should be read**

-   Requirement: Retrieve and display information helping users discern the order of publication.
-   Implementation: Where available, the book number within a series is being displayed. For the pages displaying all books of a selected series, the titles are sorted by number. For series without numbering, the titles have been added to the database in their correct order and are displayed in this order. See the screenshots [here](images/readme/usertests/user-expectation-3.jpg) and [here](images/readme/usertests/user-expecation-3-example-2.jpg). The year in which the story of each book starts (timespan) has been added to the database where available. Currently, there is no option to sort books by timespan. This is both due to this information not being available for all books and Star Trek stories often having multiple story lines taking place in different timespans. And of course, there are stories featuring time travel.

#### **Expectation: being able to read reviews or some form of rating from other users**

-   Requirement: allow users to write reviews and let users see all available reviews. Let users rate books.
-   Implementation: Users who are logged in can [write reviews](images/readme/usertests/user-expectation-4.jpg). The correspondent button at the bottom of the card displaying the information for the selected book redirects the user the review page. The series code and the book title are already entered into the form and are read-only. This is both to make it easier for the user and to prevent multiple entries for one book due to spelling errors or differences in capitalization. [All reviews](images/readme/usertests/user-expectation-4-example-2.jpg) are accessible through the navbar. The option to rate books has not been implemented. There are no immediate plans to implement this feature, but this decision might be reconsidered at a later time.

#### **Expectation: being able to write a review for a book and post it to the site**

-   Please refer to the above expectation.

#### **Expectation: being able to save books and series as favourites**

-   Requirement: allow users to mark selected books and series and display them as their favourites.
-   Implementation: each book and each series features an ['Add to favourites' button](images/readme/usertests/user-expectation-5.jpg) that adds the book or series to the favourites_books or favourites_series array of the currently logged in user. The items from those arrays are [displayed](images/readme/usertests/user-expectation-5-example-2.jpg) on the profile page. A flash message either confirms that the book or series has been added to the favourites or informs the user that the [book](images/readme/usertests/user-expectation-5-example-3.jpg) or [series](images/readme/usertests/user-expectation-5-example-4.jpg) couldn't be added because it already was in that list.

#### **Expectation: being able to distinguish between books that have already been read and those that have not been read by the user**

-   Requirement: allow users to add books to separate lists ('finished books' and 'wish list').
-   Implementation: like the above expectation this is implemented via [button](images/readme/usertests/user-expectation-6.jpg) and the [lists](images/readme/usertests/user-expectation-6-example-2.jpg) are displayed on the profile page. In contrast to the expectation above, there are no checks whether a book is already in 'the other list'. This is intentional because a trekkie might e.g. have finished the audiobook version of a title and still want the paperbook or e-book version of the same title or the same format but in another language.

#### **Expectation: being able to see which books of a series are needed to either complete it or be up to date**

-   Requirement: allow users to see a constantly updated list of all books for a series from which the titles marked as finished have been removed.
-   Implementation: This feature has not been implemented yet.

#### **Expectation: being able to add books that either have not been read yet or have not been published yet to a wish list**

-   Books, either published or not yet published, can be added to the wish list. Please refer to expectation 6 (2 above) for details.

#### **Expectation: being able to add books to the site**

-   This feature has not been implemented and there are no plans to implement it in the future. For the time being new books are being added manually by me to the database. For later updates to the site I plan to add books by web scraping.

#### **Expectation: being able to edit and delete reviews, lists and reading progress**

-   Requirement: allow users to modify their reviews, lists and reading progress and update the correspondent database documents.
-   Implementation: Each review on the profile page features [buttons](images/readme/usertests/user-expectation-7.jpg) that let users [edit](images/readme/usertests/user-expectation-7-example-1.jpg) and delete their reviews. In case of editing the series code and the book title are already entered into the form and read-only. In case of deletion a [confirmation modal](images/readme/usertests/user-expectation-7-example-2.jpg) lets users either confirm the deletion or cancel the process. This functionality has not been implemented for list and reading progress yet.

#### **Expectation: being able to contact the site owner**

-   Requirement: allow users to easily get in touch with the site owner.
-   Implementation: the site features a [contact page](images/readme/usertests/user-expectation-8.jpg) where users can send an email. A [flash message](images/readme/usertests/user-expectation-8-example-2.jpg) informs the user that the message has been received. In case of technical difficulties, [another flash message](images/readme/usertests/user-expectation-8-example-3.png) informs the user that the message could not be sent.

#### **Expectation: being able to navigate the site by using a keyboard only**

-   Requirement: make all relevant elements available with the Tab key and make all relevant interactions respond to the Enter key in addition to mouse clicks.
-   Implementation: I manually tested all elements on all pages. Where elements could not be focused using the Tab key,

        tabindex="0"

    was added to the HTML code. Please refer to commit ef9d1b16760f7315503dbd964822e05e4a9e005e.

    To enable keyboard interaction with the modal dialogue that appears when users want to delete their reviews, additional JS code was added. Please refer to commit cb55e3a3494df281d1dc168d6bc0ce1da595e255.

    To assist users in identifying the focused element, distinct :focus styles were added. Please refer to commit: 4268e7c1d6c1d161450e2618b17f548d04f32dc0.

#### **Expectation: being able to access the site by using a screen reader**

-   Requirement: allow content and structure to be recognized by screen readers.
-   Implementation: no additional measures were taken. When using the Windows 10 screen reader all content could be heard and.

#### **Expectation: being able as an admin to add new collections to the site**

-   Requirement: allow users with admin privileges to add new series and books to the site
-   Implementation: for users with admin privileges [additional links](images/readme/usertests/user-expectation-9.jpg) are available in the navbar that redirect to the correspondent forms. See screenshots [here](images/readme/usertests/user-expectation-9-example-2.jpg) and [here](images/readme/usertests/user-expectation-9-example-3.jpg).

#### **Expectation: being able as an admin to edit collections**

-   This feature is not implemented. Currently, I do not plan to allow any other users to modify the collections and if I have to make changes myself I either log into my MongoDB account and modify the collections there or I use the MongoDB Compass application.

#### **Expectation: being able as an admin to delete collections**

-   See comment above.

#### **Expectation: as an admin I want to be able to delete reviews from users if they contain any form of unacceptable content**

-   This feature is not implemented yet. In a future update to the site I want to go one step further and check the reviews before adding them to the site.

## **Functionality Testing**

## **Validators**

### **W3C Markup Validator**

### **W3CSS Validator**

### **Lighthouse**

### **JShint**

### **Python**

## **Route Handlers**

## **Usability Testing**

## **Compatibility Testing**
