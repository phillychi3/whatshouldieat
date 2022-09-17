import requests

def getdata(locdata,key,nextpage = None):

    if nextpage == None:
        r = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={locdata}&radius=1000&type=restaurant&key={key}")
    else:
        rurl = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={nextpage}&key={key}"
        r = requests.get(rurl)
    return r.json()


def getfoods(locals,key):
    returndata = []
    next = None
    for _ in range(3):
        if next == None:
            data = getdata(locals,key)
        else:
            data = getdata(locals,key,next)
        for i in data["results"]:
            if "business_status" in i:
                if i["business_status"] == "OPERATIONAL":
                    returndata.append({
                        "name": i["name"],
                        "rating": i["rating"],
                        "vicinity": i["vicinity"],
                        "ratings": i["user_ratings_total"],
                        "lat": i["geometry"]["location"]["lat"],
                        "lng": i["geometry"]["location"]["lng"],
                        "url": f"https://www.google.com.tw/maps/search/{i['geometry']['location']['lat']},{i['geometry']['location']['lng']}"

                    })
        if "next_page_token" in data:
            break
            # next = data["next_page_token"]
        else:
            break
    return returndata
    # for i in sorted(returndata, key=lambda k: k["rating"], reverse=True):
    #     print(i)
    # for i in sorted(returndata, key=lambda k: k["vicinity"], reverse=True):
    #     print(i)


def getafood(locals,key):
    import random
    data = getfoods(locals,key)
    return random.choice(data)

def sortfoodbyrating(locals,key):
    data = getfoods(locals,key)
    return sorted(data, key=lambda k: k["rating"], reverse=True)

def sortfoodbyratings(locals,key):
    data = getfoods(locals,key)
    return sorted(data, key=lambda k: k["ratings"], reverse=True)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("func", help="function name")
    parser.add_argument("locals", help="location data")
    parser.add_argument("key", help="google api key")
    args = parser.parse_args()
    if args.func == "getfoods":
        print(getfoods(args.locals,args.key))
    elif args.func == "getafood":
        print(getafood(args.locals,args.key))
    elif args.func == "sortfoodbyrating":
        print(sortfoodbyrating(args.locals,args.key))
    elif args.func == "sortfoodbyratings":
        print(sortfoodbyratings(args.locals,args.key))
    else:
        print("no function")

