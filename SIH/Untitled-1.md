APP:


 (This is a dummy app used to showcase our sensor recordings and small AI accuracy and functioning for the Hackathon) - OUR real plan that we will tell judges is that this will be developed as a SDK( or something that can be easily integrated within google maps/uber/swiggy/Ola/Rapido, etc...)

Work of the app:

1. A small trained AI model will be in the app detecting the possible potholes or other things on the road.... this sends data like latitude, longitude, timestamp, and a counter +=1 to the server if it is detected as a positive. IT WILL BE STORED IN THE SERVER IN A database OF THE SERVER. - This is the only feature of the app until some command is received from the backend.

Backend can the following things to the app:

After taking an average( of latitude and longitude and also the counter values) of the many abnormal readings from the same latitude and longitude, it will get clusterized

Then the app shows a notification to the people who are passing nearby (5-10 meters or more I'm not sure yet) the specified location asking if there is a pothole in that area or not they can send yes or no (if many people say yes, then....) // The app will also automatically start recording a 5-8 sec (as a driver is passing from near the average location of the pothole.....[It has to be accurate if there are 10000+ abnormal reading that we take average of...]) clip at 30fps and send that video to our backend. [The video clip will be deleted from the user's device after successful upload]

Later all of this will be integrated in other applications. (like google maps, uber etc.)


Website:

This will be a real website having an ADMIN login (from municipality) for the authentication of our app(since it will be a crowdsourced app)

Work of the website:

It will use deck.gl and custom google maps and show ALL the CONFIRMED potholes on the google maps as red dots.... all of this will be updated live on the site without refreshes....

Website will have all interactive features and animations and also the severity of the condition of the road....

Website will also server all other basic functions......

AI-APP:

The AI on the app will be a finetuned/trained from scratch model, its only function will be to detect abnormal readings from the mobile sensors and filter them out to find a actual positive.....

If a positive is detected then the AI will inform the app to send the required data to the backend server (data like - latitude, longitude, timestamp, confodence level, and a +1 counter to the backend server etc...)


Backend:

If on our server we detect many positives from very close locations (say 10K+ in a small radius, say 5m) then the backend will calculate the avg lat long and send the notification to the people in the passing by the location if there is a pothole there or not // or(and) one more command will be initiated that will make the app record a videoclip of 5-8 seconds [the video will start recording from a location close to the avg location and 5-8 second will make sure that the pothole image or something else is captured in the video] - The app will then again send this video clip to our backend where another AI will process it.


AI-Backend:

This AI will be finetuned on some pre-available model with more than 50K images.

The function of this AI will be to use the video data sent from the app at 30fps to locate and confirm visually if there is a pothole of not and uses another counter say cpunter2 and adds 1 to it.... if there are ample amount of positives then the pothole's avg location will be detected and displayed on the web portal of the municipal corporation...

For false readings that make it to the backend AI (say a traffic jam/traffic light/mobile dropping)..... the AI will mark areas near those locations as wrong detections and ignore all other reading from those locations (50-100mts) for some time... maybe a week.

Dataset: YOU WILL DEEPLY RESEARCH THE INTERNET TO FIND THE BEST DATA FOR BOTH ACCELEROMETER/GYROSCOPE AND POTHOLE IMAGES (or more image data like traffic/traffic lights/ OR OTHER MAJOR THINGS (LIKE ROADS WITH no potholes/ roads with very small potholes) so that out model can easily differentiate between them).

Research Papers: READ ALL THE AVAILABLE RESEARCH PAPERS ON THIS PROBELM (ALL ROAD PROBLEMS RELATED TO THIS AND MENTION THE NUMBERS) OF INDIA AVAILABLE ON GOOGLE SCHOLARS OR OTHER SITES.... DEEPLY ANAYZE THEM AND LOOK FOR INSIGHTS AND UNIQUENESS AND OTHER UNIQUE THINGS THAT WE CAN DO IN OUR PROJECT..... WHAT BETTER WE CAN DO.... WHAT THINGS WE ARE THINKING AS WRONG... ETC.... MENTION THE RESEARCH PAPERS YOU TOOK THE REFRENCE FROM IN YOUR FINAL REPORT. MENTION "ALL" YOUR GOOD AND UNIQUE FINDINGS


All other remaining stuff.....:

Databases, pipelines, coding logic, workflow, roadmap, AL ALL OTHER THINGS THAT WILL BE REQUIRED IN THIS PROJECT (MENTION THEM) 





FINALLY GENERATE A DETAILED REPORT (WITH DIAGRAMS/ FLOW CHARTS) [IN VERY SIMPLE ENGLISH LANGUAGE]. 

- IN THE REPORT THERE SHOULD BE EVERYTHING MENTIONED ABOVE IN ALL THE DETAILS AND INFORMATION THAT WILL BE BENEFIAL FOR THE PROJECT.

- ALL THE TECH STACK FROM BASIC TO ADVANCED [FROM THE ABSOLUTE BASICS OF LIKES OF HTML CSS TILL EVERYTHING ADVANCED LIIKE TRAINGIN, BACKEND, APIS, WEBSOCKETS, REDIS] - ALSO MENTION THINGS THAT CAN BE OVERLOOKED AND THE THINGS THAT WE HAVE TO COMULSORARILY DO. -- ALSO MENTION THE FESAIBILY OF THE TECH THAT WE HAVE TO USE AND THAT IS OPTIONAL...

- FOR THE RESEARCH PAPERS MENTION THE FINDINGS AND GAPS AND COMPARE THEM TO OTHER COUNTIERS TOO, ALSO LOOK FOR MORE SIMPLER SOLUTION OF THE PROBLEMS IF ANY AND MENTION THEM..... "MENTION ALL THE SOURCES OF YOUR REPORT"

- GIVE A VERY VERY DETAILED FLOWCHART FOR THE DEVELOPMENT OF THIS PROJECT..... FROM THE START TO THE END.... IT SHOULD COVER EVERYTHING THAT WE WILL NEEED TO DO "NOTHING SHOULD BE LEFT OUT OR LEFT OUT OF THE BLUE". CONNECT EVERYTHING WITH ARROWS AND BLOCKS AND DIAGRAMS.

- MENTION THE OVERALL FESABILITY OF THE PROJECT. "REMEMBER THE WHOLE PROJECT WILL BE MADE WITH AI ASSISTED CODING -- CODING HEAVYLIFTING WILL BE COMPLETELY DONE BY AI [TEAM OF 6] 3 - TEAM MEMBERS WILL BE JUST UNDERSTANDING THE CODE, ALL 6 WILL BE UNDERSTANING THE WORKFLOW, THE TECH STACK USED, THE REASON BEHIND IT, WHY NOT SOMETHING ELSE, AND WHERE IS THE TECH USED AND HOW AND WHY"

PROBLEM STATEMENT:

"Indian roads suffer from millions of potholes causing thousands of fatal road accidents annually (over 9,400+ deaths officially recorded from 2020–2024). Municipal corporations rely on slow, manual inspections or reactive citizen complaints that often take weeks or months to be resolved."

**The Solution:** A crowdsourced road monitoring system running quietly inside existing delivery/ride-hailing driver apps (e.g., Swiggy, Zomato, Ola, Uber, Rapido).

----- TELL ME THE MOTIVATION BEHIND THE CHOICE OF IDEA AND THE PLAN BY WHICH WE CAN CONVERT THIS INTO A SUCCESSFUL PROFITABLE BUSINESS ----


----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------


WRITE YOUR ENTIRE REPORT IN A MARKDOWN FILE NAMED `PROJECT.md`
