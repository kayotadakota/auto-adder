import requests
from auto_adder.base import Base



class KakaoPage(Base):


    def __init__(self):
        super().__init__('KakaoPage')
        self.update = None

    
    def get_update(self):
        url = 'https://page.kakao.com/graphql'
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://page.kakao.com",
            # If referer is not specified the server response with 403 (!)
            "Referer": "https://page.kakao.com/menu/10010/screen/93",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty", 
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        payload = {
            'query': "\n    query staticLandingTodayNewLayout($queryInput: StaticLandingTodayNewParamInput!) {\n  staticLandingTodayNewLayout(input: $queryInput) {\n    ...Layout\n  }\n}\n    \n    fragment Layout on Layout {\n  id\n  type\n  sections {\n    ...Section\n  }\n  screenUid\n}\n    \n\n    fragment Section on Section {\n  id\n  uid\n  type\n  title\n  ... on CardSection {\n    isRecommendArea\n    isRecommendedItems\n  }\n  ... on DependOnLoggedInSection {\n    loggedInTitle\n    loggedInScheme\n  }\n  ... on SchemeSection {\n    scheme\n  }\n  ... on MetaInfoTypeSection {\n    metaInfoType\n  }\n  ... on TabSection {\n    sectionMainTabList {\n      uid\n      title\n      isSelected\n      scheme\n      additionalString\n      subTabList {\n        uid\n        title\n        isSelected\n        groupId\n      }\n    }\n  }\n  ... on ThemeKeywordSection {\n    themeKeywordList {\n      uid\n      title\n      scheme\n    }\n  }\n  ... on StaticLandingDayOfWeekSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      businessModel {\n        name\n        param\n      }\n      subcategory {\n        name\n        param\n      }\n      dayTab {\n        name\n        param\n      }\n      page\n      size\n      screenUid\n    }\n    businessModelList {\n      name\n      param\n    }\n    subcategoryList {\n      name\n      param\n    }\n    dayTabList {\n      name\n      param\n    }\n    promotionBanner {\n      ...PromotionBannerItem\n    }\n  }\n  ... on StaticLandingTodayNewSection {\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n      }\n      screenUid\n    }\n    categoryTabList {\n      name\n      param\n    }\n    subcategoryList {\n      name\n      param\n    }\n    promotionBanner {\n      ...PromotionBannerItem\n    }\n    viewType\n  }\n  ... on StaticLandingTodayUpSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n      }\n      page\n    }\n    categoryTabList {\n      name\n      param\n    }\n    subcategoryList {\n      name\n      param\n    }\n  }\n  ... on StaticLandingRankingSection {\n    isEnd\n    rankingTime\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n      }\n      rankingType {\n        name\n        param\n      }\n      page\n      screenUid\n    }\n    categoryTabList {\n      name\n      param\n    }\n    subcategoryList {\n      name\n      param\n    }\n    rankingTypeList {\n      name\n      param\n    }\n    displayAd {\n      ...DisplayAd\n    }\n    promotionBanner {\n      ...PromotionBannerItem\n    }\n    withOperationArea\n    viewType\n  }\n  ... on StaticLandingGenreSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n      }\n      sortType {\n        name\n        param\n      }\n      page\n      isComplete\n      screenUid\n    }\n    subcategoryList {\n      name\n      param\n    }\n    sortTypeList {\n      name\n      param\n    }\n    displayAd {\n      ...DisplayAd\n    }\n    promotionBanner {\n      ...PromotionBannerItem\n    }\n  }\n  ... on StaticLandingFreeSeriesSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      tab {\n        name\n        param\n      }\n      page\n      screenUid\n    }\n    tabList {\n      name\n      param\n    }\n    promotionBanner {\n      ...PromotionBannerItem\n    }\n  }\n  ... on StaticLandingEventSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      page\n    }\n    categoryTabList {\n      name\n      param\n    }\n  }\n  ... on StaticLandingOriginalSection {\n    isEnd\n    totalCount\n    originalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n      }\n      sortType {\n        name\n        param\n      }\n      isComplete\n      page\n      screenUid\n    }\n    subcategoryList {\n      name\n      param\n    }\n    sortTypeList {\n      name\n      param\n    }\n    recommendItemList {\n      ...Item\n    }\n  }\n  groups {\n    ...Group\n  }\n}\n    \n\n    fragment PromotionBannerItem on PromotionBannerItem {\n  title\n  scheme\n  leftImage\n  rightImage\n  eventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment EventLogFragment on EventLog {\n  fromGraphql\n  click {\n    layer1\n    layer2\n    setnum\n    ordnum\n    copy\n    imp_id\n    imp_provider\n  }\n  eventMeta {\n    id\n    name\n    subcategory\n    category\n    series\n    provider\n    series_id\n    type\n  }\n  viewimp_contents {\n    type\n    name\n    id\n    imp_area_ordnum\n    imp_id\n    imp_provider\n    imp_type\n    layer1\n    layer2\n  }\n  customProps {\n    landing_path\n    view_type\n    helix_id\n    helix_yn\n    helix_seed\n    content_cnt\n    event_series_id\n    event_ticket_type\n    play_url\n    banner_uid\n  }\n}\n    \n\n    fragment DisplayAd on DisplayAd {\n  sectionUid\n  bannerUid\n  treviUid\n  momentUid\n}\n    \n\n    fragment Item on Item {\n  id\n  type\n  ...BannerItem\n  ...OnAirItem\n  ...CardViewItem\n  ...CleanViewItem\n  ... on DisplayAdItem {\n    displayAd {\n      ...DisplayAd\n    }\n  }\n  ...PosterViewItem\n  ...StrategyViewItem\n  ...RankingListViewItem\n  ...NormalListViewItem\n  ...MoreItem\n  ...EventBannerItem\n  ...PromotionBannerItem\n  ...LineBannerItem\n}\n    \n\n    fragment BannerItem on BannerItem {\n  bannerType\n  bannerViewType\n  thumbnail\n  videoUrl\n  badgeList\n  statusBadge\n  titleImage\n  title\n  altText\n  metaList\n  caption\n  scheme\n  seriesId\n  eventLog {\n    ...EventLogFragment\n  }\n  moreButton {\n    ...MoreButtonFragment\n  }\n}\n    \n\n    fragment MoreButtonFragment on MoreButton {\n  type\n  scheme\n  title\n}\n    \n\n    fragment OnAirItem on OnAirItem {\n  thumbnail\n  videoUrl\n  titleImage\n  title\n  subtitleList\n  caption\n  scheme\n}\n    \n\n    fragment CardViewItem on CardViewItem {\n  title\n  altText\n  thumbnail\n  titleImage\n  scheme\n  badgeList\n  ageGradeBadge\n  statusBadge\n  ageGrade\n  selfCensorship\n  subtitleList\n  caption\n  rank\n  rankVariation\n  isEventBanner\n  categoryType\n  eventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment CleanViewItem on CleanViewItem {\n  id\n  type\n  showPlayerIcon\n  scheme\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  statusBadge\n  subtitleList\n  rank\n  ageGrade\n  selfCensorship\n  eventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment PosterViewItem on PosterViewItem {\n  id\n  type\n  showPlayerIcon\n  scheme\n  title\n  altText\n  thumbnail\n  badgeList\n  ageGradeBadge\n  statusBadge\n  subtitleList\n  rank\n  rankVariation\n  ageGrade\n  selfCensorship\n  eventLog {\n    ...EventLogFragment\n  }\n  seriesId\n}\n    \n\n    fragment StrategyViewItem on StrategyViewItem {\n  id\n  title\n  count\n  scheme\n}\n    \n\n    fragment RankingListViewItem on RankingListViewItem {\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  statusBadge\n  ageGrade\n  selfCensorship\n  metaList\n  descriptionList\n  scheme\n  rank\n  eventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment NormalListViewItem on NormalListViewItem {\n  id\n  type\n  altText\n  ticketUid\n  thumbnail\n  badgeList\n  ageGradeBadge\n  statusBadge\n  ageGrade\n  isAlaramOn\n  row1\n  row2\n  row3 {\n    id\n    metaList\n  }\n  row4\n  row5\n  scheme\n  continueScheme\n  nextProductScheme\n  continueData {\n    ...ContinueInfoFragment\n  }\n  seriesId\n  isCheckMode\n  isChecked\n  isReceived\n  showPlayerIcon\n  rank\n  isSingle\n  singleSlideType\n  ageGrade\n  selfCensorship\n  eventLog {\n    ...EventLogFragment\n  }\n  giftEventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment ContinueInfoFragment on ContinueInfo {\n  title\n  isFree\n  productId\n  lastReadProductId\n  scheme\n  continueProductType\n  hasNewSingle\n  hasUnreadSingle\n}\n    \n\n    fragment MoreItem on MoreItem {\n  id\n  scheme\n  title\n}\n    \n\n    fragment EventBannerItem on EventBannerItem {\n  bannerType\n  thumbnail\n  videoUrl\n  titleImage\n  title\n  subtitleList\n  caption\n  scheme\n  eventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment LineBannerItem on LineBannerItem {\n  title\n  scheme\n  subTitle\n  bgColor\n  rightImage\n  eventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment Group on Group {\n  id\n  ... on ListViewGroup {\n    meta {\n      title\n      count\n    }\n  }\n  ... on CardViewGroup {\n    meta {\n      title\n      count\n    }\n  }\n  ... on PosterViewGroup {\n    meta {\n      title\n      count\n    }\n  }\n  type\n  dataKey\n  groups {\n    ...GroupInGroup\n  }\n  items {\n    ...Item\n  }\n}\n    \n\n    fragment GroupInGroup on Group {\n  id\n  type\n  dataKey\n  items {\n    ...Item\n  }\n  ... on ListViewGroup {\n    meta {\n      title\n      count\n    }\n  }\n  ... on CardViewGroup {\n    meta {\n      title\n      count\n    }\n  }\n  ... on PosterViewGroup {\n    meta {\n      title\n      count\n    }\n  }\n}\n    ",
            'variables': {
                'queryInput': {
                    'categoryUid': 10,
                    'screenUid': 53,
                    'type': 'Layout'
        }}}

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                self.update = response.json()
            else:
                self.logger.error(f'Bad status code: {response.status_code}')
        except Exception as ex:
            self.logger.error(f'Unexpected error: {ex}')


kakao = KakaoPage()
kakao.get_update()
data = kakao.update.get('data').get('staticLandingTodayNewLayout').get('sections')[0].get('groups')
print(data[0].get('items'))