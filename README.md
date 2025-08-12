<h1 align="center">Welcome to The Gaming Verdict, my final capstone project for Code Institute's Full Stack Developement Boot Camp</h1>
<p align="center"><img src="/static/docs/home.png"></p>
<h2 align="center"><a href="https://the-gaming-verdict-8fd4666bd959.herokuapp.com/">Website Link | <a href="https://github.com/users/PaulyDuk/projects/7/views/1">Project Board</a></h2>
<h1>Table of Contents</h1>
<ol>
<li><a href="#introduction">Introduction</a></li>
<ul>
<li><a href="#requirements">Requirements</a></li>
<li><a href="#structure">Structure & Concepts</a></li>
</ul>
<li><a href="#wireframes">Wireframes</a></li>
<ul>
<li><a href="#wf-index">Index Page</a></li>
<li><a href="#wf-review-detail">Review Details Page</a></li>
<li><a href="#wf-review-list">Reviews List Page</a></li>
<li><a href="#wf-developer-detail">Developer Details Page</a></li>
<li><a href="#wf-developer-list">Developer List Page</a></li>
<li><a href="#wf-publisher-detail">Publisher Details Page</a></li>
<li><a href="#wf-publisher-list">Publisher List Page</a></li>
<li><a href="#wf-profile">Profile Page</a></li>
<li><a href="#wf-search">Search Page</a></li>
<li><a href="#wf-form">Form Pages</a></li>

</ul>
<li><a href="#user-stories">User Stories</a></li>
<li><a href="#design">UI/UX Design</a></li>
<li><a href="#agile">Agile Framework</a></li>
<li><a href="#features">Features</a></li>
<li><a href="#ai">AI Implementation</a></li>
<li><a href="#testing">Testing and Validation</a></li>
<ul>
<li><a href="#python-validation">Python Validation</a></li>
<li><a href="#html-validation">HTML Validation</a></li>
<li><a href="#css-validation">CSS Validation</a></li>
<li><a href="#lighthouse">Lighthouse</a></li>
</ul>
<li><a href="#deployment">Deployment</a></li>
<li><a href="#conclusion">Project Conclusion</a></li>
<li><a href="#credits">Credits</a></li>
</ol>

<h1 id="introduction">Introduction</h1>
The Gaming Verdict is a computer game review site. The site itself writes a review via AI and provides information about the game, the publisher and the developer via an API from IGDB.com. Users are then able to register and add their own comments and reviews to each game that is listed. These will require admin approval to avoid any unwanted/obscene comments being automatically added. The users then will have a profile page where they can see what, where and when they have commented and reviewed on.
<br><br>
The site also features an admin panel that only super users can access. This allows the Superuser to add and edit reviews to the site without going into the Django Admin panel and adding manually. This also allows the user to access APIs for information and review population. More details will be covered later on in the readme regarding this feature.
<br><br>

<h1 id="requirements">Requirements</h1>  
There were 5 main criteria for this project:

## Criterion: 1.1 Front-End Design

| Criterion | Description | Expected Performance |
|-----------|-------------|---------------------|
| Front-End Design | Design a front-end that meets accessibility guidelines and follows UX design principles. Create a responsive full-stack application that meets its given purpose, provides a set of user interactions, and uses custom HTML and CSS/CSS frameworks. | • A user-friendly interface with consistent styles, clear navigation, and adherence to wireframes/mockups.<br>• Semantic use of HTML.<br>• Adherence to accessibility guidelines (colour contrast, alt text).<br>• No Web Content Accessibility Guideline (WCAG) errors.<br>• The layout adapts to different screen sizes using CSS media queries, Flexbox, Grid and/or Bootstrap without any major errors/loss of functionality. |

## Criterion: 1.2 Database

| Criterion | Description | Expected Performance |
|-----------|-------------|---------------------|
| Database | Build a database-backed Django web application to manage data records. Design a database structure with at least one custom model. | • A configured Django web application with a connected database.<br>• At least one custom model that fits the project requirements.<br>• Correct implementation of Django models with appropriate fields, relationships, and constraints.<br>• Use of Django's ORM for data management ensuring efficient and secure database operations. |

## Criterion: 1.3 Agile Methodology

| Criterion | Description | Expected Performance |
|-----------|-------------|---------------------|
| Agile Methodology | Use an Agile tool to plan and track all major functionality. Document and implement all user stories linking them to project goals within an agile tool. | • Use of an Agile tool to plan and track project tasks and progress.<br>• Documentation of user stories clearly linked to project goals and deliverables within the tool.<br>• Evidence of iterative development and sprint planning.<br>• Clear backlog management and task prioritization. |

