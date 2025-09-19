import functions as fc

def getEndpoint(name: str) -> str:
    """
    Gets API endpoint.

    Returns endpoint by name.

        :param name: endpoint name
        :type name: str
        :returns: endpoint
        :rtype: str 

        :Example: 
        >>> getEndpoint("standings")  
        "https://cdn.espn.com/core/nfl/standings?xhr=1"
    """
    data = fc.loadJson("json/e.json")
    return data["endpoints"][name]