# GooPy

A Google Data Parser / Info Extractor for Various Files (i.e. Browser History, Location History, YouTube Comments, YouTube Live Chats, etc. In more detail, the 
functions process the .JSON, .CSV, and .HTML files - the formats in which Google provides personal data archives - such as BrowserHistory.json which contains any 
Chrome activity.

Although if the Google account in question is even half as old as my own, the **processed** file will still be quite long - nevertheless, rather than trying to skim
through the massive, jumbled mess that is the Google .JSON data file, a more readable file is written after processing. At the very least, it's much easier on the 
eyes, and converts those annoying "epoch" timestamps that Google insists on using into a human-readable date.



  ##### <span style="color:green">**__Original File:__**</span>


     "Browser History": [
           {
            "favicon_url": "https://www.google.com/favicon.ico",
            "page_transition": "LINK",
            "title": "Google Takeout",
            "url": "https://takeout.google.com/?hl=en&pli=1",
            "client_id": "Px7oUkxeeVhCMDgYxI4KkA==",
            "time_usec": 1647590454329204
            },
         {
            "favicon_url": "https://www.google.com/favicon.ico",
            "page_transition": "LINK",
            "title": "Data & privacy",
            "url": "https://myaccount.google.com/data-and-privacy?hl=en",
            "client_id": "Px7oUkxeeVhCMDgYxI4KkA==",
            "time_usec": 1647590438978061
         }
         
       
  ##### <span style='color:green'> After GooPy: </span>
  
        Time Stamp:  Fri Mar 18 03:00:54 2022   Page:  Google Takeout
        Link:     https://takeout.google.com/?hl=en&pli=1
      __________________________________________________________________


        Time Stamp:  Fri Mar 18 03:00:38 2022   Page:  Data & privacy
        Link:     https://myaccount.google.com/data-and-privacy?hl=en
       __________________________________________________________________


        Time Stamp:  Fri Mar 18 03:00:37 2022   Page:  Personal info
        Link:     https://myaccount.google.com/personal-info?hl=en
      __________________________________________________________________
      
      
   
## Google Account

To illustrate additional functions, below is an example of the Google Account file - data of a different file format - before and after being processed. Since this 
particular data file simply contains a list of login/logout activity, the ip address from which the action was performed, and a time stamp, GooPy takes that
information a little further. 

Personally, given all the IP addresses from which my account has been accessed may as well scream *__"validate me..."__* as it begs to be 
checked. And this is just what GooPy does ... a list of the IP addresses is collected and checked, returning geolocation information for each (duplicate IPs are 
filtered out). 

As a tradeoff, the activity is *not* included in the records - being one of only 2 possible actions, most of which are **LOGIN** - the IP info should 
negate any need for knowing whether you logged in or out. As long as it *__was__*, indeed, you ... right? In the examples below, the data was altered for obvious reasons - even though posting my IP and ISP host doesn't produce any type of vulnerability, I'd still rather not.

  ##### Original File:
            Timestamp	              IP Address	        Activity    Type	Raw User Agents
          2022-03-17 19:11:10     Z	98.18.xxx.xxx	        Login	
          2022-03-17 14:58:40     Z	98.18.xxx.xxx	        Login	     GoogleAuth/1.4 (100011885 RP1A.200720.011); gzip,gzip(gfe),gzip(gfe)
          2022-03-16 11:45:52     Z	2604:cb00:1189:3d00   Login	     Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
          2022-03-16 07:22:27     Z	2604:cb00:1189:3d00 	Login	     GoogleAuth/1.4 (100011885 RP1A.200720.011); gzip,gzip(gfe),gzip(gfe)
          2022-03-14 13:14:38     Z	98.18.xxx.xxx	        Login	     GoogleAuth/1.4 (100011885 RP1A.200720.011); gzip,gzip(gfe),gzip(gfe)
          2022-03-14 11:05:25     Z	2604:cb00:1189:3d00 	Logout	   Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
          2022-03-13 05:28:39     Z	2604:cb00:1189:3d00 	Login	     GoogleAuth/1.4 (100011885 RP1A.200720.011); gzip,gzip(gfe),gzip(gfe)
          
          
  ##### After GooPy: 
  
          DATE:  2022-03-17	 TIME:  19:11:10
          IP:  98.18.xxx.xxx 	 HOST:  myisp.net
          CITY: Shepherdsville   STATE: Kentucky    ZIP: 40165    COUNTRY: US 

          DATE:  2022-03-09	 TIME:  01:16:28
          IP:  98.18.xxx.xxx 	 HOST:  myisp.net 
          CITY: Shepherdsville   STATE: Kentucky    ZIP: 40165    COUNTRY: US 

          DATE:  2022-03-05	 TIME:  06:18:44
          IP:  98.18.xxx.xxx 	 HOST:  myisp.net
          CITY: Shepherdsville   STATE: Kentucky    ZIP: 40165    COUNTRY: US 

          DATE:  2022-02-20	 TIME:  23:46:06
          IP:  98.18.xxx.xxx 	 HOST:  myisp.net 
          CITY: Shepherdsville   STATE: Kentucky    ZIP: 40165    COUNTRY: US 


At this point in time, I'm currently working on further development of this project. Whether or not I follow through to completion - since I'm the only contributor - 
is not a question of IF ... just of WHEN. I intend to incorporate not just Google data parsing but Facebook data as well, and whether this goal is realized a year down
the road is of no consequence. It *will* eventually be finished :) 
