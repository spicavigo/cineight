from utils.media import Media

class HeaderBoxMedia(Media):
    template = 'common/BoxEmpty.html'

class HeaderTabMedia(Media):
    template = 'common/TabEmpty.html'

class HeaderElementMedia(Media):
    template = 'master/ElementHeader.html'
    css = ['master/ElementHeader.css']

LoginBoxMedia = SignUpBoxMedia = HeaderBoxMedia
LoginTabMedia = SignUpTabMedia = HeaderTabMedia

class LoginElementMedia(Media):
    template = 'master/ElementLogin.html'
    css = ['master/ElementLogin.css']
    js = ['master/ElementLogin.js']

class SignUpElementMedia(Media):
    template = 'master/ElementSignUp.html'
    css = ['master/ElementSignUp.css']
    js = ['master/ElementSignUp.js']
    
class RecoBoxMedia(Media):
    template = 'common/BoxTabbed.html'
    js = ['common/BoxTabbed.js','jquery.tools.min.js']
    css = ['common/BoxTabbed.css', 'tooltip.css']
    
class UserRecoBoxMedia(Media):
    template = 'common/BoxTabbed.html'
    js = ['common/BoxTabbed.js','jquery.tools.min.js']
    css = ['common/BoxTabbed.css', 'tooltip.css']
    
class ForwardRecoTabMedia(Media):
    template = 'common/TabRA.html'
    css = ['common/TabRA.css']
    js = ['common/TabDefault.js']
    
ReverseRecoTabMedia = ForwardRecoTabMedia

class RecoElementMedia(Media):
    template = 'master/RecoElement.html'
    css = ['master/RecoElement.css', 'master/RecommendForm.css']
    js = ['master/RecoElement.js', 'master/ElementReco.js', 'jquery.rating.js']
    
class ListBoxMedia(Media):
    template = 'common/BoxTabbed.html'
    js = ['common/BoxTabbed.js', 'jquery.tools.min.js']
    css = ['common/BoxTabbed.css', 'tooltip.css']
    
SeenListTabMedia = UnseenListTabMedia = FilterListTabMedia = ForwardRecoTabMedia

class ListElementMedia(Media):
    template = 'master/ListElement.html'
    css = ['master/RecoElement.css', 'master/RecommendForm.css']
    js = ['master/RecoElement.js', 'master/ElementReco.js', 'jquery.rating.js']
    
class MovieDetailBoxMedia(Media):
    template = 'common/BoxEmpty.html'
    
class MovieDetailTabMedia(Media):
    template = 'common/TabEmpty.html'
    
class MovieDetailElementMedia(Media):
    template = 'master/ElementMovieDetail.html'
    css = ['master/ElementMovieDetail.css', 'master/RecommendForm.css']
    js = ['master/ElementMovieDetail.js', 'master/ElementReco.js', 'jquery.rating.js']
    
class RecommenderBoxMedia(Media):
    template = 'common/BoxEmpty.html'
    
class RecommenderTabMedia(Media):
    template = 'master/TabRecommender.html'

class WarnerTabMedia(Media):
    template = 'master/TabRecommender.html'
    
class RecommenderElementMedia(Media):
    template = 'master/ElementRecommender.html'
    css = ['master/ElementRecommender.css']
    js = ['master/ElementRecommender.js']
    
class ReviewBoxMedia(Media):
    template = 'common/BoxEmpty.html'
    
class ReviewTabMedia(Media):
    template = 'master/TabReview.html'
    css = ['master/TabReview.css']
    
class ReviewElementMedia(Media):
    template = 'master/ElementReview.html'
    css = ['master/ElementReview.css', 'master/RecommendForm.css']
    js = ['jquery.rating.js']
    
class CompareBoxMedia(Media):
    template='master/BoxCompare.html'
    js=['jquery.fancybox-1.3.1.pack.js','jquery.easing-1.3.pack.js','jquery.mousewheel-3.0.2.pack.js', 'jquery.tablesorter.js', 'master/BoxCompare.js']
    css=['jquery.fancybox-1.3.1.css', 'tablesorter.css', 'master/BoxCompare.css']
    
class UserBoxMedia(Media):
    template = 'common/BoxEmpty.html'

class UserTabMedia(Media):
    template = 'common/TabEmpty.html'
    
class UserElementMedia(Media):
    template = 'master/ElementUser.html'
    js=['master/ElementUser.js']
    css=['master/ElementUser.css']
    
class SearchBoxMedia(Media):
    template = 'common/BoxEmpty.html'

class SearchTabMedia(Media):
    template = 'common/TabEmpty.html'
    
class SearchElementMedia(Media):
    template = 'master/ElementSearch.html'
    js=['jquery.autocomplete-min.js', 'master/ElementSearch.js']
    css=['master/ElementSearch.css', 'autocomplete.css']
    
class SearchResultBoxMedia(Media):
    template = 'common/BoxTabbed.html'
    js = ['common/BoxTabbed.js','jquery.tools.min.js']
    css = ['common/BoxTabbed.css', 'tooltip.css']

class SearchResultTabMedia(Media):
    template = 'common/TabRA.html'
    css = ['common/TabRA.css']
    js = ['common/TabDefault.js']

SearchResultUserTabMedia = SearchResultTabMedia
SearchResultUserElementMedia = RecommenderElementMedia

class SearchResultElementMedia(Media):
    template = 'master/ElementSearchResult.html'
    css = ['master/ElementSearchResult.css', 'master/RecommendForm.css']
    js = ['master/ElementSearchResult.js', 'master/ElementReco.js', 'jquery.rating.js']
    
class FeedbackBoxMedia(Media):
    template = 'common/BoxEmpty.html'
    
class FeedbackTabMedia(Media):
    template = 'common/TabEmpty.html'

class FeedbackElementMedia(Media):
    template = 'master/ElementFeedback.html'
    css = ['master/ElementFeedback.css']
    js = ['jquery.tabSlideOut.v1.3.js', 'master/ElementFeedback.js']