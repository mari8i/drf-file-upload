===============
DRF File Upload
===============

A library to simplify file upload with the Django Rest Framework

Quick start
-----------

1. Add "drf_file_upload" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'drf_file_upload',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('upload/', include('drf_file_upload.urls')),

3. Run ``python manage.py migrate`` to create the file upload models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create see uploaded files (you'll need the Admin app enabled).

5. Run the cleanup management command `deleted_expired_uploaded_files` in a cron task or add a celery task

TODO: Improve https://docs.djangoproject.com/en/3.1/intro/reusable-apps/
