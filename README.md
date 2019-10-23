# Trivia API

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game. This application is built to do exactly that and features the ability to:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started


### Backend
The `./backend` directory contains the completed Flask and SQLAlchemy server application. Instructions on installing backend dependencies and running the backend application are detailed in the `README.md` of the `./backend` directory. Additionally, API reference and testing instructions can also be found here.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend
The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. Instructions on installing frontend dependencies and running the frontend application are detailed in the `README.md` of the `./frontend` directory.

[View the README.md within ./frontend for more details.](./frontend/README.md)

### Running the Application

After setting up both the backend and frontend we can run the complete application altogether. To run the full application:

From the `./backend` directory run:

```bash
    FLASK_APP=flaskr FLASK_ENV=development flask run
```

From the `./frontend` directory run:

```bash
    npm start
```

To see the full application in action, open the frontend application running at `http://localhost:3000/`

## Authors

Trivia API completed by Kristoffer Alquiza. Project starter code provided by the Full Stack Web Developer Course at [Udacity](https://www.udacity.com/course/).

## Acknowledgements
This project was completed as part of the Full Stack Web Developer Course at [Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044). Credit to the Udacity team for providing the couse content and starter code for this application.
