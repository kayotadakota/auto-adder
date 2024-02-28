
GET_UPDATE_KAKAO_WEBTOON_URL = 'https://gateway-kw.kakao.com/section/v1/timetables/days?placement=timetable_new'
GET_UPDATE_KAKAO_WEBTOON_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko",
    "Origin": "https://webtoon.kakao.com",
    "Referer": "https://webtoon.kakao.com/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}

SEARCH_ON_KAKAO_PAGE_URL = 'https://page.kakao.com/graphql'
SEARCH_ON_KAKAO_PAGE_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Content-Type": "application/json; charset=utf-8",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://page.kakao.com",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty", 
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}
SEARCH_ON_KAKAO_PAGE_PAYLOAD = {
    'query': "\n    query SearchKeyword($input: SearchKeywordInput!) {\n  searchKeyword(searchKeywordInput: $input) {\n    id\n    list {\n      ...NormalListViewItem\n    }\n    total\n    isEnd\n    keyword\n    sortOptionList {\n      ...SortOption\n    }\n    selectedSortOption {\n      ...SortOption\n    }\n    categoryOptionList {\n      ...SortOption\n    }\n    selectedCategoryOption {\n      ...SortOption\n    }\n    showOnlyComplete\n    page\n  }\n}\n    \n    fragment NormalListViewItem on NormalListViewItem {\n  id\n  type\n  altText\n  ticketUid\n  thumbnail\n  badgeList\n  ageGradeBadge\n  statusBadge\n  ageGrade\n  isAlaramOn\n  row1\n  row2\n  row3 {\n    id\n    metaList\n  }\n  row4\n  row5\n  scheme\n  continueScheme\n  nextProductScheme\n  continueData {\n    ...ContinueInfoFragment\n  }\n  seriesId\n  isCheckMode\n  isChecked\n  isReceived\n  showPlayerIcon\n  rank\n  isSingle\n  singleSlideType\n  ageGrade\n  selfCensorship\n  eventLog {\n    ...EventLogFragment\n  }\n  giftEventLog {\n    ...EventLogFragment\n  }\n}\n    \n\n    fragment ContinueInfoFragment on ContinueInfo {\n  title\n  isFree\n  productId\n  lastReadProductId\n  scheme\n  continueProductType\n  hasNewSingle\n  hasUnreadSingle\n}\n    \n\n    fragment EventLogFragment on EventLog {\n  fromGraphql\n  click {\n    layer1\n    layer2\n    setnum\n    ordnum\n    copy\n    imp_id\n    imp_provider\n  }\n  eventMeta {\n    id\n    name\n    subcategory\n    category\n    series\n    provider\n    series_id\n    type\n  }\n  viewimp_contents {\n    type\n    name\n    id\n    imp_area_ordnum\n    imp_id\n    imp_provider\n    imp_type\n    layer1\n    layer2\n  }\n  customProps {\n    landing_path\n    view_type\n    helix_id\n    helix_yn\n    helix_seed\n    content_cnt\n    event_series_id\n    event_ticket_type\n    play_url\n    banner_uid\n  }\n}\n    \n\n    fragment SortOption on SortOption {\n  id\n  name\n  param\n}\n    ",
    'variables': {
        'input': {
            'categoryUid': "10",
            'showOnlyComplete': False,
            'sortType': "Accuracy",
}}}

