import grpc
from sample_app.api_pb2 import AppendRequest, GetRequest, CreateRequest
from sample_app.events_pb2 import AppendEvent, CreateEvent
from sample_app.state_pb2 import State
from google.protobuf.json_format import MessageToJson
from chief_of_state.writeside_pb2_grpc import WriteSideHandlerServiceStub
from chief_of_state.writeside_pb2 import (
    HandleCommandRequest,
    HandleCommandResponse,
    HandleEventRequest,
    HandleEventResponse,
    PersistAndReply,
    Reply
)
from chief_of_state.common_pb2 import MetaData
from google.protobuf.any_pb2 import Any
from cos_helpers.grpc import get_channel
from cos_helpers.proto import ProtoHelper

class TestHandler():
    @staticmethod
    def run(host, port):
        channel = get_channel(host, port)
        stub = WriteSideHandlerServiceStub(channel)

        TestHandler.handleCommandCreate(stub)
        TestHandler.handleCommandAppend(stub)
        TestHandler.handleCommandGet(stub)

    @staticmethod
    def handleCommandCreate(stub):
        print("TestHandler.handleCommandCreate")
        id = "test-command"
        cmd = CreateRequest(id = id)
        current_state = State()
        meta = MetaData()

        request = HandleCommandRequest(
            command=ProtoHelper.pack_any(cmd),
            current_state=ProtoHelper.pack_any(current_state),
            meta=meta,
        )

        response = stub.HandleCommand(request)

        assert isinstance(response, HandleCommandResponse)

        response_event = CreateEvent()
        response.persist_and_reply.event.Unpack(response_event)

        assert response_event.id == id

    @staticmethod
    def handleCommandAppend(stub):
        print("TestHandler.handleCommandAppend")

        id = "test-append"
        value = "after"

        command = AppendRequest(id=id, append=value)
        current_state = State(id=id, values=["before"])
        meta = MetaData(revision_number=1)

        request = HandleCommandRequest(
            command=ProtoHelper.pack_any(command),
            current_state=ProtoHelper.pack_any(current_state),
            meta=meta
        )

        response = stub.HandleCommand(request)

        assert isinstance(response, HandleCommandResponse)

        response_event = AppendEvent()
        response.persist_and_reply.event.Unpack(response_event)

        assert response_event.id == id
        assert response_event.appended == value


    def handleCommandGet(stub):
        print("TestHandler.handleCommandGet")

        id = "test-get"

        command = GetRequest(id=id)
        current_state = State(id=id, values=["before"])
        meta = MetaData(revision_number=1)

        request = HandleCommandRequest(
            command=ProtoHelper.pack_any(command),
            current_state=ProtoHelper.pack_any(current_state),
            meta=meta
        )

        response = stub.HandleCommand(request)

        assert isinstance(response, HandleCommandResponse)
        assert response.HasField("reply")


if __name__ == '__main__':
    TestApi.run()