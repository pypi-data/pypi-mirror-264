"""dspygen REST API."""
import logging


import coloredlogs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware


from dspygen.utils.file_tools import dspy_modules_dir
from dspygen.workflow.workflow_router import router as workflow_router

app = FastAPI()


from importlib import import_module
import os

from dspygen.dsl.dsl_pipeline_executor import router as pipeline_router


app.include_router(pipeline_router)
app.include_router(workflow_router)


def load_module_routers(app: FastAPI):
    for filename in os.listdir(dspy_modules_dir()):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module = import_module(f"dspygen.modules.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)


@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()
    load_module_routers(app)



@app.get("/")
def read_root() -> str:
    """Read root."""
    return "Hello world"


# Define endpoint
@app.get("/pingpong")
def ping_pong():
    return {"message": "pong"}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Adjust as per your requirements
    allow_headers=["*"],  # Adjust this to your specific headers if needed
)
