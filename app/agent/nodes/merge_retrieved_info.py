from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState


async def merge_retrieved_info(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("合并召回信息")
    retrieved_column_infos = state["retrieved_column_infos"]
    retrieved_metric_infos = state["retrieved_metric_infos"]
    retrieved_value_infos = state["retrieved_value_infos"]

    # 处理表信息
    # 将指标信息的相关字段信息添加到字段信息中

    # 将字段取值加入到其对应字段的examples中

    # 按照表对字段信息进行分组，整理成目标格式

    # 处理指标信息