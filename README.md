# Grocery sharing website for neighborhood in Django, HTMX, Alpine.js

## Motivation

I started this project to deepen my understanding of Django and Javascript. At the same time, I thought it would be cool to have some web/app like this in my daily life since going shopping for grocery often takes quite an amount of valuable time. I would go around, comparing the prices, calculate my budget, and always end up complaining "How can 3 tomatoes cost so much?". (I hope I'm not the only thiking that :joy:). 


Price at local market especially at large open market is much more affordable but living alone means I can't just purchase a box of potatoes and cook them all in a week. Honestly, sometimes, I wasted a ton of grocery after buying from the supermarket because I was busy the next few days.

In light of the problem, I started sharing grocery in bulk with some friends living close. It went well but coordinating in Facebook might not the best way.
That's why I have the idea for this project. I hope to find some ways to make this process of sharing smoother.

## Thought process and choices

I knew I decided to use Django but a pure MPA in Django does not offer the modern, smooth, interactive web experience due to the constant reloading.
However, using React as a frontend-framework and Django REST as backend is a litle too much for my small project. Neither I want to spend time rebuilding the common interactivity patterns in vanilla JS. Another thing I adore is Django powerful template language so I hope to find a JS library that integrates well with it. 

I stumbled on HTMX and Alpine.js. After reading their tutorials and docs, I was convinced that they fit my needs above perfectly.

My approach:
- htmx attributes sending requests to urls, views in Django which returns rendered HTML with template. That will be used for htmx swap. The interesting thing is that htmx attributes having the philosophy of being html extension plays well with Django template language. It means not only the initial HTML but the rendered HTML from Django view can contain further htmx.

Example in the video:

- Alpine js will do some simple tasks such as dropdown, modal, responsive nav bar. 
- Javascript when necessary such as for fetching from nominatim API for geo based app. 







