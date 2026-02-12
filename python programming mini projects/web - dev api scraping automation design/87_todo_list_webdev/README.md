# To-Dozee - Task Management Web Application

## Overview
A full-stack web application for managing to-do lists and checklists. Built with Flask and SQLAlchemy, this app allows users to create custom tasks, organize them by categories, and track completion status. Perfect for personal organization and common checklist templates.

## Features
- **Custom To-Do Lists**: Create and manage personal tasks
- **Category-Based Checklists**: Organize tasks by different categories
- **Task Completion Tracking**: Mark tasks as complete with checkboxes
- **Persistent Storage**: SQLite database keeps your tasks saved
- **Task Management**: Add and delete tasks easily
- **Responsive Design**: Bootstrap-powered UI works on all devices
- **Multiple Categories**: Switch between different checklist types
- **Clean Interface**: Font Awesome icons and modern styling

## Technologies Used
- **Python 3.x**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database storage
- **Bootstrap 5.3.2** - Responsive UI framework
- **Font Awesome 6.5.0** - Icon library
- **Jinja2** - Template engine

## How to Use
1. **Home Page**: Select between custom to-do list or category-based checklists
2. **Add Tasks**: Enter new tasks using the input form
3. **Complete Tasks**: Check boxes to mark tasks as complete
4. **Delete Tasks**: Remove completed or unwanted tasks
5. **Switch Categories**: Navigate between different checklist types
6. **About Page**: Learn more about the application

## Installation
```bash
pip install flask flask-sqlalchemy
```

## Running the Application
```bash
python main.py
```
Then open your browser to: `http://127.0.0.1:5000/`

## Project Structure
```
├── main.py                 # Flask application and routes
├── templates/
│   ├── index.html         # Home page
│   ├── todo.html          # Custom to-do list
│   ├── checklists.html    # Category checklists
│   ├── calendar.html      # Calendar view (optional)
│   └── about.html         # About page
└── static/
    ├── styles.css         # Custom styling
    └── images/            # Application images
```

## Database Schema

### Todo Table
```python
- task_id: Integer (Primary Key)
- text: String(200) - Task description
- complete: Boolean - Completion status
- category: String(50) - Task category
```

## Routes

### Main Routes
- `GET /` - Home page
- `GET /todo` - Custom to-do list page
- `GET /checklists` - Category selection page
- `GET /checklist/<category>` - Specific category checklist
- `GET /about` - About page

### Task Management Routes
- `POST /add` - Add task to custom to-do list
- `POST /add/<category>` - Add task to specific category
- `POST /complete` - Mark task(s) as complete
- `POST /delete` - Delete a task

## Features in Detail

### Task Categories
- **Custom**: Personal to-do items
- **Category-Based**: Pre-defined checklist templates
- Each category maintained separately in database

### Task Operations
- **Add**: Submit new tasks via form
- **Complete**: Multi-select checkbox support
- **Delete**: Individual task removal
- **Persist**: All changes saved to SQLite database

## Database Configuration
```python
Database URI: "sqlite:///todo.db"
Auto-creates tables on first run
SQLAlchemy ORM for type-safe operations
```

## UI Components
- Navigation header with links (Home, About)
- Material icons for category selection
- Task list with checkboxes
- Add task input forms
- Delete buttons for each task
- Responsive grid layout

## Requirements
- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLAlchemy

## Development Mode
The application runs with `debug=True` for development:
- Auto-reloads on code changes
- Detailed error messages
- Interactive debugger

## Future Enhancements
Potential improvements:
- User authentication and accounts
- Calendar integration
- Task due dates and reminders
- Priority levels
- Task notes and descriptions
- Search and filter functionality
- Export/import checklists
- Sharing checklists with others
- Mobile app version

## Author
By: Irena Dav © 2025

## Note
Make sure the database file (`todo.db`) and static assets directory are properly configured before running the application.
