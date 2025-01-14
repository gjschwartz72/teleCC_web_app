from web_app import app, db
from flask import render_template, request, jsonify, url_for, redirect
from orm_models import Patient_telecc_state, Patient_telecc_history, Station_lookup
from forms import StationSelectionForm
from get_patient_details_json import get_patient_details_json

# Cache for storing loaded data
cache = {}

@app.route("/index", methods = ["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def splash():
    """Render the splash screen and handle station selection."""
    form = StationSelectionForm()
    
    # Dynamically populate the SelectField with station data
    #form.station_id.choices = [(station.station_number, station.station_name) for station in Station_lookup.query.all()]
    form.stations = Station_lookup.query.all()
    cache['stations'] = form.stations

    if form.validate_on_submit():
        # Redirect to load_data route with the selected station ID
        station_id = form.station_id.data
        return redirect(url_for("load_data", station_id=station_id))

    return render_template("splash.html", form=form)

@app.route('/load_data/<int:station_id>')
def load_data(station_id):
    #station_id = request.args.get('station_id')
    # Handle the station_id as needed

    # Use the station name from the first patient (replace with actual logic)
    station = Station_lookup.query.filter_by(station_number = station_id).all()
    station_name = station[0].station_name
 
    # Render the table template
    station_list = Patient_telecc_state.query.filter_by(station_number = station_id).all()
    if station_list:
        prediction_datetime = station_list[0].prediction_datetime
        station_list_sorted = sorted(station_list, key=lambda p: p.patientName.split()[-1])
    else:
        prediction_datetime = None

    return render_template(
        'patient_list.html',
        station_name=station_name,
        patients=station_list_sorted,
        stations = cache['stations'],
        prediction_datetime = prediction_datetime
    )

    
    return f"Loading data for station: {station_id}, {len(station_list)}"

@app.route("/testing", methods = ['GET', 'POST'])
def test():
    return render_template("patient_details.html")


@app.route('/get_patient_details/<int:patient_id>', methods=['GET'])
def get_patient_details(patient_id):
    """
    Endpoint to fetch detailed information about a specific patient.
    """
    print("Here I AM!")
    response_data = get_patient_details_json(patient_id)
    print("I've got the goods :-)")
    return (response_data.json)