from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class ContestStatus(BaseModel):
    contest_id: int = Field(alias="contestId")
    as_manager: bool = Field(alias="asManager")
    handle: str
    from_: int = Field(alias="from")
    count: int

    class Config:
        allow_population_by_field_name = True


class ProblemTypeEnum(str, Enum):
    PROGRAMMING = "PROGRAMMING"
    QUESTION = "QUESTION"


class SubmissionVerdictEnum(str, Enum):
    OK = "OK"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    WRONG_ANSWER = "WRONG_ANSWER"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    IDLENESS_LIMIT_EXCEEDED = "IDLENESS_LIMIT_EXCEEDED"
    SECURITY_VIOLATED = "SECURITY_VIOLATED"
    CRASHED = "CRASHED"
    INPUT_PREPARATION_CRASHED = "INPUT_PREPARATION_CRASHED"
    CHALLENGED = "CHALLENGED"
    SKIPPED = "SKIPPED"
    TESTING = "TESTING"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"

    @classmethod
    def is_fail(cls, verdict: str) -> bool:
        return verdict != cls.OK


class SubmissionTestsetEnum(str, Enum):
    SAMPLES = "SAMPLES"
    PRETESTS = "PRETESTS"
    TESTS = "TESTS"
    CHALLENGES = "CHALLENGES"
    TESTS1 = "TESTS1"
    TESTS2 = "TESTS2"
    TESTS3 = "TESTS3"
    TESTS4 = "TESTS4"
    TESTS5 = "TESTS5"
    TESTS6 = "TESTS6"
    TESTS7 = "TESTS7"
    TESTS8 = "TESTS8"
    TESTS9 = "TESTS9"
    TESTS10 = "TESTS10"


class Problem(BaseModel):
    contest_id: Optional[int] = Field(alias="contestId", default=None)
    problemset_name: Optional[str] = Field(alias="problemsetName", default=None)
    index: str
    name: str
    type: ProblemTypeEnum
    points: Optional[float] = Field(default=None)
    rating: Optional[int] = Field(default=None)
    tags: list[str]

    class Config:
        allow_population_by_field_name = True


class ParticipantTypeEnum(str, Enum):
    CONTESTANT = "CONTESTANT"
    PRACTICE = "PRACTICE"
    VIRTUAL = "VIRTUAL"
    MANAGER = "MANAGER"
    OUT_OF_COMPETITION = "OUT_OF_COMPETITION"


class Member(BaseModel):
    handle: str
    name: Optional[str] = Field(default=None)


class Party(BaseModel):
    contest_id: Optional[int] = Field(alias="contestId", default=None)
    members: List[Member]
    participant_type: ParticipantTypeEnum = Field(alias="participantType")
    team_id: Optional[int] = Field(alias="teamId", default=None)
    team_name: Optional[str] = Field(alias="teamName", default=None)
    ghost: bool
    room: Optional[int] = Field(default=None)
    start_time_seconds: Optional[int] = Field(alias="startTimeSeconds", default=None)

    class Config:
        allow_population_by_field_name = True


class Submission(BaseModel):
    id: int
    contest_id: Optional[int] = Field(alias="contestId", default=None)
    creation_time_seconds: int = Field(alias="creationTimeSeconds")
    relative_time_seconds: int = Field(alias="relativeTimeSeconds")
    problem: Problem
    author: Party
    programming_language: str = Field(alias="programmingLanguage")
    verdict: Optional[SubmissionVerdictEnum] = Field(default=None)
    testset: SubmissionTestsetEnum
    passed_test_count: int = Field(alias="passedTestCount")
    time_consumed_millis: int = Field(alias="timeConsumedMillis")
    memory_consumed_bytes: int = Field(alias="memoryConsumedBytes")
    points: Optional[float] = Field(default=None)

    class Config:
        allow_population_by_field_name = True


class CodeforcesApiResponseBySubmissions(BaseModel):
    status: str
    result: List[Submission]