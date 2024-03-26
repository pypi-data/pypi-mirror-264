"""
CogFramework: A class for defining reusable components and pipelines for Kubeflow Pipelines.

CogContainer: A subclass of Container that extends it with additional functionality for
adding environment variables related to model access.

CogFramework:
- Initializes methods to add model access environment variables to Container classes.
- Defines a static method `pipeline` to create pipeline decorators for defining Kubeflow Pipelines.
- Provides methods for creating components from Python functions, managing the Kubeflow Pipeline client,
and loading components from URLs.
- Provides methods for defining InputPath and OutputPath components.
"""

import time
import os
from cogflow import constant_vars
import pandas as pd
import numpy as np
import mlflow as ml
import kfp
import kserve
from typing import Union
from kubernetes.client.models import V1EnvVar
from kfp import dsl
from mlflow.models.signature import ModelSignature
from scipy.sparse import csr_matrix, csc_matrix
from kfp.components import InputPath, OutputPath
from tenacity import retry, stop_after_attempt, wait_exponential
from kserve import KServeClient
from kubernetes import client
from kserve import utils
from mlflow.tracking import MlflowClient
from datetime import datetime
from kubernetes.client.exceptions import ApiException
from kubernetes.client import V1ObjectMeta
from kubernetes import client as k8s_client, config as k8s_config
from kserve import (
    constants,
    KServeClient,
    V1beta1InferenceService,
    V1beta1InferenceServiceSpec,
    V1beta1PredictorSpec,
    V1beta1TFServingSpec,
    V1beta1ModelFormat,
    V1beta1ModelSpec,
    V1beta1SKLearnSpec,
)


class CogContainer(kfp.dsl._container_op.Container):
    """
    Subclass of Container to add model access environment variables.
    """

    def __init__(self):
        """
        Initializes the CogContainer class.
        """
        super().__init__()

    def AddModelAccess(self):
        """
        Adds model access environment variables to the container.

        Returns:
            CogContainer: Container instance with added environment variables.
        """
        return (
            self.add_env_variable(
                V1EnvVar(
                    name=constant_vars.TRACKING_URI,
                    value=os.getenv(constant_vars.TRACKING_URI),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=constant_vars.S3_ENDPOINT_URL,
                    value=os.getenv(constant_vars.S3_ENDPOINT_URL),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=constant_vars.ACCESS_KEY_ID,
                    value=os.getenv(constant_vars.ACCESS_KEY_ID),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=constant_vars.SECRET_ACCESS_KEY,
                    value=os.getenv(constant_vars.SECRET_ACCESS_KEY),
                )
            )
        )


class CogModel(ml.pyfunc.PythonModel):
    """
    A custom MLflow PythonModel implementation for demonstration purposes.
    """

    def __init__(self):
        """
        Constructor for the CustomModel class.
        """
        pass

    def fit(self):
        """
        Train the model.

        This method is called to train the model.
        """
        print("Fitting model...")

    def predict(self, context, model_input: [str]):  # type: ignore
        """
        Generate predictions.

        This method generates predictions based on the input data.

        Parameters:
            context (Any): Additional context or information passed to the prediction function.
            model_input (List[str]): List of input strings for prediction.

        Returns:
            None: This method prints the predictions instead of returning them.
        """
        print(self.get_prediction(model_input))

    def get_prediction(self, model_input: [str]):  # type: ignore
        """
        Generate predictions.

        This method generates predictions based on the input data.

        Parameters:
            model_input (List[str]): List of input strings for prediction.

        Returns:
            str: The concatenated uppercase version of the input strings.
        """

        return " ".join([w.upper() for w in model_input])


