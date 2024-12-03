from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin

from algorithm import (
    Package,
    ULD,
    confirm_validity,
    get_data,
    return_data,
    stack_economy_packages,
    stack_priority_packages,
    transition_stacking,
    log,
    save_file_and_get_name,
)

app = Flask(__name__)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/get-coords", methods=["POST"])
@cross_origin()
def get_coords():
    priority_uld_cost = request.json["priority_uld_cost"]
    packages = request.json["packages"]
    ulds = request.json["ulds"]

    package_list = []
    for package in packages:
        pkg = Package(
            name=package["name"],
            dimensions=(package["length"], package["width"], package["height"]),
            weight=package["weight"],
            delay_cost=package["delayCost"],
            is_priority=package["isPriority"],
        )
        package_list.append(pkg)

    uld_list = []
    for uld in ulds:

        uld_list.append(
            ULD(
                name=uld["name"],
                dimensions=(uld["length"], uld["width"], uld["height"]),
                weight_limit=uld["maxWeight"],
            )
        )

    try:
        ulds, priority_packages, economy_packages, priority_uld_cost = get_data(
            package_list, uld_list, priority_uld_cost
        )

        last_priority_uld, remaining_ulds = stack_priority_packages(
            ulds, priority_packages
        )

        remaining_economy_packages = transition_stacking(
            last_priority_uld, economy_packages
        )

        stack_economy_packages(ulds, remaining_ulds, remaining_economy_packages)

        confirm_validity(ulds, priority_packages)

        output_data = return_data(ulds, package_list, priority_uld_cost)

        log("Algorithm output", output_data)

        return jsonify({"success": True, "data": output_data})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})


@app.route("/get-file", methods=["POST"])
@cross_origin()
def get_file():
    data = request.json["output_data"]
    fname = save_file_and_get_name(data)
    return jsonify({"success": True, "filename": fname})

@app.route("/download-file/<filename>", methods=["GET"])
@cross_origin()
def download_file(filename):
    return send_file(filename, as_attachment=True)




if __name__ == "__main__":
    app.run(debug=True, port=5000)
