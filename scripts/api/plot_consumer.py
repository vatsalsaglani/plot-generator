from kafka import KafkaConsumer

import json
import uuid
from concurrent.futures import ThreadPoolExecutor

from predict import PredictionModelObject



print("Loading Model Object")
predictionObject = PredictionModelObject()
print("Loaded Model Object")

TOPIC_NAME = "MESSAGES"

KAFKA_SERVER = "localhost:9092"

consumer = KafkaConsumer(
    TOPIC_NAME,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

## getplot func
def getPlotFunc(msg):
    genre = msg['genre']
    cast = msg['cast']
    director = msg['director']
    ethnicity = msg['ethnicity']
    num_plots = msg['num_plots']
    seq_len = msg['seq_len']
    email = msg['email']
    print(genre, cast, director, ethnicity, num_plots, seq_len, email)
    print("Provided to object")
    plots, status = predictionObject.returnPlot(
        genre = genre, director = director, cast = cast,
        ethnicity = ethnicity, seq_len = seq_len, seq_num = num_plots
    )
    print(plots)

    with open(f'{email}-{str(uuid.uuid4())}.json', 'w') as fp:
        json.dump(plots, fp)


## consumer
with ThreadPoolExecutor(4) as tpool:

    for msg in consumer:

        msg = msg.value

        print("Got Messsage: ", msg)

        # getPlotFunc(msg)
        future = tpool.submit(getPlotFunc, msg)

        print("Submitted to pool")