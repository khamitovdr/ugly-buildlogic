import pandas as pd
from datetime import datetime


def calculate_completion_percentage(df_current_status) -> float:
    completed_tasks = df_current_status["is_done"].sum()
    total_tasks = len(df_current_status)
    # процент работ завершенных
    completion_percentage = (completed_tasks / total_tasks) * 100
    print(f"Percentage of completed works: {completion_percentage}%")
    return completion_percentage


def detect_project_delays(df_results, df_current_status) -> str:
    df_merged = pd.merge(df_results, df_current_status, on="op_id", how="left")

    mismatches = df_merged[
        (df_merged["is_done"] == True)
        & (
            (df_merged["early_start"] != df_merged["fact_start"])
            | (df_merged["early_finish"] != df_merged["fact_finish"])
        )
    ]

    if not mismatches.empty:
        print("Mismatches found between planned and actual dates for completed tasks:")
        return mismatches[
            ["op_id", "early_start", "fact_start", "early_finish", "fact_finish"]
        ].to_json(orient="records", date_format="iso")
    return {
        "message": "No mismatches found between planned and actual dates for completed tasks."
    }
