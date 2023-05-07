import json
import textwrap
import time

now = time.strftime('%Y/%m/%d %H:%M:%S')

class Subjects(object):
    def __init__(self, region, account, alarmName, metricname):
        self.region = region
        self.account = account
        self.alarmName = alarmName
        self.metricname = metricname
    
    def subject(self, stateValue):
        title = '"' + stateValue + '!\": ' + self.alarmName + '.'
        
        return title
        
        
class Messages(Subjects):
    def header(self, namespace, sentence):
        header = (now + ". UTC. \n" 
        + "You are receiving this Alert By Amazon CloudWatch in the" + self.region + "\n\n"
        + namespace + " " + self.metricname + " " + "has" + " " + sentence
        )
        
        return header
        
    def contents(self, alarmArn, description=None):
        contents = ("Alarm Details: \n"
        + "- Alarm Name:" +  self.alarmName + "\n"
        + "- Alarm Description:" + description + "\n"
        + "- AWSAccountId:" + self.account + "\n"
        + "- Alarm Arn:" + alarmArn
        )
        
        return contents
        
    def footer(self, ComparisonOperator, threshold, statistic):
        footer = ("Threshold: \n"
        + "- The alarm is warning when the" + " " + self.metricname + " " +"is" + " " + ComparisonOperator + " " + threshold + " " + "on" + " " + statistic + "." 
        )
        
        return footerßß