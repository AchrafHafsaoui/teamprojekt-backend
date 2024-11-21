## This project uses the **Django framework**.

## Apps in Django

Apps are modular components that encapsulate specific functionality (e.g., pages, admin/user rights) for the project. Each app is designed to handle a specific area of the website or application.

### Managing Apps

1. **Declaring Apps**  
   All apps must be declared in the `INSTALLED_APPS` section of the `teamprojekt_backend/settings.py` file. Example:

   ```python
   INSTALLED_APPS = [
       ...
       'your_app_name',
   ]

   ```

2. **Creating an App**
   To create a new app, use the following steps:

   $ cd teamprojekt_backend
   $ python manage.py startapp <Name_of_Your_App>
