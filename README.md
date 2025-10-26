```markdown
# Routine Management System

A Django-based web application for generating class timetables using a genetic algorithm, ensuring no clashes and respecting teacher preferences.

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/routine-management.git
cd routine-management
```

### 2. Set Up Virtual Environment
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
**requirements.txt**:
```
Django==5.2.7
mysqlclient==2.2.4
deap==1.4.1
```

### 4. Configure MySQL
1. Install MySQL and start the server.
2. Create database:
   ```sql
   mysql -u root -p
   CREATE DATABASE routine_management;
   EXIT;
   ```
3. Update `routine_management/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'routine_management',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Load Sample Data
```bash
mysql -u root -p routine_management < scripts/sample_data.sql
```

### 7. Run Server
```bash
python manage.py runserver
```
Access at `http://localhost:8000`.

## Usage
- **Generate Timetable**: POST to `http://localhost:8000/timetable/generate/`
- **View Timetable**: GET `http://localhost:8000/timetable/data/` or visit `/timetable/view/`

## License
MIT License
```
