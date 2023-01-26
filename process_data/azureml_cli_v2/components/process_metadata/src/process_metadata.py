
import argparse
import os
import mlflow

import time

parser = argparse.ArgumentParser()
parser.add_argument("--run_after", type=str)


args = parser.parse_args()


def log_lineage(args):
    '''
    
    '''
    # what are we getting from args? two ways of logging this

    mlflow.log_params(vars(args))
    mlflow.log_dict(vars(args), "inputs.json")

    # what does the mlflow object offer
    dirlist = str(dir(mlflow))
    mlflow.log_text(dirlist, "mlflowmethods.txt")
    print(type(mlflow))
    print(dir(mlflow))
    run = mlflow.active_run()
    print("active run type:", type(run))
    print(dir(run))
    print("Run info:", run.info)
    print("Run ID:", run.info.run_id)
    run_id = mlflow.active_run().info.run_id
    client = mlflow.MlflowClient()
    rundata = client.get_run(run_id).data
    print("Type (rundata):", type(rundata))
    print("Rundata:\n", rundata)
    print(dir(rundata))
    mlflow.log_text(str(rundata), 'rundata_object.txt')
    print(rundata.tags.get('mlflow.source.type'))
    if rundata.tags.get('mlflow.source.type') != 'LOCAL':
        parent_run_id = rundata.tags.get('mlflow.parentRunId')
        pipeline_run_id = rundata.tags.get('azureml.pipeline')
        pipelinerundata = client.get_run(pipeline_run_id).data
        print(type(pipelinerundata))
        print(pipelinerundata)
        mlflow.log_text(str(pipelinerundata), 'pipeline_rundata_object.txt')

    #parent_data = client.get_run

def test_sdk(args):
    


if __name__ == "__main__":
    log_lineage(args)
