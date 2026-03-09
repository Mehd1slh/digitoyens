## Citoyens Commun'ITy — Ambassador Management Platform

This repository contains the prototype developed for the **Commun'ITy Hackathon**, held from **March 4th to 6th** at **Hacienda Marrakech**. The project aims to provide a centralized "RH Vision" for **Les Citoyens**, facilitating the management, coordination, and growth of their national ambassador network.

---

### 📋 Project Context

The prototype was designed to address the need for a structured digital space where ambassadors can connect, organize civic events, and access training resources. It focuses on streamlining the **Ambassador Lifecycle**, from initial application to active participation and reporting.

### 🚀 Key Features

- **Ambassador Dashboard**: A personalized home base for members to view quick stats, upcoming events, and internal messages.
    
- **Admin Console**: A high-level oversight panel featuring **KPIs**, membership growth charts (via Chart.js), and a regional activity map.
    
- **Onboarding Workflow**: A multi-step application form ("Devenir Ambassadeur") that guides new candidates through profile setup, skill selection, and motivation statements.
    
- **Event Management**: Modules for tracking past and incoming civic events, including a system for ambassadors to submit event participation requests.
    
- **Automated Reporting**: A dedicated API endpoint that generates official activity reports in **.docx** format by injecting user data into pre-defined templates.
    
- **Resource Library**: A learning space for "Plaidoyer Citoyen" (Citizen Advocacy) and facilitation techniques.
    

---

### 🛠 Tech Stack

- **Backend**: Python 3.x with the **Flask** framework.
    
- **Frontend**:
    
    - **HTML5/CSS3**: Custom design system utilizing the **Syne** and **DM Sans** Google Fonts.
        
    - **JavaScript**: Vanilla JS for UI interactions and **Chart.js** for administrative data visualization.
        
- **Data Handling**: A mock JSON API architecture to simulate real-time database interactions.
    
- **Document Generation**: Python `zipfile` and `io` libraries for real-time XML manipulation of Word documents.
    

---

### 📂 Repository Structure

- `app.py`: The core Flask application containing routing logic and dummy data for ambassadors, events, and notifications.
    
**`static/`**: This directory houses all persistent assets and media.

- **`Formulaire.docx`**: The master Word template used by the server to inject data and generate activity reports.

**`templates/`**: A collection of Jinja2 HTML templates defining the User Interface:

- **`admin.html`**: The high-level console for network monitoring and user permission management.
    
- **`base.html`**: The fundamental layout containing the global sidebar and navigation components.
    
- **`become_ambassador.html`**: The multi-step onboarding form for prospective network members.
    
- **`calendar.html`**: A dual-view interface for tracking monthly events and preparation timelines.
    
- **`create_event.html`**: A 4-step wizard designed for ambassadors to launch and document new civic actions.
    
- **`dashboard.html`**: The personalized landing page for active ambassadors.
    
- **`events.html`**: The central hub for browsing upcoming actions and accessing the "Toolkit" resources.
    
- **`learning.html`**: The educational portal for video training and recorded strategy sessions.
    
- **`login.html`**: The entry point for user authentication.
    
- **`map.html`**: An interactive Leaflet-based map visualizing the geographic reach of the network.
    
- **`media.html`**: A photo and video gallery documenting past event impacts.
    
- **`members.html`**: The searchable directory for connecting with other ambassadors.
    
- **`messages.html`**: The internal messaging interface for real-time peer-to-peer coordination.
    
- **`opportunities.html`**: A listing of available funding, international exchanges, and advanced training.
    

---

### 🔧 Installation & Setup

1. **Clone the repository**:
    
    Bash
    
    ```
    git clone [repository-url]
    ```
    
2. **Install dependencies**:
    
    Bash
    
    ```
    pip install flask
    ```
    
3. **Run the application**:
    
    Bash
    
    ```
    python app.py
    ```
    
4. **Access the platform**: Open `http://localhost:5050` in your browser.
    
    - _Note_: Use `admin@example.com` at the login screen to access the **Admin Console**.
        

---

**Developed during the Citoyens Commun'ITy Hackathon 2026.**