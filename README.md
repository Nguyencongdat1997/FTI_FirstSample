# FTI_FirstSample
Target OS Environment : CentOS Linux - VERSION: 7
Pre-requirement: 
   - Docker
   - Docker-compose
   
# Services:   
  Token Service: Store and Manage facebook generated tokens which will be used when executing requests in other service
   - host_name:5000/createdb 
        Run Create Token database for the first running time.
        Inputed parameters: None.
        Returned data: None.
   - host_name:5000/get
        Get an available Token.
        Inputed parameters: None.
        Returned data: 
            + A token ID if there is an available one.
            + Error message "Error: No token available" if there is no token.
   - host_name:5000/insert/<toke_value>
        Insert a Token to database
        Inputed parameters: token_value.
        Returned data: None.
   - host_name:5000/pause/<token_value>
        Disable availibility of a Token for 10s
        Inputed parameters: token_value.
        Returned data: None.
   - host_name:5000/block/<token_value>
        Disable a Token perpetually
        Inputed parameters: token_value.
        Returned data: None.
   - host_name:5000/view/
        View all Tokens in database
        Inputed parameters: None.
        Returned data: View of Tokens and their status
   
  Post-Crawl Service: Crawling Post from FB API
   - host_name:5001/crawl/<uid>/<since>/<limit>
        Crawl posts of an users. Crawled data will be save to "./data/post"
        Inputed parameters:
            + uid: user id
            + since: earliest time mark of a post want to crawl
            + limit: maximum number of posts want to crawl
        Returned data: None.
        

# Example Possible Running Cycle:
Run docker:
   - docker-compose up -d
Access API:
   - host_name:5000/createdb  #OPTIONAL: run in the first time setup
   - host_name:5000/insert/<token_value>
   - host_name:5001/crawl/<uid>/<since>/<limit>
