# Pollstr

Submit a poll, find a voting box, get your voice heard! IoT!!!

## Features

- **View Polls**: View all polls with the total votes each has received.
- **Create a Poll**: Users can submit new poll questions with three multiple-choice responses.
- **IoT Integration**: IoT devices can retrieve random poll questions and submit votes via JSON endpoints.

## Installation

To get the application running on your local machine, follow these steps:

### Prerequisites

Ensure you have Python and Flask installed. If not, you can install them using pip:

    pip install flask


### Clone the Repository

First, clone this repository to your local machine:

    git clone git@github.com:ew432usna/pollstr.git
    cd pollstr

### Start the Application

Run the Flask application using:

    python3 app.py

## Usage

### Web Interface

Navigate to `http://localhost:3000/` to view and manage polls. Use the web interface to:

- View all polls and their vote counts.
- Create new polls.
- View detailed results of each poll.

### IoT Device Interaction

IoT devices interact with the application through two main JSON endpoints:

- **GET `/poll.json`**: Retrieve a random poll question suitable for IoT devices. Example:

    ```bash
       curl http://localhost:5000/poll.json

- **POST `/poll/:id.json`**: Submit a vote for a specific poll option. Example to vote for option 2 on poll ID 0:

    ```bash
       curl -X POST -H "Content-Type: application/json" -d '{"option": 2}' http://localhost:5000/poll/0.json

## Contributing

Contributions to the project are welcome! Please feel free to submit pull requests or open issues to suggest improvements or add new features.

