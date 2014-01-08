
def enum(**enums):
    return type('Enum', (), enums)

FeatureType = enum(TWO_VERTICAL = 0, TWO_HORIZONTAL = 1, THREE_HORIZONTAL = 2, FOUR = 3)

class HaarLikeFeature(object):
    '''
    classdocs
    '''


    def __init__(self, feature_type, position, width, height, threshold, polarity):
        '''
        @param feature_type: see FeatureType enum
        @param position: top left corner where the feature begins
        @param width: width of the feature
        @param height: height of the feature
        @param threshold: feature threshold
        @param polarity: polarity of the feature (-1, 1)
        '''
        self.type = feature_type
        self.top_left = position
        self.bottom_right = (position[0] + width, position[1] + height)
        self.width = width
        self.height = height
        self.threshold = threshold
        self.polarity = polarity
    
    def get_score(self, intImage):
        score = 0
        if self.type == FeatureType.TWO_VERTICAL:
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width, self.top_left[1] + self.height/2))
            second = intImage.get_area_sum((self.top_left[0], self.top_left[1] + self.height/2), self.bottom_right)
            score = first - second
        elif self.type== FeatureType.TWO_HORIZONTAL:
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width/2, self.top_left[1] + self.height))
            second = intImage.get_area_sum((self.top_left[0] + self.width/2, self.top_left[1]), self.bottom_right)
            score = first - second
        elif self.type == FeatureType.THREE_HORIZONTAL:
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width/3, self.top_left[1] + self.height))
            second = intImage.get_area_sum((self.top_left[0] + self.width/3, self.top_left[1]), (self.top_left[0] + 2*self.width/3, self.top_left[1] + self.height))
            third = intImage.get_area_sum((self.top_left[0] + 2*self.width/3, self.top_left[1]), self.bottom_right)
            score = first - second + third
        elif self.type == FeatureType.FOUR:
            # top left area
            first = intImage.get_area_sum(self.top_left, (self.top_left[0] + self.width/2, self.top_left[1] + self.height/2))
            # top right area
            second = intImage.get_area_sum((self.top_left[0] + self.width/2, self.top_left[1]), (self.bottom_right[0], self.top_left[1] + self.height/2))
            # bottom left area
            third = intImage.get_area_sum((self.top_left[0], self.top_left[1] + self.height/2), (self.top_left[0] + self.width/2, self.bottom_right[1]))
            # bottom right area
            fourth = intImage.get_area_sum((self.top_left[0] + self.width/2, self.top_left[1] + self.height/2), self.bottom_right)
            score = first - second - third + fourth
        return 1 if score < self.polarity*self.threshold else 0
    