GET_TITLE_INFO_URL = 'https://page.kakao.com/graphql'
GET_TITLE_INFO_HEADERS = {
    "Accept": "application/graphql+json, application/json",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://page.kakao.com",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty", 
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}
GET_TITLE_INFO_PAYLOAD = {
    'operationName': 'contentHomeOverview',
    'query': 'query contentHomeOverview($seriesId: Long!) {\n  contentHomeOverview(seriesId: $seriesId) {\n    id\n    seriesId\n    displayAd {\n      ...DisplayAd\n      ...DisplayAd\n      ...DisplayAd\n      __typename\n    }\n    content {\n      ...SeriesFragment\n      __typename\n    }\n    displayAd {\n      ...DisplayAd\n      __typename\n    }\n    relatedKeytalk {\n      id\n      categoryUid\n      groupUid\n      groupType\n      name\n      order\n      __typename\n    }\n    lastNoticeDate\n    moreButton {\n      type\n      scheme\n      title\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DisplayAd on DisplayAd {\n  sectionUid\n  bannerUid\n  treviUid\n  momentUid\n}\n\nfragment SeriesFragment on Series {\n  id\n  seriesId\n  title\n  thumbnail\n  categoryUid\n  category\n  categoryType\n  subcategoryUid\n  subcategory\n  badge\n  isAllFree\n  isWaitfree\n  ageGrade\n  state\n  onIssue\n  authors\n  description\n  pubPeriod\n  freeSlideCount\n  lastSlideAddedDate\n  waitfreeBlockCount\n  waitfreePeriodByMinute\n  bm\n  saleState\n  startSaleDt\n  serviceProperty {\n    ...ServicePropertyFragment\n    __typename\n  }\n  operatorProperty {\n    ...OperatorPropertyFragment\n    __typename\n  }\n  assetProperty {\n    ...AssetPropertyFragment\n    __typename\n  }\n}\n\nfragment ServicePropertyFragment on ServiceProperty {\n  viewCount\n  readCount\n  ratingCount\n  ratingSum\n  commentCount\n  pageContinue {\n    ...ContinueInfoFragment\n    __typename\n  }\n  todayGift {\n    ...TodayGift\n    __typename\n  }\n  preview {\n    ...PreviewFragment\n    ...PreviewFragment\n    ...PreviewFragment\n    __typename\n  }\n  waitfreeTicket {\n    ...WaitfreeTicketFragment\n    __typename\n  }\n  isAlarmOn\n  isLikeOn\n  ticketCount\n  purchasedDate\n  lastViewInfo {\n    ...LastViewInfoFragment\n    __typename\n  }\n  purchaseInfo {\n    ...PurchaseInfoFragment\n    __typename\n  }\n  preview {\n    ...PreviewFragment\n    __typename\n  }\n}\n\nfragment ContinueInfoFragment on ContinueInfo {\n  title\n  isFree\n  productId\n  lastReadProductId\n  scheme\n  continueProductType\n  hasNewSingle\n  hasUnreadSingle\n}\n\nfragment TodayGift on TodayGift {\n  id\n  uid\n  ticketType\n  ticketKind\n  ticketCount\n  ticketExpireAt\n  ticketExpiredText\n  isReceived\n}\n\nfragment PreviewFragment on Preview {\n  item {\n    ...PreviewSingleFragment\n    __typename\n  }\n  nextItem {\n    ...PreviewSingleFragment\n    __typename\n  }\n  usingScroll\n}\n\nfragment PreviewSingleFragment on Single {\n  id\n  productId\n  seriesId\n  title\n  thumbnail\n  badge\n  isFree\n  ageGrade\n  state\n  slideType\n  lastReleasedDate\n  size\n  pageCount\n  isHidden\n  remainText\n  isWaitfreeBlocked\n  saleState\n  operatorProperty {\n    ...OperatorPropertyFragment\n    __typename\n  }\n  assetProperty {\n    ...AssetPropertyFragment\n    __typename\n  }\n}\n\nfragment OperatorPropertyFragment on OperatorProperty {\n  thumbnail\n  copy\n  helixImpId\n  isTextViewer\n  selfCensorship\n}\n\nfragment AssetPropertyFragment on AssetProperty {\n  bannerImage\n  cardImage\n  cardTextImage\n  cleanImage\n  ipxVideo\n}\n\nfragment WaitfreeTicketFragment on WaitfreeTicket {\n  chargedPeriod\n  chargedCount\n  chargedAt\n}\n\nfragment LastViewInfoFragment on LastViewInfo {\n  isDone\n  lastViewDate\n  rate\n  spineIndex\n}\n\nfragment PurchaseInfoFragment on PurchaseInfo {\n  purchaseType\n  rentExpireDate\n  expired\n}\n',
    'variables': {
    }
}

DOWNLOAD_COVER_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}

REMANGA_LOGIN_URL = 'https://api.remanga.org/api/users/login/'
REMANGA_LOGIN_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://remanga.org',
    'Preference': '0',
    'Referer': 'https://remanga.org/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}
REMANGA_LOGIN_PAYLOAD = {
    "g-recaptcha-response": "WITHOUT_TOKEN",
}
REMANGA_PREFLIGHT_LOGIN_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
    'Access-Control-Request-Headers': 'content-type,preference',
    'Access-Control-Request-Method': 'POST',
    'Origin': 'https://remanga.org',
    'Referer': 'https://remanga.org/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

REMANGA_ADD_NEW_TITLE_URL = 'https://api.remanga.org/api/titles/'
REMANGA_ADD_NEW_TITLE_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://remanga.org',
    'Preference': '0',
    'Referer': 'https://remanga.org/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}
REMANGA_PREFLIGHT_ADD_TITLE_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
    'Access-Control-Request-Headers': 'authorization,content-type,preference',
    'Access-Control-Request-Method': 'POST',
    'Origin': 'https://remanga.org',
    'Referer': 'https://remanga.org/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

NAVER_GET_UPDATE_URL = 'https://comic.naver.com/api/webtoon/titlelist/new?order=update'
NAVER_GET_UPDATE_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Cache-Control": "no-cache, no-store, max-age=0, must-revalidate",
    "Content-Encoding": "gzip, deflate, br",
    "Content-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Host": "comic.naver.com",
    "Referer": "https://comic.naver.com/webtoon?tab=new",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}

NAVER_DOWNLOAD_IMAGE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cache-Control": "max-age=0",
    "Content-Encoding": "gzip, deflate, br",
    "Content-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}