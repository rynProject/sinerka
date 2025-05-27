# Internal Project Management - Odoo Module

This is a custom Odoo module for managing **internal projects** and their **related tasks**, built to streamline team coordination and task tracking within departments.

## Features

- Create and manage internal projects
- Assign managers and departments
- Set start and end dates
- Track progress and status
- Add and manage multiple tasks per project
- State transitions: Draft → In Progress → Done / Cancelled
- Quick access to related tasks from the project form view

## Module Structure

- **Models**
  - `project.internal`: Main model for internal projects
  - `project.task.internal`: Task model related to each project
- **Views**
  - Tree and form views for both projects and tasks
  - Notebook tab for tasks within the project form
- **Actions & Menus**
  - Main menu under Project Management
  - Smart button to open related tasks
- **State Buttons**
  - Start, Complete, Cancel, Reset to Draft

## Installation

1. Clone the repository into your Odoo `addons` directory:

   ```bash
   git clone https://github.com/yourusername/internal_project_mgmt.git
