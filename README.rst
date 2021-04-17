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

2. If upload is complete, an unique identifier for that file is returned, along an URL for accessing it::

    {
       "url": "https://example.com/media/upload/file.png",
       "uuid: "1ad29aa9-d470-442d-a5a3-5922e7ce0182"
    }

3. Use the `uuid` in your APIs for associating the uploaded file with your django model instance::

    POST https://example.com/api/foo/
    {
       [...],
       "my-file-attribute": "1ad29aa9-d470-442d-a5a3-5922e7ce0182"
    }

4. If you want to update the resource but leave the file unchanged, simply pass the file url as value::

    PUT https://example.com/api/foo/2/
    {
        [...],
        "my-file-attribute": "https://example.com/media/upload/file.png"
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

This will add both separate authenticated and anonymous users to file upload endpoints.
Todo: add single view examples

3. Add the UploadedFileField to your serializers todo

4. Run ``python manage.py migrate`` to create the file upload models.

5. Run the cleanup management command `deleted_expired_uploaded_files` in a cron task or add a celery task

TODO: Improve https://docs.djangoproject.com/en/3.1/intro/reusable-apps/
