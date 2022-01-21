class EnvVariables:

    """
    Initializing env variables
    """

    t = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJpYXQiOjE2MzcxNDI2NjZ9.AkLL2rMRyvSkRoWEg2qbMMvv28-Y94-Hth4Qyh5Nl4c"

    base_url = "https://api.prod.sb.codebuckets.in/v3/"
    auth = 'auth/oauth'
    me = ''

    # payload to get the messages as a response
    payload = {
        "last_id": 0,
        "selectedIndex": 1,
        "token": t
    }
    
    neo4j_creds = {
        'auth': ("neo4j", "SHHcaUZYNPF-qWoyOrahHksjOelYBFASgdqjrRd1Ju8"),
        'url': "neo4j+s://8219a15b.databases.neo4j.io:7687"
        
    }