## Criterion: 1.4 Code Quality

| Criterion | Description | Expected Performance |
|-----------|-------------|---------------------|
| Code Quality | Include custom Python logic demonstrating proficiency, including compound statements like if-else conditions and loops. Write code with proper readability, indentation, and meaningful naming conventions. Name files consistently and descriptively, avoiding spaces and capitalization for cross-platform compatibility. | • Inclusion of custom Python logic with clear, well-structured if-else conditions and loops.<br>• Code that follows readability standards with proper indentation and meaningful naming conventions.<br>• Consistent and descriptive file naming avoiding spaces and capital letters for compatibility.<br>• Use of comments and docstrings to explain complex logic and functions within the code.<br>• Adherence to PEP 8 guidelines for Python code style and conventions. |

## Criterion: 1.5 Documentation

| Criterion | Description | Expected Performance |
|-----------|-------------|---------------------|
| Documentation | Document the UX design process, including wireframes, mockups, and diagrams. Ensure documentation demonstrates that the design process has been followed through to implementation. | • Concise documentation of the UX design process, including wireframes, mockups, diagrams, as well as reasoning for changes throughout the development process.<br>• Well-organized README file detailing the UX process, design rationale, and final implementation. |

<h1 id="structure">Structure & Concept</h1>
The application to be structured via 4 different Django applications, home, publisher, developer and reviews. I decided separation would be best to for each separate function to keep it clear and concise as to their functionality. The site launches directly to the home page that hosts both featured reviews and all reviews with a default view of showing the last 7 days of reviews. Clicking on a review will show it and populate all of the game, developer and publisher information on the right hand side. All of this information is populated via IGDB.com's API with the review itself generated at creation via GitHub's AI model<br><br>
I had started out the website with the idea of adding all the information myself. However I quickly found that it was rather time consuming to do so! This led me to utilising the API from IGDB.com. Further on in the design process I found the use of prompting an AI to create the review. I decided to do this both to show the possibility of implementing it as well as a time saving measure for myself.
<br><br>

<h1 id="wireframes">Wireframes</h1>
Wireframes were made for each display size and are shown below, these were the basic layout that I envisaged before undertaking this project and what were originally completed to get to my MVP. The pages I made were designed for mobile first, then tablet and desktop last.
<br>
<h2 id="wf-index">Index Page:</h2>
<br>
The index page holds the main content of the site. You are greeted with a featured game reviews section and then a list of other reviews below that in a separate section.
<br><br>
<img src="/static/docs/index.png">
<br>
<h2 id="wf-review-detail">Review Details Page:</h2>
<br>
This page is the main part of the site for the user. The top section has the game name and an image of it. The main section below this is the review and the score of the game. On the right hand side of this there are several sections, for game information, developer and publisher information. At the bottom below these are user comments and user reviews.
<br><br>
<img src="/static/docs/review_page.png">
<br>
<h2 id="wf-review-list">Review List Page:</h2>
<br>
This page lists all the reviews that are listed on the website. Clicking on one will open up the review detail page above.
<br><br>
<img src="/static/docs/review_list.png">
<br>
<h2 id="wf-developer-detail">Developer Details Page:</h2>
<br>
This page shows the developer information and provides links to all the games they have developed that the website has reviewed.
<br><br>
<img src="/static/docs/developer_game.png">
<h2 id="wf-developer-list">Developer List Page:</h2>
<br>
This page lists all the developers that have been added to the website.
<br><br>
<img src="/static/docs/developer_list.png">
<br>
<h2 id="wf-publisher-detail">Publisher Details Page:</h2>
<br>
This page shows the publisher information and provides links to all the games they have developed that the website has reviewed.
<br>
<img src="/static/docs/publisher_game.png">
<br>
<h2 id="wf-publisher-list">Publisher List Page:</h2>
<br>
This page lists all the publishers that have been added to the website.
<br><br>
<img src="/static/docs/publisher_list.png">
<br>
<h2 id="wf-profile">Profile Page:</h2>
<br>
This page shows the users profile. They will be able to see their comments and reviews that they have posted, as well as do basic account management.
<br><br>
<img src="/static/docs/profile.png">
<br>
<h2 id="wf-search">Search Page:</h2>
<br>
This page shows all the games, publishers, developers or genres that match the search criteria and would show as separate sections.
<br><br>
<img src="/static/docs/search.png">
<br>
<h2 id="wf-form">Form Pages:</h2>
<br>
I decided I wwould want all my forms simply centered in the screen with no other distractions from the task in hand. This will be used for Sign in/out, Register and Password Change pages.
<br><br>
<img src="/static/docs/form.png">
<br>

