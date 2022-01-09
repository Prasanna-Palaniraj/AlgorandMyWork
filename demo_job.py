from time import time, sleep
import base64

from algosdk import account, encoding
from algosdk.logic import get_application_address
#from mywork.operations import createmyworkApp, setupmyworkApp, placeBid, closemywork
from mywork.operations_job import completeJobRequest, createJobApp, pullJobRequest, transferFunds
from mywork.util import *
from mywork.testing.setup import getAlgodClient
from mywork.testing.resources import (
    getTemporaryAccount,
    optInToAsset,
    createDummyAsset,
)


def simple_job():
    client = getAlgodClient()

    print("Generating temporary accounts...")
    poster = getTemporaryAccount(client)
    worker = getTemporaryAccount(client)
    print("=========================")
    print(poster.getAddress())
    print("=========================")
    print("Creating job post...")

    #job_start = 15/12/2021
    #job_end = 17/12/2021

    post_id = 1

    post_title = "Android mobile application for the cake shop"

    post_compensation = 1_000_000

    post_skill = "Android"

    post_skill_level = 5

    print(
        "Creating job smart contract..."
    )
    appID = createJobApp(
        client=client,
        sender=poster,
        poster=poster.getAddress(),
        posttitle = post_title,
        postid= post_id,
        compensation= post_compensation,
        skill= post_skill,
        skill_level= post_skill_level
    )

    print(appID)
    print("=========================")
    print("Worker reviews the job, approves the compensation and agrees work to be done. \n Requests poster for pull job")
    print("1. Poster reviews the worker and approves pull job...")
    print("2. Poster transfers amount to the escrow account...")
    print("3. Poster updates app with the worker details...")
    print("Poster balance")
    print(client.account_info(poster.getAddress())["amount"])
    pullJobResponse = pullJobRequest(
        client = client,
        appID = appID,
        worker= worker,
        poster=poster,
    )
    print(pullJobResponse)
    print("=========================")
    print("Poster balance")
    print(client.account_info(poster.getAddress())["amount"])
    print("Global state:", read_global_state(client, poster.getAddress(), appID))
    
    print("Worker submits for complete job")
    print("1. Poster reviews the work and approves complete job...")
    print("2. Poster authorizes the payment to worker account...") ## todo
    completeJobRequest(
        client = client,
        appID = appID,
        worker=worker,
        poster=poster,
    )
    print("=========================")
    print("post Complete job")
    print("Global state:", read_global_state(client, poster.getAddress(), appID))
    print("Poster balance")
    print(client.account_info(poster.getAddress())["amount"])
    print(client.account_info(worker.getAddress())["amount"])
    print(client.account_info(get_application_address(appID))["amount"])
    print("=========================")
    print("transfer Funds")
    print("=========================")
    
    transferFundsResponse = transferFunds(
        client = client,
        appID = appID,
        worker=worker,
        poster=poster,
    )

    print(transferFundsResponse)
    print("post transfer funds job")
    print("Global state:", read_global_state(client, poster.getAddress(), appID))
    print("Poster balance")
    print(client.account_info(poster.getAddress())["amount"])
    print(client.account_info(worker.getAddress())["amount"])
    print(client.account_info(get_application_address(appID))["amount"])

simple_job()
