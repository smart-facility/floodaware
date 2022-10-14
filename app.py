from flask import Flask
import os, re, datetime, pytz
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

app = Flask(__name__)

engine = create_engine(f"postgresql://postgres:1234@floodaware-db.postgres.database.azure.com:5432/floodaware", future=True)

@app.route("/newfile")
def newfile():
    print("Configuring experiment")
    tz = pytz.timezone("Australia/Sydney")
    endtime = datetime.datetime.now()
    starttime = endtime - datetime.timedelta(hours=24)
    startstring = starttime.astimezone(tz).strftime("%Y%m%d")
    endstring = endtime.astimezone(tz).strftime("%Y%m%d %H:%M")
    

    file = open("gama/experiments/config_mhl.json", "r")
    contents = file.read()
    file.close()
    file = open("gama/experiments/config_mhl.json", "w")
    contents = re.sub(r"start\".*\"", f"start\":\"{startstring}\"", contents)
    contents = re.sub(r"end\".*\"", f"end\":\"{endstring}\"", contents)
    file.write(contents)
    file.close()

    file = open("gama/experiments/config_bom.json", "r")
    contents = file.read()
    file.close()
    file = open("gama/experiments/config_bom.json", "w")
    contents = re.sub(r"start\".*\"", f"start\":\"{startstring}\"", contents)
    contents = re.sub(r"end\".*\"", f"end\":\"{endstring}\"", contents)
    file.write(contents)
    file.close()
    #starttime = 
    print("Initialising gama")
    os.system("bash run_gama.sh")
    print("Beginning transaction")
    session = Session(engine)
    with session.begin():
        session.execute("""
        DELETE FROM experiment_data WHERE index = 9000001
        """)
        session.execute(text("""
        INSERT INTO experiment_data (SELECT 9000001 AS index, timestep, catchment, rain_in, rain_buffer, storage, flow FROM experiment_data WHERE index=9000000)
        """))
        session.execute("""
        DELETE FROM experiment_data WHERE index = 9000000
        """)
    print("Transaction complete")
    return "updated"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)