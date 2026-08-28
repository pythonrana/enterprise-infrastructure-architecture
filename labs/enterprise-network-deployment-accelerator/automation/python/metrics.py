def calculate_improvement(metrics):
    baseline = metrics["deployment_metrics"]["baseline"]["duration_minutes"]
    automated = metrics["deployment_metrics"]["automated"]["duration_minutes"]

    time_saved = baseline - automated

    percentage_reduction = (
        time_saved / baseline
    ) * 100

    return time_saved, percentage_reduction