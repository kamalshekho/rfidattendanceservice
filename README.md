# rfidattendanceservice

Backend service for Raspberry Pi to read RFID UIDs and manage attendance check-in/out.

---

## Overview

This project is a Python backend service designed to run on a Raspberry Pi.  
It reads RFID chip UIDs via a serial interface and posts them to an attendance management backend.  
The project is modular, simple, and easy to extend.

---

## Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/kamalshekho/rfidattendanceservice.git
cd rfidattendanceservice
```

### Step 2: Create a virtual environment

A virtual environment isolates the Python dependencies of this project from your system Python.
This prevents conflicts with other projects and keeps your system environment clean.

#### Windows:

```bash
python -m venv venv
```

#### macOS/Linux:

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

Before installing packages or running the app, you need to activate the virtual environment.

#### Windows:

```bash
venv\Scripts\activate
```

#### macOS/Linux:

```bash
source venv/bin/activate
```

### Step 4: Install project dependencies

- All required packages are listed in requirements.txt.

```bash
pip install -r requirements.txt
```

- Whenever you add new packages to the project, update requirements.txt using:

```bash
pip freeze > requirements.txt
```

### Step 5: Run the application

- The main entry point of the project is src/main.py.

```bash
python src/main.py
```
