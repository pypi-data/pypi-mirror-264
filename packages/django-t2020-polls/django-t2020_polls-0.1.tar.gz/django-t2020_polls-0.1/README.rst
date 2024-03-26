=====
T2020_Polls
=====

T2020_Polls is a Django app to conduct web-based t2020_polls. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "t2020_polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "t2020_polls",
    ]

2. Include the t2020_polls URLconf in your project urls.py like this::

    path("t2020_polls/", include("t2020_polls.urls")),

3. Run ``python manage.py migrate`` to create the t2020_polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/t2020_polls/ to participate in the poll.