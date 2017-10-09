import re


regex = r'/stocks/detail/\?code=\w+'
regex = r'/stocks/detail/\?code=[1111|1234|9999]+'
codes = '[1111|1234|9999]+'
regex = r'/stocks/detail/\?code=' + codes
pattern = re.compile(regex)

pattern1 = '/stocks/detail/?code=1111'
pattern2 = '/stocks/detail/?code=1234'
pattern3 = '/stocks/detail/?code=5678'
pattern4 = '/stocks/detail/?code=9999'

pattern_list = [pattern1,pattern2,pattern3,pattern4]
for p in pattern_list:
    print(pattern.match(p))
