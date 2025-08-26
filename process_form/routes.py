from flask import Blueprint, jsonify, request
from .models import db, ProcessDetails
from datetime import datetime

process_bp = Blueprint("process", __name__)

@process_bp.route("/departments", methods=["GET"])
def get_departments():
    departments = db.session.query(ProcessDetails.ProcessOwnerDepartment).distinct().all()
    return jsonify([d[0] for d in departments])

@process_bp.route("/functions/<department>", methods=["GET"])
def get_functions(department):
    functions = (
        db.session.query(ProcessDetails.ProcessOwnerFunction)
        .filter(ProcessDetails.ProcessOwnerDepartment == department)
        .distinct()
        .all()
    )
    return jsonify([f[0] for f in functions])

@process_bp.route("/availableprocesses/<function>", methods=["GET"])
def get_processes(function):
    processes = (
        db.session.query(
            ProcessDetails.ProcessCode,
            ProcessDetails.ProcessName,
            ProcessDetails.ProcessDefinition,
        )
        .filter(ProcessDetails.ProcessOwnerFunction == function)
        .distinct()
        .all()
    )
    return jsonify(
        [
            {
                "ProcessCode": p.ProcessCode,
                "ProcessName": p.ProcessName,
                "ProcessDefinition": p.ProcessDefinition,
            }
            for p in processes
        ]
    )

@process_bp.route("/tasks/<process_name>", methods=["GET"])
def get_activities(process_name):
    activities = (
        db.session.query(
            ProcessDetails.Activity,
            ProcessDetails.Description,
            ProcessDetails.ResponsibleRole,
            ProcessDetails.RequiredTimeMins,
            ProcessDetails.ResponsibleEmpNo,
            ProcessDetails.TransactionsCount,
            ProcessDetails.RemarksForTransaction
        )
        .filter(ProcessDetails.ProcessName == process_name)
        .all()
    )

    if not activities:
        return jsonify({"error": "Process not found"}), 404

    # Extract transactions count  and remarks from the first record
    transactions_count = activities[0].TransactionsCount if activities else 0
    remarks = activities[0].RemarksForTransaction if activities else 0

    task_list = [
        {
            "Activity": a.Activity,
            "Description": a.Description,
            "ResponsibleRole": a.ResponsibleRole,
            "RequiredTime": a.RequiredTimeMins,
            "ResponsibleEmpNo": a.ResponsibleEmpNo
        }
        for a in activities
    ]

    return jsonify({
        "process_name": process_name,
        "no_of_transactions": transactions_count,
        "remarks": remarks,
        "tasks": task_list
    })

@process_bp.route("/submit", methods=["POST"])
def submit_process_details():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    
    process_name = data.get("process_name")
    no_of_transactions = data.get("no_of_transactions")
    tasks = data.get("tasks")  # list of tasks with Activity, RequiredTimeMins, ResponsibleEmpNo
    remarks = data.get("remarks") 

    # Fetch all rows for the process
    process_rows = ProcessDetails.query.filter_by(ProcessName=process_name).all()
    if not process_rows:
        return jsonify({"error": "Process not found"}), 404

    # Update process-level info for all rows
    for row in process_rows:
        row.TransactionsCount = no_of_transactions
        row.RemarksForTransaction = remarks
        row.UpdatedAt = datetime.utcnow()

    # Update task-level info
    for t in tasks:
        task_record = ProcessDetails.query.filter_by(ProcessName=process_name, Activity=t["Activity"]).first()
        if task_record:
            task_record.RequiredTimeMins = t["RequiredTimeMins"]
            task_record.ResponsibleEmpNo = t["ResponsibleEmpNo"]
            task_record.UpdatedAt = datetime.utcnow()

    db.session.commit()
    return jsonify({"message": "Details for the current process submitted successfully"}), 200

@process_bp.route("/processdetails/<string:process_name>", methods=["GET"])
def get_process_details(process_name):
    
    processes = ProcessDetails.query.filter_by(ProcessName=process_name).all()
    
    if not processes:
        return jsonify({"error": "Process not found"}), 404

    task_list = [
        {
            "Activity": p.Activity,
            "ResponsibleRole": p.ResponsibleRole,
            "RequiredTime": p.RequiredTimeMins,
            "ResponsibleEmpNo": p.ResponsibleEmpNo
        }
        for p in processes
    ]

    return jsonify({
        "process_name": processes[0].ProcessName,
        "no_of_transactions": processes[0].TransactionsCount,
        "tasks": task_list
    })
    
@process_bp.route("/deptfunctions/access-codes", methods=["GET"])
def get_dept_function_access_codes():
    proccessdetails = (
    db.session.query(ProcessDetails.ProcessOwnerFunction, ProcessDetails.AccessCode)
    .distinct()
    .all()
)
    data = [
    {"function": func, "accessCode": code}
    for func, code in proccessdetails
]
    return jsonify(data)