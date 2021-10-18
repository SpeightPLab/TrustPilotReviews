import requests as req
from bs4 import BeautifulSoup
import json

"""

Need to make sure you have installed:

- bs4 -> BeautifulSoup
- requests

Suggest deploying via serverless for AWS lamda

"""


def makeTrustyImageURL(score):
    score = float(score)
    if score < 4.0:
        return 'No Image' # I doubt you'll be under 4 .. you're amazing 😉
    if score > 4 and score < 4.2:
        return 'https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-4.svg'
    if score > 4.2 and score < 4.8:
        return 'https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-4.5.svg'
    if score > 4.5 and score <= 5 :
        return 'https://cdn.trustpilot.net/brand-assets/4.1.0/stars/stars-5.svg'


def run(site):

    response = req.get('https://uk.trustpilot.com/review/'+site+'?utm_medium=trustbox&utm_source=MicroStar')
    if response.status_code == 200:
        print('Site connection/response - good ✅')
    else:
        print('Site connection/response - bad 🤬')

    soup = BeautifulSoup(response.text, 'html.parser')


    TrustyP_score_count = json.loads(soup.find(attrs={'data-initial-state': 'rating-distribution-chart'}).contents[0]) # Current trustyP score 
    TrustyP_score = soup.find(attrs={'class': 'header_trustscore'}).text # Current trustyP score 
    reviews = soup.find_all(attrs={'class': 'review-card'})
    output = {}

    for review in reviews:
        ## Get the values for the review
        info_review  = json.loads(review.find(attrs={'data-initial-state': 'review-info'}).contents[0])

        review_id = info_review['reviewId']
        review_score = info_review['stars']
        review_person_name = info_review['consumerName']
        review_imageURL = info_review['consumerProfileImage']
        review_title = info_review['reviewHeader']
        review_content = info_review['reviewBody']
        # review_location = review.find(attrs={'class': 'consumer-information__location'})
        review_URL = info_review['socialShareUrl']

        output[review_id] = {
            'reviewId': review_id,
            'review_person_name': review_person_name,
            'review_score': review_score,
            'review_person_imageURL': review_imageURL,
            'review_title': review_title,
            'review_content': review_content,
            'review_URL': review_URL,
            'review_score_imageURL': makeTrustyImageURL(review_score)
        }


    API_OUTPUT = {
        'trustyP_score': TrustyP_score,
        'trustyP_score_count': TrustyP_score_count,
        'trustyP_score_imageURL': makeTrustyImageURL(TrustyP_score),
        'reviews': output
    }
    

    return API_OUTPUT



def hello(event, context):
        return run("sitename.com") ## this will be the value that is after the `https://uk.trustpilot.com/review/` domain, example: https://uk.trustpilot.com/review/www.google.com ... value `site` is "www.google.com"

