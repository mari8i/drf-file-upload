===============
DRF File Upload
===============

A reusable django library to handle file upload with the Django Rest Framework.

It provides views, serializers and models for simplifying file uploads and their model association in your RESTful application.

 
How it works
------------

1. Upload the file using this library multi-part APIs::

    POST https://example.com/api/upload/
    # A multipart request with a `file` field that contains your file 

2. If upload is complete, an unique identifier for that file and a URL for accessing it are returned::

    {
       "url": "https://example.com/media/upload/file.png",
       "uuid: "1ad29aa9-d470-442d-a5a3-5922e7ce0182"
    }

3. Use the `uuid` in your APIs for associating the uploaded file with your django model instance::

    {
       [...],
       "my-file-attribute": "1ad29aa9-d470-442d-a5a3-5922e7ce0182"
    }

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
