# Grocery sharing website for neighborhood in Django, GeoDjango, HTMX, Alpine.js

## Motivation

I started this project to deepen my understanding of Django and Javascript. At the same time, I thought it would be cool to have some web/app like this in my daily life since going shopping for grocery often takes quite an amount of valuable time. I would go around, comparing the prices, calculating my budget, and always end up complaining "How can 3 tomatoes cost so much?". (I hope I'm not the only thiking that :joy:). 


Price at local market especially at large open market is much more affordable but living alone means I can't just purchase a box of potatoes and cook them all in a week. Honestly, sometimes, I wasted a ton of grocery after buying from the supermarket because I was busy the next few days.

In light of the problem, I started sharing grocery in bulk with some friends living close. It went well but coordinating in Facebook might not the best way.
That's why I have the idea for this project. I hope to find some ways to make this process of sharing smoother.

## Thought process and choices

I knew I decided to use Django but a pure MPA in Django does not offer the modern, smooth, interactive web experience due to the constant reloading.
However, using React as a frontend-framework and Django REST as backend is a litle too much for my small project. Neither I want to spend time rebuilding the common interactivity patterns in vanilla JS. Another thing I adore is Django powerful template language so I hope to find a JS library that integrates well with it. 

I stumbled on HTMX and Alpine.js. After reading their tutorials and docs, I was convinced that they fit my needs above perfectly.

My approach:
- htmx attributes sending requests to urls, views in Django which returns rendered HTML with template. That will be used for htmx swap. The interesting thing is that htmx attributes having the philosophy of being html extension plays well with Django template language. It means not only the initial HTML but the rendered HTML from Django view can contain further htmx.
- Alpine js will do some simple tasks such as dropdown, modal, responsive nav bar. It was cool that I can combine htmx and alpine. 

Example in the video:


- Javascript when necessary such as for fetching from Nominatim API for geo based app. 
- Django typical testing for model, model methods, views
- Small test for some Javascript
- Test on the live web by hand for frontend since I'm just not sure what is approriate for htmx and alpine js. I am thinking to use cypress or selenium. Thanksfully, the project is still small enough to test frontend by hand.
- Native CSS with CSS Grid, CSS custom properties, CSS animations, media query for responsiveness

## Dependencies and installation steps
- htmx: https://htmx.org/ django-htmx extension is used https://github.com/adamchainz/django-htmx
- alpine js: https://alpinejs.dev/
- leaflet: https://leafletjs.com/ with openstreetmap as provider
- leaflet plugin for marker rotation: https://github.com/bbecquet/Leaflet.RotatedMarker. This is used to provide a simple solution for overlapping markers at the same coordinates
- fontawesome: https://fontawesome.com/ fontawesomefree django extension is used 
- plotly: for plotting graph `pip install plotly`
- geodjango: https://docs.djangoproject.com/en/4.0/ref/contrib/gis/ It is shipped with django but further installation is necessary. Installation steps here use spatialite extension for sqlite on Windows 64. This is an alternative to geodjango official guide as I failed to replicate that. 
  - Install spatialite binary for Windows 64-bit here http://www.gaia-gis.it/gaia-sins/
  - Unzip the entire folder to the directory of python (which should alreadby in PATH) or directory of python within the virtual environment
  - Download then install gdal from here  https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal by pip: `pip install /path/to/GDAL‑3.3.3‑cp310‑cp310‑win_amd64.whl`
  - Here check the gdal carefully before correct python version, 64 bit, and what version of gdal is supported by geodjango
  - You can check that by going to python directory/Lib/site-packages/django/contrib/gis/gdal/libgal.py. Check the line that lists version of gdal supported
  - Add to settings.py
  ```
    if os.name == 'nt':
        VENV_BASE = os.environ['VIRTUAL_ENV']
        os.environ['PATH'] = os.path.join(VENV_BASE, 'Lib\\site-packages\\osgeo') + ';' + os.environ['PATH']
        os.environ['PROJ_LIB'] = os.path.join(VENV_BASE, 'Lib\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH']
    SPATIALITE_LIBRARY_PATH = "mod_spatialite"
    ```
No one is probably going to run my project. But to run it, just clone and install requirements for django, geodjango, django-htmx, fontawesome, plotly. 
Or use requirements.txt. 

## Project structure

Standard django project structure 
```
+-- accounts
+-- community
+-- geocommunity
+-- polls
|   +-- templates/polls
|   +-- static/polls
|   +-- ...
+-- posts
```

## What I learnt and problems that I faced
Firstly, I understand a little more why combination of React for frontend and Django REST API for backend is wonderful and perfect for large applications with complex state and API calls to other services. On the other hand, HTMX and Alpine.js may be good for projects without difficult frontend. 

One interesting thing to note is that because of htmx's nature, I can organize some components in Django HTML template and employ 
`{% include "app/example.html" %}` to reuse them in several other template pages. 

I also learnt more and practiced to make good modular OOP Javascript code. I learnt a bit more about geo based applications, Map API, geojson.  

I was able to deepen my knowledge in Django, basic of how Django REST use Json reponse to work with frontend framework, appreciate how convenient this structure is.

## Reference

This series about modular OOP Javascript was eye-opening to me. It made me understand the practical applications of OOP concepts.
https://www.youtube.com/watch?v=HkFlM73G-hk









