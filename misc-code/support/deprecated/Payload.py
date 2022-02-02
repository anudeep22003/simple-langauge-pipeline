import requests

class Payload:
    
    """
    This would instantiate a new payload. 
    The reason to have this as a class is that there might be verifications and checks to be peformed on the payload to ensure it is valid. 
    We will include those verifications here, although for now it is going to be a simple text field.
    
    We will have mediatype specific verifications too as this block starts taking on more responsibility. 
    """
    
    def __init__(self, media):
        self.payload = media
        self.status = self.link_verifier()
        
    
    def link_verifier(self):
        
        """
        Want this to check if the link passed is a valid link or not, check if the api errors out with status.code > 200
        """
        
        return requests.head(self.payload, allow_redirects = True).status_code
    
    def print_attributes(self):
        print(f"{'payload:':15} {self.payload}")
        print(f"{'status code:':15} {self.status}")
                