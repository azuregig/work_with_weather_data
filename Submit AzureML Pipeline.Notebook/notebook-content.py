# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Pre-requisite
# **!**  upload a `.env` file to the `builtin` resources with the following format.
# ```
# AZURE_TENANT_ID=<your_tenant_id>
# AZURE_CLIENT_ID=<your_sp_client_id>
# AZURE_CLIENT_SECRET=<your_sp_secret>
# ```
# 
# **Alternatively**, use the shell magic below to write a .env file, but take care to remove sensitive data from the notebook before sharing it. 

# CELL ********************

# MAGIC %%sh
# MAGIC #rm builtin/.env
# MAGIC #touch builtin/.env
# MAGIC # echo "AZURE_TENANT_ID=<your tenant>" >> builtin/.env
# MAGIC # echo "AZURE_CLIENT_ID=<your sp client id>" >> builtin/.env
# MAGIC # echo "AZURE_CLIENT_SECRET=<your sp secret>" >> builtin/.env
# MAGIC cat builtin/.env

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%pip install azure.ai.ml python-dotenv azureml-mlflow

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from dotenv import load_dotenv
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.identity import EnvironmentCredential

#load_dotenv('builtin/.env')

subscription_id = "bb97abc6-283f-4ec5-8088-99533835ca89"  # Azure subscription id
resource_group = "ukmo-learning"  # workspace resource group
workspace = "weather-aml-ws"  # aml workspace name

identity = DefaultAzureCredential()
#identity = EnvironmentCredential()

ml_client = MLClient(
    identity, subscription_id, resource_group, workspace
)
#verify connection
for d in ml_client.datastores.list():
    print(d.name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Create Compute Targets In AzureML


# CELL ********************

# create a compute cluster
# tip: create two, one 'cpu-cluster' and one 'gpu-cluster'
# tip: depending on permissions of this user, these can be pre-configured

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from azure.ai.ml.entities import  IdentityConfiguration, AmlCompute
from azure.ai.ml.constants import ManagedServiceIdentityType

# Create an identity configuration from the user-assigned managed identity
identity_config = IdentityConfiguration(type = ManagedServiceIdentityType.SYSTEM_ASSIGNED)


cluster_basic = AmlCompute(
    name="cpu-cluster",
    type="amlcompute",
    size="STANDARD_DS3_v2",
    location="uksouth",
    min_instances=0,
    max_instances=10,
    idle_time_before_scale_down=120,
    identity=identity_config
)

# note - only have low priority quota in this sub
cluster_basic_gpu = AmlCompute(
    name="gpu-cluster",
    type="amlcompute",
    size="Standard_NC6s_v3",
    tier="low_priority",
    location="uksouth",
    min_instances=0,
    max_instances=10,
    idle_time_before_scale_down=120,
    identity=identity_config
)

cpu = ml_client.begin_create_or_update(cluster_basic)
gpu = ml_client.begin_create_or_update(cluster_basic_gpu)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

gpu.result()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# also check available compute targets

for t in ml_client.compute.list():
    print(t.name, t.provisioning_state)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Set up AzureML compute permissions over storage
# 
# If the workspace does not have credentials for the storage account (via key-based access configuration, or in the case of data lake storage, via service principal), then the compute target must have a managed identity, and that managed identity must have access to the storage account:
# 
# Find the `principal ID` for the compute target in the compute pane in the Azure Machine learning studio, and create a role assignment for the desired `scope` (i.e the data lake storage account.)
# ```
# az role assignment create --assignee $principal --role "Storage Blob Data Contributor" --scope $scope
# ```
# 
# see also: [MSLearn: Assign a managed identity access to an Azure resource or another resource](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-assign-access-azure-resource?pivots=identity-mi-access-cli)

# MARKDOWN ********************

# ### Get azureml job files from github 

# MARKDOWN ********************

# Thanks to https://sebastianwallkoetter.wordpress.com/2022/01/30/copy-github-folders-using-python/ for a solutuion to get hold of code from github
# (adapted in [gist here](https://gist.github.com/lindacmsheard/553c46a8bd705405a965e5bf76e00cff)).

# CELL ********************

import fsspec
from pathlib import Path
from tqdm import tqdm

destination = Path.cwd() / "builtin" / "azureml"
destination.mkdir(exist_ok=True, parents=True)
fs = fsspec.filesystem("github", org="azuregig", repo="work_with_weather_data")
start = "process_data/azureml_cli_v2"
paths = len(list(fs.walk(start)))
for p,s,f in tqdm(fs.walk(start), total=paths):
    relpath = p.replace(start,".")
    dest = destination / relpath
    fs.get(fs.ls(p), dest.as_posix())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Review the pipeline definition

# CELL ********************

%cat ./builtin/azureml/pipelines/1-pipeline-one-step.yml

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from azure.ai.ml import load_job

pipeline = load_job('./builtin/azureml/pipelines/2-pipeline-two-step.yml')

pipeline_run = ml_client.jobs.create_or_update(pipeline)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# double check which paths ahve been set in the pipeline and job definitions

def print_paths(inputs, outputs):
    for i,inputdef in inputs.items():
        if not inputdef.type:
            print(i)
            print('  ', inputdef)
        else:
            try:
                print(i)
                print('  ' ,inputdef.path)
            except:
                print('  (path reference)')
                continue
    for i,outputdef in outputs.items():
        if not outputdef.type:
            print(i)
            print('  ',outputdef)
        else:
            try:
                print(i)
                print('  ' ,outputdef.path)
            except:
                print('  (path reference)')
                continue

print("\nPipeline-level settings")
print_paths(pipeline.inputs, pipeline.outputs)

for n,j in pipeline.jobs.items():
    print(f"\nPipeline step: {n}")
    print_paths(j.inputs, j.outputs)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
