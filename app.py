from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Render the auto-refreshing attendance dashboard."""
    csv_path = 'attendance.csv'

    # Ensure attendance.csv exists
    if not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0:
        pd.DataFrame(columns=["Name", "Time"]).to_csv(csv_path, index=False)

    try:
        df = pd.read_csv(csv_path)

        # Clean names — remove extensions like .jpg, .png, etc.
        df["Name"] = df["Name"].apply(lambda x: os.path.splitext(str(x))[0].capitalize())

        # Convert dataframe to list for HTML table
        data = df.values.tolist()

    except Exception as e:
        print(f"⚠️ Error reading attendance.csv: {e}")
        data = []

    return render_template('index.html', data=data)


if __name__ == '__main__':
    print("🌐 AttendX Web Dashboard running at: http://127.0.0.1:5000/")
    print("🔁 Press CTRL+C to stop the server.")
    app.run(debug=True, use_reloader=False)
