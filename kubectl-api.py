from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/run_kubectl', methods=['GET'])
def run_kubectl():
    cmd = request.args.get('cmd')

    if not cmd:
        return jsonify({"error": "No command provided"}), 400

    # Split the command using shlex to handle spaces correctly
    cmd_list = shlex.split(cmd)

    # Ensure the command starts with 'kubectl'
    if cmd_list[0] != 'kubectl':
        return jsonify({"error": "Command must start with 'kubectl'"}), 400

    # Remove 'kubectl' from the command list
    cmd_list = cmd_list[1:]

    try:
        result = subprocess.run(['kubectl'] + cmd_list, check=True, capture_output=True, text=True)

        formatted_stdout = result.stdout.split('\n')
        
        return jsonify({
            "stdout": formatted_stdout,
            "stderr": result.stderr.split('\n'),
            "returncode": result.returncode
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Command execution failed",
            "stdout": e.stdout.split('\n'),
            "stderr": e.stderr.split('\n'),
            "returncode": e.returncode
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
