from vllm.sampling_params import SamplingParams, RequestOutputKind
from .harness import Case

def run_case(case: Case) -> None:
    params = SamplingParams(
        output_kind=RequestOutputKind.FINAL_ONLY,
        stop=case.stop_string,
        include_stop_str_in_output=case.include_stop_str_in_output,
        min_tokens=0,
        max_tokens=64
    )
    request = case.make_request(params)
    case.processor.add_request(request, case.prompt)

    for time in range(2):
        engine_outputs = [case.make_output(case.chunks[time]), ]
        processor_output = case.processor.process_outputs(engine_outputs)
    engine_outputs = [case.make_output(case.late_ids), ]
    processor_output = case.processor.process_outputs(engine_outputs)
