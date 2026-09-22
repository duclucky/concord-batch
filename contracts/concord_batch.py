# v0.3.0
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }
import genlayer as gl
from genlayer.storage import TreeMap
from genlayer.types import bigint
import json


class ConcordBatch(gl.contract.Contract):
    values: TreeMap[str, str]
    total_received: bigint
    total_locked: bigint
    total_credits: bigint
    total_withdrawn: bigint

    def __init__(self) -> None:
        pass

    @gl.public.view
    def get_accounting(self) -> str:
        return json.dumps({
            "total_received": str(self.total_received),
            "total_locked": str(self.total_locked),
            "total_credits": str(self.total_credits),
            "total_withdrawn": str(self.total_withdrawn),
        })

    @gl.public.write.payable
    def create_batch(self, batch_id: str, participant_a, participant_b, participant_c,
                     priority_csv: str, policy: str, submit_deadline: int,
                     review_deadline: int) -> None:
        raise gl.vm.UserError("not implemented")
