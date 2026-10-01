class DashboardAnalyzer:

    def __init__(
        self,
        driver_analyzer,
        trip_analyzer
    ):
        self.driver_analyzer = driver_analyzer
        self.trip_analyzer = trip_analyzer

    def get_kpis(self):

        driver_metrics = (
            self.driver_analyzer
            .get_driver_metrics()
        )

        trip_metrics = (
            self.trip_analyzer
            .get_dashboard_metrics()
        )

        return {
            **driver_metrics,
            **trip_metrics
        }