from finter.framework_model.submission.config import (
    get_model_info,
    validate_and_get_benchmark_name,
    validate_and_get_model_type_name,
)
from finter.framework_model.submission.helper_github import commit_folder_to_github
from finter.framework_model.submission.helper_notebook import (
    extract_and_convert_notebook,
)
from finter.framework_model.submission.helper_position import load_and_get_position
from finter.framework_model.submission.helper_simulation import Simulation
from finter.framework_model.submission.helper_submission import submit_model
from finter.framework_model.validation import ValidationHelper
from finter.settings import log_section, log_warning, logger


class NotebookSubmissionHelper:
    """
    A helper class to facilitate the submission process of financial models
    developed in Jupyter Notebooks. It supports extracting relevant cells from a
    notebook, running simulations, performing validations, and submitting the model
    for further use or evaluation.

    Attributes:
        cell_indices (list): Indices of the cells to extract from the notebook.
        notebook_name (str): The name of the notebook file (including path if necessary).
        model_name (str): The path where the model will be saved. The last part of the path is considered the name of the model. For example, 'path/to/model_name' would save the model in the 'path/to/' directory with 'model_name' as the model name.
        model_universe (str): The universe for the model (e.g. "kr_stock").
        model_type (str): The type of the model (e.g. "alpha" or "portfolio").
        benchmark (str): The benchmark to use for the model. Default is None. If not specified, the default benchmark for the model universe will be used. If False, no benchmark will be used.
    """

    def __init__(
        self,
        notebook_name,
        model_name,
        model_universe,
        model_type="alpha",
        benchmark=None,
    ):
        """
        Initializes the NotebookSubmissionHelper with necessary information.

        Parameters:
            notebook_name (str): The name of the notebook file (including path if necessary).
            model_name (str): The path where the model will be saved. The last part of the path is considered the name of the model. This allows for specifying the directory to save the model along with the model's name. For example, 'path/to/model_name' would save the model in the 'path/to/' directory with 'model_name' as the model name.
            model_universe (str): The universe for the model (e.g. "kr_stock").
            model_type (str): The type of the model (e.g. "alpha" or "portfolio").
            benchmark (str): The benchmark to use for the model. Default is None. If not specified, the default benchmark for the model universe will be used. If False, no benchmark will be used.
        """
        log_warning(
            "!!! IMPORTANT: Please ensure your current notebook is SAVED before proceeding with the submission process. !!!"
        )

        self.notebook_name = notebook_name
        self.model_name = model_name
        self.notebook_name = notebook_name
        self.model_name = model_name
        self.model_universe = model_universe

        self.model_info = get_model_info(model_universe, model_type)
        self.model_type = validate_and_get_model_type_name(model_type)
        self.benchmark = validate_and_get_benchmark_name(model_universe, benchmark)

    def process(
        self,
        start,
        end,
        position=False,
        simulation=False,
        validation=False,
        submit=False,
        git=False,
    ):
        """
        Processes the notebook by extracting specified cells, and optionally running position extraction,
        simulation, validation, and submission steps. Validation is automatically performed if submission is
        requested. Position extraction is mandatory for simulation.

        Parameters:
            start (str): The start date for the simulation and validation processes.
            end (str): The end date for the simulation and validation processes.
            position (bool): Flag to determine whether to extract positions from the model. Default is False.
            simulation (bool): Flag to determine whether to run a simulation based on the extracted positions. Default is False.
            validation (bool): Flag to determine whether to validate the model. Default is False.
            submit (bool): Flag to determine whether to submit the model. Default is False.
            git (bool): Flag to determine whether to commit the model to GitHub. Default is False.
        """
        # Extract and convert the notebook
        log_section("Notebook Extraction")
        output_file_path = extract_and_convert_notebook(
            self.notebook_name,
            self.model_name,
            model_type=self.model_type,
        )

        if not output_file_path:
            logger.error("Error extracting notebook.")
            return
        logger.info(f"Notebook extracted to {output_file_path}")

        # Ensure position extraction if simulation is requested
        if simulation and not position:
            position = True
            logger.warning(
                "Position extraction is required for simulation. Setting position=True."
            )

        # Perform position extraction if required
        if position:
            log_section("Position Extraction")
            self.position = load_and_get_position(
                start, end, output_file_path, model_type=self.model_type
            )
            if self.position is None:
                logger.error("Error running notebook for position extraction.")
                return
            logger.info("Position extraction from notebook ran successfully.")

        # Run simulation with the extracted positions if requested
        if simulation:
            self.model_stat = Simulation(
                model_universe=self.model_universe,
                model_type=self.model_type,
                position=self.position,
                benchmark=self.benchmark,
            ).run(start, end)

        # Validate the model if requested
        if validation:
            log_section("Validation")
            validator = ValidationHelper(
                model_path=self.model_name, model_info=self.model_info
            )
            validator.validate()
            logger.info("Model validated successfully.")

        # Submit the model if requested
        if submit:
            log_section("Model Submission")
            self.submit_result = submit_model(self.model_info, self.model_name)
            logger.info("Model submitted successfully.")

        # Commit the model to GitHub if requested
        if git:
            log_section("GitHub Commit")
            commit_folder_to_github(folder_path=self.model_name)
            logger.info("Model committed to GitHub successfully.")
