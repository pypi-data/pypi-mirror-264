import requests
import matplotlib.pyplot as plt
import json
import argparse

parser = argparse.ArgumentParser(
                    prog='Telegram notification allure',
                    description='Notification allure test result for Telegram'
                    )
parser.add_argument('--config_file', default='config.json', help='Configuration file', required=True)
config_file = parser.parse_args().config_file


def duration_readable(duration_ms):
    duration_seconds = duration_ms//1000
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}.000"


with open("../allure-report/widgets/summary.json", "r") as summary_f:
    summary_data = json.load(summary_f)

    # Данные для построения
    labels_dict = {'passed': "green", 'failed': "red", "broken": "yellow", "skipped": "grey", "unknown": "purple"}
    labels = []
    colors = []
    sizes = []

    for k, v in labels_dict.items():
        if summary_data['statistic'][k] != 0:
            labels.append(k)
            colors.append(v)

    sizes = [(summary_data['statistic'][i] / summary_data['statistic']['total']) * 100 for i in labels]

    # Построение диаграммы
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=None, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.set_position([0.1, 0.2, 0.5, 0.75])

    text = 'TEST RESULT\n'
    text += f"Total tests : {summary_data['statistic']['total']}\n\n"
    for label in labels:
        text += f"{summary_data['statistic'][label]} - {label}\n"
    plt.text(2.1, .0, text, ha='center', va='center', fontsize=18)
    plt.axis('equal')
    plt.savefig('notification.png')

    with open(config_file, "r") as config_f:
        config_data = json.load(config_f)
        token_tg = config_data['telegram']['token']
        project_name = config_data['base']['project']
        report_link = config_data['base']['reportLink']
        environment = config_data['base']['environment']
        chat_id = config_data['telegram']['chat']
        duration = duration_readable(summary_data['time']['duration'])
        requests.post(f"https://api.telegram.org/bot{token_tg}/sendPhoto",
                      data={'chat_id': chat_id,
                            'caption': f'*Test results* \n'
                                       f'*Environment:* {environment} \n'
                                       f'*Duration:* {duration} \n'
                                       f'*Total tests:* {summary_data["statistic"]["total"]} \n'
                                       f'*Total passed:* {summary_data["statistic"]["passed"]} '
                                       f'({(summary_data["statistic"]["passed"] * 100) / summary_data["statistic"]["total"]:.2f}%)\n'
                                       f'*Total failed:*  {summary_data["statistic"]["failed"]} '
                                       f'({(summary_data["statistic"]["failed"] * 100) / summary_data["statistic"]["total"]:.2f}%)\n'
                                       f'*Total broken:* {summary_data["statistic"]["broken"]}\n'
                                       f'*Total unknown:* {summary_data["statistic"]["unknown"]}\n'
                                       f'*Total skipped:* {summary_data["statistic"]["skipped"]}\n'
                                       f'*Report available at the link:* {report_link}\n',
                            'parse_mode': 'Markdown',
                            "disable_notification": True
                            },
                      files={'photo': open('notification.png', 'rb')}
                      )
