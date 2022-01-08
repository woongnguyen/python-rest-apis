from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrott(UserRateThrottle):
    scope = 'ReviewCreate'
    
    
class ReviewListThrott(UserRateThrottle):
    scope = 'ReviewList'