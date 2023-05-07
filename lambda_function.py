import json
import boto3
import textwrap
import os

from template import Subjects, Messages


def lambda_handler(event, context):
    client = boto3.client('sns')

    # 環境変数代入
    TOPIC_ARN = os.environ['sns_arn']

    # Messageの中身を変数に代入
    m = event['Records'][0]['Sns']['Message']
    print(type(m))
    
    
    # 辞書型に変換
    e = json.loads(m)
    print(e)
    print(type(e))
    

    # インスタンス変数作成
    objects = Messages(e['Region'], e['AWSAccountId'], e['AlarmName'], e['Trigger']['MetricName'])
    
    # 共通変数
    content = objects.contents(str(e['AlarmArn']), str(e['AlarmDescription']))
    footer = objects.footer(e['Trigger']['ComparisonOperator'], str(e['Trigger']['Threshold']), e['Trigger']['Statistic'])
    
    # 条件分岐
    if e['NewStateValue'] == "OK":
        subject = objects.subject(e['NewStateValue'])
        header = objects.header(e['Trigger']['Namespace'], sentence="been Recovered to a \"Normal State\" !")
        
        message = textwrap.dedent("""\
            {Header}
            
            {Content}
        """).format(Header=header, Content=content).strip()
        
        print(subject)
        print(message)
        
    elif e['NewStateValue'] == "ALARM":
        subject = objects.subject(e['NewStateValue'])
        header = objects.header(e['Trigger']['Namespace'], sentence="detected an \"Abnormal State\" !")
        
        message = textwrap.dedent("""\
            {Header}
            
            {Content}
            
            {Footer}
        """).format(Header=header, Content=content, Footer=footer).strip()
        
        print(subject)
        print(message)
    
        
    response = client.publish(
        TopicArn = TOPIC_ARN,
        Message = message,
        Subject = subject
    )
    return response