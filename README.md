# Telemetry

**User Guide**

*Requirements*

   - This repository is divided into two actual sections, client code and service code,
    along with independent common code that is needed for both. To run either the
    client or service application, both the common code and application specific code
    is needed. However, you do not need the service code to run a client application or
    vice-versa.
    
    
   - ***Required libraries/modules:***
   
        - *Required for both:*
        
            - Twisted
   
        - *Service specific:*
               
            - Raspberry Pi GPIO libraries
            
        - *Client specific:*
            
            - PySide2