# Chess
Chess engine is a simple chess game that can be played without leaving your terminal.
It supports both single player and two player game. For single player game, you need to play against computer, which uses _mini-max_ algorithm to find the optimal move.

### Prerequisites
* Install Python
* Install Python Package Manager (pip/pip3) :
    ```
    apt-get install python-pip
    ```
    ```
    apt-get install python3-pip
    ```
* Install [virtualenv](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b) :
    ```
    apt-get install virtualenv
    ```

### Project Installation
1. Clone the repository - `git clone <remote-url>`
2. Go to the project directory - `cd <cloned-repo>`
3. Set up the environment :
    * Create virtual environment files - `virtualenv venv`
    * Activate virtual environment - `source venv/bin/activate`
4. Install dependencies - `pip3 install -r requirements.txt`
5. Start/Run game - `python3 engine.py`

### License
[GPLv3](LICENSE)