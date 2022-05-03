# Grocery sharing website for neighborhood in Django, HTMX, Alpine.js

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

Example in the video:

- Alpine js will do some simple tasks such as dropdown, modal, responsive nav bar. It was fascinating that I can even combine htmx and alpine as in the video below. 
- Javascript when necessary such as for fetching from nominatim API for geo based app. 
- Django typical testing for model, model methods, views
- Small test for some Javascript
- Test on the live web by hand for frontend as I'm just not sure what is approriate for htmx and alpine js. I may use cypress or selenium. Thanksfully, the project is still small enough to test frontend by hand.
- Native CSS with CSS Grid, CSS custom properties, CSS animations, media query for responsiveness

## More details of technical choices for implementation, API, libaries 

## What I learnt and problems that I faced
Firstly, I understand why combination of React for frontend and Django REST API for backend is wonderful and perfect for large applications with complex state and API calls to other services. On the other hand, HTMX and Alpine.js are good for projects without difficult frontend. 

One interesting thing to note is that because of htmx's nature, I can organize some components in Django HTML template and employ 
`{% include "app/example.html" %}` to reuse them in several other template pages. 

I also learnt more and practiced to make modular OOP Javascript code. I learnt a bit more about geo based applications, Map API, geojson.  

I was able to deepend understanding of Django, basic of how Django REST use Json reponse to work with frontend framework, appreciate how convenient this structure is.

## Reference

This video about modular OOP Javascript was eye-opening to me. It made me understand the practical applications of OOP concepts.









