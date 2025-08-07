<h1 align="center">Welcome to The Gaming Verdict, my final capstone project for Code Institute's Full Stack Developement Boot Camp</h1>
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
<li><a href="#design">Agile Framework</a></li>
<li><a href="#features">Features</a></li>
<li><a href="#ai">AI Implementation</a></li>
<li><a href="#testing">Testing and Validation</a></li>
<ul>
<li><a href="#html-validation">HTML Validation</a></li>
<li><a href="#css-validation">CSS Validation</a></li>
<li><a href="#lighthouse">Lighthouse</a></li>
<li><a href="#contrast">Contrast Checker</a></li>
</ul>
<li><a href="#design">Deployment</a></li>
<li><a href="#conclusion">Project Conclusion</a></li>
<li><a href="#credits">Credits</a></li>
</ol>

<h1 id="introduction">Introduction</h1>
The Gaming Verdict is a computer game review site. The site itself writes a review and provides information about the game, the publisher and the developer. Users are then able to register and add their own comments and reviews to each game that is listed. These will require admin approval to avoid any unwanted/obscene comments being automatically added. The users then will have a profile page where they can see what, where and when they have commented and reviewed on.
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

<br><br>

I feel like my code holds these critierias to a high standard as demonstrated through my code and this README.
<h1 id="structure">Structure & Concept</h1>
The application to be structured to provide:<br><br>
<ul>
    <li> an initial presentation of 'rules' and 'start' options to user;</li>
    <li>selection of 'rules' lanuches modal setting out how to play</li>
    <li>selection of 'start' launches selection of subject matter categories</li>
    <li>each category, on selection, launching a series of subject related multiple choice questions</li>
    <li>the user's score tallied in real-time as answers to each question are selected</li>
  </ul><br>

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

There were quite a few user stories to begin with to get the CRUD design in place. Once completed new user stories emerged as the project progressed. There was an iteration of design that caused new user stories to be produced. The design and features section will expand upon this. These followed the MoSoCo proess for priority.<br><br>
<ul>
<li>list them </li>
</ul>
<br>

<h1 id="design">UI/UX Design</h1>

<br><br>

<h1 id="features">Features</h1>

<br><br>

<br><br>

<h1 id="ai">AI Implementation</h1>
The Pubtastic Quizathon used the team's skills in combination with AI in a number of key areas:
<ul>
<li>Imagery - the images were developed using a Freepik AI image and graphics generation account, iterating designs and color schemes to achieve the desired result.</li>
<li>Code Assistance - AI was used in different instances to support learning in the application of code in all areas as appropriate - this included HTML, CSS, and JavaScript. Iteration and defining clear concise prompts was critical for getting the correct assistance from AI</li>
<li>Debugging - AI was very useful in helping to identify the basis for areas where functionality was not as expected, and allowing different approaches or be used to eliminate those issues. It also served as a learning tool during that process when paricular code segments were not particularly clear.</li>
</ul>
AI is a fantastic tool but is not a replacement for a developer who does not understand the code that is generated. Duplicate segments of code had to be removed during iterations as well as moving inline CSS styles that it preferred to a separate CSS file.
<br><br>

<h1 id="testing">Testing & Validation</h1>

<br><br>

<h2 id="html-validation">HTML Validation</h2>
HTML Validation passes successfully with no errors:
<br><br>
<img src="#" alt="HTML Validation">
<br>

<h2 id="css-validation">CSS Validation</h2>
CSS Validation passes successfully with no errors:
<br><br>
<img src="#" alt="CSS Validation">
<br>


<h2 id="lighthouse">Lighthouse</h2>
Lighthouse scores a perfect 100% due to the lightweight design of the site:
<br><br>
<img src="#" alt="CSS Validation">
<br>

<h2 id="contrast">Contrast Checker</h2>
Contrast checker passes for our text against our background:
<br><br>
<img src="#" alt="Contrast Checker">
<br><br>

<h1 id="conclusion">Conclusion</h1>
yep
<br><br>

<h1 id="credits">Credits</h1>

- [Code Insitute](https://codeinstitute.net/) - For providing the training to build this website
- [Bootstrap](https://getbootstrap.com/) - For the responsive site layout tools
- [Flaticon](https://www.flaticon.com/) - Question mark icon by Freepik
- [favicon](https://favicon.io/) - Favicon generation
- [Google Fonts](https://fonts.google.com/) - Font library used

