from tqdm import tqdm
import pandas as pd
import collections


def pre_process(df):
    
    lines = collections.defaultdict(list)

    processed_msgs = []

    print ("Preprocessing...")
    for message in tqdm(df["messages"]):
        msg = ""
        if type(message["text"]) == type([]):
            for ele in message["text"]:
                if type(ele) == type(""):
                    msg += ele
        else:
            msg = message["text"]

        if "SHIB" in msg or "shib" in msg or "DOGE" in msg or "doge" in msg:
            msg = msg.replace('\n', '')
            msg = bytes(msg, 'utf-8').decode('utf-8', 'ignore')
            processed_msgs.append([msg, message["date"][:10]])
    print("Completed")


    return pd.DataFrame(processed_msgs, columns=["Msg", "Date"])


