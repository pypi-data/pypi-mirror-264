from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Callable, Iterable, List, Tuple, TypeVar

from dotenv import find_dotenv, load_dotenv


import magicapp_api.api_calls as magic_api
import magicapp_common_assets.data_models.api_dtos as api_dtos

load_dotenv(find_dotenv())


ItemType = TypeVar("ItemType")
ResultType = TypeVar("ResultType")


def get_all_guideline_dtos(guideline_id: int):
    guideline_dto = _fetch_guideline(guideline_id)
    section_dtos = _fetch_sections(guideline_id)
    rec_dtos = _fetch_recs(guideline_id)
    pico_dtos = _fetch_picos(rec_dtos)
    outcomes = _fetch_outcomes(pico_dtos)
    return api_dtos.AllGuidelineDTOs(
        guideline_dto=guideline_dto,
        section_dtos=section_dtos,
        recommendation_dtos=rec_dtos,
        pico_dtos=pico_dtos,
        dichotomous_outcome_dtos=outcomes.di_outcome_dtos,
        continuous_outcome_dtos=outcomes.co_outcome_dtos,
        non_poolable_outcome_dtos=outcomes.np_outcome_dtos,
    )


def _fetch_guideline(guideline_id: int) -> api_dtos.Guideline:
    guideline_response = magic_api.fetch_guideline(guideline_id)
    return api_dtos.Guideline(**guideline_response)


def _fetch_sections(guideline_id: int) -> List[api_dtos.Section]:
    sections_response = magic_api.fetch_guideline_sections(guideline_id)
    return [api_dtos.Section(**section) for section in sections_response]


def _fetch_section(guideline_id: int, section_id: int) -> api_dtos.Section:
    sections_response = magic_api.fetch_guideline_section(guideline_id, section_id)
    return api_dtos.Section(**sections_response)


def _fetch_recs(guideline_id: int) -> List[api_dtos.Recommendation]:
    recs_response = magic_api.fetch_guideline_recs(guideline_id)
    return [api_dtos.Recommendation(**rec) for rec in recs_response]


def _fetch_rec(guideline_id: int, rec_id: int) -> api_dtos.Recommendation:
    rec_response = magic_api.fetch_guideline_rec(guideline_id, rec_id)
    return api_dtos.Recommendation(**rec_response)


def _fetch_picos(rec_dtos: List[api_dtos.Recommendation]) -> List[api_dtos.Pico]:
    ts = []
    ids = [(r.guideline_id, r.section_id, r.recommendation_id) for r in rec_dtos]
    pico_dtos: List[api_dtos.Pico] = []
    ts.extend(_get_threads(ids, pico_dtos, _fetch_rec_picos))
    _run_threads(ts)
    return pico_dtos


def _fetch_rec_picos(ids: Tuple[int, int, int], pico_dtos: List[api_dtos.Pico]):
    guideline_id, section_id, rec_id = ids
    picos_response = magic_api.fetch_rec_picos(section_id, rec_id)
    for i in range(len(picos_response)):
        picos_response[i]["guidelineId"] = guideline_id  # Add guideline ID to response
        picos_response[i]["recommendationId"] = rec_id  # Add rec ID to response
    pico_dtos.extend([api_dtos.Pico(**pico) for pico in picos_response])


def _fetch_outcomes(pico_dtos: List[api_dtos.Pico]) -> api_dtos.Outcomes:
    ts = []
    ids = _get_outcome_ids(pico_dtos)
    di_outcome_dtos: List[api_dtos.DichotomousOutcome] = []
    ts.extend(_get_threads(ids.di_outcome_ids, di_outcome_dtos, _fetch_di_outcomes))
    co_outcome_dtos: List[api_dtos.ContinuousOutcome] = []
    ts.extend(_get_threads(ids.co_outcome_ids, co_outcome_dtos, _fetch_co_outcomes))
    np_outcome_dtos: List[api_dtos.NonPoolableOutcome] = []
    ts.extend(_get_threads(ids.np_outcome_ids, np_outcome_dtos, _fetch_np_outcomes))
    _run_threads(ts)
    return api_dtos.Outcomes(
        di_outcome_dtos=di_outcome_dtos,
        co_outcome_dtos=co_outcome_dtos,
        np_outcome_dtos=np_outcome_dtos,
    )


def _fetch_di_outcomes(ids: Tuple[int, int, int], di_outcomes_dtos: List[dict]):
    guideline_id, rec_id, outcome_id = ids
    di_outcome_response = magic_api.fetch_dichotomous_outcome(outcome_id)
    di_outcome_response["guidelineId"] = guideline_id  # Add guideline ID to response
    di_outcome_response["recommendationId"] = rec_id  # Add rec ID to response
    di_outcomes_dtos.append(api_dtos.DichotomousOutcome(**di_outcome_response))


def _fetch_co_outcomes(ids: Tuple[int, int, int], co_outcomes_dtos: List[dict]):
    guideline_id, rec_id, outcome_id = ids
    co_outcome_response = magic_api.fetch_continuous_outcome(outcome_id)
    co_outcome_response["guidelineId"] = guideline_id  # Add guideline ID to response
    co_outcome_response["recommendationId"] = rec_id  # Add rec ID to response
    co_outcomes_dtos.append(api_dtos.ContinuousOutcome(**co_outcome_response))


def _fetch_np_outcomes(ids: Tuple[int, int, int], np_outcome_dtos: List[dict]):
    guideline_id, rec_id, outcome_id = ids
    np_outcome_response = magic_api.fetch_non_poolable_outcome(outcome_id)
    np_outcome_response["guidelineId"] = guideline_id  # Add guideline ID to response
    np_outcome_response["recommendationId"] = rec_id  # Add rec ID to response
    np_outcome_dtos.append(api_dtos.NonPoolableOutcome(**np_outcome_response))


def _get_outcome_ids(pico_dtos: List[api_dtos.Pico]) -> api_dtos.OutcomeIDs:
    di_outcome_ids, co_outcome_ids, np_outcome_ids = [], [], []
    for pico_dto in pico_dtos:
        for outcome in pico_dto.outcomes:
            if outcome.outcome_type == api_dtos.PicoOutcomeType.DICHOTOMOUS:
                di_outcome_ids.append(
                    (
                        pico_dto.guideline_id,
                        pico_dto.recommendation_id,
                        outcome.outcome_id,
                    )
                )
            elif outcome.outcome_type == api_dtos.PicoOutcomeType.CONTINUOUS:
                co_outcome_ids.append(
                    (
                        pico_dto.guideline_id,
                        pico_dto.recommendation_id,
                        outcome.outcome_id,
                    )
                )
            elif outcome.outcome_type == api_dtos.PicoOutcomeType.NON_POOLABLE:
                np_outcome_ids.append(
                    (
                        pico_dto.guideline_id,
                        pico_dto.recommendation_id,
                        outcome.outcome_id,
                    )
                )
    return api_dtos.OutcomeIDs(
        di_outcome_ids=di_outcome_ids,
        co_outcome_ids=co_outcome_ids,
        np_outcome_ids=np_outcome_ids,
    )


def _get_threads(
    items: Iterable[ItemType],
    results: List[ResultType],
    fetch_func: Callable[[ItemType, List[ResultType]], None],
) -> List[Thread]:
    with ThreadPoolExecutor(max_workers=20) as executor:
        return [executor.submit(fetch_func, item, results) for item in items]


def _run_threads(futures):
    for future in futures:
        future.result()
    futures.clear()


if __name__ == "__main__":
    get_all_guideline_dtos(6989)
