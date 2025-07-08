import re
import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, FilterExpression,
    Filter, FilterExpressionList
)
from google.oauth2 import service_account
from events.models import ActivityStats, SponsorshipStats

KEY_PATH = '/Users/kingcurtis618/未命名檔案夾/cococo/coco/event_matcher/ga_key.json'
PROPERTY_ID = '495740137'

def fetch_daily_ga4_data():
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = BetaAnalyticsDataClient(credentials=credentials)

    ####### 日期範圍設定：抓昨天資料 ########
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_range = DateRange(start_date=str(yesterday), end_date=str(yesterday))

    ####### 抓曝光數據（page views） ########
    request_views = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[date_range],
    )
    response_views = client.run_report(request_views)

    for row in response_views.rows:
        path = row.dimension_values[0].value
        views = int(row.metric_values[0].value)

        activity_match = re.match(r"^/activity/(\d+)/?$", path)
        sponsor_match = re.match(r"^/sponsor/(\d+)/?$", path)

        if activity_match:
            pk = int(activity_match.group(1))
            stats, _ = ActivityStats.objects.get_or_create(activity_id=pk)
            stats.impressions = views
            stats.save()
        elif sponsor_match:
            pk = int(sponsor_match.group(1))
            stats, _ = SponsorshipStats.objects.get_or_create(sponsorship_id=pk)
            stats.impressions = views
            stats.save()

    ####### 抓點擊＋曝光事件數據 ########
    tracked_events = [
        "clickActivity", "clickSponsorship",
        "impression_activity", "impression_sponsorship"
    ]

    request_events = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="eventName"), Dimension(name="pagePath")],
        metrics=[Metric(name="eventCount")],
        date_ranges=[date_range],
        dimension_filter=FilterExpression(
            or_group=FilterExpressionList(
                expressions=[
                    FilterExpression(
                        filter=Filter(
                            field_name="eventName",
                            string_filter=Filter.StringFilter(value=event)
                        )
                    ) for event in tracked_events
                ]
            )
        )
    )

    response_events = client.run_report(request_events)
    print(response_events.rows)
    for row in response_events.rows:
        event = row.dimension_values[0].value
        path = row.dimension_values[1].value
        count = int(row.metric_values[0].value)

        activity_match = re.match(r"^/activity/(\d+)/?$", path)
        sponsor_match = re.match(r"^/sponsor/(\d+)/?$", path)

        if event == "clickActivity" and activity_match:
            pk = int(activity_match.group(1))
            stats, _ = ActivityStats.objects.get_or_create(activity_id=pk)
            stats.clicks = count
            stats.save()
        elif event == "clickSponsorship" and sponsor_match:
            pk = int(sponsor_match.group(1))
            stats, _ = SponsorshipStats.objects.get_or_create(sponsorship_id=pk)
            stats.clicks = count
            stats.save()
        elif event == "impression_activity" and activity_match:
            pk = int(activity_match.group(1))
            stats, _ = ActivityStats.objects.get_or_create(activity_id=pk)
            stats.impressions = count
            stats.save()
        elif event == "impression_sponsorship" and sponsor_match:
            pk = int(sponsor_match.group(1))
            stats, _ = SponsorshipStats.objects.get_or_create(sponsorship_id=pk)
            stats.impressions = count
            stats.save()
