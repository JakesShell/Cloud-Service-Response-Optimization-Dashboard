import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "data" / "service_response_logs.json"
REPORT_FILE = PROJECT_ROOT / "reports" / "optimization_report.txt"

SLOW_RESPONSE_THRESHOLD = 1000
ERROR_STATUS_THRESHOLD = 500
HIGH_REQUEST_VOLUME_THRESHOLD = 1000


def load_logs():
    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def analyze_service(log):
    issues = []

    if log["response_time_ms"] > SLOW_RESPONSE_THRESHOLD:
        issues.append("Slow response time detected")

    if log["status_code"] >= ERROR_STATUS_THRESHOLD:
        issues.append("Server error detected")

    if log["request_count"] > HIGH_REQUEST_VOLUME_THRESHOLD:
        issues.append("High request volume detected")

    return issues


def get_recommended_action(issues):
    if "Server error detected" in issues and "Slow response time detected" in issues:
        return "Review error logs, check service dependencies, and optimize endpoint handling."

    if "Slow response time detected" in issues:
        return "Investigate latency, database calls, and application processing time."

    if "High request volume detected" in issues:
        return "Review scaling rules, caching strategy, and load balancing behavior."

    return "Continue monitoring service health and response trends."


def generate_report(logs):
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total_services = len(logs)
    affected_services = 0
    report_lines = []

    report_lines.append("Cloud Service Response Optimization Report")
    report_lines.append("=" * 52)
    report_lines.append(f"Total Services Reviewed: {total_services}")

    for log in logs:
        issues = analyze_service(log)

        if issues:
            affected_services += 1

    report_lines.append(f"Services Requiring Attention: {affected_services}")
    report_lines.append("")

    for log in logs:
        issues = analyze_service(log)
        recommended_action = get_recommended_action(issues)

        report_lines.append(f"Service: {log['service']}")
        report_lines.append(f"Endpoint: {log['endpoint']}")
        report_lines.append(f"Response Time: {log['response_time_ms']} ms")
        report_lines.append(f"Status Code: {log['status_code']}")
        report_lines.append(f"Request Count: {log['request_count']}")

        if issues:
            report_lines.append("Findings:")
            for issue in issues:
                report_lines.append(f"- {issue}")
            report_lines.append("Recommended Action:")
            report_lines.append(f"- {recommended_action}")
        else:
            report_lines.append("Findings: No major issues detected")
            report_lines.append("Recommended Action:")
            report_lines.append("- Continue monitoring this endpoint.")

        report_lines.append("-" * 52)

    REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")

    return REPORT_FILE


def main():
    logs = load_logs()
    report_location = generate_report(logs)

    print("Cloud Service Response Optimization Dashboard")
    print("=" * 52)
    print("Optimization report generated successfully.")
    print(f"Services reviewed: {len(logs)}")
    print(f"Report location: {report_location}")
    print("")
    print(report_location.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
