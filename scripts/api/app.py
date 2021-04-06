from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from kafka import KafkaConsumer, KafkaProducer
from concurrent.futures import ThreadPoolExecutor
import uuid


from predict import PredictionModelObject

# from plot_consumer import predictionObject

app = Flask(__name__)
CORS(app)

print("Loading Model Object")
predictionObject = PredictionModelObject()
print("Loaded Model Object")


TOPIC_NAME = "MESSAGES"
KAFKA_SERVER = "localhost:9092"

consumer = KafkaConsumer(
    "TOPIC_NAME",
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
)

producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    api_version = (0, 11, 15)
)

     
        


@app.route('/api/generatePlot', methods=['POST'])
def gen_plot():

    req = request.get_json()
    genre = req['genre']
    director = req['director']
    cast = req['cast']
    ethnicity = req['ethnicity']
    num_plots = req['num_plots']
    seq_len = req['seq_len']

    if not isinstance(num_plots, int) or not isinstance(seq_len, int):
        return jsonify({
            "message": "Number of words in plot and Number of plots must be integers",
            "status": "Fail"
        })
    # assert isinstance(seq_len, int) and isinstance(num_plots, int), return jsonify({"message": "Number of words in plot and Number of plots must be integers", "status": "Fail"})
 
    try:
        plot, status = predictionObject.returnPlot(
            genre = genre, 
            director = director,
            cast = cast,
            ethnicity = ethnicity,
            seq_len = seq_len,
            seq_num = num_plots
        )

        if status == 'Pass':
            
            plot["message"] = "Success!"
            plot["status"] = "Pass"
            return jsonify(plot)
        
        else:

            return jsonify({"message": plot, "status": status})
    
    except Exception as e:

        return jsonify({"message": "Error getting plot for the given input", "status": "Fail"})



@app.route('/kafka/returnPlotQueue', methods=['POST'])
def kafkaProducer():

    req = request.get_json()
    json_payload = json.dumps(req)
    json_payload = str.encode(json_payload)
    producer.send(TOPIC_NAME, json_payload)
    producer.flush()
    print("Sent to consumer")
    return jsonify({
        "message": "You will receive an email in a short while with the plot", 
        "status": "Pass"})


if __name__ == "__main__":
    app.run(debug=True)
    

    