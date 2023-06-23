import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,4}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message _ date type
    df[' message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={' message_date': 'date'}, inplace=True)
    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([w\w]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df.drop(columns=['message_date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num']=df['date'].dt.month

    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+ "-"+str('0'))
        elif hour==0:
            period.append(str('00')+ "-"+str(hour+1))
        else:
            period.append(str(hour)+ "-"+str(hour+1))
    df['period'] = period

    return df