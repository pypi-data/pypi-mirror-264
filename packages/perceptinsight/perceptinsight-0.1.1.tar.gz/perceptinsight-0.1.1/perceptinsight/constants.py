from perceptinsight.models import InitOptions

EVENT_TRACKING_ENDPOINT = 'https://app.perceptinsight.com/track/v1/event'

USER_TRACKING_ENDPOINT = 'https://app.perceptinsight.com/track/v1/user'

DEFAULT_INIT_OPTIONS = InitOptions(autoFlushBatchSize=50, autoFlushThresholdMs=5000, maxApiRetry=2)
