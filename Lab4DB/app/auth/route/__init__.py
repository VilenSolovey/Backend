from flask import Flask
from .error_handler import err_handler_bp

def register_routes(app: Flask) -> None:
    app.register_blueprint(err_handler_bp)

    from .request_route import requests_bp
    from .request_status_route import requeststatus_bp
    from .request_priority_route import requestpriority_bp
    from .employees_route import employees_bp
    from .equipment_route import equipment_bp
    from .equipment_changes_route import equipmentchanges_bp
    from .locations_route import locations_bp
    from .software_route import software_bp
    from .software_issues_route import softwareissues_bp
    from .software_update_route import softwareupdates_bp
    from .request_has_employees_route import requestshasemployees_bp
    from .request_has_request_issue_type_route import requestshasrequestissuetype_bp
    from .request_issue_type_route import requestissuetype_bp
    from .tasks_route import task_bp

    app.register_blueprint(requests_bp)
    app.register_blueprint(requeststatus_bp)
    app.register_blueprint(requestpriority_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(equipmentchanges_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(software_bp)
    app.register_blueprint(softwareissues_bp)
    app.register_blueprint(softwareupdates_bp)
    app.register_blueprint(requestshasemployees_bp)
    app.register_blueprint(requestshasrequestissuetype_bp)
    app.register_blueprint(requestissuetype_bp)
    app.register_blueprint(task_bp)