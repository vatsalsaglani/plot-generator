import requests

# url = "http://localhost:5000/api/generatePlot"
url = "http://localhost:5000/kafka/returnPlotQueue"
json = {
    "genre": str(input("Genre: ")),
    "director": str(input("Director: ")),
    "cast": str(input("Cast: ")),
    "ethnicity": str(input("Ethnicity: ")),
    "num_plots": int(input("Num Plots: ")),
    "seq_len": int(input("Sequence Length: ")),
    "email": "saglanivatsal@gmail.com"
}

r = requests.post(url, json = json)
print(r.json())