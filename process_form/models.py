from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects import mssql
from sqlalchemy import Numeric

db = SQLAlchemy()

class ProcessDetails(db.Model):
    __tablename__ = "ProcessDetails"
    __table_args__ = {"schema": "process_mgmt"}

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProcessOwnerDepartment = db.Column(db.String(100), nullable=False)
    ProcessOwnerFunction = db.Column(db.String(100), nullable=False)
    ProcessCode = db.Column(mssql.NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)
    ProcessName = db.Column(mssql.NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)
    ProcessDefinition = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    SqNo = db.Column(db.String(100), nullable=True)
    Activity = db.Column(mssql.NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)
    Description = db.Column(mssql.NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)
    Output = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    ResponsibleRole = db.Column(mssql.NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)
    Accountable = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    Consulted = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    Informed = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    SLA = db.Column(db.Integer, nullable=True)
    System = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    ResponsibleEmpNo = db.Column(db.String(50), nullable=True)
    ResponsibleEmpName = db.Column(db.String(100), nullable=True)
    TransactionsCount = db.Column(db.Integer, nullable=True)
    RequiredTimeMins = db.Column(Numeric(10, 2), nullable=True)
    RemarksForTransaction = db.Column(mssql.NVARCHAR(None), nullable=True)  # NVARCHAR(MAX)
    AccessCode = db.Column(mssql.NVARCHAR(100), nullable=False)  # NVARCHAR(100)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<ProcessDetails(Id={self.Id}, "
            f"ProcessCode='{self.ProcessCode}', ProcessName='{self.ProcessName}')>"
        )
