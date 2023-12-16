# Satellite Tracking Application

## Description
This application tracks satellites in real-time by fetching and parsing TLE (Two-Line Element Set) data. It visualizes satellite positions on a 3D globe using CesiumJS, backed by a Python Flask server for data processing.

## Features
- Fetch and parse TLE data from NORAD/Celestrak.
- Calculate real-time satellite positions (latitude, longitude, altitude).
- Visualize satellite trajectories on a 3D globe.
- Python Flask backend for data handling.

## Prerequisites
- Python 3.x
- Flask
- Requests library
- Skyfield library
- Node.js (for CesiumJS frontend)
- Web browser with modern WebGL support

## Installation

### Clone the Repository
```bash
git clone https://github.com/Dynathy/satellitemap.git
cd satellitemap
```

### Set Up the Backend
```bash
cd backend
pip install -r requirements.txt
```

### Set Up the Frontend
```bash
cd frontend
npm install
```

## Usage

### Run the Flask Backend
Navigate to the backend directory and start the Flask server:

```bash
cd backend
python app.py
```
The Flask server will start on localhost:5000.

### Run the Frontend
Navigate to the frontend directory and start a simple HTTP server to serve the frontend files:

```bash
cd frontend
python -m http.server
```
This will start a local server (usually on localhost:8000). Open your web browser and go to http://localhost:8000 to view the application.

## Configuration
- To change the source of TLE data, modify the URL in `backend/app.py`.
- For frontend customizations, adjust settings in `frontend/js/app.js`.

## Contributing
Contributions are welcome! Please fork the repository and open a pull request with your changes, or open an issue for any bugs or feature requests.

## License
This project is open source and available under the [MIT License](LICENSE).