<h1 id="user-stories">User Stories</h1>

There were quite a few user stories to begin with to get the CRUD design in place. Once completed, new user stories emerged as the project progressed. There was an iteration of design as the project progressed. These followed the MoSoCo proess for priority.<br><br>
<ul>
<li>USER STORY: I would like to see what I have commented and reviewed </li>
<li>USER STORY: Approve comments: As a Site Admin I can approve or disapprove comments so that I can filter out objectionable comments</li>
<li>USER STORY: Modify or delete comment on a post: As a Site User I can modify or delete my comment on a post so that I can be involved in the conversation </li>
<li>USER STORY: Comment on a post: As a Site User I can leave comments on a post</li>
<li>USER STORY: Account registration: As a Site User I can register an account so that I can comment on a post </li>
<li>USER STORY: View comments: As a Site User / Admin I can view comments on an individual post so that I can read the conversation </li>
<li>USER STORY: As a user I would like to see previous comments and reviews </li>
<li>USER STORY: As a user I would like to filter the reviews to particular genres</li>
<li>USER STORY: As a site user, I would like to leave my own review</li>
<li>USER STORY: Open a post: As a Site User, I can click on a post so that I can read the full text.</li>
<li>USER STORY: As a user I would like to see all games by a developer/publisher</li>
<li>USER STORY: User should be able to search for a game</li>
</ul>
<br>

<h1 id="design">UI/UX Design</h1>
 I decided to go with a card based approach for my layout. This made it easy to style each segment as well as apply styles to make the appearance "pop" a bit more with drop shadows. Using cards also gave a consistent layout and was easy to iterate with loops for repeated segments, such as the review cards.
<br><br>
 For the colour scheme I decided to have the navbar dark with colour hex #2a2a2a, the background is slightly lighter to contrast with #457b9d used as the card bodies. For the text I used a mix of #ffc107 for highlighting the text and for link usage, so it was a bit more apparent what was hyperlinked or not. The main body of the text would then be white to ensure good readability. I originally went with an off white for text but this failed WCAG visibility checking so had to be adjusted.
<br><br>
I wanted the Developer and Publisher information on each card that would link to the specific section, originally I was using IDs to do so but after integrating the API for pulling this information I moved to slugs of the developer/publisher name. This made it easier to link and the URL was much more readable having this.
<br><br>

<h1 id="agile">Agile Framework</h1>
The Agile framework was used throughout the development lifecycle, follow the MoSoCo process of priority. This quickly enabled me to get an MVP and then work on designing and implementing ideal features to enhance the user experience and make the site more interactive. There are still a couple of ideas that I have in the backlog and will look at implementing in the future as a personal project.
<br>
<img src="/static/docs/projectboard.png">
<br>
<a href="https://github.com/users/PaulyDuk/projects/7/views/1">Project Board</a>
<br><br>

<h1 id="features">Features</h1>

- **Game Review Listings**  
  Browse a comprehensive list of game reviews, each with detailed descriptions, scores, and user-generated content. Reviews are displayed in a card-based, responsive layout for easy navigation.

