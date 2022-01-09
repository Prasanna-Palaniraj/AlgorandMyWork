from algosdk.future import transaction
from algosdk.future.transaction import OnComplete
from pyteal import *

def approval_program():
    poster_key = Bytes("poster") #0
    #start_time_key = Bytes("expectedstart") #1
    #end_time_key = Bytes("expectedend") #2
    post_id_key = Bytes("id") #3
    post_title_key = Bytes("title") #4
    post_compensation_key = Bytes("fee") #5
    post_skill_key = Bytes("skill") #6
    post_skill_level_key = Bytes("level") #7
    ### Job pulled and completed by
    transaction_type_key = Bytes("txntype") #8
    pulled_by_key = Bytes("worker") #9
    pulled_time_key = Bytes("actualstart") #10
    completed_time_key = Bytes("actualend") #11
    post_approved_key = Bytes("approved") #12
    approved_time_key = Bytes("approvedtime") #13

    
    @Subroutine(TealType.none)
    def closeAccountTo(account: Expr) -> Expr:
        return If(Balance(Global.current_application_address()) != Int(0)).Then(
            Seq(
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields(
                    {
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.close_remainder_to: account,
                    }
                ),
                InnerTxnBuilder.Submit(),
            )
        )

    #on_create_start_time = Btoi(Txn.application_args[1])
    #on_create_end_time = Btoi(Txn.application_args[2])

    handle_creation = Seq(
        # Set the job details and the required skill for the job
        App.globalPut(poster_key,Txn.application_args[0]),
        App.globalPut(poster_key,Txn.application_args[0]),
        #App.globalPut(start_time_key,on_create_start_time),
        #App.globalPut(end_time_key,on_create_end_time),
        App.globalPut(post_id_key,Txn.application_args[1]),
        App.globalPut(post_title_key,Txn.application_args[2]),
        App.globalPut(post_compensation_key,Txn.application_args[3]),
        App.globalPut(post_skill_key,Txn.application_args[4]),
        App.globalPut(post_skill_level_key,Txn.application_args[5]),
        App.globalPut(post_approved_key,Int(0)),
        # Assert(
        #     And(
        #         Global.latest_timestamp() < on_create_start_time,
        #         on_create_start_time < on_create_end_time,
        #     )
        # ),
        Approve(),
        Return(Int(1))
    )

    handle_optin = Seq(
        Return(Int(0))
    )

    handle_closeout = Seq(
        Return(Int(0))
    )

    handle_updateapp= Seq(
        Return(Int(0))
    )


    handle_deleteapp= Seq(
        #closeJob(App.globalGet(pulled_by_key)),
        #Assert(
         #  Txn.sender() == App.globalGet(pulled_by_key),
        #),
        closeAccountTo(Txn.sender()),
        Approve()
    )

    job_pulled = Seq(
        App.globalPut(transaction_type_key,Txn.application_args[0]),
        App.globalPut(pulled_by_key,Txn.application_args[1]),
        App.globalPut(pulled_time_key,Global.latest_timestamp()),
        Return(Int(1))
    )

    job_completed = Seq(
        App.globalPut(completed_time_key,Global.latest_timestamp()),
        Return(Int(1))
    )

    job_approved = Seq(
        App.globalPut(post_approved_key, Int(1)),
        App.globalPut(approved_time_key, Global.latest_timestamp()),
        Return(Int(1))
    )

    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("pull"), job_pulled],
        [Txn.application_args[0] == Bytes("complete"), job_completed],
        [Txn.application_args[0] == Bytes("approved"), job_approved],
    )

    program = Cond(
        [Txn.application_id() == Int(0),handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
    )

    #return compileTeal(program, Mode.Application, version=5)

    with open("myWork_approval.teal", "w") as f:
        compiled = compileTeal(program, mode=Mode.Application, version=5)
        f.write(compiled)

    return program


def clear_state_program():
    program = Return(Int(1))

    #return compileTeal(program, Mode.Application, version=5)

    with open("myWork_clear.teal", "w") as f:
        compiled = compileTeal(program, mode=Mode.Application, version=5)
        f.write(compiled)

    return program

print(approval_program())
print(clear_state_program())