class CogFramework:
    """
    Class for defining reusable components and pipelines for Kubeflow Pipelines.
    """

    def __init__(self):
        """
        Initializes the CogFramework class.
        """
        kfp.dsl._container_op.Container.AddModelAccess = self.AddModelAccess
        kfp.dsl._container_op.ContainerOp.AddModelAccess = self.AddModelAccess
        self.mlflow = ml
        self.sklearn = ml.sklearn
        self.tensorflow = ml.tensorflow
        self.pyfunc = ml.pyfunc
        self.models = ml.models
        self.cogclient = MlflowClient()

    def delete_registered_model(self, model_name):
        """
        Deletes a registered model with the given name.

        Args:
            model_name (str): The name of the registered model to delete.

        Returns:
            bool: True if the model was successfully deleted, False otherwise.
        """
        return self.cogclient.delete_registered_model(model_name)

    def search_registered_models(self):
        """
        Searches for registered models.

        Returns:
            list: A list of registered model objects matching the search criteria.
        """
        registered_models = self.cogclient.search_registered_models()
        return registered_models

    def load_model(self, model_name: str, model_version: int):
        """
        Loads a model from MLflow.

        Args:
            model_name (str): The name of the registered MLflow model.
            model_version (int): The version of the registered MLflow model.

        Returns:
            loaded_model: The loaded model.
        """
        model_uri = f"models:/{model_name}/{model_version}"
        loaded_model = ml.sklearn.load_model(model_uri)
        return loaded_model

    def register_model(self, model, model_uri):
        """
        Registers the given model with MLflow.

        Args:
            model: The model object to register.
            model_uri (str): The MLflow model URI.
        """
        return ml.register_model(model, model_uri)

    def autolog(self):
        """
        Enable automatic logging of parameters, metrics, and models with MLflow.

        Returns:
            None
        """
        return self.mlflow.autolog()

    # def cogclient(self):
    #     """
    #     Get the MLflow Tracking client.

    #     Returns:
    #         MlflowClient: MLflow Tracking client instance.
    #     """
    #     return MlflowClient()

    def create_registered_model(self, name):
        """
        Create a registered model.

        Args:
            name (str): Name of the registered model.

        Returns:
            str: ID of the created registered model.
        """
        # client = self.cogclient()
        return self.cogclient.create_registered_model(name)

    def create_model_version(self, name, source):
        """
        Create a model version for a registered model.

        Args:
            name (str): Name of the registered model.
            source (str): Source path or URI of the model.

        Returns:
            str: ID of the created model version.
        """
        # client = self.cogclient()
        return self.cogclient.create_model_version(name, source)

    def set_tracking_uri(self, tracking_uri):
        """
        Set the MLflow tracking URI.

        Args:
            tracking_uri (str): The URI of the MLflow tracking server.

        Returns:
            None
        """
        return self.mlflow.set_tracking_uri(tracking_uri)

    def set_experiment(self, experiment_name):
        """
        Set the active MLflow experiment.

        Args:
            experiment_name (str): The name of the experiment to set as active.

        Returns:
            None
        """
        return self.mlflow.set_experiment(experiment_name)

    def get_artifact_uri(self, run_id=None):
        """
        Get the artifact URI of the current or specified MLflow run.

        Args:
            run_id (str, optional): ID of the MLflow run. If not provided, the current run's artifact URI is returned.

        Returns:
            str: Artifact URI of the specified MLflow run.
        """
        return self.mlflow.get_artifact_uri(run_id)

    def start_run(self, experiment_name=None, run_name=None):
        """
        Start an MLflow run.

        Args:
            experiment_name (str): Name of the MLflow experiment to log the run to.
            run_name (str): Name of the MLflow run.

        Returns:
            MLflow Run object
        """
        return self.mlflow.start_run(run_name=run_name)

    def end_run(self):
        """
        Start an MLflow run.

        Args:
            experiment_name (str): Name of the MLflow experiment to log the run to.
            run_name (str): Name of the MLflow run.

        Returns:
            MLflow Run object
        """
        return self.mlflow.end_run()

    def log_param(self, *args):
        """
        Log parameters to the MLflow run.

        Args:
            run: MLflow Run object returned by start_mlflow_run method.
            params (dict): Dictionary containing parameters to log.

        Returns:
            None
        """
        return self.mlflow.log_param(*args)

    def log_metric(self, *args):
        """
        Log metrics to the MLflow run.

        Args:
            run: MLflow Run object returned by start_mlflow_run method.
            metrics (dict): Dictionary containing metrics to log.

        Returns:
            None
        """
        return self.mlflow.log_metric(*args)

    def log_model(
        self,
        sk_model,
        artifact_path,
        conda_env=None,
        code_paths=None,
        serialization_format="cloudpickle",
        registered_model_name=None,
        signature: ModelSignature = None,
        input_example: Union[
            pd.DataFrame,
            np.ndarray,
            dict,
            list,
            csr_matrix,
            csc_matrix,
            str,
            bytes,
            tuple,
        ] = None,
        await_registration_for=300,
        pip_requirements=None,
        extra_pip_requirements=None,
        pyfunc_predict_fn="predict",
        metadata=None,
    ):
        return self.mlflow.sklearn.log_model(
            sk_model=sk_model,
            artifact_path=artifact_path,
            conda_env=conda_env,
            code_paths=code_paths,
            serialization_format=serialization_format,
            registered_model_name=registered_model_name,
            signature=signature,
            input_example=input_example,
            await_registration_for=await_registration_for,
            pip_requirements=pip_requirements,
            extra_pip_requirements=extra_pip_requirements,
            pyfunc_predict_fn=pyfunc_predict_fn,
            metadata=metadata,
        )

    def pipeline(name=None, description=None):
        """
        Decorator function to define Kubeflow Pipelines.

        Args:
            name (str, optional): Name of the pipeline. Defaults to None.
            description (str, optional): Description of the pipeline. Defaults to None.

        Returns:
            Callable: Decorator for defining Kubeflow Pipelines.
        """
        return dsl.pipeline(name=name, description=description)

    def create_component_from_func(
        func, output_component_file=None, base_image=None, packages_to_install=None
    ):
        """
        Create a component from a Python function.

        Args:
            func (Callable): Python function to convert into a component.
            output_component_file (str, optional): Path to save the component YAML file. Defaults to None.
            base_image (str, optional): Base Docker image for the component. Defaults to None.
            packages_to_install (List[str], optional): List of additional Python packages to install in the component.
            Defaults to None.

        Returns:
            kfp.components.ComponentSpec: Component specification.
        """
        training_var = kfp.components.create_component_from_func(
            func=func,
            output_component_file=output_component_file,
            base_image=base_image,
            packages_to_install=packages_to_install,
        )
        kfp.dsl._container_op.ContainerOp.AddModelAccess = CogFramework.AddModelAccess
        return training_var

    def client():
        """
        Get the Kubeflow Pipeline client.

        Returns:
            kfp.Client: Kubeflow Pipeline client instance.
        """
        return kfp.Client()

    def load_component_from_url(url):
        """
        Load a component from a URL.

        Args:
            url (str): URL to load the component from.

        Returns:
            kfp.components.ComponentSpec: Loaded component specification.
        """
        return kfp.components.load_component_from_url(url)

    def InputPath(label: str):
        """
        Create an InputPath component.

        Args:
            label (str): Label for the input path.

        Returns:
            InputPath: InputPath component instance.
        """
        return kfp.components.InputPath(label)

    def OutputPath(label: str):
        """
        Create an OutputPath component.

        Args:
            label (str): Label for the output path.

        Returns:
            OutputPath: OutputPath component instance.
        """
        return kfp.components.OutputPath(label)

    def AddModelAccess(self):
        """
        Add model access environment variables to the container.

        Returns:
            CogContainer: Container instance with added environment variables.
        """
        return (
            self.add_env_variable(
                V1EnvVar(
                    name=constant_vars.TRACKING_URI,
                    value=os.getenv(constant_vars.TRACKING_URI),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=constant_vars.S3_ENDPOINT_URL,
                    value=os.getenv(constant_vars.S3_ENDPOINT_URL),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=constant_vars.ACCESS_KEY_ID,
                    value=os.getenv(constant_vars.ACCESS_KEY_ID),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=constant_vars.SECRET_ACCESS_KEY,
                    value=os.getenv(constant_vars.SECRET_ACCESS_KEY),
                )
            )
        )

    def Serve_Model_v2(model_uri: str, name: str):
        """
        Create a kserve instance.

        Args:
            model_uri (str): URI of the model.
            name (str, optional): Name of the kserve instance. If not provided, a default name will be generated.

        Returns:
            None
        """

        namespace = utils.get_default_target_namespace()
        if name is None:
            now = datetime.now()
            v = now.strftime("%d%M")
            name = "predictor_model{}".format(v)
        ISVC_NAME = name
        predictor = V1beta1PredictorSpec(
            service_account_name="kserve-controller-s3",
            min_replicas=1,
            model=V1beta1ModelSpec(
                model_format=V1beta1ModelFormat(
                    name=constant_vars.ML_TOOL,
                ),
                storage_uri=model_uri,
                protocol_version="v2",
            ),
        )

        isvc = V1beta1InferenceService(
            api_version=constants.KSERVE_V1BETA1,
            kind=constants.KSERVE_KIND,
            metadata=client.V1ObjectMeta(
                name=ISVC_NAME,
                namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"},
            ),
            spec=V1beta1InferenceServiceSpec(predictor=predictor),
        )
        KServe = KServeClient()
        try:
            KServe.create(isvc)
        except ApiException as e:
            if e.status == 409:
                # Handle the conflict error
                print("Inference service already exists.")
            else:
                #    Handle other ApiException errors
                print("An error occurred:", e)

    def Serve_Model_v1(model_uri: str, name: str):
        """
        Create a kserve instance version1.

        Args:
            model_uri (str): URI of the model.
            name (str, optional): Name of the kserve instance. If not provided, a default name will be generated.

        Returns:
            None
        """

        ISVC_NAME = name
        namespace = utils.get_default_target_namespace()
        isvc = V1beta1InferenceService(
            api_version=constants.KSERVE_V1BETA1,
            kind=constants.KSERVE_KIND,
            metadata=V1ObjectMeta(
                name=ISVC_NAME,
                namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"},
            ),
            spec=V1beta1InferenceServiceSpec(
                predictor=V1beta1PredictorSpec(
                    service_account_name="kserve-controller-s3",
                    sklearn=V1beta1SKLearnSpec(storage_uri=model_uri),
                )
            ),
        )

        client = KServeClient()
        client.create(isvc)
        time.sleep(constant_vars.Timer_IN_SEC)

    def GetModelUrl(modelName: str):
        """
        Retrieve the URL of a deployed model.

        Args:
            modelName (str): Name of the deployed model.

        Returns:
            str: URL of the deployed model.
        """
        client = KServeClient()
        namespace = utils.get_default_target_namespace()

        time.sleep(constant_vars.Timer_IN_SEC)
        isvc_resp = client.get(modelName)
        isvc_url = isvc_resp["status"]["address"]["url"]
        print(isvc_url)
        return isvc_url
