import os
import threading

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


class Server:
    def __init__(self, ui_controller, web_dir="../../web"):
        self.ui_controller = ui_controller
        self.teams = {}
        self.current_buzz_team = None
        self.web_dir = os.path.abspath(web_dir)

        self.app = Flask(__name__, static_folder=self.web_dir)
        CORS(self.app)

        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            return send_from_directory(self.web_dir, "index.html")

        @self.app.route("/teams", methods=["GET"])
        def get_teams():
            teams = [
                team.name for team in self.ui_controller.game_controller.get_teams()
            ]
            return jsonify({"teams": teams})

        @self.app.route("/buzz", methods=["POST"])
        def buzz_in():
            data = request.json
            team_name = data.get("team")
            if team_name not in [
                team.name for team in self.ui_controller.game_controller.get_teams()
            ]:
                return jsonify({"error": "Invalid team"}), 400

            if self.current_buzz_team is None:
                self.current_buzz_team = team_name
                return jsonify({"success": True, "team": team_name})
            else:
                return jsonify(
                    {
                        "success": False,
                        "message": f"{self.current_buzz_team} already buzzed",
                    }
                ), 409

        @self.app.route("/reset_buzz", methods=["POST"])
        def reset_buzz():
            self.current_buzz_team = None
            return jsonify({"success": True})

    def start(self, host="0.0.0.0", port=5000):
        threading.Thread(
            target=lambda: self.app.run(
                host=host, port=port, debug=False, use_reloader=False
            ),
            daemon=True,
        ).start()
        print(f"[Flask] Server running at http://{host}:{port}")