- **Game Details with Rich Metadata**  
  Each review page displays extensive information about the game, including platforms, genres, release dates, developer and publisher details, and cover images. This metadata is dynamically fetched from the [IGDB.com API](https://api.igdb.com/), ensuring up-to-date and accurate information.

- **Automated Review Generation with GitHub AI**  
  When a new game review is created, the review text is automatically generated using [GitHub AI](https://github.com/features/ai). This integration produces professional, multi-paragraph reviews, reducing manual effort and maintaining consistent quality.

- **User Registration and Profiles**  
  Users can register, log in, and manage their profiles. Each profile displays the user’s submitted reviews and comments, allowing users to track their contributions.

- **User Reviews and Comments**  
  Authenticated users can submit their own reviews and comments on games. All user-generated content is subject to admin approval to maintain quality and appropriateness.

- **Admin Review Management**  
  Superusers have access to a custom admin interface for managing reviews, including bulk actions (publish, unpublish, feature, delete) and the ability to populate reviews directly from IGDB.com data. The review itself is generated via GitHub AI for automatic content.

- **Search and Filtering**  
  Users can search for games by name, filter reviews by genre, and view all games by a specific developer or publisher.

- **Accessibility and Responsive Design**  
  The site is designed with accessibility in mind, using semantic HTML, proper color contrast, and responsive layouts for optimal viewing on all devices.

### Key Technologies

- Django (backend and templating)
- [IGDB.com API](https://api.igdb.com/) for game data (`IGDBService`)
- [GitHub AI](https://github.com/features/ai) for review text generation
- Bootstrap for responsive UI

<h1 id="ai">AI Implementation</h1>
AI was used throughout the project lifecycle and was a very important part in the development process. It enabled me to quickly repeat repetitive tasks. For example once I had functioning code to list the developers I could use AI to repeat this code for publishers, as all the information and layout would remain the same. It also quickly allowed me to layout my website using bootstrap and make quick changes when testing new functionality.
<ul>
<li>Imagery - The logo was generated with Copilot and edited in Photoshop. All other images are generated from IGDB.com and uploaded to Cloudinary</li>
<li>Code Assistance - AI was used in different instances to support learning in the application of code in all areas. Sometimes multiple prompts were rqeuired as AI would "go off the beaten path" and make some incorrect choices, where further iterations made further mistakes. Understanding the programming language was critical to see these errors and where AI was going wrong.</li>
<li>Debugging - AI was very useful in helping to identify the basis for areas where functionality was not as expected, and allowing different approaches or be used to eliminate those issues. It also served as a learning tool during that process when particular code segments were not particularly clear, or to explain the functionality furthe.</li>
</ul>
AI is a great tool and was really beneficial when creating this website. It served amazingly well for repeating repetitive tasks and getting a layout that I wanted quickly. It was also particurly good at implementing Django for creating loops for each review. That said it did have short comings and would often introduce errors or redundant code, or repeat sections that already existed so its definitely not a replacement for a competant developer!  
<br><br>

<h1 id="testing">Testing & Validation</h1>

<h2 id="python-validation">Python Validation</h2>

All pages are clear of any errors and pass PEP8 standard:

<h2>Admin views:</h2>
<br>
<img src="/static/docs/py/admin_views.png">
<br><br>

<h2>Developer Models:</h2>
<br>
<img src="/static/docs/py/developer_models.png">
<br><br>

<h2>Developer URLs:</h2>
<br>
<img src="/static/docs/py/developer_urls.png">
<br><br>

<h2>Developer Views:</h2>
<br>
<img src="/static/docs/py/developer_views.png">
<br><br>

<h2>Home URLs:</h2>
<br>
<img src="/static/docs/py/home_urls.png">
<br><br>

<h2>Home Views:</h2>
<br>
<img src="/static/docs/py/home_views.png">
<br><br>

<h2>IGDB Service:</h2>
<br>
<img src="/static/docs/py/igdb_service.png">
<br><br>

<h2>Populate Reviews:</h2>
<br>
<img src="/static/docs/py/populate_reviews.png">
<br><br>

<h2>Populate Models:</h2>
<br>
<img src="/static/docs/py/publisher_models.png">
<br><br>

<h2>Publisher Models:</h2>
<br>
<img src="/static/docs/py/publisher_models.png">
<br><br>

<h2>Publisher URLs:</h2>
<br>
<img src="/static/docs/py/publisher_urls.png">
<br><br>

<h2>Publisher Views:</h2>
<br>
<img src="/static/docs/py/publisher_views.png">
<br><br>

<h2>Review Models:</h2>
<br>
<img src="/static/docs/py/reviews_models.png">
<br><br>

<h2>Review URLs:</h2>
<br>
<img src="/static/docs/py/reviews_urls.png">
<br><br>

<h2>Review Views:</h2>
<br>
<img src="/static/docs/py/reviews_views.png">
<br><br>

<h2 id="html-validation">HTML Validation</h2>
HTML Validation passes successfully with no errors, I have only shown the one index.html validation for brevity given the amount of pages validated. The following pages were all checked and clear of any errors:
<br><br>
index.html<br>
developer_games.html<br>
developer_list.html<br>
publisher_games.html<br>
publisher_list.html<br>
approve_comments.html<br>
approve_reviews.html<br>
populate_reviews.html<br>
review_detail.html<br>
review_list.html<br>
logout.html<br>
login.html<br>
register.html<br>
profile.html<br>
change_password.html<br>
<br><br>
<img src="/static/docs/index_validartion.png" alt="HTML Validation">
<br>

<h2 id="css-validation">CSS Validation</h2>
CSS Validation passes successfully with no errors, there are some warnings for using webkit within the CSS as this is a vendor specific code:
<br><br>
<img src="/static/docs/css.png" alt="CSS Validation">
<br>


<h2 id="lighthouse">Lighthouse</h2>
Lighthouse scores 95% for perforamnce. Unfortuantely best practices drops to 59%. This is due to Cloudinary serving the game cover images that are stored via HTTP rather than HTTPS:
<br><br>
<img src="/static/docs/lighthouse.png" alt="Lighthouse Score">
<br>

<h1 id="deployment">Deployment</h1>

This project is deployed on [Heroku](https://heroku.com/). To deploy your own instance, follow these steps:

### 1. Prerequisites

- A Heroku account
- A GitHub account
- IGDB API credentials (requires a Twitch developer account)
- A GitHub token for AI review generation

### 2. IGDB API and GitHub Token Setup

1. **IGDB API Access**
   - Go to [Twitch Developer Console](https://dev.twitch.tv/console/apps) and create a new application.
   - Note your `Client ID` and `Client Secret` for IGDB API access.

2. **GitHub Token**
   - Generate a [GitHub Personal Access Token](https://github.com/settings/tokens) with appropriate permissions for AI review generation.

3. **Create `env.py`**
   - At the root of your project, create a file named `env.py` and add the following (replace values with your own):

     os.environ["SECRET_KEY"] = "your-django-secret-key"
     os.environ["DATABASE_URL"] = "your-database-url"
     os.environ["CLOUDINARY_URL"] = "your-cloudinary-url"
     os.environ["IGDB_CLIENT_ID"] = "your-igdb-client-id"
     os.environ["IGDB_CLIENT_SECRET"] = "your-igdb-client-secret"
     os.environ["GITHUB_TOKEN"] = "your-github-token"

### 3. Heroku Setup

1. **Create a new Heroku app**
   - In the Heroku dashboard, click "New" > "Create new app".
   - Choose a unique name and region.

2. **Set Config Vars**
   - Go to "Settings" > "Reveal Config Vars".
   - Add the following keys and values (copy from your `env.py`):
     - `SECRET_KEY`
     - `DATABASE_URL`
     - `CLOUDINARY_URL`
     - `IGDB_CLIENT_ID`
     - `IGDB_CLIENT_SECRET`
     - `GITHUB_TOKEN`

3. **Prepare for Deployment**
   - Install requirements:
     ```
     pip install -r requirements.txt
     ```
   - Freeze dependencies:
     ```
     pip freeze > requirements.txt
     ```
   - Create a `Procfile` at the project root:
     ```
     web: gunicorn config.wsgi
     ```
   - In `settings.py`, set `DEBUG = False` and add your Heroku app domain to `ALLOWED_HOSTS`.

4. **Push to GitHub and Deploy**
   - Commit and push your code to GitHub.
   - In Heroku, go to the "Deploy" tab, connect your GitHub repo, and click "Deploy Branch".

### 4. Usage of IGDB API and GitHub AI

- **IGDB API:**  
  The site fetches game, developer, and publisher data dynamically from IGDB.com using your API credentials.
- **GitHub AI:**  
  When a new review is created, the review text is generated using GitHub AI, authenticated via your GitHub token.

<h1 id="conclusion">Conclusion</h1>
I have thoroughly enjoyed undertaking this project. I have learnt a lot through the process and am proud of what I have been able to produce. AI was particularly useful during the process, although you have to be mindful and understand the code when it starts going down the wrong path! It was particularly useful for quick design layouts using bootstrap and for repeating code between sections (devloper and publisher for myself).
<br><br>
I hope this showcases what I am able to produce and I look forward to continuing learning in the future.
<br><br>

<h1 id="credits">Credits</h1>

- [Code Insitute](https://codeinstitute.net/) - For providing the training to build this website
- [Bootstrap](https://getbootstrap.com/) - For the responsive site layout tools
- [favicon](https://favicon.io/) - Favicon generation
- [Google Fonts](https://fonts.google.com/) - Font library used
- [Cloudinary](https://cloudinary.com/) - Image hosting
- [IGDB.com](https://www.igdb.com/) - API usage for game, developer and publisher information
- [Github AI](https://github.com/features/ai) - For review text generation

