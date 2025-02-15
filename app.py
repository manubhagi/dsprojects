from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Route to execute tasks
@app.route('/run', methods=['POST'])
def run_task():
    task = request.args.get('task')
    if not task:
        return jsonify({"error": "Task description is required"}), 400

    try:
        # Example task: Count the number of Wednesdays in /data/dates.txt
        if "count the number of Wednesdays" in task.lower():
            with open('/data/dates.txt', 'r') as file:
                dates = file.readlines()
            wednesdays = sum(1 for date in dates if date.strip().endswith('Wed'))
            with open('/data/dates-wednesdays.txt', 'w') as file:
                file.write(str(wednesdays))
            return jsonify({"message": "Task completed", "result": wednesdays}), 200

        return jsonify({"error": "Task not recognized"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to read file content
@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path is required"}), 400

    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(path, 'r') as file:
            content = file.read()
        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
